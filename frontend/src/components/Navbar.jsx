import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import Logo from './Logo';

const LINKS = [
  { name: 'How it works', href: '#how-it-works' },
  { name: 'What you get', href: '#application' },
  { name: 'Sources', href: '#sources' },
];

const Navbar = () => {
  const { user } = useAuth();

  return (
    <header className="sticky top-0 z-50 border-b border-rule bg-desk/90 backdrop-blur-sm">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-6 px-4 sm:px-8">
        <Link to="/" aria-label="JobMatcher home">
          <Logo />
        </Link>

        <nav className="hidden items-center gap-7 md:flex" aria-label="Page sections">
          {LINKS.map((link) => (
            <a key={link.href} href={link.href} className="text-[0.9375rem] text-graphite transition-colors hover:text-ink">
              {link.name}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-2 sm:gap-4">
          {user ? (
            <Link to="/dashboard" className="btn btn-primary btn-sm">Open my matches</Link>
          ) : (
            <>
              <Link to="/signin" className="px-2 text-[0.9375rem] font-semibold text-ink hover:text-pen">Sign in</Link>
              <Link to="/upload" className="btn btn-primary btn-sm">Upload your CV</Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
