import { Link } from 'react-router-dom';
import Logo from './Logo';

const STEPS = ['Upload your CV', 'Check what was read'];

/** The two-step setup flow: upload, then review. `step` is 1 or 2. */
const OnboardingLayout = ({ step, title, intro, children }) => (
  <div className="min-h-screen">
    <header className="border-b border-rule">
      <div className="mx-auto flex h-16 max-w-3xl items-center justify-between px-4 sm:px-8">
        <Link to="/" aria-label="JobMatcher home"><Logo /></Link>
        <Link to="/dashboard" className="text-[0.9375rem] font-medium text-graphite hover:text-ink">Go to my matches</Link>
      </div>
    </header>

    <main className="mx-auto max-w-3xl px-4 py-10 sm:px-8 sm:py-14">
      <ol className="mb-8 flex flex-wrap gap-x-6 gap-y-2 text-[0.9375rem]" aria-label="Setup steps">
        {STEPS.map((name, i) => {
          const n = i + 1;
          const current = n === step;
          const done = n < step;
          return (
            <li key={name} aria-current={current ? 'step' : undefined} className={`flex items-center gap-2 ${current ? 'font-semibold text-ink' : 'text-graphite'}`}>
              <span className={`grid h-6 w-6 place-items-center rounded-full text-[0.8125rem] font-semibold ${current ? 'bg-ink text-white' : done ? 'bg-ok-wash text-ok' : 'border border-rule-strong'}`}>
                {done ? <span className="material-symbols-outlined text-[1rem]" aria-hidden="true">check</span> : n}
              </span>
              {name}
            </li>
          );
        })}
      </ol>

      <h1 className="text-[2rem] font-bold sm:text-[2.5rem]">{title}</h1>
      {intro && <p className="mt-3 max-w-2xl text-[1.0625rem] text-graphite">{intro}</p>}

      <div className="mt-8">{children}</div>
    </main>
  </div>
);

export default OnboardingLayout;
