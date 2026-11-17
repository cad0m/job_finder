
const LoadingState = ({ message = 'Loading…' }) => (
  <div className="flex w-full items-center gap-3 py-16 text-graphite" role="status">
    <span className="spinner" aria-hidden="true" />
    <span>{message}</span>
  </div>
);

export default LoadingState;
