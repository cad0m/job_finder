import { Fragment, useEffect, useMemo, useRef, useState } from 'react';
import { Link, Navigate, useLocation, useParams } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { supabaseDB } from '../../services/supabaseDB';
import { edgeFunctions } from '../../services/edgeFunctions';
import { ApplyGuideArt, ApplyGuideMiniArt } from './ApplyArt';
import { initials, loadCandidate, loadJob, logoClass, TODAY } from '../dashboard/data';
import '../shared/jm-base.css';
import './Apply.css';

/* Prepare application (design/previews/apply.html): choose a template on the user's real CV,
   then generate-cv writes the CV, letter and email, and generate-pdf makes the files. */

const TPL = [
  ['t1', 'Classic', 'Classic is the safest template. It reads well in any office, from banks to public institutions.'],
  ['t2', 'Two columns', 'Two columns puts contact and skills on the right and gives your experience room.'],
  ['t3', 'Dark sidebar', 'Dark sidebar keeps your skills in view. A recruiter sees them in a second.'],
  ['t4', 'Formal serif', 'Formal serif reads like a printed letter. A good fit for consulting and large groups.'],
  ['t5', 'Warm sidebar', 'Warm sidebar is soft and easy to read, even on a phone screen.'],
];
const READY_TIP = 'All set. Read it once, then send it from your own email.';

const Cup = ({ p = 0, w = 22, lid }) => {
  const h = Math.round(37 * Math.max(0, Math.min(100, p))) / 100;
  return (
    <svg className="cup" viewBox="0 0 48 56" width={w} height={Math.round((w * 56) / 48)} aria-hidden="true">
      <rect className="lvl" id={lid} x="16" y={50 - h} width="16" height={h} rx="1.5" fill="#FF7F45" />
      <rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" strokeWidth="2.8" />
      <path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" strokeWidth="2.8" strokeLinejoin="round" />
    </svg>
  );
};
const IcBack = () => <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6" /></svg>;
const IcChev2 = () => <svg className="chev2" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6" /></svg>;
const IcArr = () => <svg className="arr" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" /></svg>;
const IcDl = () => <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5" /><path d="M5 20h14" /></svg>;
const IcCopy = () => <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinejoin="round" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2" /><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3" /></svg>;
const IcPrev = () => <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6" /></svg>;
const IcNext = () => <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6" /></svg>;
const IcTick = () => <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#FFFFFF" strokeWidth="3.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>;
const IcZoom = () => <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5" /><path d="M16 16l4 4M11 8v6M8 11h6" /></svg>;

/* ── One CV model for both sources: the saved CV (before) and generate-cv's data_cv (after) ── */
const names = (xs) => (Array.isArray(xs) ? xs : []).map((x) => (typeof x === 'string' ? x : x?.name)).filter(Boolean);
const fromCandidate = (c, links) => ({
  name: c?.full_name || '',
  headline: c?.experience?.[0]?.job_title || '',
  contact: [c?.email, c?.phone, c?.location, links.linkedin && `linkedin.com/in/${links.linkedin}`].filter(Boolean),
  summary: c?.professional_summary || '',
  jobs: (c?.experience || []).slice(0, 3).map((j) => ({ title: j.job_title, dates: [j.start_date, j.is_current ? 'Present' : j.end_date].filter(Boolean).join(' to '), company: j.company, bullets: (j.responsibilities || []).filter(Boolean).slice(0, 3) })),
  edu: (c?.education || []).slice(0, 3).map((e) => ({ title: [e.degree, e.field].filter(Boolean).join(', '), sub: [e.institution, e.graduation_year].filter(Boolean).join(', ') })),
  cert: names(c?.certifications)[0] || '',
  skills: names(c?.skills).slice(0, 10),
  langs: names(c?.languages),
});
const fromDataCv = (d) => ({
  name: d.name || '',
  headline: d.title || '',
  contact: [d.email, d.phone, d.location, d.linkedin].filter(Boolean),
  summary: d.description || d.tagline || '',
  jobs: (d.experience || []).slice(0, 3).map((j) => ({ title: j.role, dates: j.date, company: [j.company, j.location].filter(Boolean).join(', '), bullets: (j.bullets || []).slice(0, 3) })),
  edu: (d.education || []).slice(0, 3).map((e) => ({ title: e.degree, sub: [e.school, e.date].filter(Boolean).join(', ') })),
  cert: '',
  skills: (d.skills?.length ? d.skills : (d.skills_structured || []).flatMap((s) => String(s.items || '').split(',').map((x) => x.trim()))).filter(Boolean).slice(0, 10),
  langs: names(d.languages),
});

