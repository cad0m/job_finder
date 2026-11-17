import { useEffect, useState } from 'react';
import { useParams, Link, useLocation } from 'react-router-dom';
import AppShell from '../components/AppShell';
import MatchScore from '../components/MatchScore';
import EmptyState from '../components/EmptyState';
import LoadingState from '../components/common/LoadingState';
import { supabaseDB } from '../services/supabaseDB';
import { useAuth } from '../hooks/useAuth';

const Fact = ({ label, children }) =>
  children ? (
    <div className="flex items-baseline justify-between gap-4 py-2.5">
      <dt className="text-graphite">{label}</dt>
      <dd className="text-right font-medium">{children}</dd>
    </div>
  ) : null;

const JobDetails = () => {
  const { jobId } = useParams();
  const { state: routeState } = useLocation();
  const matchScore = routeState?.match_score ?? null;
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isSaved, setIsSaved] = useState(false);
  const { user } = useAuth();

  useEffect(() => {
    const fetchJobAndSavedStatus = async () => {
      setLoading(true);
      const data = await supabaseDB.getJobById(jobId);
      setJob(data);

      if (user && data) {
        const saved = await supabaseDB.checkIfJobSaved(user.id, jobId);
        setIsSaved(saved);
      }

      setLoading(false);
    };
    fetchJobAndSavedStatus();
  }, [jobId, user]);

  const [isProcessing, setIsProcessing] = useState(false);
  const handleToggleSave = async () => {
    if (!user || isProcessing) return;

    setIsProcessing(true);
    const previousSavedState = isSaved;
    try {
      // Optimistic update
      setIsSaved(!previousSavedState);
      await supabaseDB.toggleSavedJob(user.id, jobId, previousSavedState);
    } catch (err) {
      console.error('Failed to toggle save:', err);
      // Revert if it fails
      setIsSaved(previousSavedState);
    } finally {
      setIsProcessing(false);
    }
  };

  if (loading) {
    return (
      <AppShell>
        <LoadingState message="Loading the offer…" />
      </AppShell>
    );
  }

  if (!job) {
    return (
      <AppShell>
        <EmptyState
          icon="link_off"
          title="This offer is no longer available"
          action={<Link to="/dashboard" className="btn btn-primary">Back to your matches</Link>}
        >
          It may have been filled or taken down by the company.
        </EmptyState>
      </AppShell>
    );
  }

  const skills = job.skills || [];

  return (
    <AppShell>
      <Link to="/dashboard" className="mb-6 inline-flex items-center gap-1.5 text-[0.9375rem] font-medium text-graphite hover:text-ink">
        <span className="material-symbols-outlined" aria-hidden="true">arrow_back</span>
        Your matches
      </Link>

      <header className="mb-8 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div className="flex min-w-0 gap-4">
          {job.logo_url && (
            <img src={job.logo_url} alt="" className="h-14 w-14 shrink-0 rounded-lg border border-rule bg-paper object-contain p-1.5" />
          )}
          <div className="min-w-0">
            <h1 className="text-[2rem] font-bold sm:text-[2.5rem]">{job.title}</h1>
            <p className="mt-2 flex flex-wrap gap-x-3 text-[1.0625rem] text-graphite">
              {job.company_website ? (
                <a href={job.company_website} target="_blank" rel="noreferrer" className="font-semibold text-ink underline decoration-rule-strong underline-offset-4 hover:decoration-ink">
                  {job.company}
                </a>
              ) : (
                <span className="font-semibold text-ink">{job.company}</span>
              )}
              {job.location && <span>{job.location}</span>}
            </p>
          </div>
        </div>

        <div className="flex flex-wrap gap-3">
          <button onClick={handleToggleSave} aria-pressed={isSaved} className="btn btn-secondary">
            <span className={`material-symbols-outlined ${isSaved ? 'icon-fill text-pen' : ''}`} aria-hidden="true">bookmark</span>
            {isSaved ? 'Saved' : 'Save'}
          </button>
          <Link to={`/apply/${job.id}`} state={{ match_score: matchScore }} className="btn btn-primary">
            Prepare application
          </Link>
        </div>
      </header>

      <div className="grid gap-6 lg:grid-cols-[1fr_18rem]">
        <article className="sheet p-6 sm:p-9">
          <h2 className="text-xl font-semibold">About the job</h2>
          <div className="mt-4 max-w-[68ch] whitespace-pre-line leading-relaxed text-graphite">
            {job.description || 'The company did not publish a description for this offer.'}
          </div>

          {skills.length > 0 && (
            <>
              <h2 className="mt-8 text-xl font-semibold">Skills asked for</h2>
              <ul className="mt-4 flex flex-wrap gap-1.5">
                {skills.map((skill, i) => (
                  <li key={i} className="chip">{skill}</li>
                ))}
              </ul>
            </>
          )}
        </article>

        <aside className="space-y-6">
          {matchScore !== null && (
            <section className="sheet p-6">
              <h2 className="font-sans text-[0.9375rem] font-semibold tracking-normal text-graphite">Match with your CV</h2>
              <MatchScore score={matchScore} size="lg" className="mt-3" />
              <p className="mt-3 text-[0.9375rem] text-graphite">
                How close this offer’s description is to the experience and skills on your CV.
              </p>
            </section>
          )}

          <section className="sheet px-6 py-4">
            <h2 className="sr-only">Details</h2>
            <dl className="divide-y divide-rule text-[0.9375rem]">
              <Fact label="Posted">{job.posted_at}</Fact>
              <Fact label="Level">{job.experience_level}</Fact>
              <Fact label="Salary">{job.salary_range}</Fact>
              <Fact label="Applicants">{job.num_application ? job.num_application.toLocaleString() : null}</Fact>
            </dl>
            {job.job_url && (
              <a href={job.job_url} target="_blank" rel="noreferrer" className="link mt-3 inline-flex items-center gap-1.5 pb-1 text-[0.9375rem]">
                View the original posting
                <span className="material-symbols-outlined" aria-hidden="true">open_in_new</span>
              </a>
            )}
          </section>
        </aside>
      </div>
    </AppShell>
  );
};

export default JobDetails;
