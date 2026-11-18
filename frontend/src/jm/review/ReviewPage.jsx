import { useEffect, useMemo, useRef, useState } from 'react';
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { supabase } from '../../lib/supabaseClient';
import { supabaseDB } from '../../services/supabaseDB';
import { edgeFunctions } from '../../services/edgeFunctions';
import '../shared/jm-base.css';
import './Review.css';

/* "Check your details": the approved design (design/previews/review.html) as a React form.
   Data: candidates row (from cv-ocr), links in the user's account metadata. */

const LEVELS = [['junior', 'Junior'], ['mid', 'Mid-level'], ['senior', 'Senior'], ['lead', 'Lead']];
const asList = (xs) => (Array.isArray(xs) ? xs : []).map((x) => (typeof x === 'string' ? x : x?.name)).filter(Boolean);
const blankJob = () => ({ job_title: '', company: '', start_date: '', end_date: '', is_current: false, responsibilities: [''] });
const blankEdu = () => ({ degree: '', field: '', institution: '', graduation_year: '' });
const jobMissingEnd = (j) => !j.is_current && !String(j.end_date || '').trim();

const Chev = ({ cls = 'chev2' }) => <svg className={cls} viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6" /></svg>;
const Tick = () => <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#FFFFFF" strokeWidth="3.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>;
const Plus = () => <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14" /></svg>;
const Arrow = () => <svg className="arr" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" /></svg>;
const Ok = () => <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#FFFFFF" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>;
const FileIc = () => <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinejoin="round" aria-hidden="true"><path d="M6 3h8l4 4v14H6z" /><path d="M14 3v4h4" /></svg>;

function Chips({ items, onChange, label }) {
  const [draft, setDraft] = useState('');
  return (
    <div className="chips">
      {items.map((s, i) => (
        <span className="chip" key={`${s}-${i}`}>{s}<button type="button" aria-label={`Remove ${s}`} onClick={() => onChange(items.filter((_, k) => k !== i))}>×</button></span>
      ))}
      <span className="addchip"><Plus /><input aria-label={label} placeholder={label} value={draft} onChange={(e) => setDraft(e.target.value)}
        onKeyDown={(e) => { if (e.key === 'Enter' && draft.trim()) { e.preventDefault(); onChange([...items, draft.trim()]); setDraft(''); } }} /></span>
    </div>
  );
}

/** The "your file" sheet on the left, rebuilt from what was read. */
function Doc({ c, links }) {
  const jobs = c.experience || [];
  const contact = [c.email, c.location, links.linkedin && `linkedin.com/in/${links.linkedin}`].filter(Boolean).join(' · ');
  return (
    <div className="doc" aria-hidden="true">
      <div className="db d-name">{(c.full_name || 'Your name').toUpperCase()}</div>
      <div className="db d-role">{jobs[0]?.job_title || ''}</div>
      <div className="db d-contact">{contact}</div>
      <div className="db d-rule" />
      {c.professional_summary && <div className="db d-sum"><div className="d-h">Profile</div><div className="d-p">{c.professional_summary}</div></div>}
      {jobs.length > 0 && <div className="db d-exp"><div className="d-h">Experience</div>
        {jobs.map((j, i) => (
          <div key={i}>
            <div className="d-job">{[j.job_title, j.company].filter(Boolean).join(', ')}<span>{[j.start_date, j.is_current ? 'Present' : j.end_date].filter(Boolean).join(' to ')}</span></div>
            {(j.responsibilities || []).filter(Boolean).slice(0, 3).map((r, k) => <div className="d-li" key={k}>{r}</div>)}
            {i < jobs.length - 1 && <div className="d-gap" />}
          </div>
        ))}</div>}
      {(c.education || []).length > 0 && <div className="db d-edu"><div className="d-h">Education</div><div className="d-p">
        {c.education.map((e, i) => <span key={i}><b>{[e.degree, e.field].filter(Boolean).join(', ')}</b>{e.institution ? `, ${e.institution}` : ''}{i < c.education.length - 1 && <br />}</span>)}</div></div>}
      {asList(c.skills).length > 0 && <div className="db d-skl"><div className="d-h">Skills</div><div className="d-p">{asList(c.skills).join(', ')}</div></div>}
      {asList(c.languages).length > 0 && <div className="db d-lng"><div className="d-h">Languages</div><div className="d-p">{asList(c.languages).join(', ')}</div></div>}
      {asList(c.certifications).length > 0 && <div className="db d-crt"><div className="d-h">Certifications</div><div className="d-p">{asList(c.certifications).join(', ')}</div></div>}
      <div className="hl" />
    </div>
  );
}

