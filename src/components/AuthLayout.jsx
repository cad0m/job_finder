import { Link } from 'react-router-dom';
import Logo from './Logo';

/** Sign-in and sign-up share this: logo, one sheet of paper, nothing else. */
const AuthLayout = ({ title, intro, children, footer }) => (
  <div className="flex min-h-screen flex-col items-center px-4 py-10 sm:py-16">
    <Link to="/" aria-label="JobMatcher home" className="mb-8">
      <Logo />
    </Link>

    <main className="sheet w-full max-w-md p-6 sm:p-9">
      <h1 className="text-[1.75rem] font-bold">{title}</h1>
      {intro && <p className="mt-2 text-graphite">{intro}</p>}
      <div className="mt-7">{children}</div>
    </main>

    {footer && <p className="mt-6 text-[0.9375rem] text-graphite">{footer}</p>}
  </div>
);

export default AuthLayout;
