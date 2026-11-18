"""
Embed jobs and candidates with Voyage AI and store the vectors in Postgres.

Only rows whose `embedding` is NULL are embedded, so the task is safe to re-run:
it picks up where it stopped. Jobs and CVs must use the same model and size,
because matching compares a CV vector with job vectors (cosine distance).

Settings (.env):
  VOYAGE_API_KEY   required
  VOYAGE_MODEL     default voyage-3.5
  VOYAGE_DIM       default 1024 (must match the vector(N) columns)
  VOYAGE_RPM       requests per minute, default 3 (free tier without a payment method)
  VOYAGE_TPM       tokens per minute, default 10000 (same)
"""
import os
import time
import json
from typing import Iterable, List, Optional

from curl_cffi import requests
from dotenv import load_dotenv

from etl.core.databaseConnection import DatabaseConnection

load_dotenv()

API_URL = "https://api.voyageai.com/v1/embeddings"
MODEL = os.getenv("VOYAGE_MODEL", "voyage-3.5")
DIM = int(os.getenv("VOYAGE_DIM", "1024"))
RPM = max(1, int(os.getenv("VOYAGE_RPM", "3")))
TPM = max(1000, int(os.getenv("VOYAGE_TPM", "10000")))
MAX_CHARS = 2400            # about 600 tokens per document: enough for title, company and the key requirements
CHARS_PER_TOKEN = 4         # rough estimate, used only to pace requests under the TPM limit


class VoyageClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("VOYAGE_API_KEY")
        if not self.api_key:
            raise RuntimeError("VOYAGE_API_KEY is missing in .env")
        self._last_call = 0.0

    def _pace(self):
        wait = 60.0 / RPM - (time.time() - self._last_call)
        if wait > 0:
            time.sleep(wait)

    def embed(self, texts: List[str], input_type: str = "document") -> List[List[float]]:
        """Embed a batch. Retries on rate limits and server errors with a growing wait."""
        for attempt in range(6):
            self._pace()
            self._last_call = time.time()
            r = requests.post(
                API_URL,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                data=json.dumps({"input": texts, "model": MODEL, "input_type": input_type, "output_dimension": DIM}),
                timeout=60,
            )
            if r.status_code == 200:
                data = sorted(r.json()["data"], key=lambda d: d["index"])
                return [d["embedding"] for d in data]
            if r.status_code in (429, 500, 502, 503, 504):
                wait = min(120, 20 * (attempt + 1))
                print(f"Voyage {r.status_code}, waiting {wait}s (attempt {attempt + 1}/6)")
                time.sleep(wait)
                continue
            raise RuntimeError(f"Voyage error {r.status_code}: {r.text[:300]}")
        raise RuntimeError("Voyage kept failing after 6 attempts")


def _batches(items: list, text_of) -> Iterable[list]:
    """Group items so each request stays under the tokens-per-minute budget."""
    budget = int(TPM / RPM * 0.9) * CHARS_PER_TOKEN   # characters allowed per request
    batch, size = [], 0
    for it in items:
        n = len(text_of(it))
        if batch and (size + n > budget or len(batch) >= 128):
            yield batch
            batch, size = [], 0
        batch.append(it)
        size += n
    if batch:
        yield batch


def _vector_literal(v: List[float]) -> str:
    return "[" + ",".join(f"{x:.7f}" for x in v) + "]"


# ── Jobs ────────────────────────────────────────────────────────────────────────

JOBS_SQL = """
SELECT j.id, j.title, co.name, l.city, l.country, j.seniority_level, f.name,
       (SELECT string_agg(i.name, ', ') FROM job_industry ji JOIN industry i ON i.id = ji.industry_id WHERE ji.job_id = j.id),
       j.job_description
FROM jobs j
LEFT JOIN company co ON co.id = j.company_id
LEFT JOIN location l ON l.id = j.location_id
LEFT JOIN job_function f ON f.id = j.function_id
WHERE j.embedding IS NULL
ORDER BY j.posted_date DESC NULLS LAST
LIMIT %s
"""


