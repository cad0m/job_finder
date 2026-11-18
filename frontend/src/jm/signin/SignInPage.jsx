import { useRef, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { authMessage } from '../../lib/authErrors';
import usePauseOffscreen from '../shared/usePauseOffscreen';
import '../shared/jm-base.css';
import './SignIn.css';
import { SignInHostHostMArt, SignInHostArt } from './SignInArt';

/* Markup generated from design/previews/signin.html by design/tools/html2react.py; behaviour wired by hand. */
export default function SignInPage() {
  const { signIn, resendConfirmation } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const rootRef = useRef(null);
  const emailRef = useRef(null);
  usePauseOffscreen(rootRef);
  const [state, setState] = useState('idle');          // idle | wait | ok: drives the button
  const [showPw, setShowPw] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState(location.state?.notice || '');
  const [needsConfirm, setNeedsConfirm] = useState(false);
  const [shake, setShake] = useState(0);

  const onSubmit = async (e) => {
    e.preventDefault();
    if (state !== 'idle') return;
    const f = new FormData(e.currentTarget);
    const email = String(f.get('email') || ''), password = String(f.get('password') || '');
    setError(''); setNotice(''); setNeedsConfirm(false); setState('wait');
    const { error: err } = await signIn(email, password);
    if (err) {
      setState('idle'); setError(authMessage(err)); setShake((n) => n + 1);
      setNeedsConfirm((err.message || '').toLowerCase().includes('email not confirmed'));
      return;
    }
    // "Keep me signed in" off: forget the session when the browser closes
    try {
      if (f.get('keep')) localStorage.removeItem('jm-session-only');
      else { localStorage.setItem('jm-session-only', '1'); sessionStorage.setItem('jm-alive', '1'); }
    } catch { /* storage blocked: keep the default */ }
    setState('ok');
    setTimeout(() => navigate(location.state?.from?.pathname || '/dashboard', { replace: true }), 700);
  };

  const resend = async () => {
    const email = emailRef.current?.value || '';
    const { error: err } = await resendConfirmation(email);
    if (err) setError(authMessage(err));
    else { setNeedsConfirm(false); setError(''); setNotice(`We sent a new confirmation link to ${email.trim()}.`); }
  };

  return (
    <div className="jm-signin" ref={rootRef}><div className="page">
<div className={`auth signin${state === 'ok' ? ' done' : ''}`} id="auth">
  <header className="ahdr">
    <Link className="logo" to="/"><img src="/jm/nabta-mark.svg" alt="" width="40" height="40" /><span className="display">JobMatcher</span></Link>
    <button className="lang" type="button" aria-label="Language: English. Also available in French and Arabic."><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#1E1C2B" strokeWidth="2" aria-hidden="true"><circle cx="12" cy="12" r="9" /><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z" /></svg><span>EN</span></button>
  </header>
  <main className="aform">
    <div className="head">
      <h1 className="display atitle"><span className="wd" style={{ "--w": "0" }}>Welcome</span> <span className="wd" style={{ "--w": "1" }}>back.</span></h1>
      <p className="asub rise" style={{ "--d": "0" }}>Sign in to see your matches and the applications you have prepared.</p>
    </div>
    <div className="fwrap">
      <p className="mchip" aria-hidden="true"><span className="mc-ic"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" /><path d="M15.5 15.5L20 20" /></svg></span><span className="mc-sk">Python</span><span className="mc-ar">→</span><span><b>Data Analyst</b> · 91%</span></p>
      <SignInHostHostMArt />
    <form id="authform" action="#" method="post" onSubmit={onSubmit} onInvalidCapture={() => setShake((n) => n + 1)}>
      <div className="fld rise" style={{ "--d": "1" }}>
        <label className="lbl" htmlFor="email">Email</label>
        <span className="ctl"><svg className="ic" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3" /><path d="M4 7l8 6 8-6" /></svg><input ref={emailRef} id="email" name="email" type="email" autoComplete="email" placeholder="you@example.com" defaultValue={location.state?.email || ''} required /></span>
      </div>
      <div className="fld rise" style={{ "--d": "2" }}>
        <span className="lbl"><label htmlFor="password">Password</label><Link to="/forgot-password" onClick={(e) => { e.preventDefault(); navigate('/forgot-password', { state: { email: emailRef.current?.value || '' } }); }}>Forgot password?</Link></span>
        <span className="ctl"><svg className="ic" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><rect x="5" y="10" width="14" height="10" rx="3" /><path d="M8 10V7a4 4 0 0 1 8 0v3" /></svg><input id="password" name="password" type={showPw ? 'text' : 'password'} autoComplete="current-password" placeholder="Your password" required /><button className="eye" type="button" data-for="password" aria-pressed={showPw} aria-label={showPw ? 'Hide password' : 'Show password'} onClick={() => setShowPw((v) => !v)}><svg className="e-on" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" /><circle cx="12" cy="12" r="3" /></svg><svg className="e-off" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M3 3l18 18" /><path d="M10.6 6.1A9.8 9.8 0 0 1 12 6c6.5 0 10 6 10 6a17 17 0 0 1-3.2 3.9M6.6 7.6C3.9 9.4 2 12 2 12s3.5 6 10 6c1.6 0 3-.3 4.3-.9" /><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2" /></svg></button></span>
      </div>
      <label className="chk rise" style={{ "--d": "3" }}><input type="checkbox" id="keep" name="keep" defaultChecked /><span className="box"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#FFFFFF" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path pathLength="1" d="M5 12.5l4.5 4.5L19 7.5" /></svg></span>Keep me signed in on this device</label>
      <button key={shake} className={`go rise${shake ? ' shake' : ''}`} style={{ "--d": "4" }} type="submit" data-state={state}><span className="s-go">Sign in<svg className="arr" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" /></svg></span><span className="s-wait"><i className="spin" />Signing in…</span><span className="s-ok"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#FFFFFF" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>Welcome back</span></button>
    </form>
    </div>
    {notice && <p className="note jm-msg" role="status">{notice}</p>}
    {error && <p className="note jm-msg bad" role="alert">{error}{needsConfirm && <> <button type="button" className="jm-linkbtn" onClick={resend}>Send the link again</button></>}</p>}
    <p className="switch rise" style={{ "--d": "5" }}>New to JobMatcher? <Link to="/signup">Create an account</Link></p>
  </main>
  <footer className="afoot"><span>© 2026 JobMatcher</span><Link to="/">Back to the home page</Link></footer>
  <aside className="stage" aria-label="How JobMatcher reads your CV">
    <div className="aura a1" aria-hidden="true" /><div className="aura a2" aria-hidden="true" />
    <div className="st-in">
      <span className="st-chip"><i className="live" /><span>New offers every day<span className="hide-sm"> from ANAPEC, Jobzyn and LinkedIn</span></span></span>
      <h2 className="display st-title">Your CV in. The right jobs out.</h2>
    </div>
    <div className="scan" aria-hidden="true">
      <div className="cv">
        <div className="cv-top"><span className="cv-av"><img src="/jm/peep-cv-match.svg" alt="" /></span><span><span className="cv-name">Salma El Idrissi</span><span className="cv-role">Data analyst · Casablanca</span></span></div>
        <span className="cv-sec">Experience</span>
        <i className="ln" style={{ "--w": "92%" }} /><i className="ln" style={{ "--w": "76%" }} /><i className="ln" style={{ "--w": "84%" }} />
        <span className="cv-sec">Skills</span>
        <div className="cv-skills"><span className="sk" data-k="0" style={{ "--hit": "hit0", "--dot": "dot0" }}>Python</span><span className="sk">Excel</span><span className="sk" data-k="1" style={{ "--hit": "hit1", "--dot": "dot1" }}>SQL</span><span className="sk">Tableau</span><span className="sk" data-k="2" style={{ "--hit": "hit2", "--dot": "dot2" }}>Power BI</span><span className="sk">Arabic</span><span className="sk">French</span></div>
        <span className="cv-sec">Education</span>
        <i className="ln" style={{ "--w": "70%" }} /><i className="ln" style={{ "--w": "52%" }} />
      </div>
      <div className="finds">
        <div className="find top" style={{ "--pop": "pop0" }}><span className="pct">91<small>%</small></span><span style={{ minWidth: "0" }}><span className="t1">Data Analyst</span><span className="t2">Attijariwafa bank · Casablanca</span></span></div>
        <div className="find" style={{ "--pop": "pop1" }}><span className="pct">84<small>%</small></span><span style={{ minWidth: "0" }}><span className="t1">BI Developer</span><span className="t2">OCP Group · Rabat</span></span></div>
        <div className="find" style={{ "--pop": "pop2" }}><span className="pct">76<small>%</small></span><span style={{ minWidth: "0" }}><span className="t1">Stage PFE Data</span><span className="t2">inwi · Casablanca</span></span></div>
      </div>
      <div className="loupe"><i className="lens" /><i className="handle" /></div>
    </div>
    <SignInHostArt />
    <label className="mp" title="Pause the animation"><input type="checkbox" aria-label="Pause the animation" /><svg className="i-pause" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1.2" fill="#1E1C2B" /><rect x="14" y="5" width="4" height="14" rx="1.2" fill="#1E1C2B" /></svg><svg className="i-play" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="#1E1C2B" /></svg></label>
  </aside>
</div>
</div></div>
  );
}
