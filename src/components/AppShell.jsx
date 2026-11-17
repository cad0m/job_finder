import Sidebar from './Sidebar';

/** Signed-in layout: navigation plus a centred content column. */
const AppShell = ({ children, width = 'max-w-5xl' }) => (
  <div className="min-h-screen bg-desk">
    <Sidebar />
    <main className="pb-24 md:pb-0 md:pl-60">
      <div className={`mx-auto w-full ${width} px-4 py-8 sm:px-8 md:py-12`}>{children}</div>
    </main>
  </div>
);

export const PageHeader = ({ title, children, action }) => (
  <header className="mb-8 flex flex-wrap items-end justify-between gap-4">
    <div className="max-w-2xl">
      <h1 className="text-[2rem] font-bold sm:text-[2.5rem]">{title}</h1>
      {children && <p className="mt-2 text-[1.0625rem] text-graphite">{children}</p>}
    </div>
    {action}
  </header>
);

export default AppShell;
