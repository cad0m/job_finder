import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import MatchScore from './MatchScore';

/*
  The hero shows the product doing its one job: a CV on the left, ranked offers
  on the right, and a highlighter marking what the selected offer matched.
  Everything here is example data and is labelled as such on the page.
*/
const OFFERS = [
  { id: 'data-eng', score: 91, title: 'Data Engineer', company: 'Banque Atlas', city: 'Casablanca', source: 'Jobzyn', skills: ['Python', 'Spark', 'Airflow', 'SQL'] },
  { id: 'bi', score: 84, title: 'Ingénieur BI', company: 'Groupe Tensift', city: 'Rabat', source: 'ANAPEC', skills: ['SQL', 'dbt', 'Power BI'] },
  { id: 'backend', score: 72, title: 'Développeur Python backend', company: 'Sqala Telecom', city: 'Tanger', source: 'LinkedIn', skills: ['Python', 'FastAPI', 'Docker'] },
];

// CV text as plain strings and skills. Skills are written as { s: 'name' }.
const CV_LINES = [
  ['Built the daily sales pipelines in ', { s: 'Python' }, ' and ', { s: 'Spark' }, ', scheduled with ', { s: 'Airflow' }, '.'],
  ['Modelled the warehouse in ', { s: 'SQL' }, ' and ', { s: 'dbt' }, '; reporting in ', { s: 'Power BI' }, '.'],
  ['Shipped internal services with ', { s: 'FastAPI' }, ' and ', { s: 'Docker' }, '.'],
];

const MatchDemo = () => {
  const [selected, setSelected] = useState(0);
  const [ready, setReady] = useState(false);

  // One load moment: the highlighter strokes draw in once the page is up.
  useEffect(() => {
    const t = setTimeout(() => setReady(true), 350);
    return () => clearTimeout(t);
  }, []);

  const offer = OFFERS[selected];
  let skillIndex = 0;

  return (
    <div className="relative">
      {/* The CV */}
      <article className="sheet relative z-10 w-full max-w-md -rotate-1 p-6 pb-12 shadow-[0_18px_40px_-24px_rgba(20,23,43,0.45)] sm:p-7 sm:pb-14" aria-label="Example CV">
        <p className="font-display text-xl font-bold" style={{ fontVariationSettings: '"wdth" 90' }}>Yasmine El Idrissi</p>
        <p className="text-sm text-graphite">Data engineer, Casablanca</p>
        <hr className="my-4 border-rule" />
        <p className="text-sm font-semibold">Experience</p>
        <ul className="mt-2 space-y-2 text-[0.9375rem] leading-relaxed text-graphite">
          {CV_LINES.map((line, i) => (
            <li key={i}>
              {line.map((part, j) => {
                if (typeof part === 'string') return <React.Fragment key={j}>{part}</React.Fragment>;
                const hit = ready && offer.skills.includes(part.s);
                const delay = hit ? `${skillIndex++ * 90}ms` : '0ms';
                return (
                  <span key={j} className="markable font-medium text-ink" data-hit={hit} style={{ transitionDelay: delay }}>
                    {part.s}
                  </span>
                );
              })}
            </li>
          ))}
        </ul>
      </article>

      {/* The ranked offers */}
      <div className="sheet relative z-20 -mt-5 ml-auto w-[94%] max-w-md overflow-hidden shadow-[0_18px_40px_-24px_rgba(20,23,43,0.45)] sm:-mt-8">
        <p className="border-b border-rule px-5 py-3 text-sm font-semibold">Offers ranked for this CV</p>
        <ul>
          {OFFERS.map((o, i) => {
            const active = i === selected;
            return (
              <li key={o.id} className="border-b border-rule last:border-b-0">
                <button
                  type="button"
                  aria-pressed={active}
                  onClick={() => setSelected(i)}
                  onMouseEnter={() => setSelected(i)}
                  onFocus={() => setSelected(i)}
                  className={`flex w-full items-center gap-4 px-5 py-3.5 text-left transition-colors ${active ? 'bg-pen-wash' : 'hover:bg-desk/70'}`}
                >
                  <MatchScore score={o.score} className="shrink-0" />
                  <span className="min-w-0">
                    <span className="block truncate font-semibold text-ink">{o.title}</span>
                    <span className="block truncate text-sm text-graphite">{o.company}, {o.city}. From {o.source}</span>
                  </span>
                </button>
              </li>
            );
          })}
        </ul>
      </div>

      <p className="mt-4 text-sm text-pencil">Example data. Pick an offer to see what it matched in the CV.</p>
    </div>
  );
};

const Hero = () => (
  <section className="mx-auto grid max-w-6xl items-center overflow-x-clip gap-12 px-4 pb-20 pt-12 sm:px-8 lg:grid-cols-[1.05fr_1fr] lg:gap-16 lg:pb-28 lg:pt-20">
    <div>
      <h1 className="text-[2.75rem] font-bold leading-[1.02] tracking-[-0.035em] sm:text-[3.75rem] lg:text-[4.25rem]">
        Your CV, matched against Morocco’s job boards.
      </h1>
      <p className="mt-6 max-w-xl text-lg text-graphite sm:text-xl">
        Upload your CV once. JobMatcher reads it, ranks offers from ANAPEC, Jobzyn and LinkedIn by how well they fit,
        and drafts the CV, cover letter and email for the ones you choose.
      </p>
      <div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-4">
        <Link to="/upload" className="btn btn-primary btn-lg">Upload your CV</Link>
        <a href="#how-it-works" className="link">See how it works</a>
      </div>
      <p className="mt-5 text-sm text-graphite">PDF or a photo of your CV, up to 10 MB.</p>
    </div>

    <MatchDemo />
  </section>
);

export default Hero;
