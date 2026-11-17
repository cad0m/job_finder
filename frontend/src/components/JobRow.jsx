import { Link } from 'react-router-dom';
import MatchScore from './MatchScore';

const normalise = (value) => String(value).trim().toLowerCase();

/**
 * One offer in a ranked list.
 * `candidateSkills` is optional: when given, the offer's skills that also
 * appear on the CV are highlighted.
 */
const JobRow = ({ job, candidateSkills = [], showScore = true, meta, aside, linkState }) => {
  const owned = candidateSkills.map(normalise);
  const isHit = (skill) => {
    const s = normalise(skill);
    return owned.some((o) => o === s || o.includes(s) || s.includes(o));
  };
  const skills = (job.skills || []).slice(0, 6);

  return (
    <li className="group relative grid grid-cols-[auto_1fr] gap-x-4 gap-y-3 px-4 py-5 transition-colors hover:bg-desk/60 sm:grid-cols-[auto_1fr_auto] sm:gap-x-6 sm:px-6">
      {showScore && (
        <div className="row-span-2 pt-0.5 sm:row-span-1">
          <MatchScore score={job.match_score} />
        </div>
      )}

      <div className={`min-w-0 ${showScore ? '' : 'col-span-2 sm:col-span-1'}`}>
        <h3 className="font-sans text-[1.0625rem] font-semibold leading-snug tracking-normal text-ink">
          <Link
            to={`/job-details/${job.id}`}
            state={linkState ?? { match_score: job.match_score ?? null }}
            className="after:absolute after:inset-0 after:content-[''] group-hover:text-pen"
          >
            {job.title}
          </Link>
        </h3>
        <p className="mt-0.5 flex flex-wrap gap-x-3 text-[0.9375rem] text-graphite">
          <span className="font-medium text-ink">{job.company}</span>
          {job.location && <span>{job.location}</span>}
        </p>

        {(skills.length > 0 || job.salary_range) && (
          <ul className="mt-3 flex flex-wrap gap-1.5">
            {skills.map((skill, i) => (
              <li key={i} className={`chip ${isHit(skill) ? 'chip-hit' : ''}`}>{skill}</li>
            ))}
            {job.salary_range && <li className="chip">{job.salary_range}</li>}
          </ul>
        )}
      </div>

      <div className="col-start-2 flex items-center gap-3 text-sm text-graphite sm:col-start-3 sm:flex-col sm:items-end sm:justify-between sm:gap-2">
        <span>{meta ?? job.posted_at ?? ''}</span>
        {/* Sits above the stretched title link so its controls stay clickable. */}
        {aside && <div className="relative z-10">{aside}</div>}
      </div>
    </li>
  );
};

export const JobRowSkeleton = () => (
  <li className="grid grid-cols-[auto_1fr] gap-x-4 px-4 py-5 sm:gap-x-6 sm:px-6" aria-hidden="true">
    <div className="skeleton h-9 w-16" />
    <div>
      <div className="skeleton h-5 w-2/5" />
      <div className="skeleton mt-2 h-4 w-1/4" />
      <div className="mt-3 flex gap-1.5">
        <div className="skeleton h-6 w-16" />
        <div className="skeleton h-6 w-20" />
        <div className="skeleton h-6 w-14" />
      </div>
    </div>
  </li>
);

/** Paper sheet that holds a list of JobRow items. */
export const JobList = ({ children, label }) => (
  <ul className="sheet divide-y divide-rule overflow-hidden" aria-label={label}>
    {children}
  </ul>
);

export default JobRow;
