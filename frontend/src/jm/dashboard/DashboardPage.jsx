import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { supabase } from '../../lib/supabaseClient';
import { IcHome, IcSaved, IcApplied, IcUpload, IcChev, IcSearch, IcFilter, IcTick, IcArrow, IcBook, EmptyCup, IcPrev, IcNext, IcClose, IcExtLg } from './icons';
import { ago, initials, loadCandidate, loadJob, loadMatches, loadSaved, logoClass, setSaved } from './data';
import TrackerView from './TrackerView';
import '../shared/jm-base.css';
import './Dash.css';

/* Dashboard: Matches, Saved and the Applied tracker, from design/previews/dashboard.html. */

export const Cup = ({ p = 0, w = 22, cls = 'cup' }) => {
  const h = Math.round(37 * Math.max(0, Math.min(100, p))) / 100;
  return (
    <svg className={cls} viewBox="0 0 48 56" width={w} height={Math.round((w * 56) / 48)} aria-hidden="true">
      <rect className="lvl" x="16" y={50 - h} width="16" height={h} rx="1.5" fill="#FF7F45" />
      <rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" strokeWidth="2.8" />
      <path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" strokeWidth="2.8" strokeLinejoin="round" />
    </svg>
  );
};

const FILTERS = [
  ['type', 'Type', ['Any', 'Full-time', 'Internship', 'Contract']],
  ['level', 'Level', ['Any', 'Intern', 'Junior', 'Mid', 'Senior']],
  ['city', 'City', ['Any', 'Casablanca', 'Rabat', 'Tanger', 'Marrakech']],
  ['source', 'Source', ['Any', 'ANAPEC', 'Jobzyn', 'LinkedIn']],
];
const NONE = { type: 'Any', level: 'Any', city: 'Any', source: 'Any' };
const PAGE = 10;

function Row({ job, saved, onOpen, onSave, k, savedRow }) {
  const n = job.hits?.length || 0;
  return (
    <article className={`row${savedRow ? ' srow' : ''}`} style={{ '--k': String(k) }}>
      <a className="stretch" href={`#job-${job.id}`} aria-label={`${job.title} at ${job.company}${job.score != null ? `, ${job.score}% match` : ''}`} onClick={(e) => { e.preventDefault(); onOpen(job); }} />
      <span className={`logo-c ${logoClass(job.company)}`} aria-hidden="true">{initials(job.company)}</span>
      <span className="r-t"><b>{job.title}<span className="ar" aria-hidden="true">→</span></b><span>{[job.company, job.city, job.source].filter(Boolean).join(' · ')}</span></span>
      {!savedRow && <span className="r-sk"><span className={`k${n >= 3 ? ' full' : ''}`}>{n}</span><span className="names">{n ? job.hits.slice(0, 3).join(', ') : 'No skill named'}</span></span>}
      <span className={`r-d${!savedRow && /Today|1 day/.test(ago(job.posted)) ? ' new' : ''}`}>{savedRow ? `Saved ${ago(job.savedAt).toLowerCase()}` : ago(job.posted)}</span>
      <span className="r-sc">{job.score != null ? <><Cup p={job.score} /><b>{job.score}<small>%</small></b></> : null}</span>
      {savedRow && <Link className="mini-go" to={`/apply/${job.id}`} state={{ score: job.score }}>Prepare</Link>}
      <button className="save" type="button" aria-pressed={saved} aria-label={`${saved ? 'Remove' : 'Save'} ${job.title}${savedRow ? ' from saved' : ` at ${job.company}`}`} onClick={() => onSave(job)}><IcBook /></button>
    </article>
  );
}

