import Logo from '../Logo';

const InitialLoader = () => (
  <div className="fixed inset-0 z-[100] flex flex-col items-center justify-center gap-5 bg-desk" role="status">
    <Logo />
    <span className="spinner" aria-hidden="true" />
    <span className="sr-only">Loading JobMatcher</span>
  </div>
);

export default InitialLoader;
