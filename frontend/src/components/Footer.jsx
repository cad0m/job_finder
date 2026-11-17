import { Link } from 'react-router-dom';
import Logo from './Logo';

const Footer = () => (
  <footer className="border-t border-rule">
    <div className="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-8 text-sm text-graphite sm:flex-row sm:items-center sm:justify-between sm:px-8">
      <Logo />
      <nav className="flex flex-wrap gap-x-6 gap-y-2" aria-label="Footer">
        <Link to="/signin" className="hover:text-ink">Sign in</Link>
        <Link to="/signup" className="hover:text-ink">Create an account</Link>
        <a href="https://github.com/cad0m/job_finder" className="hover:text-ink" target="_blank" rel="noreferrer">Source on GitHub</a>
      </nav>
      <p>© {new Date().getFullYear()} JobMatcher</p>
    </div>
  </footer>
);

export default Footer;
