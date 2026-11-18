import { useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { edgeFunctions } from '../../services/edgeFunctions';
import usePauseOffscreen from '../shared/usePauseOffscreen';
import '../shared/jm-base.css';
import './Upload.css';

const OK_TYPES = ['application/pdf', 'image/jpeg', 'image/png', 'image/webp'];
const MAX = 10 * 1048576;
const size = (b) => (b > 1048576 ? (b / 1048576).toFixed(1) + ' MB' : Math.max(1, Math.round(b / 1024)) + ' KB');
const initials = (s) => (s || '').trim().split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0].toUpperCase()).join('') || '?';
const names = (xs) => (Array.isArray(xs) ? xs : []).map((x) => (typeof x === 'string' ? x : x?.name)).filter(Boolean);
const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;
const toBase64 = (file) => new Promise((resolve, reject) => {
  const r = new FileReader();
  r.onload = () => resolve(String(r.result).split(',')[1]);
  r.onerror = () => reject(new Error('The file could not be opened. Choose it again.'));
  r.readAsDataURL(file);
});

/* Markup generated from design/previews/upload.html by design/tools/html2react.py; behaviour wired by hand.
   States: empty, drag, file, loading (waiting for cv-ocr), reading (reveal), done, error. */
export default function UploadPage() {
  const { user } = useAuth();
  const rootRef = useRef(null);
  const fileRef = useRef(null);
  const camRef = useRef(null);
  usePauseOffscreen(rootRef);
  const [state, setState] = useState('empty');
  const [file, setFile] = useState(null);
  const [error, setError] = useState('Use a PDF, or a clear photo of your CV in JPEG, PNG or WEBP, up to 10 MB.');
  const [cand, setCand] = useState(null);
  const fullName = user?.user_metadata?.full_name || '';

  const take = (f) => {
    if (!f) return;
    if (!OK_TYPES.includes(f.type)) { setError('This file type is not supported. Use a PDF, or a photo of your CV in JPEG, PNG or WEBP.'); setState('error'); return; }
    if (f.size > MAX) { setError('This file is larger than 10 MB. Try a smaller PDF, or a photo of your CV.'); setState('error'); return; }
    setFile(f); setState('file');
  };
  const pick = () => fileRef.current?.click();
  const onPicked = (e) => { take(e.target.files[0]); e.target.value = ''; };

  const read = async () => {
    if (!file) return;
    setState('loading');
    try {
      const fileBase64 = await toBase64(file);
      const data = await edgeFunctions.invokeCvOcr({ fileBase64, filename: file.name, mimeType: file.type });
      edgeFunctions.invokeEmbedCv().catch((err) => console.warn('Embedding delayed', err));
      setCand(data?.candidate || { skills: [], experience: [], education: [], languages: [] });
      setState('reading');
      setTimeout(() => setState('done'), 4600);
    } catch (err) {
      setError(err.message || 'Your CV could not be read. Upload it again, or use a different file.');
      setState('error');
    }
  };

  const jobs = Array.isArray(cand?.experience) ? cand.experience : [];
  const skills = names(cand?.skills);
  const edu = Array.isArray(cand?.education) ? cand.education : [];
  const langs = names(cand?.languages);
  const found = cand ? [plural(jobs.length, 'job', 'jobs'), plural(skills.length, 'skill', 'skills'), plural(edu.length, 'degree', 'degrees'), plural(langs.length, 'language', 'languages')] : [];
  const foundText = found.length ? `Found ${found.slice(0, -1).join(', ')} and ${found[found.length - 1]}.` : '';

  return (
    <div className="jm-upload" ref={rootRef}><div role="main" className="page">
<div className="auth signup up" id="auth" data-state={state}>
  <header className="ahdr">
    <Link className="logo" to="/"><img src="/jm/nabta-mark.svg" alt="" width="40" height="40" /><span className="display">JobMatcher</span></Link>
    <button className="lang" type="button" aria-label="Language: English. Also available in French and Arabic."><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#1E1C2B" strokeWidth="2" aria-hidden="true"><circle cx="12" cy="12" r="9" /><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z" /></svg><span>EN</span></button>
  </header>
  <section className="intro">
    <ol className="steps rise" style={{ "--d": "0" }} aria-label="Getting started">
      <li className="st ok"><b>✓</b>Account</li><li className="bar ok" aria-hidden="true" /><li className="st on" aria-current="step"><b>2</b>Your CV</li><li className="bar" aria-hidden="true" /><li className="st"><b>3</b>Matches</li>
    </ol>
    <div className="head">
      <h1 className="display atitle"><span className="wd" style={{ "--w": "0" }}>Add</span> <span className="wd" style={{ "--w": "1" }}>your</span> <span className="wd" style={{ "--w": "2" }}>CV.</span></h1>
      <p className="asub rise" style={{ "--d": "1" }}>JobMatcher reads it and fills in the rest of your sheet. You check everything before it is saved.</p>
    </div>
    <ul className="next rise" style={{ "--d": "2" }}>
      <li><span className="ni"><svg className="" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M7 3h7l4 4v14H7z" /><path d="M14 3v4h4M10 12h5M10 16h5" /></svg></span>A PDF, or a photo or scan in JPEG, PNG or WEBP, up to 10 MB</li>
      <li><span className="ni"><svg className="" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="8" /><circle cx="12" cy="12" r="3" /></svg></span>Experience, skills, education and languages are read for you</li>
      <li><span className="ni"><svg className="" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M12 16V4M7 9l5-5 5 5" /><path d="M5 20h14" /></svg></span>Then you see the offers that fit you, best first</li>
    </ul>
  </section>
  <footer className="afoot"><span>© 2026 JobMatcher</span><Link to="/">Back to the home page</Link></footer>
  <div className="desk">
    <div className="aura a1" aria-hidden="true" /><div className="aura a2" aria-hidden="true" />
    <div className="fwrap">
    <div className="sheet" id="sheet">
      <div className="kicker"><span>Curriculum vitae</span></div>
      <div className="stamp read" aria-hidden="true">CV<br />read</div>
      <div className="s-head">
        <span className="s-av done" aria-hidden="true">{initials(fullName || user?.email)}</span>
        <div className="s-name"><span className="s-nm">{fullName || 'Your CV'}</span><span className="s-me">{user?.email}</span></div>
      </div>
      <div className="zone" aria-live="polite">
        <label className="drop" data-z="empty" htmlFor="cvfile" id="drop" onDragEnter={(e) => { e.preventDefault(); setState('drag'); }} onDragOver={(e) => { e.preventDefault(); if (state !== 'drag') setState('drag'); }} onDragLeave={(e) => { if (!e.currentTarget.contains(e.relatedTarget)) setState('empty'); }} onDrop={(e) => { e.preventDefault(); setState('empty'); take(e.dataTransfer.files[0]); }}>
          <span className="drop-ic"><svg viewBox="0 0 48 48" width="44" height="44" fill="none" stroke="#1E1C2B" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M13 6h15l9 9v27H13z" fill="#FFFFFF" /><path d="M28 6v9h9" /><path d="M25 37V22M19 28l6-6 6 6" stroke="#FF7F45" /></svg></span>
          <p className="drop-t"><span className="d-desk">Drop your CV here</span><span className="d-phone">Choose your CV</span></p>
          <p className="drop-s">PDF, JPEG, PNG or WEBP, up to 10 MB</p>
          <span className="drop-b"><span className="pill ink"><svg className="" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M3 7h6l2 2h10v10H3z" /></svg>Choose a file</span><button className="pill line cam" type="button" id="camb" onClick={(e) => { e.preventDefault(); camRef.current?.click(); }}><svg className="" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M4 8h3l2-3h6l2 3h3v11H4z" /><circle cx="12" cy="13" r="3.5" /></svg>Take a photo</button></span>
          
        </label>
        <input ref={fileRef} onChange={onPicked} className="vh" type="file" id="cvfile" accept=".pdf,.jpg,.jpeg,.png,.webp,application/pdf,image/jpeg,image/png,image/webp" />
        <input ref={camRef} onChange={onPicked} className="vh" type="file" id="cvcam" aria-label="Take a photo of your CV" accept="image/*" capture="environment" />
        <div className="picked" data-z="file">
          <div className="fchip" style={{ "--k": "0" }}><span className="fdoc">CV<b id="fext">{(file?.name.split('.').pop() || 'PDF').toUpperCase().slice(0, 4)}</b></span><span style={{ minWidth: "0" }}><span className="fname" id="fname">{file?.name}</span><span className="fsize" id="fsize">{file ? size(file.size) : ''}</span></span><button className="fx" type="button" id="fremove" aria-label="Remove this file" onClick={() => { setFile(null); setState('empty'); }}><svg className="" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" /></svg></button></div>
          <button className="go" type="button" id="read" style={{ "--k": "1" }} data-state="idle" onClick={read}><span className="s-go">Read my CV<svg className="arr" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" /></svg></span></button>
          <p className="alt" style={{ "--k": "2" }}>Wrong file? <button type="button" id="again" onClick={() => { setState('empty'); pick(); }}>Choose another one</button></p>
        </div>
        <div className="cvbody" data-z="read">
          <div className="scanl" aria-hidden="true" />
          <div className="sec"><span className="sl">Experience</span><div className="cell"><div className="ph" style={{ "--t": "1" }} aria-hidden="true"><i style={{ width: "92%" }} /><i style={{ width: "70%" }} /></div>
            {jobs.slice(0, 4).map((j, k) => <div key={k} className="job rv-i" style={{ "--t": "1", "--k": String(k) }}><b>{[j.job_title, j.company].filter(Boolean).join(' · ')}</b><span>{String(j.start_date || '').slice(-4)}</span></div>)}</div></div>
          <div className="sec"><span className="sl">Skills</span><div className="cell"><div className="ph" style={{ "--t": "2" }} aria-hidden="true"><i style={{ width: "84%" }} /><i style={{ width: "56%" }} /></div>
            <div className="chips">{skills.slice(0, 12).map((s, k) => <span key={k} className="c rv-i" style={{ "--t": "2", "--k": String(k) }}>{s}</span>)}</div></div></div>
          <div className="sec"><span className="sl">Education</span><div className="cell"><div className="ph" style={{ "--t": "3" }} aria-hidden="true"><i style={{ width: "76%" }} /></div>
            {edu.slice(0, 3).map((e, k) => <div key={k} className="edu rv-i" style={{ "--t": "3", "--k": String(k) }}><b>{[e.degree, e.field].filter(Boolean).join(', ')}</b><span>{e.institution}</span></div>)}</div></div>
          <div className="sec"><span className="sl">Languages</span><div className="cell"><div className="ph" style={{ "--t": "3.6" }} aria-hidden="true"><i style={{ width: "50%" }} /></div>
            <div className="chips">{langs.slice(0, 6).map((s, k) => <span key={k} className="c rv-i" style={{ "--t": "3.6", "--k": String(k) }}>{s}</span>)}</div></div></div>
          <p className="status"><i className="spin" /><span className="sw"><span>Reading your CV…</span><span>Finding your experience…</span><span>Listing your skills…</span><span>Almost done…</span></span></p>
        </div>
        <div className="donebar" data-z="done">
          <p className="found"><span className="ok"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#FFFFFF" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg></span><b>{foundText}</b></p>
          <Link className="go" to="/review" state={{ candidate: cand }} id="toreview"><span className="s-go">Check your details<svg className="arr" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" /></svg></span></Link>
          <p className="alt">Not your best version? <button type="button" id="redo" onClick={() => { setCand(null); setState('empty'); pick(); }}>Upload a different file</button></p>
        </div>
        <div className="oops" data-z="error" role="alert">
          <span className="oops-ic" style={{ "--k": "0" }}><svg className="" viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M12 4l9 16H3z" /><path d="M12 10v4M12 17.5v.5" /></svg></span>
          <h3 style={{ "--k": "1" }}>We could not read this file</h3>
          <p id="errmsg" style={{ "--k": "2" }}>{error}</p>
          <button className="pill ink" type="button" id="retry" onClick={() => { setState('empty'); pick(); }} style={{ "--k": "3" }}><svg className="" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M3 7h6l2 2h10v10H3z" /></svg>Choose another file</button>
        </div>
      </div>
    </div>
    </div>
    <label className="mp" title="Pause the animation"><input type="checkbox" aria-label="Pause the animation" /><svg className="i-pause" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1.2" fill="#1E1C2B" /><rect x="14" y="5" width="4" height="14" rx="1.2" fill="#1E1C2B" /></svg><svg className="i-play" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="#1E1C2B" /></svg></label>
  </div>
</div>
</div></div>
  );
}
