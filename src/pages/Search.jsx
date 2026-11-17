import { useState, useRef } from 'react';
import AppShell, { PageHeader } from '../components/AppShell';
import JobRow, { JobList, JobRowSkeleton } from '../components/JobRow';
import EmptyState from '../components/EmptyState';
import { supabaseDB } from '../services/supabaseDB';
import { edgeFunctions } from '../services/edgeFunctions';

const EXAMPLES = [
  'Data engineer with Python and Spark in Casablanca',
  'Développeur React junior, télétravail',
  'Stage PFE en data science',
  'Chef de projet digital à Rabat',
];

const Search = () => {
  const [query, setQuery] = useState('');
  const [searched, setSearched] = useState('');
  const [jobs, setJobs] = useState([]);
  const [status, setStatus] = useState('idle'); // idle | loading | results | empty | error
  const [error, setError] = useState(null);
  const [isSemantic, setIsSemantic] = useState(true); // did the AI embedding succeed?
  const inputRef = useRef(null);

  const handleSearch = async (e) => {
    e?.preventDefault();
    const trimmed = query.trim();
    if (!trimmed) return;

    setStatus('loading');
    setSearched(trimmed);
    setError(null);
    setIsSemantic(true);

    // ── Tier 1: Semantic (AI embedding + vector RPC) ──────────────────
    try {
      const embedResult = await edgeFunctions.invokeEmbedText(trimmed);
      const embedding = embedResult?.embedding ?? embedResult;

      if (!embedding || !Array.isArray(embedding)) {
        throw new Error('Invalid embedding returned');
      }

      const results = await supabaseDB.searchJobsByEmbedding(embedding, trimmed);

      if (results.length > 0 && results[0].match_score === null) {
        setIsSemantic(false); // RPC fallback was used inside supabaseDB
      }

      setJobs(results);
      setStatus(results.length > 0 ? 'results' : 'empty');
      return; // success — stop here
    } catch (embedErr) {
      console.warn('Semantic search failed, falling back to keyword:', embedErr.message);
      // Don't throw — fall through to keyword fallback
    }

    // ── Tier 2: Keyword fallback ──────────────────────────────────────
    try {
      setIsSemantic(false);
      const results = await supabaseDB.getJobs(trimmed);
      const mapped = results.map((job) => ({ ...job, match_score: null }));
      setJobs(mapped);
      setStatus(mapped.length > 0 ? 'results' : 'empty');
    } catch (kwErr) {
      console.error('Keyword fallback also failed:', kwErr);
      setError('The search could not run. Check your connection and search again.');
      setStatus('error');
    }
  };

  return (
    <AppShell>
      <PageHeader title="Search">
        Describe the job you want in your own words, in French or English. Offers are ranked by how close they are to
        your description.
      </PageHeader>

      <form onSubmit={handleSearch} className="mb-6 flex flex-col gap-3 sm:flex-row">
        <div className="relative flex-1">
          <span className="material-symbols-outlined pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-pencil" aria-hidden="true">search</span>
          <input
            ref={inputRef}
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. Data engineer with Python and Spark in Casablanca"
            aria-label="Describe the job you want"
            className="field min-h-13 pl-11 text-[1.0625rem]"
          />
        </div>
        <button type="submit" disabled={status === 'loading' || !query.trim()} className="btn btn-primary btn-lg">
          {status === 'loading' ? 'Searching…' : 'Search'}
        </button>
      </form>

      {status === 'idle' && (
        <div>
          <p className="mb-3 text-[0.9375rem] font-semibold">Try one of these</p>
          <ul className="flex flex-col items-start gap-2">
            {EXAMPLES.map((example) => (
              <li key={example}>
                <button
                  type="button"
                  onClick={() => { setQuery(example); setTimeout(() => inputRef.current?.focus(), 50); }}
                  className="link text-left font-medium"
                >
                  {example}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {status === 'error' && (
        <div className="notice notice-bad" role="alert">
          <span className="material-symbols-outlined" aria-hidden="true">error</span>
          <span>{error}</span>
        </div>
      )}

      {status === 'loading' && (
        <JobList label="Searching">
          {Array.from({ length: 5 }, (_, i) => <JobRowSkeleton key={i} />)}
        </JobList>
      )}

      {status === 'empty' && (
        <EmptyState icon="search_off" title={`Nothing found for “${searched}”`}>
          Describe the role more broadly, or use fewer words.
        </EmptyState>
      )}

      {status === 'results' && (
        <>
          <p className="mb-3 text-[0.9375rem] text-graphite" role="status">
            {jobs.length} {jobs.length === 1 ? 'offer' : 'offers'} for “{searched}”
          </p>
          {!isSemantic && (
            <div className="notice notice-warn mb-4">
              <span className="material-symbols-outlined" aria-hidden="true">info</span>
              <span>Ranking by meaning is unavailable right now, so these are plain keyword results without a score.</span>
            </div>
          )}
          <JobList label="Search results">
            {jobs.map((job) => (
              <JobRow key={job.id} job={job} showScore={isSemantic} linkState={{ match_score: job.match_score }} />
            ))}
          </JobList>
        </>
      )}
    </AppShell>
  );
};

export default Search;