/** Wrap the skills the offer asks for in the orange highlighter */
const Marked = ({ text, hits }) => {
  if (!hits?.length || !text) return text || null;
  const re = new RegExp(`(${hits.map((h) => h.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})`, 'gi');
  return String(text).split(re).map((part, i) => (i % 2 ? <span className="mark" key={i}>{part}</span> : <Fragment key={i}>{part}</Fragment>));
};

function CvDoc({ cv, tpl, hits, shown = 99 }) {
  const cls = (k, i) => `s ${k}${i < shown ? ' shw' : ''}`;
  return (
    <div className={`cvd ${tpl}`} aria-hidden="true"><div className="in">
      <div className={cls('h', 0)} style={{ gridArea: 'h' }}><span className="nm">{cv.name}</span><span className="hl">{cv.headline}</span></div>
      <div className={cls('ct', 1)} style={{ gridArea: 'ct' }}>{cv.contact.map((c, i) => <Fragment key={i}>{c}{i < cv.contact.length - 1 && <br />}</Fragment>)}</div>
      <div className={cls('sum', 2)} style={{ gridArea: 'sum' }}><h6>Profile</h6><p><Marked text={cv.summary} hits={hits} /></p></div>
      <div className={cls('exp', 3)} style={{ gridArea: 'exp' }}><h6>Experience</h6>{cv.jobs.map((j, i) => (
        <div className="j" key={i}><b>{j.title}<span>{j.dates}</span></b><em>{j.company}</em><ul>{j.bullets.map((b, k) => <li key={k}><Marked text={b} hits={hits} /></li>)}</ul></div>
      ))}</div>
      <div className={cls('edu', 4)} style={{ gridArea: 'edu' }}><h6>Education</h6>{cv.edu.map((e, i) => <p key={i}><b>{e.title}</b><br />{e.sub}</p>)}{cv.cert && <p className="crt"><b>Certification</b><br />{cv.cert}</p>}</div>
      <div className={cls('skl', 5)} style={{ gridArea: 'skl' }}><h6>Skills</h6><p>{cv.skills.map((s, i) => <Fragment key={i}>{hits.some((h) => h.toLowerCase() === s.toLowerCase()) ? <span className="mark">{s}</span> : s}{i < cv.skills.length - 1 && ' · '}</Fragment>)}</p></div>
      <div className={cls('lng', 6)} style={{ gridArea: 'lng' }}><h6>Languages</h6><p>{cv.langs.map((l, i) => <Fragment key={i}>{l}{i < cv.langs.length - 1 && <br />}</Fragment>)}</p></div>
      <div className={cls('side', 7)} style={{ gridArea: 'side' }} />
    </div></div>
  );
}

const greeting = (txt) => (/[àâçéèêëîïôûù]|veuillez|madame|monsieur/i.test(txt) ? 'Madame, Monsieur,' : 'Dear hiring team,');

