/* Form pieces shared by the auth screens (same markup as the approved sign-in design). */
export const MailIc = () => <svg className="ic" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3" /><path d="M4 7l8 6 8-6" /></svg>;
export const LockIc = () => <svg className="ic" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><rect x="5" y="10" width="14" height="10" rx="3" /><path d="M8 10V7a4 4 0 0 1 8 0v3" /></svg>;
const Arr = () => <svg className="arr" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" /></svg>;
const Ok = () => <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#FFFFFF" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>;

export const GoButton = ({ state, label, wait, ok, d = 3 }) => (
  <button className="go rise" style={{ '--d': String(d) }} type="submit" data-state={state}>
    <span className="s-go">{label}<Arr /></span><span className="s-wait"><i className="spin" />{wait}</span><span className="s-ok"><Ok />{ok}</span>
  </button>
);