export default function ReviewPage() {
  const { user } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const rootRef = useRef(null);
  const [c, setC] = useState(() => location.state?.candidate || null);
  const [loading, setLoading] = useState(!location.state?.candidate);
  const [links, setLinks] = useState(() => ({
    linkedin: user?.user_metadata?.linkedin || '', github: user?.user_metadata?.github || '', portfolio: user?.user_metadata?.portfolio || '',
  }));
  const [save, setSave] = useState('idle');
  const [error, setError] = useState('');
  const wide = useMemo(() => typeof window !== 'undefined' && window.matchMedia('(min-width: 901px)').matches, []);

  // Coming back later (from Profile → Edit): load the saved CV
  useEffect(() => {
    if (c || !user) return;
    supabaseDB.getCandidateProfile(user.id, user.email).then((row) => { setC(row); setLoading(false); });
  }, [c, user]);

  if (loading && !c) return <div className="jm-review" style={{ minHeight: '100vh' }} />;
  if (!c) return <Navigate to="/upload" replace />;

  const set = (k, v) => setC((p) => ({ ...p, [k]: v }));
  const jobs = c.experience?.length ? c.experience : [];
  const edu = c.education || [];
  const setJob = (i, patch) => set('experience', jobs.map((j, k) => (k === i ? { ...j, ...patch } : j)));
  const setEdu = (i, patch) => set('education', edu.map((e, k) => (k === i ? { ...e, ...patch } : e)));
  const years = Math.round(Number(c.years_experience) || 0);
  const level = ['junior', 'mid', 'senior', 'lead'].includes(c.seniority_level) ? c.seniority_level : '';

  // What still needs a look
  const needPhone = !String(c.phone || '').trim();
  const needLevel = !level;
  const needEnds = jobs.filter(jobMissingEnd).length;
  const todo = Number(needPhone) + Number(needLevel) + needEnds;

  const skills = asList(c.skills), langs = asList(c.languages), certs = asList(c.certifications);
  const fileName = c.source_file || 'Your CV';

  const goTo = (e, id) => {
    const t = rootRef.current?.querySelector(id); if (!t) return;
    e.preventDefault(); if (t.tagName === 'DETAILS') t.open = true;
    t.scrollIntoView({ behavior: 'smooth', block: 'start' });
    const f = t.querySelector('input, textarea'); setTimeout(() => f && f.focus({ preventScroll: true }), 450);
  };
  const nextCheck = () => {
    const f = rootRef.current?.querySelector('.fl.req.miss, .fl.lv.miss');
    if (!f) return;
    const d = f.closest('details.rs'); if (d) d.open = true;
    const j = f.closest('details.jc'); if (j) j.open = true;
    f.scrollIntoView({ behavior: 'smooth', block: 'center' });
    const i = f.querySelector('.in, input'); setTimeout(() => i && i.focus({ preventScroll: true }), 450);
  };

  const onSave = async () => {
    if (save !== 'idle' || !user) return;
    setSave('wait'); setError('');
    try {
      const clean = {
        ...c,
        experience: jobs.map((j) => ({ ...j, end_date: j.is_current ? null : j.end_date, responsibilities: (j.responsibilities || []).map((r) => r.trim()).filter(Boolean) })),
        education: edu.filter((e) => e.degree || e.institution),
      };
      await supabaseDB.saveProfile(clean, user.id);
      await supabase.auth.updateUser({ data: { full_name: c.full_name, linkedin: links.linkedin.trim(), github: links.github.trim(), portfolio: links.portfolio.trim() } });
      try { await edgeFunctions.invokeEmbedCv(); } catch (err) { console.warn('Embedding will be retried by the pipeline', err); }
      setSave('ok');
      setTimeout(() => navigate('/dashboard'), 1000);
    } catch (err) {
      setSave('idle');
      setError(`Your details were not saved: ${err.message || 'the database did not respond'}. Check your connection and save again.`);
    }
  };

  const Counter = ({ cls }) => (
    <button className={`${cls} nextcheck${todo === 0 ? ' allset' : ''}`} type="button" onClick={nextCheck}>
      <span className="todo-n" aria-hidden="true" data-n={todo} /><span className="sw"><span className="sa">to check</span><span className="sb">All set</span></span>
    </button>
  );
  const SaveBtn = ({ label }) => (
    <button className="go save-go" type="button" data-state={save} onClick={onSave}>
      <span className="s-go">{label}<Arrow /></span><span className="s-wait"><i className="spin" />Saving…</span><span className="s-ok"><Ok />Saved</span>
    </button>
  );
  const railItem = (key, href, label, t, need, count) => (
    <a className={`rl-${key}${need ? ' need' : ''}`} href={href} style={{ '--t': String(t) }} onClick={(e) => goTo(e, href)}><span className="st"><Tick /></span>{label}<span className="c">{count ?? ''}</span></a>
  );

  return (
    <div className="jm-review" ref={rootRef}><div role="main" className="page">
      <div className={`auth rv2${todo === 0 ? ' alldone' : ''}`} id="auth">
        <div className="rbar">
          <Link className="logo" to="/"><img src="/jm/nabta-mark.svg" alt="" width="40" height="40" /><span className="display">JobMatcher</span></Link>
          <ol className="steps" aria-label="Getting started">
            <li className="st ok"><b>✓</b>Account</li><li className="bar ok" aria-hidden="true" /><li className="st on" aria-current="step"><b>2</b>Your CV</li><li className="bar" aria-hidden="true" /><li className="st"><b>3</b>Matches</li>
          </ol>
          <Counter cls="cnt" />
          <SaveBtn label="Save and find my jobs" />
        </div>
        <div className="rmain">
          <section className="src" aria-label="Your file">
            <div className="aura a1" aria-hidden="true" /><div className="aura a2" aria-hidden="true" />
            <div className="src-h"><span><b>Your file</b><small>{fileName}</small></span><Link to="/upload">Replace file</Link></div>
            <div className="doc-wrap"><Doc c={c} links={links} /></div>
          </section>
          <section className="data" aria-label="What JobMatcher read">
            <nav className="rail" aria-label="Sections"><p className="rl">Sections</p>
              {railItem('profile', '#s-profile', 'Profile', 0, needLevel)}
              {railItem('contact', '#s-contact', 'Contact and links', 1, needPhone)}
              {railItem('exp', '#s-exp', 'Experience', 2, needEnds > 0, jobs.length)}
              {railItem('edu', '#s-edu', 'Education', 3, false, edu.length)}
              {railItem('skills', '#s-skills', 'Skills', 4, false, skills.length)}
              {railItem('lang', '#s-lang', 'Languages', 5, false, langs.length)}
              {railItem('cert', '#s-cert', 'Certifications', 6, false, certs.length)}
              <p className="tip"><b>Point at a section</b> to see where it came from in your file.</p>
            </nav>
            <div className="scroll" id="scroll">
              <div className="stamp" aria-hidden="true">Ready<br />for<br />matches</div>
              <div className="dhead">
                <h1 className="display"><span className="wd" style={{ '--w': '0' }}>Check</span> <span className="wd" style={{ '--w': '1' }}>your</span> <span className="wd" style={{ '--w': '2' }}>details.</span></h1>
                <p>This is everything JobMatcher read from your CV. Compare it with your file, fix anything that is off, then save. Your matches are built from this.</p>
                {error && <p className="note jm-msg bad" role="alert">{error}</p>}
              </div>
              <details className="mfile"><summary><FileIc /><span>Compare with your file<small>{fileName}</small></span><Chev cls="chev" /></summary><div className="mdoc"><Doc c={c} links={links} /></div></details>
              <nav className="jump" aria-label="Sections">
                {[['profile', 'Profile', needLevel], ['contact', 'Contact and links', needPhone], ['exp', 'Experience', needEnds > 0], ['edu', 'Education'], ['skills', 'Skills'], ['lang', 'Languages'], ['cert', 'Certifications']].map(([k, l, n]) => (
                  <a key={k} className={`j-${k}${n ? ' need' : ''}`} href={`#s-${k}`} onClick={(e) => goTo(e, `#s-${k}`)}>{l}</a>
                ))}
              </nav>

              <details className="rs" id="s-profile" style={{ '--t': '1' }} open><summary className="rs-h"><h2>Profile</h2><span className="pv" /><Chev /></summary><div className="rs-b">
                <div className="g2">
                  <div className="fl full"><label htmlFor="fn">Full name</label><input className="in big" id="fn" value={c.full_name || ''} onChange={(e) => set('full_name', e.target.value)} /></div>
                  <div className="fl"><label htmlFor="loc">Location</label><input className="in" id="loc" value={c.location || ''} onChange={(e) => set('location', e.target.value)} /></div>
                  <div className="fl"><span className="lb">Years of experience</span><div className="stepper">
                    <button type="button" aria-label="One year less" onClick={() => set('years_experience', Math.max(0, years - 1))}>−</button>
                    <output id="yrs" aria-live="polite">{years} {years === 1 ? 'year' : 'years'}</output>
                    <button type="button" aria-label="One year more" onClick={() => set('years_experience', Math.min(40, years + 1))}>+</button></div></div>
                  <div className={`fl full lv${needLevel ? ' miss' : ''}`} id="lvl"><span className="lb"><span>Level</span><span className="need-tag">Check</span></span>
                    <div className="seg4" role="radiogroup" aria-label="Level">
                      {LEVELS.map(([v, l]) => <label key={v} className={c.seniority_level === v ? 'sug' : ''}><input type="radio" name="lvl" value={v} checked={level === v} onChange={() => set('seniority_level', v)} />{l}</label>)}
                    </div>
                    <p className="help">Pick the level you want to be matched at.</p></div>
                  <div className="fl full"><label htmlFor="sum">Summary</label><textarea className="in" id="sum" rows="3" value={c.professional_summary || ''} onChange={(e) => set('professional_summary', e.target.value)} /></div>
                </div>
              </div></details>

              <details className="rs" id="s-contact" style={{ '--t': '2' }} open><summary className="rs-h"><h2>Contact and links</h2><span className="pv" /><Chev /></summary><div className="rs-b">
                <div className="g2">
                  <div className="fl"><label htmlFor="em">Email</label><input className="in" id="em" type="email" value={c.email || user?.email || ''} onChange={(e) => set('email', e.target.value)} /></div>
                  <div className={`fl req${needPhone ? ' miss' : ''}`} id="f-phone"><label htmlFor="phone"><span>Phone</span><span className="need-tag">Check</span></label><input className="in" id="phone" type="tel" placeholder="+212 6 00 00 00 00" value={c.phone || ''} onChange={(e) => set('phone', e.target.value)} />{needPhone && <p className="help">Not found in your CV. Recruiters use it to reach you.</p>}</div>
                  <div className="fl"><label htmlFor="li">LinkedIn</label><div className="pre"><span>linkedin.com/in/</span><input className="in" id="li" value={links.linkedin} onChange={(e) => setLinks({ ...links, linkedin: e.target.value })} /></div></div>
                  <div className="fl"><label htmlFor="gh">GitHub <span className="opt">optional</span></label><div className="pre"><span>github.com/</span><input className="in" id="gh" placeholder="username" value={links.github} onChange={(e) => setLinks({ ...links, github: e.target.value })} /></div></div>
                  <div className="fl full"><label htmlFor="pf">Portfolio or website <span className="opt">optional</span></label><input className="in" id="pf" type="url" placeholder="https://" value={links.portfolio} onChange={(e) => setLinks({ ...links, portfolio: e.target.value })} /></div>
                </div>
              </div></details>

              <details className="rs" id="s-exp" style={{ '--t': '3' }} open={wide}><summary className="rs-h"><h2>Experience</h2><span className="c">{jobs.length} {jobs.length === 1 ? 'job' : 'jobs'}</span><span className="pv" /><Chev /></summary><div className="rs-b">
                {jobs.map((j, i) => (
                  <details className="jc" key={i} open={wide || jobMissingEnd(j)}><summary className="jsum"><b>{j.job_title || 'New job'}</b><span>{[j.company, [j.start_date, j.is_current ? 'Present' : j.end_date || '…'].filter(Boolean).join(' to ')].filter(Boolean).join(' · ')}</span><Chev /></summary><div className="jc-b">
                    <button className="rm" type="button" aria-label="Remove this job" onClick={() => set('experience', jobs.filter((_, k) => k !== i))}>×</button>
                    <div className="g4">
                      <div className="fl"><label htmlFor={`jt${i}`}>Job title</label><input className="in" id={`jt${i}`} value={j.job_title || ''} onChange={(e) => setJob(i, { job_title: e.target.value })} /></div>
                      <div className="fl"><label htmlFor={`jco${i}`}>Company</label><input className="in" id={`jco${i}`} value={j.company || ''} onChange={(e) => setJob(i, { company: e.target.value })} /></div>
                      <div className="dd">
                        <div className="fl"><label htmlFor={`js${i}`}>Start</label><input className="in" id={`js${i}`} placeholder="Month year" value={j.start_date || ''} onChange={(e) => setJob(i, { start_date: e.target.value })} /></div>
                        <div className={`fl${jobMissingEnd(j) ? ' req miss' : ''}`}><label htmlFor={`end${i}`}><span>End</span><span className="need-tag">Check</span></label>
                          <input className="in" id={`end${i}`} aria-label="End date" placeholder="Month year" disabled={j.is_current} value={j.is_current ? 'Present' : (j.end_date || '')} onChange={(e) => setJob(i, { end_date: e.target.value })} /></div>
                      </div>
                    </div>
                    {jobMissingEnd(j) && <p className="help" style={{ marginTop: '-6px' }}>The end date is missing from your CV.</p>}
                    <label className="now"><input type="checkbox" className="nowbox" checked={!!j.is_current} onChange={(e) => setJob(i, { is_current: e.target.checked })} />I still work here</label>
                    <div className="fl"><span className="lb">What you did</span>
                      <ul className="duties">{(j.responsibilities?.length ? j.responsibilities : ['']).map((r, k) => (
                        <li key={k}><textarea className="in" rows="1" aria-label="Duty" placeholder="What you did" value={r} onChange={(e) => setJob(i, { responsibilities: (j.responsibilities?.length ? j.responsibilities : ['']).map((x, m) => (m === k ? e.target.value : x)) })} /></li>
                      ))}</ul>
                      <button className="lnk addduty" type="button" onClick={() => setJob(i, { responsibilities: [...(j.responsibilities || []), ''] })}>Add a line</button></div>
                  </div></details>
                ))}
                <div className="addrow"><button className="add" type="button" id="addjob" onClick={() => set('experience', [...jobs, blankJob()])}><Plus />Add a job</button></div>
              </div></details>

              <details className="rs" id="s-edu" style={{ '--t': '4' }} open={wide}><summary className="rs-h"><h2>Education</h2><span className="c">{edu.length}</span><span className="pv">{edu.map((e) => e.degree).filter(Boolean).join(' · ')}</span><Chev /></summary><div className="rs-b">
                {edu.map((e, i) => (
                  <div className="edu2" key={i}>
                    <div className="fl"><label htmlFor={`dg${i}`}>Degree</label><input className="in" id={`dg${i}`} value={[e.degree, e.field].filter(Boolean).join(', ')} onChange={(ev) => setEdu(i, { degree: ev.target.value, field: '' })} /></div>
                    <div className="fl"><label htmlFor={`sc${i}`}>School</label><input className="in" id={`sc${i}`} value={e.institution || ''} onChange={(ev) => setEdu(i, { institution: ev.target.value })} /></div>
                    <button className="rm" type="button" aria-label="Remove this degree" onClick={() => set('education', edu.filter((_, k) => k !== i))}>×</button>
                  </div>
                ))}
                <div className="addrow"><button className="add" type="button" id="addedu" onClick={() => set('education', [...edu, blankEdu()])}><Plus />Add</button></div>
              </div></details>

              <details className="rs" id="s-skills" style={{ '--t': '5' }} open={wide}><summary className="rs-h"><h2>Skills</h2><span className="c">{skills.length}</span><span className="pv">{skills.slice(0, 3).join(', ')}{skills.length > 3 ? ` +${skills.length - 3}` : ''}</span><Chev /></summary><div className="rs-b">
                <Chips items={skills} onChange={(v) => set('skills', v)} label="Add a skill" />
              </div></details>
              <details className="rs" id="s-lang" style={{ '--t': '6' }} open={wide}><summary className="rs-h"><h2>Languages</h2><span className="c">{langs.length}</span><span className="pv">{langs.join(', ')}</span><Chev /></summary><div className="rs-b">
                <Chips items={langs} onChange={(v) => set('languages', v)} label="Add a language" />
              </div></details>
              <details className="rs" id="s-cert" style={{ '--t': '7' }} open={wide}><summary className="rs-h"><h2>Certifications</h2><span className="c">{certs.length}</span><span className="pv">{certs.join(', ')}</span><Chev /></summary><div className="rs-b">
                <Chips items={certs} onChange={(v) => set('certifications', v)} label="Add a certification" />
              </div></details>
            </div>
          </section>
        </div>
        <div className="mbar"><Counter cls="mleft" /><SaveBtn label="Find my jobs" /></div>
      </div>
    </div></div>
  );
}