export default function ApplyPage() {
  const { jobId } = useParams();
  const { user } = useAuth();
  const location = useLocation();
  const [cand, setCand] = useState(undefined);
  const [job, setJob] = useState(null);
  const [tpl, setTpl] = useState('t3');
  const [step, setStep] = useState('setup');
  const [doc, setDoc] = useState('cv');
  const [face, setFace] = useState('open');
  const [tip, setTip] = useState(TPL[2][2]);
  const [nodOn, setNodOn] = useState(false);
  const [phase, setPhase] = useState(0);          // writing step: 0 CV, 1 letter, 2 email, 3 PDFs, 4 done
  const [pct, setPct] = useState(0);
  const [out, setOut] = useState(null);           // { data_cv, data_letter, data_email, files }
  const [shown, setShown] = useState(99);
  const [error, setError] = useState('');
  const [toast, setToast] = useState('');
  const [lift, setLift] = useState(0);
  const [pen, setPen] = useState(0);
  const [links, setLinks] = useState(() => ({ linkedin: user?.user_metadata?.linkedin || '', github: user?.user_metadata?.github || '', portfolio: user?.user_metadata?.portfolio || '' }));
  const zoomRef = useRef(null);
  const faceT = useRef(null);
  const swipeX = useRef(null);
  const score = location.state?.score ?? null;

  useEffect(() => {
    if (!user || !jobId) return;
    (async () => {
      const c = await loadCandidate(user.id);
      const full = c ? await supabaseDB.getCandidateProfile(user.id, user.email) : null;
      setCand(full);
      setJob(await loadJob(Number(jobId), c));
    })();
  }, [user, jobId]);

  const speak = (text, after = 'open') => {
    setTip(text); setNodOn(false); requestAnimationFrame(() => setNodOn(true)); setFace('talk');
    clearTimeout(faceT.current); faceT.current = setTimeout(() => setFace(after), 900);
  };
  const say = (t) => { setToast(t); setTimeout(() => setToast(''), 3000); };

  const hits = job?.hits || [];
  const cv = useMemo(() => (out?.data_cv ? fromDataCv(out.data_cv) : fromCandidate(cand, links)), [out, cand, links]);
  const letter = out?.data_letter;
  const mail = out?.data_email;

  const pick = (t) => {
    const apply = () => setTpl(t);
    if (document.startViewTransition && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) document.startViewTransition(apply); else apply();
    setDoc('cv'); setLift((n) => n + 1);
    speak(TPL.find((x) => x[0] === t)[2]);
  };
  const stepTpl = (d) => { const i = TPL.findIndex((x) => x[0] === tpl); pick(TPL[(i + d + TPL.length) % TPL.length][0]); };

  /* Writing: the cup fills while the real calls run; sections reveal as results arrive */
  const write = async () => {
    if (!user || !job) return;
    setError(''); setOut(null); setStep('writing'); setDoc('cv'); setPhase(0); setPct(0); setShown(0); setPen((n) => n + 1);
    speak(hits.length ? `I am putting ${hits.slice(0, 3).join(', ')} first, because the offer asks for them.` : 'I am tailoring your CV to this offer.', 'focus');
    const t0 = performance.now();
    let target = 0.55;
    const tick = () => { const p = Math.min(target, (performance.now() - t0) / 60000 + 0.02); setPct((x) => Math.max(x, Math.round(p * 100))); };
    const iv = setInterval(tick, 250);
    try {
      const social = {
        linkedin: links.linkedin ? `linkedin.com/in/${links.linkedin}` : '', linkedin_url: links.linkedin ? `https://www.linkedin.com/in/${links.linkedin}` : '',
        github_label: links.github ? `github.com/${links.github}` : '', github_url: links.github ? `https://github.com/${links.github}` : '',
        portfolio_label: links.portfolio || '', portfolio_url: links.portfolio ? `https://${links.portfolio.replace(/^https?:\/\//, '')}` : '',
      };
      const gen = await edgeFunctions.invokeGenerateCv({ user_id: user.id, job_id: Number(jobId), ...social });
      setOut({ ...gen });
      for (let i = 1; i <= 8; i += 1) setTimeout(() => setShown(i), i * 220);
      setTimeout(() => { setDoc('cl'); setPhase(1); setPen((n) => n + 1); speak(`Now a letter to ${job.company}, in your words.`, 'focus'); }, 2200);
      setTimeout(() => { setDoc('em'); setPhase(2); setPen((n) => n + 1); speak('A short email to send with both files.', 'focus'); }, 4600);
      target = 0.9;
      const [pdf] = await Promise.all([
        edgeFunctions.invokeGeneratePdf({ user_id: user.id, job_id: Number(jobId), template_id: `template${tpl.slice(1)}.tex`, ...gen }),
        new Promise((r) => setTimeout(r, 5200)),
      ]);
      setPhase(3); setDoc('cv'); speak('Turning everything into PDFs.', 'focus');
      const files = pdf?.files || {};
      setOut({ ...gen, files });
      try {
        await supabaseDB.saveJobApplication({
          user_id: user.id, job_id: Number(jobId), candidate_id: cand?.id || null, template_id: `template${tpl.slice(1)}.tex`,
          linkedin_url: social.linkedin_url, github_url: social.github_url, portfolio_url: social.portfolio_url,
          cv_url: files.cv, cover_letter_url: files.cover_letter, email_url: files.email,
          data_cv: gen.data_cv, data_letter: gen.data_letter, data_email: gen.data_email, status: 'ready',
          track_status: 'Applied', date_applied: TODAY(), last_activity: TODAY(), sent_kind: 'gen',
          company: job.company, role: job.title, city: job.city, source: job.source, job_link: job.url,
        });
      } catch (err) { console.warn('Application saved later', err); }
      clearInterval(iv); setPct(100); setPhase(4);
      setTimeout(() => { setStep('ready'); speak(READY_TIP, 'happy'); }, 600);
    } catch (err) {
      clearInterval(iv);
      setStep('setup'); setShown(99); setOut(null);
      setError(err.message || 'The documents could not be written. Try again in a minute.');
      speak('Something went wrong on our side. Try again in a minute.');
    }
  };

  const copy = async (what) => {
    const text = what === 'sub' ? mail?.subject : `${mail?.subject}\n\n${mail?.body}`;
    try { await navigator.clipboard.writeText(text || ''); say('Copied'); } catch { say('Select the text and copy it'); }
  };
  const openFile = (k) => { const u = out?.files?.[k]; if (u) window.open(u, '_blank', 'noopener'); else say('This file is not ready yet'); };

  if (!jobId) return <Navigate to="/dashboard" replace />;
  if (cand === null) return <Navigate to="/upload" replace />;
  const stepN = { setup: 1, writing: 2, ready: 3 }[step];
  const who = (cv.name || user?.email || 'You').replace(/\s+/g, '_');
  const wsteps = [['Tailoring your CV', 'Your matched skills go first'], ['Writing the cover letter', job ? `Addressed to ${job.company}` : 'Addressed to the company'], ['Drafting the email', 'Short, with both files attached'], ['Making the PDFs', 'One page each']];

  return (
    <div className="jm-apply"><div role="main" className="page">
      <div className={`studio${phase >= 1 || step === 'ready' ? ' marks-on' : ''}${step === 'writing' ? ' writing-on' : ''}`} id="studio" data-step={step} data-face={face}>
        <header className="stop">
          <Link className="back" to="/dashboard" aria-label="Back to your matches"><IcBack /><span>Back to your matches</span></Link>
          <ol className="psteps" aria-label="Progress">{['Set up', 'Writing', 'Ready'].map((l, i) => (
            <li key={l} className={i + 1 === stepN ? 'on' : i + 1 < stepN ? 'ok' : ''} data-s={i + 1} onClick={() => { if (i === 0 && step === 'ready') { setStep('setup'); setDoc('cv'); } }}><b>{i + 1 < stepN ? '✓' : i + 1}</b><span>{l}</span></li>
          ))}</ol>
          {job && <div className="ochip"><span className={`logo-c ${logoClass(job.company)}`} aria-hidden="true">{initials(job.company)}</span><span><b>{job.title}</b><span>{job.company}</span></span>{score != null && <span className="cupv"><Cup p={score} w={18} />{score}<small>%</small></span>}</div>}
        </header>
        <div className="st2">
          <div className="ctrl">
            <section className="cpane c-setup" aria-labelledby="h1s">
              <div className="cscroll">
                <span className="kick2" style={{ '--d': '0' }}>Step 1 of 3</span>
                <h1 className="display" id="h1s" style={{ '--d': '1' }}>Choose a CV template.</h1>
                <p className="lead3" style={{ '--d': '2' }}>Every template shows your real CV. Switch between them above the preview, or swipe it on a phone.</p>
                {job && <div className="offer2" style={{ '--d': '3' }}><div className="o-h"><span><b>{job.title}</b><small>{[job.company, job.city].filter(Boolean).join(' · ')}</small></span>{score != null && <span className="o-c"><Cup p={score} />{score}<small>%</small></span>}</div>
                  {hits.length > 0 && <span className="chips2">{hits.slice(0, 6).map((h) => <span className="c2 hit" key={h}>{h}</span>)}</span>}
                  <p>{hits.length ? 'These go first, marked in orange on the CV.' : 'Your CV is tailored to the words of this offer.'}</p>
                  <Link className="editl" to="/review">Something wrong in your CV? Edit your details</Link></div>}
                {error && <p className="note jm-msg bad" role="alert">{error}</p>}
                <details className="lkd" style={{ '--d': '4' }}><summary><span>Links on your CV <small>· {[links.linkedin, links.github, links.portfolio].filter(Boolean).length} of 3</small></span><IcChev2 /></summary>
                  <div className="lnks">
                    <div className="lk"><label htmlFor="ln-li">LinkedIn</label><div className="pre2"><span>linkedin.com/in/</span><input id="ln-li" value={links.linkedin} onChange={(e) => setLinks({ ...links, linkedin: e.target.value })} /></div></div>
                    <div className="lk"><label htmlFor="ln-gh">GitHub</label><div className="pre2"><span>github.com/</span><input id="ln-gh" placeholder="username" value={links.github} onChange={(e) => setLinks({ ...links, github: e.target.value })} /></div></div>
                    <div className="lk"><label htmlFor="ln-pf">Portfolio</label><div className="pre2"><span>https://</span><input id="ln-pf" placeholder="yoursite.ma" value={links.portfolio} onChange={(e) => setLinks({ ...links, portfolio: e.target.value })} /></div></div>
                  </div></details>
                <ul className="get" style={{ '--d': '5' }}><li><i>CV</i>A CV tailored to this offer</li><li><i>CL</i>A cover letter to the company</li><li><i>EM</i>An email to send with both</li></ul>
              </div>
              <div className="cta2" style={{ '--d': '5' }}><button className="go write" type="button" disabled={!job || !cand} onClick={write}><span className="s-go">Write my application<IcArr /></span></button><small>A CV, a cover letter and an email. About a minute.</small></div>
            </section>
            <section className="cpane c-writing" aria-labelledby="h1w" aria-live="polite">
              <div className="cscroll">
                <span className="kick2">Step 2 of 3</span>
                <h1 className="display" id="h1w">Writing your application.</h1>
                <div className="wcup"><span className="bigcup"><Cup p={pct} w={52} /><span>{pct}</span><small>%</small></span></div>
                <ol className="wsteps2">{wsteps.map(([a, b], i) => <li key={a} className={i < phase ? 'done' : i === phase ? 'now' : ''}><i /><span>{a}<small>{b}</small></span></li>)}</ol>
                <p className="lead2">You can leave; it will wait for you in <Link to="/applied" style={{ color: 'var(--ink)', fontWeight: '600' }}>Applied</Link>.</p>
              </div>
            </section>
            <section className="cpane c-ready" aria-labelledby="h1r">
              <div className="cscroll">
                <span className="kick2">Step 3 of 3</span>
                <h1 className="display" id="h1r">Ready to send.</h1>
                <div className="dlist" role="tablist" aria-label="Documents">
                  {[['cv', 'CV', 'CV', `${who}_CV.pdf · 1 page`, 'cv'], ['cl', 'CL', 'Cover letter', `${who}_Letter.pdf · 1 page`, 'cover_letter'], ['em', 'EM', 'Email', 'Subject and message to copy', null]].map(([d, i, b, s, f]) => (
                    <button key={d} className="ditem" role="tab" aria-selected={doc === d} type="button" onClick={() => { setDoc(d); if (window.matchMedia('(max-width: 900px)').matches) document.getElementById('stage')?.scrollIntoView({ behavior: 'smooth', block: 'start' }); }}>
                      <span className="di">{i}</span><span><b>{b}</b><small>{s}</small></span>
                      {f ? <span className="dl2 dl" role="button" aria-label={`Download the ${b.toLowerCase()}`} onClick={(e) => { e.stopPropagation(); openFile(f); }}><IcDl /></span> : <span className="dl2" aria-hidden="true"><IcCopy /></span>}
                    </button>
                  ))}
                </div>
                <div className="racts2"><Link className="go" to="/applied"><span className="s-go">Done<IcArr /></span></Link><button className="ghost3 dlall" type="button" onClick={() => { openFile('cv'); openFile('cover_letter'); }}><IcDl />Download all</button></div>
                <div className="ready-more"><button className="chdesign" type="button" onClick={() => { setStep('setup'); setDoc('cv'); speak(TPL.find((x) => x[0] === tpl)[2]); }}>Change the template</button><button className="chdesign" type="button" onClick={write}>Write it again</button></div>
              </div>
            </section>
          </div>
          <section className="stage3" id="stage" data-doc={doc} aria-label="Preview">
            <div className="tbar" role="group" aria-labelledby="tb-l"><div className="tb-l" id="tb-l"><b>CV template</b><span>{TPL.findIndex((x) => x[0] === tpl) + 1} of 5</span></div>
              <button className="arw" type="button" aria-label="Previous template" onClick={() => stepTpl(-1)}><IcPrev /></button>
              <div className="tstrip" role="radiogroup" aria-label="CV template">{TPL.map(([t, n]) => (
                <label className="tthumb" key={t}><input type="radio" name="tpl" value={t} checked={tpl === t} onChange={() => pick(t)} /><span className="tt-doc"><CvDoc cv={cv} tpl={t} hits={[]} />{t === 't3' && <em className="sug">Suggested</em>}<i className="tt-ck"><IcTick /></i></span><span className="tt-n">{n}</span></label>
              ))}</div>
              <button className="arw" type="button" aria-label="Next template" onClick={() => stepTpl(1)}><IcNext /></button></div>
            <div className="paper" id="paper" key={`lift${lift}`} onPointerDown={(e) => { swipeX.current = e.clientX; }} onPointerUp={(e) => { if (swipeX.current !== null && step === 'setup' && Math.abs(e.clientX - swipeX.current) > 50) stepTpl(e.clientX < swipeX.current ? 1 : -1); swipeX.current = null; }}>
              <div className="layer l-cv big" id="bigcv"><CvDoc cv={cv} tpl={tpl} hits={hits} shown={step === 'writing' ? shown : 99} /></div>
              <div className="layer l-cl"><div className="ltr" aria-hidden="true"><div className="lin">
                <div className="from shw"><b>{cv.name}</b><span>{cv.contact.slice(0, 3).join(' · ')}</span></div>
                {letter ? <>
                  <p className="shw">{letter.date}</p><p className="shw">{letter.company_name}</p><p className="shw">{greeting((letter.sections || []).join(' '))}</p>
                  {(letter.sections || []).map((s, i) => <p className="shw" key={i}>{s}</p>)}
                  <p className="shw">{letter.closing_line}<br />{cv.name}</p>
                </> : <p className="shw" style={{ color: 'var(--muted)' }}>Your letter is being written…</p>}
              </div></div></div>
              <div className="layer l-em"><div className="mail">
                <div className="mrow shw"><span>To</span><b>The recruiter, from the original post</b><span /></div>
                <div className="mrow shw"><span>Subject</span><b>{mail?.subject || '…'}</b><button className="copy" type="button" onClick={() => copy('sub')}><IcCopy />Copy</button></div>
                <p className="mbody shw">{mail?.body || 'Your email is being written…'}</p>
                <div className="shw"><button className="copy" type="button" onClick={() => copy('all')}><IcCopy />Copy subject and message</button></div>
              </div></div>
              <div className={`pen${step === 'writing' ? ' run' : ''}`} key={`pen${pen}`} aria-hidden="true" />
              <button className="zoomb" type="button" onClick={() => zoomRef.current?.showModal()}><IcZoom />View full size</button>
              <ApplyGuideArt nod={nodOn} />
              <div className="bubble" role="status"><b>Your guide</b><span className="bt swap" key={tip}>{tip}</span></div>
            </div>
            <div className="tipbar"><span className="mini-g"><ApplyGuideMiniArt /></span><p className="swap" key={tip}>{tip}</p></div>
            <div className="pdfs" aria-hidden="true">{['CV.pdf', 'Letter.pdf', 'Email'].map((p) => <span key={p} className={phase >= 3 ? 'shw' : ''}>{p}</span>)}</div>
            <div className="stamp2" aria-hidden="true">Ready<br />to<br />send</div>
          </section>
          <dialog className="zoom" ref={zoomRef} aria-label="Your CV at full size"><div className="zbar"><b>Your CV</b><button className="zx" type="button" aria-label="Close" onClick={() => zoomRef.current?.close()}>×</button></div><div className="zbody"><div className="zdoc"><CvDoc cv={cv} tpl={tpl} hits={hits} /></div></div></dialog>
        </div>
        {toast && <div className="toast" role="status">{toast}</div>}
      </div>
    </div></div>
  );
}
