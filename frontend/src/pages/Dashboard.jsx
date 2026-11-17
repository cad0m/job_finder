import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import AppShell, { PageHeader } from '../components/AppShell';
import JobRow, { JobList, JobRowSkeleton } from '../components/JobRow';
import EmptyState from '../components/EmptyState';
import { useAuth } from '../hooks/useAuth';
import { useJobMatch } from '../hooks/useJobMatch';
import { supabaseDB } from '../services/supabaseDB';

const DEFAULT_FILTERS = { roleType: 'All', minSalary: 0, experienceLevel: 'All' };

const Dashboard = () => {
  const { user } = useAuth();
  const [candidateProfile, setCandidateProfile] = useState(undefined);
  const [profileLoading, setProfileLoading] = useState(true);

  // Fetch the candidate profile so we can pass it to the hook for scoring
  useEffect(() => {
    const loadProfile = async () => {
      if (user) {
        setProfileLoading(true);
        try {
          // Use our standardized method with email fallback
          const profileData = await supabaseDB.getCandidateProfile(user.id, user.email);
          setCandidateProfile(profileData);
        } catch (err) {
          console.error('Dashboard: Failed to load profile for matching', err);
        } finally {
          setProfileLoading(false);
        }
      } else {
        setProfileLoading(false);
      }
    };
    loadProfile();
  }, [user]);

  const {
    jobs,
    loading: jobsLoading,
    searchQuery,
    setSearchQuery,
    filters,
    setFilters,
    loadMore,
    hasMore,
    totalCount,
  } = useJobMatch(candidateProfile);

  // Combine loading states
  const loading = profileLoading || jobsLoading;
  const hasProfile = Boolean(candidateProfile?.user_id);
  const candidateSkills = Array.isArray(candidateProfile?.skills) ? candidateProfile.skills : [];
  const filtersActive =
    searchQuery !== '' ||
    filters.roleType !== DEFAULT_FILTERS.roleType ||
    filters.minSalary !== DEFAULT_FILTERS.minSalary ||
    filters.experienceLevel !== DEFAULT_FILTERS.experienceLevel;

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const clearAll = () => {
    setSearchQuery('');
    setFilters(DEFAULT_FILTERS);
  };

  return (
    <AppShell>
      <PageHeader title="Your matches">
        {loading
          ? 'Ranking offers against your CV…'
          : hasProfile
            ? `${totalCount} ${totalCount === 1 ? 'offer' : 'offers'}, best fit first. Highlighted skills are on your CV.`
            : `${totalCount} ${totalCount === 1 ? 'offer' : 'offers'}, not ranked yet.`}
      </PageHeader>

      {!loading && !hasProfile && (
        <div className="notice notice-info mb-6 items-center justify-between">
          <span>Upload your CV to rank these offers by how well they fit you.</span>
          <Link to="/upload" className="btn btn-primary btn-sm shrink-0">Upload your CV</Link>
        </div>
      )}

      {/* Search and filters */}
      <div className="mb-5 grid gap-3 sm:grid-cols-[1fr_auto_auto_auto]">
        <div className="relative">
          <span className="material-symbols-outlined pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-pencil" aria-hidden="true">search</span>
          <input
            type="search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Filter by title, company or skill"
            aria-label="Filter your matches"
            className="field pl-10"
          />
        </div>

        <select
          value={filters.roleType}
          onChange={(e) => handleFilterChange('roleType', e.target.value)}
          aria-label="Contract type"
          className="field sm:w-40"
        >
          <option value="All">Any contract</option>
          <option value="Full-time">Full-time</option>
          <option value="Contract">Contract</option>
        </select>

        <select
          value={filters.experienceLevel}
          onChange={(e) => handleFilterChange('experienceLevel', e.target.value)}
          aria-label="Experience level"
          className="field sm:w-40"
        >
          <option value="All">Any level</option>
          <option value="Junior">Junior</option>
          <option value="Mid">Mid-level</option>
          <option value="Senior">Senior</option>
        </select>

        <select
          value={filters.minSalary}
          onChange={(e) => handleFilterChange('minSalary', Number(e.target.value))}
          aria-label="Minimum salary"
          className="field sm:w-40"
        >
          <option value="0">Any salary</option>
          <option value="120000">$120k+</option>
          <option value="150000">$150k+</option>
          <option value="180000">$180k+</option>
        </select>
      </div>

      {loading ? (
        <JobList label="Loading offers">
          {Array.from({ length: 5 }, (_, i) => <JobRowSkeleton key={i} />)}
        </JobList>
      ) : jobs.length === 0 ? (
        <EmptyState
          icon="search_off"
          title={filtersActive ? 'No offers fit these filters' : 'No offers yet'}
          action={filtersActive && <button onClick={clearAll} className="btn btn-secondary">Clear filters</button>}
        >
          {filtersActive
            ? 'Widen the filters or clear them to see every offer again.'
            : 'New offers are collected every day. Check back soon.'}
        </EmptyState>
      ) : (
        <>
          <JobList label="Offers ranked by match">
            {jobs.map((job) => (
              <JobRow key={job.id} job={job} candidateSkills={candidateSkills} showScore={hasProfile || job.match_score != null} />
            ))}
          </JobList>

          <div className="mt-6 flex flex-wrap items-center gap-4">
            {hasMore && <button onClick={loadMore} className="btn btn-secondary">Show more offers</button>}
            {filtersActive && <button onClick={clearAll} className="link">Clear filters</button>}
          </div>
        </>
      )}
    </AppShell>
  );
};

export default Dashboard;
