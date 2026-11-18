import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { supabase } from '../../lib/supabaseClient';
import { edgeFunctions } from '../../services/edgeFunctions';
import { authMessage } from '../../lib/authErrors';
import { IcHome, IcSaved, IcApplied, IcUpload, IcChev } from '../dashboard/icons';
import { IcCam, IcPin, IcDl, IcLock, IcOut } from './icons';
import { initials, loadCandidate, loadMatches } from '../dashboard/data';
import { addPref, cvFileUrl, loadProfile, loadSuggestions, removePref, saveCandidate, saveProfileRow, uploadAvatar } from './data';
import '../shared/jm-base.css';
import './Profile.css';

/* Profile (design/previews/profile.html): hero with the completeness cup, then Profile, Preferences and Account
   on a swipeable track. */

const Cup = ({ p = 0, w = 30 }) => {
  const h = Math.round(37 * Math.max(0, Math.min(100, p))) / 100;
  return (
    <svg className="cup" viewBox="0 0 48 56" width={w} height={Math.round((w * 56) / 48)} aria-hidden="true">
      <rect className="lvl" x="16" y={50 - h} width="16" height={h} rx="1.5" fill="#FF7F45" style={{ transition: 'all .6s cubic-bezier(.16,1,.3,1)' }} />
      <rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" strokeWidth="2.8" />
      <path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" strokeWidth="2.8" strokeLinejoin="round" />
    </svg>
  );
};
const names = (xs) => (Array.isArray(xs) ? xs : []).map((x) => (typeof x === 'string' ? x : x?.name)).filter(Boolean);
const TABS = [['profile', 'Profile'], ['prefs', 'Preferences'], ['account', 'Account']];

function ChipEditor({ items, onAdd, onRemove, label, suggest, listId, counts }) {
  const [draft, setDraft] = useState('');
  const submit = () => { const v = draft.trim(); if (v) { onAdd(v); setDraft(''); } };
  return (
    <div className="chips">
      {items.map((it) => (
        <span className="chip" key={it.key ?? it.name}>{it.name}{counts?.[it.name.toLowerCase()] != null && <span className="n" title={`${counts[it.name.toLowerCase()]} of your matches ask for ${it.name}`}>{counts[it.name.toLowerCase()]}</span>}
          <button type="button" aria-label={`Remove ${it.name}`} onClick={() => onRemove(it)}>×</button></span>
      ))}
      <span className="addc">+<input aria-label={label} placeholder={label} list={listId} value={draft} onChange={(e) => setDraft(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); submit(); } }} /></span>
      {suggest && <datalist id={listId}>{suggest.map((s) => <option key={s.id} value={s.name} />)}</datalist>}
    </div>
  );
}

