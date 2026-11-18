import { useRef } from 'react';
import { Link } from 'react-router-dom';
import usePauseOffscreen from '../shared/usePauseOffscreen';
import { SignInHostHostMArt, SignInHostArt } from './SignInArt';
import '../shared/jm-base.css';
import './SignIn.css';

/** The sign-in page's frame (figure, CV stage, footer) for the other auth screens: forgot and reset password. */
export default function AuthShell({ title, sub, children, foot, done = false }) {
  const rootRef = useRef(null);
  usePauseOffscreen(rootRef);
  return (
    <div className="jm-signin" ref={rootRef}><div className="page">
<div className={`auth signin${done ? ' done' : ''}`} id="auth">
  <header className="ahdr">
    <Link className="logo" to="/"><img src="/jm/nabta-mark.svg" alt="" width="40" height="40" /><span className="display">JobMatcher</span></Link>
    <button className="lang" type="button" aria-label="Language: English. Also available in French and Arabic."><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#1E1C2B" strokeWidth="2" aria-hidden="true"><circle cx="12" cy="12" r="9" /><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z" /></svg><span>EN</span></button>
  </header>
  <main className="aform">
    <div className="head">
      <h1 className="display atitle">{title.map((w, i) => <span key={i}><span className="wd" style={{ "--w": String(i) }}>{w}</span>{i < title.length - 1 ? ' ' : ''}</span>)}</h1>
      <p className="asub rise" style={{ "--d": "0" }}>{sub}</p>
    </div>
    <div className="fwrap">
      <p className="mchip" aria-hidden="true"><span className="mc-ic"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" /><path d="M15.5 15.5L20 20" /></svg></span><span className="mc-sk">Python</span><span className="mc-ar">→</span><span><b>Data Analyst</b> · 91%</span></p>
      <SignInHostHostMArt />
    {children}
    </div>
    
    {foot && <p className="switch rise" style={{ "--d": "5" }}>{foot}</p>}
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