function Drawer({ job, list, saved, onClose, onSave, onNav, dref }) {
  const i = job ? list.findIndex((j) => j.id === job.id) : -1;
  const paras = String(job?.description || '').split(/\n{2,}|\r\n\r\n/).map((p) => p.trim()).filter(Boolean).slice(0, 12);
  return (
    <dialog className="dw" ref={dref} aria-labelledby="dw-t" onClose={onClose} onClick={(e) => { if (e.target === e.currentTarget) e.currentTarget.close(); }}>
      {job && <div className="dw-in">
        <header className="dw-top">
          <button className="dw-ib" type="button" aria-label="Previous offer" disabled={i <= 0} onClick={() => onNav(-1)}><IcPrev /></button>
          <button className="dw-ib" type="button" aria-label="Next offer" disabled={i < 0 || i >= list.length - 1} onClick={() => onNav(1)}><IcNext /></button>
          <span className="dw-pos">{i >= 0 ? `${i + 1} of ${list.length}` : ''}</span>
          <button className="dw-ib dw-x" type="button" aria-label="Close" onClick={() => dref.current?.close()}><IcClose /></button>
        </header>
        <div className="dw-body" key={job.id}>
          <div className="dw-hero" style={{ '--i': '0' }}><span className={`logo-c ${logoClass(job.company)}`} aria-hidden="true">{initials(job.company)}</span><span><b>{job.company}</b><span>{[job.city, job.posted && `posted ${ago(job.posted).toLowerCase()}`].filter(Boolean).join(' · ')}</span></span></div>
          <h2 className="dw-t" id="dw-t" style={{ '--i': '1' }}>{job.title}</h2>
          <div className="dw-tags" style={{ '--i': '2' }}>{[job.type, job.level, job.city].filter(Boolean).map((t) => <span className="t" key={t}>{t}</span>)}{job.source && <span className="src-b">{job.source}</span>}</div>
          {job.score != null && <section className="dw-match" style={{ '--i': '3' }}><div className="cupbig sm" role="img" aria-label={`${job.score}% match`}><Cup p={job.score} w={52} cls="cup big" /><span className="v"><b>{job.score}<small>%</small></b><span>match</span></span></div>
            <div className="facts">{job.hits.length > 0 && <span className="fact"><i className="ok"><IcTick /></i>{job.hits.length} of your skills</span>}{job.level && <span className="fact"><i className="ok"><IcTick /></i>{job.level}</span>}{job.city && <span className="fact"><i className="ok"><IcTick /></i>{job.city}</span>}</div></section>}
          {job.hits.length > 0 && <section className="dw-s" style={{ '--i': '4' }}><h3>Your skills it mentions</h3><div className="dw-sk">{job.hits.map((s) => <span className="t hit" key={s}>{s}</span>)}</div></section>}
          <section className="dw-s" style={{ '--i': '5' }}><h3>About the role</h3>{paras.length ? paras.map((p, k) => <p key={k}>{p}</p>) : <p>The full description is on the original post.</p>}</section>
          <section className="dw-grid" style={{ '--i': '6' }}>
            {job.salary ? <div><span>Salary</span><b>{Number(job.salary).toLocaleString('fr-MA')} MAD</b></div> : null}
            <div><span>Contract</span><b>{job.type}</b></div>{job.level && <div><span>Level</span><b>{job.level}</b></div>}{job.source && <div><span>Source</span><b>{job.source}</b></div>}
          </section>
        </div>
        <footer className="dw-foot">
          <Link className="go" to={`/apply/${job.id}`} state={{ score: job.score }}><span className="s-go">Prepare application<IcArrow /></span></Link>
          <button className="dw-save" type="button" aria-pressed={saved} aria-label={saved ? 'Remove from saved' : 'Save this offer'} onClick={() => onSave(job)}><IcBook /></button>
          {job.url && <a className="dw-ext" href={job.url} target="_blank" rel="noopener noreferrer"><IcExtLg /><span>Original post</span></a>}
        </footer>
      </div>}
    </dialog>
  );
}