export default function ProfilePage() {
  const { user, signOut, updatePassword } = useAuth();
  const navigate = useNavigate();
  const [d, setD] = useState(null);
  const [sug, setSug] = useState({ cities: [], industries: [], roles: [] });
  const [matches, setMatches] = useState(null);
  const [tab, setTab] = useState('profile');
  const [toast, setToast] = useState('');
  const [links, setLinks] = useState(() => ({ linkedin: user?.user_metadata?.linkedin || '', github: user?.user_metadata?.github || '', portfolio: user?.user_metadata?.portfolio || '' }));
  const [editing, setEditing] = useState('');
  const [acc, setAcc] = useState({ name: '', city: '' });
  const [acc0, setAcc0] = useState({ name: '', city: '' });
  const [pwOpen, setPwOpen] = useState(false);
  const [pw, setPw] = useState({ a: '', b: '', msg: '', bad: false });
  const [score, setScore] = useState(60);
  const trackRef = useRef(null);
  const panes = useRef({});
  const indRef = useRef(null);
  const tabRefs = useRef({});
  const photoRef = useRef(null);
  const tt = useRef(null);
  const say = useCallback((t) => { setToast(t); clearTimeout(tt.current); tt.current = setTimeout(() => setToast(''), 2800); }, []);

  useEffect(() => {
    if (!user) return;
    (async () => {
      const data = await loadProfile(user);
      setD(data);
      const name = data.prof?.full_name || data.cand?.full_name || user.user_metadata?.full_name || '';
      setAcc({ name, city: data.cand?.location || '' }); setAcc0({ name, city: data.cand?.location || '' });
      setScore(data.prof?.min_match_score || 60);
      const c = await loadCandidate(user.id);
      if (c) setMatches(await loadMatches(user.id, c).catch(() => []));
    })();
    loadSuggestions().then(setSug).catch(() => {});
  }, [user]);

  /* Sliding tabs: the pill follows the scroll; the track takes the height of the shown pane */
  const fit = useCallback(() => {
    const t = trackRef.current; const p = panes.current[tab];
    if (t && p) t.style.height = `${p.offsetHeight}px`;
  }, [tab]);
  const place = useCallback((x) => {
    const order = TABS.map(([k]) => tabRefs.current[k]); const i = Math.max(0, Math.min(order.length - 1, Math.floor(x))); const f = x - i;
    const a = order[i]; const b = order[Math.min(i + 1, order.length - 1)]; const ind = indRef.current;
    if (!a || !b || !ind) return;
    ind.style.width = `${a.offsetWidth + (b.offsetWidth - a.offsetWidth) * f}px`;
    ind.style.translate = `${a.offsetLeft + (b.offsetLeft - a.offsetLeft) * f}px 0`;
  }, []);
  useLayoutEffect(() => { place(TABS.findIndex(([k]) => k === tab)); fit(); }, [tab, d, place, fit]);
  useEffect(() => {
    const ro = new ResizeObserver(() => fit());
    Object.values(panes.current).forEach((p) => p && ro.observe(p));
    return () => ro.disconnect();
  }, [fit, d]);
  const go = (k) => { const i = TABS.findIndex(([x]) => x === k); const t = trackRef.current; if (t) t.scrollTo({ left: i * t.clientWidth, behavior: 'smooth' }); setTab(k); };
  const onScroll = () => {
    const t = trackRef.current; if (!t) return; const x = t.scrollLeft / t.clientWidth; place(x);
    Object.entries(panes.current).forEach(([k, p]) => { if (!p) return; const i = TABS.findIndex(([x2]) => x2 === k); const dd = Math.min(1, Math.abs(i - x)); p.style.opacity = String(1 - dd * 0.75); });
    const n = TABS[Math.round(x)]?.[0]; if (n && n !== tab) setTab(n);
  };

  const cand = d?.cand;
  const skills = names(cand?.skills);
  const counts = useMemo(() => {
    if (!matches) return null;
    const o = {}; skills.forEach((s) => { o[s.toLowerCase()] = matches.filter((m) => m.hits.some((h) => h.toLowerCase() === s.toLowerCase())).length; }); return o;
  }, [matches, skills]);
  const effect = matches ? matches.filter((m) => m.score >= score).length : null;

  // Completeness: what makes a CV and a profile useful to recruiters
  const checks = [
    ['photo', !!d?.prof?.avatar_url, 'Add a photo'], ['summary', !!cand?.professional_summary, 'Add a summary'], ['phone', !!cand?.phone, 'Add your phone'],
    ['skills', skills.length >= 3, 'Add skills'], ['exp', (cand?.experience || []).length > 0, 'Add experience'], ['edu', (cand?.education || []).length > 0, 'Add education'],
    ['linkedin', !!links.linkedin, 'Add LinkedIn'], ['github', !!links.github, 'Add GitHub'],
  ];
  const pct = Math.round((100 * checks.filter((c) => c[1]).length) / checks.length);
  const next = checks.find((c) => !c[1]);

  const setSkills = async (list) => {
    setD((p) => ({ ...p, cand: { ...p.cand, skills: list } }));
    try { await saveCandidate(user.id, { skills: list }); edgeFunctions.invokeEmbedCv().catch(() => {}); } catch (e) { say(`Not saved: ${e.message}`); }
  };
  const saveLinks = async (next2) => {
    setLinks(next2); setEditing('');
    const { error } = await supabase.auth.updateUser({ data: { linkedin: next2.linkedin.trim(), github: next2.github.trim(), portfolio: next2.portfolio.trim() } });
    say(error ? `Not saved: ${error.message}` : 'Link saved');
  };
  const prefAdd = async (kind, name) => {
    const hit = sug[kind].find((s) => s.name.toLowerCase() === name.toLowerCase());
    if (!hit) { say(`No offers mention “${name}” yet. Pick one from the list.`); return; }
    if (d[kind].some((x) => x.id === hit.id)) return;
    setD((p) => ({ ...p, [kind]: [...p[kind], hit] }));
    try { await addPref(kind, d.prof.id, hit.id); } catch (e) { setD((p) => ({ ...p, [kind]: p[kind].filter((x) => x.id !== hit.id) })); say(`Not saved: ${e.message}`); }
  };
  const prefRemove = async (kind, it) => {
    setD((p) => ({ ...p, [kind]: p[kind].filter((x) => x.id !== it.id) }));
    try { await removePref(kind, d.prof.id, it.id); } catch (e) { setD((p) => ({ ...p, [kind]: [...p[kind], it] })); say(`Not saved: ${e.message}`); }
  };
  const setProf = async (patch, msg) => {
    setD((p) => ({ ...p, prof: { ...p.prof, ...patch } }));
    try { await saveProfileRow(d.prof.id, patch); if (msg) say(msg); } catch (e) { say(`Not saved: ${e.message}`); }
  };
  const onPhoto = async (e) => {
    const f = e.target.files?.[0]; if (!f) return;
    try { const url = await uploadAvatar(user.id, f); await setProf({ avatar_url: url }, 'Photo updated'); } catch { say('The photo could not be uploaded. Choose it again.'); }
  };
  const dirty = acc.name !== acc0.name || acc.city !== acc0.city;
  const saveAccount = async () => {
    try {
      await Promise.all([
        saveProfileRow(d.prof.id, { full_name: acc.name.trim() }),
        cand ? saveCandidate(user.id, { full_name: acc.name.trim(), location: acc.city.trim() }) : null,
        supabase.auth.updateUser({ data: { full_name: acc.name.trim() } }),
      ]);
      setAcc0(acc); setD((p) => ({ ...p, prof: { ...p.prof, full_name: acc.name.trim() }, cand: p.cand ? { ...p.cand, full_name: acc.name.trim(), location: acc.city.trim() } : p.cand })); say('Saved');
    } catch (e) { say(`Not saved: ${e.message}`); }
  };
  const savePw = async () => {
    if (pw.a.length < 8) { setPw((p) => ({ ...p, msg: 'Use 8 or more characters.', bad: true })); return; }
    if (pw.a !== pw.b) { setPw((p) => ({ ...p, msg: 'The two passwords are not the same.', bad: true })); return; }
    const { error } = await updatePassword(pw.a);
    if (error) { setPw((p) => ({ ...p, msg: authMessage(error), bad: true })); return; }
    setPwOpen(false); setPw({ a: '', b: '', msg: '', bad: false }); say('Password updated');
  };
  const openCv = async () => { const u = await cvFileUrl(cand?.cv_storage_path); if (u) window.open(u, '_blank', 'noopener'); else say('Your CV file is not available. Upload it again.'); };

  const name = acc0.name || user?.email || '';
  const headline = cand?.experience?.[0]?.job_title || (cand ? 'Your CV is on file' : 'Add your CV to see matches');
  const avatar = d?.prof?.avatar_url;
  const nav = [['/dashboard', IcHome, 'Matches', matches?.length ?? ''], ['/saved', IcSaved, 'Saved', d?.saved ?? ''], ['/applied', IcApplied, 'Applied', d?.applied ?? '']];
  const linkRow = (k, label, prefix, ph) => (
    <div className={`lnkrow${links[k] ? '' : ' miss'}${editing === k ? ' editing' : ''}`} id={k === 'github' ? 'gh' : undefined}>
      <span>{label}</span><b>{links[k] ? `${prefix}${links[k]}` : 'Not added'}</b>
      <button className="add2" type="button" onClick={() => setEditing(k)}>{links[k] ? 'Edit' : 'Add'}</button>
      {editing === k && <input className="lin2" autoFocus placeholder={ph} aria-label={label} defaultValue={links[k]}
        onKeyDown={(e) => { if (e.key === 'Enter') saveLinks({ ...links, [k]: e.currentTarget.value.replace(/^https?:\/\/(www\.)?(linkedin\.com\/in\/|github\.com\/)?/, '') }); if (e.key === 'Escape') setEditing(''); }}
        onBlur={(e) => saveLinks({ ...links, [k]: e.currentTarget.value.replace(/^https?:\/\/(www\.)?(linkedin\.com\/in\/|github\.com\/)?/, '') })} />}
    </div>
  );

  return (
    <div className="jm-profile"><div className="page" id="top">
      <div className="app">
        <aside className="side" aria-label="Main">
          <Link className="logo" to="/dashboard"><img src="/jm/nabta-mark.svg" alt="" width="40" height="40" /><span className="display">JobMatcher</span></Link>
          {nav.map(([to, Ic, l, n]) => <Link key={to} className="nav-i" to={to}><Ic /><span>{l}</span><span className="b">{n}</span></Link>)}
          <span className="sp" />
          <Link className="newcv" to="/upload"><IcUpload /><span>Upload a new CV</span></Link>
          <Link className="me on" to="/profile" aria-current="page"><span className="s-av done" aria-hidden="true">{initials(name)}</span><div><b>{name}</b><small>Your profile</small></div><IcChev /></Link>
        </aside>
        <main className="main">
          <div className="mtop"><Link className="logo" to="/dashboard"><img src="/jm/nabta-mark.svg" alt="" width="36" height="36" /><span className="display">JobMatcher</span></Link></div>
          <section className="hero" aria-label="Your profile">
            <span className="halo" aria-hidden="true"><i /><i /></span>
            <div className="pav"><span className="face" aria-hidden="true" style={avatar ? { background: `center / cover url(${avatar})` } : undefined}>{avatar ? '' : initials(name)}</span>
              <button className="cam" type="button" aria-label="Change your photo" onClick={() => photoRef.current?.click()}><IcCam /></button>
              <input type="file" ref={photoRef} accept="image/*" hidden onChange={onPhoto} /></div>
            <h1 className="display">{name}</h1>
            <p className="hl">{headline}{cand?.location && <span><IcPin />{cand.location}</span>}</p>
            <div className="hbar">
              <a className="hs comp" href="#links" onClick={(e) => { e.preventDefault(); if (next?.[0] === 'github' || next?.[0] === 'linkedin') { go('profile'); setEditing(next[0]); } else if (next?.[0] === 'photo') photoRef.current?.click(); else if (next) navigate('/review'); }}>
                <Cup p={pct} /><span><b><em>{pct}</em>%</b><small>{next ? next[2] : 'complete'}</small></span></a>
              <Link className="hs" to="/applied"><b>{d?.applied ?? '…'}</b><small>applied</small></Link>
              <Link className="hs" to="/saved"><b>{d?.saved ?? '…'}</b><small>saved</small></Link>
              <Link className="hs" to="/dashboard"><b>{matches?.length ?? '…'}</b><small>matches</small></Link>
            </div>
          </section>
          <div className="ptabs" role="tablist" aria-label="Profile sections"><span className="ind ready" ref={indRef} aria-hidden="true" />
            {TABS.map(([k, l]) => <button key={k} ref={(el) => { tabRefs.current[k] = el; }} className="ptab" role="tab" type="button" aria-selected={tab === k} onClick={() => go(k)}>{l}</button>)}</div>
          <div className="track" ref={trackRef} onScroll={onScroll}>
            <section className="tp" ref={(el) => { panes.current.profile = el; }} role="tabpanel" aria-label="Profile" inert={tab !== 'profile'}>
              <div className="g2p">
                <div className="stack2">
                  <div className="card"><h2>About <Link to="/review">Edit</Link></h2><p className="body">{cand?.professional_summary || 'Add a short summary in your details.'}</p></div>
                  <div className="card"><h2>Experience <Link to="/review">Edit</Link></h2><ol className="xp">{(cand?.experience || []).map((j, i) => (
                    <li key={i}><div className="xh"><b>{j.job_title}</b><span className="when">{[j.start_date, j.is_current ? 'Present' : j.end_date].filter(Boolean).join(' to ')}</span></div><span className="co">{j.company}</span>{(j.responsibilities || []).length > 0 && <ul>{j.responsibilities.slice(0, 3).map((r, k) => <li key={k}>{r}</li>)}</ul>}</li>
                  ))}</ol></div>
                  <div className="card"><h2>Education <Link to="/review">Edit</Link></h2><ol className="xp edu">
                    {(cand?.education || []).map((e, i) => <li key={i}><div className="xh"><b>{[e.degree, e.field].filter(Boolean).join(', ')}</b><span className="when">{e.graduation_year || ''}</span></div><span className="co">{e.institution}</span></li>)}
                    {names(cand?.certifications).map((c, i) => <li key={`c${i}`}><div className="xh"><b>{c}</b></div><span className="co">Certification</span></li>)}
                  </ol></div>
                </div>
                <div className="stack2">
                  <div className="card"><h2>Your CV</h2>{cand ? <div className="cvf"><span className="ic3">{(cand.cv_mime_type || '').includes('pdf') ? 'PDF' : 'IMG'}</span><span><b>{cand.source_file || 'Your CV'}</b>{(cand.updated_at || cand.created_at) && <small>Read on {new Date(cand.updated_at || cand.created_at).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })}</small>}</span></div> : <p className="body">No CV yet.</p>}
                    <div className="btnrow"><Link className="pbtn ink" to="/upload"><IcUpload />{cand ? 'Update' : 'Add your CV'}</Link>{cand && <button className="pbtn line dlcv" type="button" onClick={openCv}><IcDl />Download</button>}</div></div>
                  <div className="card"><h2>Skills <span className="hint">in your matches</span></h2>
                    <ChipEditor items={skills.map((s) => ({ name: s }))} counts={counts} label="Add a skill" onAdd={(v) => !skills.some((s) => s.toLowerCase() === v.toLowerCase()) && setSkills([...skills, v])} onRemove={(it) => setSkills(skills.filter((s) => s !== it.name))} /></div>
                  <div className="card" id="links"><h2>Links</h2>
                    {linkRow('linkedin', 'LinkedIn', '', 'linkedin.com/in/username')}{linkRow('github', 'GitHub', 'github.com/', 'github.com/username')}{linkRow('portfolio', 'Portfolio', '', 'https://')}
                  </div>
                </div>
              </div>
            </section>
            <section className="tp" ref={(el) => { panes.current.prefs = el; }} role="tabpanel" aria-label="Preferences" inert={tab !== 'prefs'}>
              <div className="prefs">
                <div className="card score"><span className="cupv2"><Cup p={score} w={56} /><span>{score}</span><small>%</small></span>
                  <div><h2>Minimum match score</h2>
                    <input className="rng" type="range" min="30" max="95" step="5" value={score} aria-label="Minimum match score" style={{ '--f': `${((score - 30) / 65) * 100}%` }} onChange={(e) => setScore(Number(e.target.value))} onPointerUp={() => setProf({ min_match_score: score }, `Saved. Matches start at ${score}%`)} onKeyUp={() => setProf({ min_match_score: score })} />
                    <div className="rng-l"><span>More offers</span><span>Only close fits</span></div>
                    {effect != null && <p className="effect"><b>{effect} of your {matches.length} matches</b> are at {score}% or more.</p>}
                    <div className="sw2"><span><b>Email me new offers above this score</b></span><label className="tog"><input type="checkbox" checked={d?.prof?.smart_alerts ?? true} aria-label="Email me new offers above this score" onChange={(e) => setProf({ smart_alerts: e.target.checked }, e.target.checked ? 'Turned on' : 'Turned off')} /><i /></label></div></div></div>
                <div className="card"><h2>Cities</h2><ChipEditor items={(d?.cities || []).map((x) => ({ ...x, key: x.id }))} suggest={sug.cities} listId="dl-cities" label="Add a city" onAdd={(v) => prefAdd('cities', v)} onRemove={(it) => prefRemove('cities', it)} />
                  <div className="sw2"><span><b>Remote offers too</b></span><label className="tog"><input type="checkbox" checked={!!d?.prof?.open_to_remote} aria-label="Remote offers too" onChange={(e) => setProf({ open_to_remote: e.target.checked }, e.target.checked ? 'Turned on' : 'Turned off')} /><i /></label></div></div>
                <div className="card"><h2>Roles</h2><ChipEditor items={(d?.roles || []).map((x) => ({ ...x, key: x.id }))} suggest={sug.roles} listId="dl-roles" label="Add a role" onAdd={(v) => prefAdd('roles', v)} onRemove={(it) => prefRemove('roles', it)} /></div>
                <div className="card"><h2>Industries</h2><ChipEditor items={(d?.industries || []).map((x) => ({ ...x, key: x.id }))} suggest={sug.industries} listId="dl-ind" label="Add an industry" onAdd={(v) => prefAdd('industries', v)} onRemove={(it) => prefRemove('industries', it)} /></div>
              </div>
            </section>
            <section className="tp" ref={(el) => { panes.current.account = el; }} role="tabpanel" aria-label="Account" inert={tab !== 'account'}>
              <div className="stack2 acc">
                <div className="card"><h2>Account</h2><div className="sform">
                  <div className="fld2"><label htmlFor="s-name">Name</label><input id="s-name" autoComplete="name" value={acc.name} onChange={(e) => setAcc({ ...acc, name: e.target.value })} /></div>
                  <div className="fld2"><label htmlFor="s-loc">City</label><input id="s-loc" autoComplete="address-level2" value={acc.city} onChange={(e) => setAcc({ ...acc, city: e.target.value })} /></div>
                  <div className="fld2 wide"><label htmlFor="s-mail">Email</label><input id="s-mail" value={user?.email || ''} readOnly /><small>You sign in with it, so it cannot be changed here.</small></div></div></div>
                <div className={`card pw${pwOpen ? ' open' : ''}`}><div className="pw-h"><span><h2>Password</h2><small>Use 8 or more characters</small></span>
                  <button className="pbtn ink" type="button" aria-expanded={pwOpen} onClick={() => setPwOpen(true)}><IcLock />Change password</button></div>
                  <div className="pw-f" inert={!pwOpen}><div className="pw-in"><div className="sform">
                    <div className="fld2"><label htmlFor="s-p1">New password</label><input id="s-p1" type="password" placeholder="8 or more characters" autoComplete="new-password" value={pw.a} onChange={(e) => setPw({ ...pw, a: e.target.value, msg: '' })} /></div>
                    <div className="fld2"><label htmlFor="s-p2">Type it again</label><input id="s-p2" type="password" placeholder="Same password" autoComplete="new-password" value={pw.b} onChange={(e) => setPw({ ...pw, b: e.target.value, msg: '' })} /></div></div>
                    <p className={`pw-msg${pw.bad ? ' bad' : ''}`} aria-live="polite">{pw.msg}</p>
                    <div className="btnrow"><button className="pbtn ink" type="button" onClick={savePw}>Update password</button><button className="pbtn line" type="button" onClick={() => { setPwOpen(false); setPw({ a: '', b: '', msg: '', bad: false }); }}>Cancel</button></div></div></div></div>
                <button className="pbtn line signout" type="button" onClick={async () => { await signOut(); navigate('/'); }}><IcOut />Sign out</button>
              </div>
            </section>
          </div>
        </main>
        <nav className="tabs" aria-label="Main">{nav.map(([to, Ic, l]) => <Link key={to} to={to}><Ic />{l}</Link>)}</nav>
      </div>
      <div className={`savebar${dirty ? ' on' : ''}`} role="status"><span>Unsaved changes</span><span className="btnrow"><button className="pbtn lite" type="button" onClick={() => setAcc(acc0)}>Undo</button><button className="pbtn wh" type="button" onClick={saveAccount}>Save</button></span></div>
      {toast && <div className="toast" role="status">{toast}</div>}
    </div></div>
  );
}
