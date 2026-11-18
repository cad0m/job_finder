import { useRef, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { authMessage } from '../../lib/authErrors';
import usePauseOffscreen from '../shared/usePauseOffscreen';
import '../shared/jm-base.css';
import './SignUp.css';
import { SignUpHostHostMArt, SignUpHostArt } from './SignUpArt';

const strength = (v) => {
  let s = 0;
  if (v.length >= 8) s++; if (/[0-9]/.test(v)) s++; if (/[^A-Za-z0-9]/.test(v)) s++; if (v.length >= 12) s++;
  if (v.length < 8) s = Math.min(s, 1);
  return v ? s : 0;
};
const initials = (name) => name.trim().split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0].toUpperCase()).join('');

/* Markup generated from design/previews/signup.html by design/tools/html2react.py; behaviour wired by hand. */
export default function SignUpPage() {
  const { signUp } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const rootRef = useRef(null);
  usePauseOffscreen(rootRef);
  const [state, setState] = useState('idle');
  const [name, setName] = useState('');
  const [pw, setPw] = useState('');
  const [showPw, setShowPw] = useState(false);
  const [error, setError] = useState('');
  const [sentTo, setSentTo] = useState('');
  const [shake, setShake] = useState(0);
  const s = strength(pw);
  const hint = !pw || pw.length < 8 ? '8 or more characters. A number or a symbol makes it stronger.'
    : s < 3 ? 'Good start. Add a number or a symbol to make it stronger.' : 'Strong password.';
  const ini = initials(name);

  const onSubmit = async (e) => {
    e.preventDefault();
    if (state !== 'idle') return;
    const f = new FormData(e.currentTarget);
    const email = String(f.get('email') || '');
    setError(''); setState('wait');
    const { data, error: err } = await signUp(name, email, pw);
    if (err) { setState('idle'); setError(authMessage(err)); setShake((n) => n + 1); return; }
    // An existing, unconfirmed email comes back with no identities
    if (data?.user && Array.isArray(data.user.identities) && data.user.identities.length === 0) {
      setState('idle'); setError(authMessage({ message: 'User already registered' })); setShake((n) => n + 1); return;
    }
    setState('ok');
    if (!data?.session) { setSentTo(email.trim()); return; }     // email confirmation is on
    setTimeout(() => navigate(location.state?.from?.pathname || '/upload', { replace: true }), 900);
  };

  return (
    <div className="jm-signup" ref={rootRef}><div role="main" className="page">
<div className={`auth signup${state === 'ok' ? ' done' : ''}`} id="auth">
  <header className="ahdr">
    <Link className="logo" to="/"><img src="/jm/nabta-mark.svg" alt="" width="40" height="40" /><span className="display">JobMatcher</span></Link>
    <button className="lang" type="button" aria-label="Language: English. Also available in French and Arabic."><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#1E1C2B" strokeWidth="2" aria-hidden="true"><circle cx="12" cy="12" r="9" /><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z" /></svg><span>EN</span></button>
  </header>
  <section className="intro">
    <ol className="steps rise" style={{ "--d": "0" }} aria-label="Getting started">
      <li className="st on" aria-current="step"><b>1</b>Account</li><li className="bar" aria-hidden="true" /><li className="st"><b>2</b>Your CV</li><li className="bar" aria-hidden="true" /><li className="st"><b>3</b>Matches</li>
    </ol>
    <div className="head">
      <h1 className="display atitle"><span className="wd" style={{ "--w": "0" }}>Create</span> <span className="wd" style={{ "--w": "1" }}>your</span> <span className="wd" style={{ "--w": "2" }}>account.</span></h1>
      <p className="asub rise" style={{ "--d": "1" }}>Your account is the top of your CV. Fill it in here, then add the rest from your CV file.</p>
    </div>
    <ul className="next rise" style={{ "--d": "2" }}>
      <li><span className="ni"><svg className="" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M12 16V4M7 9l5-5 5 5" /><path d="M5 20h14" /></svg></span>Upload a PDF or a photo of your CV</li>
      <li><span className="ni"><svg className="" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="8" /><circle cx="12" cy="12" r="3" /></svg></span>See the offers that fit you, best first</li>
      <li><span className="ni"><svg className="" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M7 3h7l4 4v14H7z" /><path d="M14 3v4h4M10 12h5M10 16h5" /></svg></span>Get a tailored CV, cover letter and email</li>
    </ul>
  </section>
  <footer className="afoot"><span>© 2026 JobMatcher</span><Link to="/">Back to the home page</Link></footer>
  <div className="desk">
    <div className="aura a1" aria-hidden="true" /><div className="aura a2" aria-hidden="true" />
    <div className="fwrap">
    <SignUpHostHostMArt />
    <form className="sheet" id="authform" action="#" method="post" onSubmit={onSubmit} onInvalidCapture={() => setShake((n) => n + 1)}>
      <div className="kicker"><span>Curriculum vitae</span></div>
      <div className="stamp" aria-hidden="true">Ready<br />for<br />matches</div>
      <div className="s-head">
        <span className={`s-av${ini ? ' has' : ''}`} id="av" aria-hidden="true">{ini || <svg className="u" viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4" /><path d="M4 20c1.5-4 4.5-6 8-6s6.5 2 8 6" /></svg>}</span>
        <div className="s-name"><label htmlFor="name">Full name</label><input id="name" name="name" type="text" autoComplete="name" placeholder="Your full name" required value={name} onChange={(e) => setName(e.target.value)} /></div>
      </div>
      <div className="s-sec">
        <span className="sl">Contact</span>
        <div className="fld"><label className="lbl" htmlFor="email">Email</label><span className="ctl"><svg className="ic" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3" /><path d="M4 7l8 6 8-6" /></svg><input id="email" name="email" type="email" autoComplete="email" placeholder="you@example.com" required /></span></div>
      </div>
      <div className="s-sec">
        <span className="sl">Private</span>
        <div className="fld">
          <label className="lbl" htmlFor="password">Password</label>
          <span className="ctl"><svg className="ic" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><rect x="5" y="10" width="14" height="10" rx="3" /><path d="M8 10V7a4 4 0 0 1 8 0v3" /></svg><input id="password" name="password" type={showPw ? 'text' : 'password'} autoComplete="new-password" placeholder="At least 8 characters" required minLength="8" aria-describedby="pw-hint" value={pw} onChange={(e) => setPw(e.target.value)} /><button className="eye" type="button" data-for="password" aria-pressed={showPw} aria-label={showPw ? 'Hide password' : 'Show password'} onClick={() => setShowPw((v) => !v)}><svg className="e-on" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" /><circle cx="12" cy="12" r="3" /></svg><svg className="e-off" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M3 3l18 18" /><path d="M10.6 6.1A9.8 9.8 0 0 1 12 6c6.5 0 10 6 10 6a17 17 0 0 1-3.2 3.9M6.6 7.6C3.9 9.4 2 12 2 12s3.5 6 10 6c1.6 0 3-.3 4.3-.9" /><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2" /></svg></button></span>
          <div className="meter" data-s={s} aria-hidden="true"><i /><i /><i /><i /></div>
          <p className="hint" id="pw-hint">{hint}</p>
        </div>
      </div>
      <p className="next-m">Experience and skills come from your CV in step 2.</p>
      <div className="s-sec ghost" aria-hidden="true">
        <span className="sl">Experience</span>
        <div style={{ display: "flex", flexDirection: "column", gap: "7px", paddingTop: "4px" }}><i className="ln" style={{ "--w": "88%" }} /><i className="ln" style={{ "--w": "64%" }} /><span className="gnote">Filled in from your CV in step 2.</span></div>
      </div>
      <div className="s-sec ghost" aria-hidden="true" style={{ borderBottom: "0" }}>
        <span className="sl">Skills</span>
        <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}><i className="gpill" style={{ width: "64px" }} /><i className="gpill" style={{ width: "48px" }} /><i className="gpill" style={{ width: "80px" }} /><i className="gpill" style={{ width: "56px" }} /></div>
      </div>
      <div className="s-foot">
        <button key={shake} className={`go${shake ? ' shake' : ''}`} style={{ "--d": "0" }} type="submit" data-state={state}><span className="s-go">Create account<svg className="arr" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" /></svg></span><span className="s-wait"><i className="spin" />Creating your account…</span><span className="s-ok"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#FFFFFF" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>Account created</span></button>
        {error && <p className="note jm-msg bad" role="alert">{error}</p>}
        {sentTo && <p className="note jm-msg" role="status">Check your inbox: we sent a confirmation link to {sentTo}. Open it, then <Link to="/signin" state={{ email: sentTo }}>sign in</Link>.</p>}
        <p className="switch">Already have an account? <Link to="/signin">Sign in</Link></p>
      </div>
    </form>
    </div>
    <SignUpHostArt />
    <label className="mp" title="Pause the animation"><input type="checkbox" aria-label="Pause the animation" /><svg className="i-pause" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1.2" fill="#1E1C2B" /><rect x="14" y="5" width="4" height="14" rx="1.2" fill="#1E1C2B" /></svg><svg className="i-play" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="#1E1C2B" /></svg></label>
  </div>
</div>
</div></div>
  );
}
