from typing import Dict
from datetime import datetime
from pydantic import BaseModel, Field

class BaseJob(BaseModel):
    job_id: str | None = None
    job_title: str | None = None
    company_name: str | None = None
    company_logo: str | None = None
    location: str | None = None
    posted_date: str | None = None
    num_applicants: int | None = None
    job_description: str | None = None
    seniority_level: str | None = None
    employment_type: str | None = None
    job_function: str | None = None
    industries: list[str] | None = None
    job_url: str | None = None
    company_url: str | None = None
    source: str | None = None
    scraped_at: str = Field(default_factory=lambda: datetime.now().isoformat())
