import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import AppShell, { PageHeader } from '../components/AppShell';
import JobRow, { JobList } from '../components/JobRow';
import EmptyState from '../components/EmptyState';
import LoadingState from '../components/common/LoadingState';
import { supabaseDB } from '../services/supabaseDB';
import { useAuth } from '../hooks/useAuth';

const formatDate = (value) =>
  new Date(value || Date.now()).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });

const Saved = () => {
  const { user } = useAuth();
  const [savedJobs, setSavedJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSavedJobs = async () => {
      if (!user) return;
      setLoading(true);
      const jobs = await supabaseDB.getSavedJobs(user.id);
      setSavedJobs(jobs);
      setLoading(false);
    };

    fetchSavedJobs();
  }, [user]);

  const handleUnsave = async (jobId) => {
    if (!user) return;
    // Optimistically remove from UI
    setSavedJobs((prev) => prev.filter((job) => job.id !== jobId));
    try {
      // Toggle saved status to false
      await supabaseDB.toggleSavedJob(user.id, jobId, true);
    } catch (err) {
      console.error('Failed to unsave job:', err);
      // If it fails, reload the list
      const jobs = await supabaseDB.getSavedJobs(user.id);
      setSavedJobs(jobs);
    }
  };

  return (
    <AppShell>
      <PageHeader title="Saved offers">
        {!loading && savedJobs.length > 0
          ? `${savedJobs.length} ${savedJobs.length === 1 ? 'offer' : 'offers'} kept for later.`
          : 'Offers you keep for later.'}
      </PageHeader>

      {loading && <LoadingState message="Loading your saved offers…" />}

      {!loading && savedJobs.length === 0 && (
        <EmptyState
          icon="bookmark_add"
          title="Nothing saved yet"
          action={<Link to="/dashboard" className="btn btn-primary">See your matches</Link>}
        >
          Open an offer and choose “Save” to keep it here.
        </EmptyState>
      )}

      {!loading && savedJobs.length > 0 && (
        <JobList label="Saved offers">
          {savedJobs.map((job) => (
            <JobRow
              key={job.id}
              job={job}
              showScore={false}
              meta={`Saved ${formatDate(job.saved_at || job.posted_at)}`}
              aside={
                <button onClick={() => handleUnsave(job.id)} className="btn btn-secondary btn-sm">
                  <span className="material-symbols-outlined" aria-hidden="true">bookmark_remove</span>
                  Remove
                </button>
              }
            />
          ))}
        </JobList>
      )}
    </AppShell>
  );
};

export default Saved;
