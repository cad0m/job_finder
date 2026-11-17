import { Link, NavLink, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import Logo from './Logo';

const NAV = [
  { name: 'Matches', icon: 'format_list_numbered', path: '/dashboard', also: ['/job-details', '/apply'] },
  { name: 'Search', icon: 'search', path: '/search' },
  { name: 'Saved', icon: 'bookmark', path: '/saved' },
  { name: 'Applications', short: 'Applied', icon: 'send', path: '/applied' },
  { name: 'Profile', icon: 'person', path: '/profile' },
];

const Sidebar = () => {
  const { signOut } = useAuth();
  const navigate = useNavigate();
  const { pathname } = useLocation();

  const handleLogout = async () => {
    await signOut();
    navigate('/');
  };

  const isActive = (item) =>
    pathname === item.path || (item.also || []).some((prefix) => pathname.startsWith(prefix));

  return (
    <>
      {/* Desktop: fixed left column */}
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-60 flex-col border-r border-rule bg-paper md:flex">
        <Link to="/dashboard" className="px-6 pb-6 pt-7">
          <Logo />
        </Link>

        <nav className="flex-1 px-3" aria-label="Main">
          <ul className="space-y-0.5">
            {NAV.map((item) => {
              const active = isActive(item);
              return (
                <li key={item.path}>
                  <NavLink
                    to={item.path}
                    aria-current={active ? 'page' : undefined}
                    className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-[0.9375rem] transition-colors ${
                      active ? 'bg-pen-wash font-semibold text-pen-dark' : 'text-graphite hover:bg-desk hover:text-ink'
                    }`}
                  >
                    <span className={`material-symbols-outlined ${active ? 'icon-fill' : ''}`} aria-hidden="true">{item.icon}</span>
                    {item.name}
                  </NavLink>
                </li>
              );
            })}
          </ul>
        </nav>

        <div className="space-y-1 border-t border-rule p-3">
          <Link to="/upload" className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-[0.9375rem] text-graphite transition-colors hover:bg-desk hover:text-ink">
            <span className="material-symbols-outlined" aria-hidden="true">upload_file</span>
            Upload a new CV
          </Link>
          <button onClick={handleLogout} className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-[0.9375rem] text-graphite transition-colors hover:bg-desk hover:text-ink">
            <span className="material-symbols-outlined" aria-hidden="true">logout</span>
            Sign out
          </button>
        </div>
      </aside>

      {/* Mobile: top bar + bottom tabs */}
      <header className="sticky top-0 z-40 flex h-14 items-center justify-between border-b border-rule bg-paper px-4 md:hidden">
        <Link to="/dashboard"><Logo /></Link>
        <div className="flex items-center gap-1">
          <Link to="/upload" className="grid h-10 w-10 place-items-center rounded-lg text-graphite hover:bg-desk" aria-label="Upload a new CV">
            <span className="material-symbols-outlined" aria-hidden="true">upload_file</span>
          </Link>
          <button onClick={handleLogout} className="grid h-10 w-10 place-items-center rounded-lg text-graphite hover:bg-desk" aria-label="Sign out">
            <span className="material-symbols-outlined" aria-hidden="true">logout</span>
          </button>
        </div>
      </header>

      <nav className="fixed inset-x-0 bottom-0 z-40 border-t border-rule bg-paper pb-[env(safe-area-inset-bottom)] md:hidden" aria-label="Main">
        <ul className="grid grid-cols-5">
          {NAV.map((item) => {
            const active = isActive(item);
            return (
              <li key={item.path}>
                <NavLink
                  to={item.path}
                  aria-current={active ? 'page' : undefined}
                  className={`flex flex-col items-center gap-0.5 py-2 text-[0.6875rem] ${active ? 'font-semibold text-pen-dark' : 'text-graphite'}`}
                >
                  <span className={`material-symbols-outlined text-[1.375rem] ${active ? 'icon-fill' : ''}`} aria-hidden="true">{item.icon}</span>
                  {item.short || item.name}
                </NavLink>
              </li>
            );
          })}
        </ul>
      </nav>
    </>
  );
};

export default Sidebar;