export default function DashboardPage({ view = 'matches' }) {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [cand, setCand] = useState(undefined);
  const [jobs, setJobs] = useState(null);
  const [saved, setSavedList] = useState([]);
  const [q, setQ] = useState('');
  const [f, setF] = useState(NONE);
  const [draftF, setDraftF] = useState(NONE);
  const [shown, setShown] = useState(PAGE);
  const [open, setOpen] = useState(null);
  const [toast, setToast] = useState(null);
  const [appliedCount, setAppliedCount] = useState(0);
  const dref = useRef(null);
  const ttRef = useRef(null);
  const name = cand?.full_name || user?.user_metadata?.full_name || user?.email || '';

  const say = useCallback((text, action) => {
    clearTimeout(ttRef.current); setToast({ text, action, k: Date.now() });
    ttRef.current = setTimeout(() => setToast(null), 5000);
  }, []);

  useEffect(() => {
    if (!user) return;
    (async () => {
      const c = await loadCandidate(user.id);
      setCand(c);
      const [m, s] = await Promise.all([c ? loadMatches(user.id, c).catch(() => []) : [], loadSaved(user.id)]);
      setJobs(m); setSavedList(s);
    })();
    // Applied count for the sidebar, before the tracker is opened
    supabase.from('job_applications').select('id', { count: 'exact', head: true }).eq('user_id', user.id).not('date_applied', 'is', null)
      .then(({ count }) => { if (typeof count === 'number') setAppliedCount(count); });
  }, [user]);

  const savedIds = useMemo(() => new Set(saved.map((s) => s.id)), [saved]);
  const toggleSave = async (job, want) => {
    const was = want === undefined ? savedIds.has(job.id) : !want;
    setSavedList((l) => (was ? l.filter((s) => s.id !== job.id) : [{ ...job, savedAt: new Date().toISOString() }, ...l]));
    try {
      await setSaved(user.id, job, !was);
      say(was ? 'Removed from saved' : 'Saved', was ? { label: 'Undo', run: () => toggleSave(job, true) } : { label: 'See saved', run: () => navigate('/saved') });
    } catch {
      setSavedList((l) => (was ? [job, ...l] : l.filter((s) => s.id !== job.id)));
      say('That did not save. Check your connection and try again.');
    }
  };

  const filtered = useMemo(() => {
    const t = q.trim().toLowerCase();
    return (jobs || []).filter((j) => (f.type === 'Any' || j.type === f.type) && (f.level === 'Any' || j.level === f.level)
      && (f.city === 'Any' || (j.location || '').toLowerCase().includes(f.city.toLowerCase())) && (f.source === 'Any' || j.source === f.source)
      && (!t || `${j.title} ${j.company} ${j.city} ${j.hits.join(' ')}`.toLowerCase().includes(t)));
  }, [jobs, q, f]);
  const countFor = (ff) => (jobs || []).filter((j) => (ff.type === 'Any' || j.type === ff.type) && (ff.level === 'Any' || j.level === ff.level)
    && (ff.city === 'Any' || (j.location || '').toLowerCase().includes(ff.city.toLowerCase())) && (ff.source === 'Any' || j.source === ff.source)).length;
  const activeF = Object.entries(f).filter(([, v]) => v !== 'Any');
  const best = filtered[0];
  const rest = filtered.slice(1);

  const openJob = async (job) => {
    setOpen(job);
    if (!dref.current?.open) dref.current?.showModal();
    if (job.score == null && !job.description) { const full = await loadJob(job.id, cand); if (full) setOpen({ ...full, savedAt: job.savedAt }); }
  };
  const drawerList = view === 'saved' ? saved : filtered;
  const navDrawer = (d) => { const i = drawerList.findIndex((j) => j.id === open?.id); const n = drawerList[i + d]; if (n) openJob(n); };

  const nav = [['matches', '/dashboard', IcHome, 'Matches', jobs?.length ?? ''], ['saved', '/saved', IcSaved, 'Saved', saved.length], ['applied', '/applied', IcApplied, 'Applied', appliedCount]];

  return (
    <div className="jm-dash"><div className="page">
      <div className="app" id="app" data-view={view}>
        <aside className="side" aria-label="Main">
          <Link className="logo" to="/dashboard"><img src="/jm/nabta-mark.svg" alt="" width="40" height="40" /><span className="display">JobMatcher</span></Link>
          {nav.map(([v, to, Ic, label, n]) => (
            <Link key={v} className={`nav-i${view === v ? ' on' : ''}`} to={to} aria-current={view === v ? 'page' : undefined}><Ic /><span>{label}</span><span className="b">{n}</span></Link>
          ))}
          <span className="sp" />
          <Link className="newcv" to="/upload"><IcUpload /><span>Upload a new CV</span></Link>
          <Link className="me" to="/profile" aria-label="Your profile"><span className="s-av done" aria-hidden="true">{initials(name)}</span><div><b>{name}</b><small>View profile</small></div><IcChev /></Link>
        </aside>
        <main className="main">
          <div className="mtop"><Link className="logo" to="/dashboard"><img src="/jm/nabta-mark.svg" alt="" width="36" height="36" /><span className="display">JobMatcher</span></Link><Link className="avl" to="/profile" aria-label="Your profile"><span className="s-av done">{initials(name)}</span></Link></div>

          {view === 'matches' && <section className="view v-matches" aria-label="Your matches">
            <div className="mhead" style={{ '--d': '0' }}><h1 className="display">Your matches</h1><span className="count"><b>{jobs ? filtered.length : '…'}</b>offers</span></div>
            {cand === null ? (
              <div className="sempty"><EmptyCup /><b>Add your CV to see your matches</b><span>JobMatcher ranks every offer against it.</span><Link className="go" to="/upload"><span className="s-go">Add your CV<IcArrow /></span></Link></div>
            ) : <>
              <div className="sbar" style={{ '--d': '1' }}><IcSearch /><input type="search" placeholder="Search a role, company or skill" aria-label="Search your matches" value={q} onChange={(e) => { setQ(e.target.value); setShown(PAGE); }} />
                <button className="fbtn" type="button" popoverTarget="fp" aria-label="Filters" onClick={() => setDraftF(f)}><IcFilter /><span className="lbl">Filters</span>{activeF.length > 0 && <span className="n">{activeF.length}</span>}</button></div>
              {activeF.length > 0 && <div className="act">{activeF.map(([k, v]) => <button key={k} className="achip" type="button" onClick={() => setF({ ...f, [k]: 'Any' })}>{v}<i>×</i></button>)}<button className="reset" type="button" onClick={() => setF(NONE)}>Clear all</button></div>}
              <div className="fp" popover="auto" id="fp" aria-label="Filters">
                <div className="fp-h"><b>Filters</b><button className="fp-x" type="button" popoverTarget="fp" popoverTargetAction="hide" aria-label="Close filters">×</button></div>
                {FILTERS.map(([k, label, opts]) => (
                  <div className="fgp" key={k}><span>{label}</span><div className="seg">{opts.map((o) => <button key={o} className="opt2" type="button" aria-pressed={draftF[k] === o} onClick={() => setDraftF({ ...draftF, [k]: o })}>{o}</button>)}</div></div>
                ))}
                <div className="fp-f"><button className="lnk" type="button" onClick={() => setDraftF(NONE)}>Reset</button><button className="go" type="button" popoverTarget="fp" popoverTargetAction="hide" onClick={() => { setF(draftF); setShown(PAGE); }}><span className="s-go">Show {countFor(draftF)} offers</span></button></div>
              </div>
              {jobs === null && <p className="note">Ranking the offers against your CV…</p>}
              {best && <article className="best">
                <div className="cupbig" role="img" aria-label={`${best.score}% match`}><Cup p={best.score} w={70} cls="cup big" /><span className="v"><b>{best.score}<small>%</small></b><span>match</span></span></div>
                <div className="b-m">
                  <span className="kick" style={{ '--d': '0' }}><i className="live" />Best match today</span>
                  <h2 style={{ '--d': '1' }}><a className="blink" href={`#job-${best.id}`} onClick={(e) => { e.preventDefault(); openJob(best); }}>{best.title}</a></h2>
                  <span className="co" style={{ '--d': '2' }}>{[best.company, best.city].filter(Boolean).join(' · ')}</span>
                  <div className="facts" style={{ '--d': '3' }}>{best.hits.length > 0 && <span className="fact"><i className="ok"><IcTick /></i>{best.hits.length} of your skills</span>}{best.level && <span className="fact"><i className="ok"><IcTick /></i>{best.level}</span>}{best.city && <span className="fact"><i className="ok"><IcTick /></i>{best.city}</span>}</div>
                </div>
                <div className="b-r" style={{ '--d': '4' }}><Link className="go" to={`/apply/${best.id}`} state={{ score: best.score }}><span className="s-go">Prepare application<IcArrow /></span></Link>
                  <div className="sub"><button className="ghost2 bsave" type="button" aria-pressed={savedIds.has(best.id)} aria-label={`Save ${best.title} at ${best.company}`} onClick={() => toggleSave(best)}><IcBook />{savedIds.has(best.id) ? 'Saved' : 'Save'}</button><a className="ghost2" href={`#job-${best.id}`} onClick={(e) => { e.preventDefault(); openJob(best); }}>View offer</a></div></div>
              </article>}
              {rest.length > 0 && <div className="lh"><h3>Next best matches</h3><span>Sorted by match</span></div>}
              <div className="list">
                {rest.slice(0, shown).map((j, k) => <Row key={j.id} job={j} k={k % PAGE} saved={savedIds.has(j.id)} onOpen={openJob} onSave={(j) => toggleSave(j)} />)}
                {jobs && filtered.length === 0 && <div className="empty" style={{ display: 'flex' }}><b>Nothing here</b><span>No offers match these filters.</span><button type="button" onClick={() => { setF(NONE); setQ(''); }}>Clear filters</button></div>}
              </div>
              {rest.length > shown && <button className="more" type="button" onClick={() => setShown((s) => s + PAGE)}>Show more</button>}
            </>}
          </section>}

          {view === 'saved' && <section className="view v-saved" aria-labelledby="h-saved">
            <div className="mhead"><h1 className="display" id="h-saved">Saved</h1><span className="count"><b>{saved.length}</b>offers</span></div>
            {saved.length > 0 ? (
              <div className="list">{saved.map((j, k) => <Row key={j.id} savedRow job={{ ...j, ...(jobs || []).find((m) => m.id === j.id), savedAt: j.savedAt }} k={k} saved onOpen={openJob} onSave={(j) => toggleSave(j)} />)}</div>
            ) : (
              <div className="sempty"><EmptyCup /><b>Nothing saved yet</b><span>Tap the bookmark on any offer to keep it here.</span><Link className="go" to="/dashboard"><span className="s-go">See your matches<IcArrow /></span></Link></div>
            )}
          </section>}

          {view === 'applied' && <TrackerView user={user} say={say} onCount={setAppliedCount} />}
        </main>
        {toast && <div className="toast in" role="status" key={toast.k}>{toast.text}{toast.action && <button type="button" className="undo" onClick={() => { setToast(null); toast.action.run(); }}>{toast.action.label}</button>}</div>}
        <Drawer job={open} list={drawerList} saved={open ? savedIds.has(open.id) : false} onClose={() => setOpen(null)} onSave={(j) => toggleSave(j)} onNav={navDrawer} dref={dref} />
        <nav className="tabs" aria-label="Main">{nav.map(([v, to, Ic, label]) => <Link key={v} className={view === v ? 'on' : ''} to={to}><Ic />{label}</Link>)}</nav>
      </div>
    </div></div>
  );
}
