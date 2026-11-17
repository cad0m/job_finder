import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import AppShell, { PageHeader } from '../components/AppShell';
import EmptyState from '../components/EmptyState';
import LoadingState from '../components/common/LoadingState';
import { supabaseDB } from '../services/supabaseDB';
import { useAuth } from '../hooks/useAuth';

const STATUS = {
  ready: { label: 'Documents ready', className: 'status-ok' },
  pending: { label: 'Waiting', className: 'status-warn' },
  generating: { label: 'Writing documents', className: 'status-info' },
  failed: { label: 'Failed', className: 'status-bad' },
};

const formatDate = (value) =>
  new Date(value).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });

const DocLink = ({ href, icon, children }) =>
  href ? (
    <a href={href} target="_blank" rel="noreferrer" className="btn btn-secondary btn-sm">
      <span className="material-symbols-outlined" aria-hidden="true">{icon}</span>
      {children}
    </a>
  ) : null;

const Applied = () => {
  const { user } = useAuth();
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchApplications = async () => {
      if (!user) return;
      setLoading(true);
      const data = await supabaseDB.getApplications(user.id);
      setApplications(data);
      setLoading(false);
    };

    fetchApplications();
  }, [user]);

  return (
    <AppShell>
      <PageHeader title="Applications">
        {!loading && applications.length > 0
          ? `${applications.length} ${applications.length === 1 ? 'application' : 'applications'}, newest first, with the documents written for each.`
          : 'Every application you generate, with its documents.'}
      </PageHeader>

      {loading && <LoadingState message="Loading your applications…" />}

      {!loading && applications.length === 0 && (
        <EmptyState
          icon="send"
          title="No applications yet"
          action={<Link to="/dashboard" className="btn btn-primary">See your matches</Link>}
        >
          Open an offer and choose “Prepare application” to get a CV, cover letter and email written for it.
        </EmptyState>
      )}

      {!loading && applications.length > 0 && (
        <ul className="sheet divide-y divide-rule overflow-hidden" aria-label="Applications">
          {applications.map((app) => {
            const status = STATUS[app.status] || { label: app.status, className: '' };
            return (
              <li key={app.id} className="grid gap-x-6 gap-y-3 px-4 py-5 sm:grid-cols-[1fr_auto] sm:px-6">
                <div className="min-w-0">
                  <h2 className="font-sans text-[1.0625rem] font-semibold leading-snug tracking-normal">
                    <Link to={`/job-details/${app.job_id}`} className="hover:text-pen">
                      {app.job?.title || 'Offer no longer available'}
                    </Link>
                  </h2>
                  <p className="mt-0.5 flex flex-wrap gap-x-3 text-[0.9375rem] text-graphite">
                    {app.job?.company && <span className="font-medium text-ink">{app.job.company}</span>}
                    {app.job?.location && <span>{app.job.location}</span>}
                  </p>

                  {app.status === 'ready' && (app.cv_url || app.cover_letter_url || app.email_url) && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      <DocLink href={app.cv_url} icon="badge">CV</DocLink>
                      <DocLink href={app.cover_letter_url} icon="article">Cover letter</DocLink>
                      <DocLink href={app.email_url} icon="mail">Email</DocLink>
                    </div>
                  )}

                  {app.status === 'failed' && (
                    <p className="mt-3 text-[0.9375rem] text-bad">
                      {app.error_message || 'The documents could not be written.'}{' '}
                      <Link to={`/apply/${app.job_id}`} className="link">Generate again</Link>
                    </p>
                  )}
                </div>

                <div className="flex items-center gap-3 sm:flex-col sm:items-end sm:gap-2">
                  <span className={`status ${status.className}`}>{status.label}</span>
                  <span className="text-sm text-graphite">{formatDate(app.created_at)}</span>
                </div>
              </li>
            );
          })}
        </ul>
      )}
    </AppShell>
  );
};

export default Applied;
