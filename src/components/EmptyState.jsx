
const EmptyState = ({ icon, title, children, action }) => (
  <div className="sheet flex flex-col items-start gap-3 border-dashed px-6 py-10 sm:px-10">
    {icon && <span className="material-symbols-outlined text-[1.75rem] text-pencil" aria-hidden="true">{icon}</span>}
    <h2 className="text-xl font-semibold">{title}</h2>
    {children && <p className="max-w-prose text-graphite">{children}</p>}
    {action && <div className="mt-2">{action}</div>}
  </div>
);

export default EmptyState;