def job_text(row) -> str:
    _id, title, company, city, country, seniority, function, industries, desc = row
    parts = [f"Job title: {title or 'Unknown'}"]
    if company: parts.append(f"Company: {company}")
    loc = ", ".join(x for x in (city, country) if x)
    if loc: parts.append(f"Location: {loc}")
    if seniority: parts.append(f"Seniority: {seniority}")
    if function: parts.append(f"Function: {function}")
    if industries: parts.append(f"Industries: {industries}")
    if desc: parts.append("Description:\n" + " ".join(str(desc).split()))
    return "\n".join(parts)[:MAX_CHARS]


def embed_pending_jobs(limit: int = 2000) -> int:
    """Embed jobs that have no embedding yet. Returns how many were embedded."""
    db = DatabaseConnection()
    db.connect()
    try:
        db.execute(JOBS_SQL, (limit,))
        rows = db.cursor.fetchall()
        print(f"{len(rows)} jobs need an embedding")
        if not rows:
            return 0
        client = VoyageClient()
        done = 0
        for batch in _batches(rows, job_text):
            vectors = client.embed([job_text(r) for r in batch], input_type="document")
            for r, v in zip(batch, vectors):
                db.execute("UPDATE jobs SET embedding = %s::vector WHERE id = %s", (_vector_literal(v), r[0]))
            db.commit()            # commit per batch: a crash keeps the work already done
            done += len(batch)
            print(f"  embedded {done}/{len(rows)} jobs")
        return done
    finally:
        db.close()


# ── Candidates (CVs) ────────────────────────────────────────────────────────────

CANDIDATES_SQL = """
SELECT c.id, c.seniority_level, c.years_experience, c.professional_summary,
       c.skills, c.experience, c.education, c.certifications,
       (SELECT string_agg(f.name, ', ') FROM candidate_function cf JOIN job_function f ON f.id = cf.function_id WHERE cf.candidate_id = c.id),
       (SELECT string_agg(i.name, ', ') FROM candidate_industry ci JOIN industry i ON i.id = ci.industry_id WHERE ci.candidate_id = c.id)
FROM candidates c
WHERE c.embedding IS NULL
LIMIT %s
"""


def _names(items) -> List[str]:
    out = []
    for s in items or []:
        if isinstance(s, str) and s.strip():
            out.append(s.strip())
        elif isinstance(s, dict) and s.get("name"):
            out.append(str(s["name"]).strip())
    return out


def candidate_text(row) -> str:
    """Same content as the embed-cv edge function, so both paths give the same vector."""
    _id, seniority, years, summary, skills, experience, education, certs, functions, industries = row
    parts = []
    if seniority: parts.append(f"Seniority: {seniority}")
    if years: parts.append(f"Years of Experience: {years}")
    if functions: parts.append(f"Functions: {functions}")
    if industries: parts.append(f"Industries: {industries}")
    if summary: parts.append(f"Summary: {summary}")
    sk = _names(skills)
    if sk: parts.append("Skills: " + ", ".join(sk))
    if experience:
        lines = []
        for e in experience:
            line = f"- {e.get('job_title', '')} at {e.get('company', '')}"
            resp = e.get("responsibilities") or []
            if isinstance(resp, list) and resp:
                line += ": " + "; ".join(str(x) for x in resp)
            lines.append(line)
        parts.append("Experience:\n" + "\n".join(lines))
    if education:
        parts.append("Education:\n" + "\n".join(
            f"- {e.get('degree', '')} in {e.get('field', '')} from {e.get('institution', '')}" for e in education))
    ce = _names(certs)
    if ce: parts.append("Certifications: " + ", ".join(ce))
    return "\n\n".join(parts)[:MAX_CHARS * 2]


def embed_pending_candidates(limit: int = 500) -> int:
    """Embed CVs that have no embedding yet (for example after switching models)."""
    db = DatabaseConnection()
    db.connect()
    try:
        db.execute(CANDIDATES_SQL, (limit,))
        rows = [r for r in db.cursor.fetchall()]
        rows = [r for r in rows if candidate_text(r).strip()]
        print(f"{len(rows)} CVs need an embedding")
        if not rows:
            return 0
        client = VoyageClient()
        done = 0
        for batch in _batches(rows, candidate_text):
            vectors = client.embed([candidate_text(r) for r in batch], input_type="document")
            for r, v in zip(batch, vectors):
                db.execute("UPDATE candidates SET embedding = %s::vector WHERE id = %s", (_vector_literal(v), r[0]))
            db.commit()
            done += len(batch)
            print(f"  embedded {done}/{len(rows)} CVs")
        return done
    finally:
        db.close()
