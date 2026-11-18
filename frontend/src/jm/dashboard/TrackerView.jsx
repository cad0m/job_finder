import { useEffect, useMemo, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { IcDownload, IcPlus, IcSearchSm, IcExt, IcSelChev, IcMark, IcClip, IcClose } from './icons';
import { Cup } from './DashboardPage';
import { INT, SOURCES, STATUSES, TODAY, deleteRow, fileUrl, initials, loadTracker, logoClass, saveRow, uploadOwnFile } from './data';

/* Applied: a tracker with the same columns as the user's Google Sheet ("job-application"). */

const HEAD = ['Company', 'Role', 'city', 'Job link', 'Source', 'Status', 'Date applied', 'First interview', 'Last activity', 'Days quiet', 'Follow up?', 'Next step', 'Next step date', 'Contact', 'Posted pay range', 'Notes'];
const SORTS = { 0: 'co', 5: 'st', 6: 'ap', 7: 'fi', 8: 'last', 9: 'q', 12: 'nextd' };
const day = (s) => new Date(`${s}T00:00:00`);
const quiet = (r) => (r.last ? Math.max(0, Math.round((day(TODAY()) - day(r.last)) / 864e5)) : null);
const grp = (st) => (st === 'Saved' ? 'saved' : st === 'Applied' ? 'applied' : INT.includes(st) ? 'int' : st === 'Offer' ? 'offer' : 'closed');
const followUp = (r) => { const q = quiet(r); return q !== null && ((r.st === 'Applied' && q >= 14) || (INT.includes(r.st) && q >= 10)); };
const fdate = (s) => (s ? day(s).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' }) : '');
const host = (u) => { try { return new URL(u).hostname.replace('www.', ''); } catch { return u; } };
const weekStart = () => { const d = day(TODAY()); const k = (d.getDay() + 6) % 7; d.setDate(d.getDate() - k); return d.toISOString().slice(0, 10); };
const plusDays = (s, n) => { const d = day(s); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); };
const cap = (s) => s.replace(/\b\w/g, (c) => c.toUpperCase());

/** "Paste a link and we fill in what we can" */
const fromLink = (value) => {
  let u; try { u = new URL(value.trim()); } catch { return null; }
  const h = u.hostname;
  const out = { src: /linkedin/.test(h) ? 'LinkedIn' : /anapec/.test(h) ? 'ANAPEC' : /jobzyn/.test(h) ? 'Jobzyn' : /rekrute|emploi|joblia|indeed|marocannonces/.test(h) ? 'Job board' : 'Company site' };
  const slug = decodeURIComponent(u.pathname.split('/').filter(Boolean).pop() || '').toLowerCase();
  const m = slug.match(/^(.+?)-recrute-(?:une?-|des-|\d+-)?(.+?)(?:-a-|-au-|-en-)([a-z-]+?)(?:-\d+)?$/);
  if (m) Object.assign(out, { co: cap(m[1].replace(/-/g, ' ')), role: cap(m[2].replace(/-/g, ' ')), city: cap(m[3].split('-')[0]) });
  return out;
};

function StatusSelect({ row, onChange, big, id }) {
  return (
    <span className={`stw${big ? ' big' : ''}`} data-g={grp(row.st)}>
      <select id={id} value={row.st} aria-label={`Status for ${row.role} at ${row.co}`} onChange={(e) => onChange(e.target.value)} onClick={(e) => e.stopPropagation()}>
        {STATUSES.map((s) => <option key={s}>{s}</option>)}
      </select><IcSelChev />
    </span>
  );
}

function SentCell({ r, onOpen }) {
  if (r.sent === 'gen') return <button className="sent gen" type="button" aria-label="See the CV, cover letter and email made with JobMatcher" onClick={(e) => { e.stopPropagation(); onOpen(r, 'gen'); }}><IcMark />3 files</button>;
  if (r.sent === 'own') return <button className="sent own" type="button" aria-label="See what you sent yourself" onClick={(e) => { e.stopPropagation(); onOpen(r, 'own'); }}><IcClip />Yours</button>;
  if (r.sent === 'writing') return <span className="sent wr"><i className="spin sm" />Writing</span>;
  if (r.st === 'Saved' && r.jobId) return <Link className="sent prep" to={`/apply/${r.jobId}`} onClick={(e) => e.stopPropagation()}>Prepare</Link>;
  return <button className="sent add" type="button" aria-label="Add what you sent" onClick={(e) => { e.stopPropagation(); onOpen(r, 'own'); }}><IcPlus />Add</button>;
}

/** Details drawer for one application: status, what you sent, tracking, offer. */
function Details({ row, dref, onSave, onDelete, onClose, userId, say }) {
  // Remounted per row (key), so the form starts from that row
  const [d, setD] = useState(row);
  const [tab, setTab] = useState(() => row?._tab || (row?.sent === 'gen' || row?.sent === 'writing' ? 'gen' : row?.own?.subject || row?.own?.file || row?.sent === 'own' ? 'own' : 'gen'));
  const [file, setFile] = useState(null);
  const [busy, setBusy] = useState(false);
  if (!row || !d) return <dialog className="dw td" ref={dref} onClose={onClose} />;
  const q = quiet(d);
  const set = (k, v) => setD((p) => ({ ...p, [k]: v }));
  const setOwn = (k, v) => setD((p) => ({ ...p, own: { ...(p.own || {}), [k]: v } }));
  const gen = d.sent === 'gen' || d.sent === 'writing';
  const mail = d.gen?.data_email || null;
  const openFile = async (path) => { const u = await fileUrl(path); if (u) window.open(u, '_blank', 'noopener'); };

  const submit = async (e) => {
    e.preventDefault(); setBusy(true);
    try {
      let next = { ...d };
      if (next.st !== row.st) { next.last = TODAY(); if (next.st !== 'Saved' && !next.ap) next.ap = TODAY(); if (INT.includes(next.st) && !next.fi) next.fi = TODAY(); }
      if (file) next.own = { ...(next.own || {}), file: await uploadOwnFile(userId, file) };
      const hasOwn = next.own?.subject || next.own?.body || next.own?.file;
      if (hasOwn && !gen) next.sent = 'own';
      if (next.st === 'Saved' && !row.appId && !hasOwn && next.st === row.st && next.notes === row.notes && next.next === row.next) { dref.current?.close(); return; }
      if (next.st === 'Saved' && (hasOwn || next.next || next.notes)) next.st = row.st;   // keep it, the row becomes an entry
      await onSave(next);
      dref.current?.close();
    } catch (err) {
      say(`Not saved: ${err.message || 'try again'}`);
    } finally { setBusy(false); }
  };

  return (
    <dialog className="dw td" ref={dref} aria-labelledby="td-t" onClose={onClose} onClick={(e) => { if (e.target === e.currentTarget) e.currentTarget.close(); }}>
      <form className="dw-in td-in" onSubmit={submit}>
        <header className="td-top"><span className={`logo-c ${logoClass(d.co)}`} aria-hidden="true">{initials(d.co)}</span><span className="td-h"><b id="td-t">{d.role || 'Role'}</b><span>{[d.co, d.city].filter(Boolean).join(' · ')}</span></span><button className="dw-ib dw-x" type="button" aria-label="Close" onClick={() => dref.current?.close()}><IcClose /></button></header>
        <div className="td-body">
          <div className="td-stat"><StatusSelect row={d} big id="td-st" onChange={(v) => set('st', v)} /><span className="td-q">{q === null ? '' : q === 0 ? 'Active today' : `Quiet for ${q} day${q > 1 ? 's' : ''}`}</span></div>
          {followUp(d) && <div className="td-fu"><b>No reply for {q} days.</b><span>A short, polite follow-up often gets an answer.</span><button className="lnk3" type="button" onClick={() => setD((p) => ({ ...p, next: 'Send a short follow-up email', nextd: plusDays(TODAY(), 2) }))}>Plan a follow-up</button></div>}
          <section className="td-sec"><h3>What you sent</h3>
            <div className="seg7" role="radiogroup" aria-label="What you sent">
              <label><input type="radio" name="tds" value="gen" checked={tab === 'gen'} onChange={() => setTab('gen')} />Made with JobMatcher</label>
              <label><input type="radio" name="tds" value="own" checked={tab === 'own'} onChange={() => setTab('own')} />Your own</label>
            </div>
            {tab === 'gen' && <div className="tds-p p-gen" style={{ display: 'flex' }}>
              {gen ? <>
                <div className="tdocs">
                  {[['cv', 'CV', 'CV', 'Tailored to this offer'], ['cover_letter', 'CL', 'Cover letter', 'Addressed to the company'], ['email', 'EM', 'Email', 'Subject and message']].map(([k, i, b, s]) => (
                    <button key={k} className="tdoc" type="button" disabled={!d.gen?.[k]} onClick={() => d.gen?.[k] && window.open(d.gen[k], '_blank', 'noopener')}><i>{i}</i><span><b>{b}</b><small>{d.gen?.[k] ? s : 'Not ready'}</small></span></button>
                  ))}
                </div>
                {mail && <div className="tmail"><span className="tm-s"><small>Subject</small><b>{mail.subject}</b></span><p>{mail.body}</p></div>}
              </> : <div className="tnone"><span>Nothing was made with JobMatcher for this offer.</span>{d.jobId && <Link className="lnk3" to={`/apply/${d.jobId}`}>Prepare it with JobMatcher</Link>}</div>}
            </div>}
            {tab === 'own' && <div className="tds-p p-own" style={{ display: 'flex' }}>
              <div className="fld3"><label htmlFor="td-osub">Subject</label><input id="td-osub" placeholder="The subject of your email" value={d.own?.subject || ''} onChange={(e) => setOwn('subject', e.target.value)} /></div>
              <div className="fld3"><label htmlFor="td-obody">Message</label><textarea id="td-obody" rows="5" placeholder="Paste the email or message you sent" value={d.own?.body || ''} onChange={(e) => setOwn('body', e.target.value)} /></div>
              <div className={`tfile${file || d.own?.file ? ' has' : ''}`}>
                <input type="file" id="td-ofile" accept=".pdf,.doc,.docx,image/*" className="vh" onChange={(e) => setFile(e.target.files[0] || null)} />
                <label htmlFor="td-ofile" className="tf-b"><IcClip /><span>{file?.name || (d.own?.file ? d.own.file.split('/').pop().replace(/^\d+-/, '') : 'Attach the CV you sent')}</span></label>
                {!file && d.own?.file && <button type="button" className="lnk3" onClick={() => openFile(d.own.file)}>Open</button>}
              </div>
            </div>}
          </section>
          <section className="td-sec"><h3>Tracking</h3>
            <div className="tgrid">
              {[['ap', 'Date applied'], ['fi', 'First interview'], ['last', 'Last activity'], ['nextd', 'Next step date']].map(([k, l]) => (
                <div className="fld3" key={k}><label htmlFor={`td-${k}`}>{l}</label><input type="date" id={`td-${k}`} value={d[k] || ''} onChange={(e) => set(k, e.target.value)} /></div>
              ))}
              <div className="fld3 wide"><label htmlFor="td-next">Next step</label><input id="td-next" placeholder="Send the case study, call back, wait…" value={d.next || ''} onChange={(e) => set('next', e.target.value)} /></div>
            </div>
          </section>
          <section className="td-sec"><h3>Offer</h3>
            <div className="tgrid">
              <div className="fld3 wide"><label htmlFor="td-link">Job link</label><span className="lk"><input id="td-link" type="url" value={d.link || ''} onChange={(e) => set('link', e.target.value)} />{d.link && <a href={d.link} target="_blank" rel="noopener noreferrer" aria-label="Open the job post"><IcExt /></a>}</span></div>
              <div className="fld3"><label htmlFor="td-src">Source</label><select id="td-src" value={d.src || 'Other'} onChange={(e) => set('src', e.target.value)}>{[...new Set([...SOURCES, d.src].filter(Boolean))].map((s) => <option key={s}>{s}</option>)}</select></div>
              <div className="fld3"><label htmlFor="td-city">city</label><input id="td-city" value={d.city || ''} onChange={(e) => set('city', e.target.value)} /></div>
              <div className="fld3"><label htmlFor="td-ct">Contact</label><input id="td-ct" value={d.contact || ''} onChange={(e) => set('contact', e.target.value)} /></div>
              <div className="fld3"><label htmlFor="td-pay">Posted pay range</label><input id="td-pay" value={d.pay || ''} onChange={(e) => set('pay', e.target.value)} /></div>
              <div className="fld3 wide"><label htmlFor="td-notes">Notes</label><textarea id="td-notes" rows="3" value={d.notes || ''} onChange={(e) => set('notes', e.target.value)} /></div>
            </div>
          </section>
        </div>
        <footer className="td-foot">{row.appId ? <button className="tdel" type="button" onClick={() => { dref.current?.close(); onDelete(row); }}>Delete</button> : <span />}<button className="go td-save" type="submit" disabled={busy}><span className="s-go">{busy ? 'Saving…' : 'Save changes'}</span></button></footer>
      </form>
    </dialog>
  );
}

export default function TrackerView({ user, say, onCount }) {
  const [rows, setRows] = useState(null);
  const [filt, setFilt] = useState('all');
  const [q, setQ] = useState('');
  const [sort, setSort] = useState({ k: null, dir: 1 });
  const [goal, setGoal] = useState(() => { try { return Number(localStorage.getItem('jm-goal')) || 5; } catch { return 5; } });
  const [openRow, setOpenRow] = useState(null);
  const [flash, setFlash] = useState(null);
  const [add, setAdd] = useState({ link: '', co: '', role: '', city: '', src: 'Job board', st: 'Applied', ap: TODAY() });
  const dref = useRef(null);
  const aref = useRef(null);
  const twRef = useRef(null);

  useEffect(() => { loadTracker(user.id).then(setRows).catch(() => { setRows([]); say('The tracker could not load. Refresh the page.'); }); }, [user.id, say]);
  useEffect(() => { try { localStorage.setItem('jm-goal', String(goal)); } catch { /* per-device only */ } }, [goal]);

  const all = useMemo(() => rows || [], [rows]);
  const sent = all.filter((r) => r.ap);
  useEffect(() => { onCount?.(sent.length); }, [sent.length, onCount]);
  const ints = all.filter((r) => r.fi).length;
  const ws = weekStart();
  const week = all.filter((r) => r.ap && r.ap >= ws && r.ap <= plusDays(ws, 6));
  const perDay = [0, 1, 2, 3, 4, 5, 6].map((i) => week.filter((r) => r.ap === plusDays(ws, i)).length);
  const todayIdx = Math.round((day(TODAY()) - day(ws)) / 864e5);
  const done = week.length >= goal;
  const counts = { all: all.length, saved: 0, applied: 0, int: 0, offer: 0, closed: 0 };
  all.forEach((r) => { counts[grp(r.st)] += 1; });
  const fuN = all.filter(followUp).length;

  const visible = useMemo(() => {
    const t = q.trim().toLowerCase();
    let list = all.filter((r) => (filt === 'all' || (filt === 'fu' ? followUp(r) : grp(r.st) === filt)) && (!t || `${r.co} ${r.role} ${r.city}`.toLowerCase().includes(t)));
    if (sort.k) list = [...list].sort((a, b) => { const va = sort.k === 'q' ? quiet(a) ?? -1 : a[sort.k] || ''; const vb = sort.k === 'q' ? quiet(b) ?? -1 : b[sort.k] || ''; return (va > vb ? 1 : va < vb ? -1 : 0) * sort.dir; });
    return list;
  }, [all, filt, q, sort]);

  const replace = (old, next) => { setRows((rs) => rs.map((r) => (r.key === old.key ? next : r))); setFlash(next.key); };
  const persist = async (old, next) => { const saved = await saveRow(user.id, next); replace(old, saved); return saved; };

  const changeStatus = async (r, st) => {
    const next = { ...r, st, last: TODAY(), ap: st !== 'Saved' && !r.ap ? TODAY() : r.ap, fi: INT.includes(st) && !r.fi ? TODAY() : r.fi };
    replace(r, next);
    try { await persist(next, next); say(`${r.co}: ${st}${st === 'Offer' ? '. Congratulations!' : ''}`); if (!done && st !== 'Saved' && !r.ap && week.length + 1 >= goal) say(`Weekly goal reached: ${week.length + 1} applications sent`); }
    catch (err) { replace(next, r); say(`Not saved: ${err.message || 'try again'}`); }
  };
  const remove = async (r) => {
    setRows((rs) => rs.filter((x) => x.key !== r.key));
    try { await deleteRow(r); say(`Deleted ${r.co}`); } catch (err) { setRows((rs) => [r, ...rs]); say(`Not deleted: ${err.message}`); }
  };
  const open = (r, tab) => { setOpenRow({ ...r, _tab: tab }); setTimeout(() => dref.current?.showModal(), 0); };

  const submitAdd = async (e) => {
    e.preventDefault();
    const r = { key: `n${Date.now()}`, appId: null, jobId: null, co: add.co.trim(), role: add.role.trim(), city: add.city.trim(), link: add.link.trim(), src: add.src, st: add.st,
      ap: add.st === 'Saved' ? '' : add.ap, fi: INT.includes(add.st) ? TODAY() : '', last: TODAY(), next: '', nextd: '', contact: '', pay: '', notes: '', sent: null, gen: {}, own: {} };
    try {
      const saved = await saveRow(user.id, r);
      setRows((rs) => [saved, ...rs]); setFilt('all'); setFlash(saved.key); aref.current?.close();
      say(`Added ${saved.co}`);
      setAdd({ link: '', co: '', role: '', city: '', src: 'Job board', st: 'Applied', ap: TODAY() });
    } catch (err) { say(`Not added: ${err.message || 'try again'}`); }
  };

  const exportCsv = () => {
    const c = (v) => { v = v == null ? '' : String(v); return /[",\n]/.test(v) ? `"${v.replace(/"/g, '""')}"` : v; };
    const lines = [HEAD.map(c).join(',')].concat(all.map((r) => { const qd = quiet(r); return [r.co, r.role, r.city, r.link, r.src, r.st, r.ap, r.fi, r.last, qd ?? '', qd === null ? '' : followUp(r) ? 'Yes' : 'No', r.next, r.nextd, r.contact, r.pay, r.notes].map(c).join(','); }));
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([String.fromCharCode(0xfeff) + lines.join('\n')], { type: 'text/csv' })); a.download = 'job-applications.csv'; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    say('Downloaded job-applications.csv. Import it into Google Sheets.');
  };

  const [shadow, setShadow] = useState({ l: false, r: true });
  const onScroll = () => { const t = twRef.current; if (t) setShadow({ l: t.scrollLeft > 4, r: t.scrollLeft < t.scrollWidth - t.clientWidth - 4 }); };
  const chip = (k, label, n, extra = '') => <button key={k} className={`tchip${extra}`} type="button" data-g={k} aria-pressed={filt === k} onClick={() => setFilt(filt === k && k !== 'all' ? 'all' : k)}>{label}<em>{n}</em></button>;

  return (
    <section className="view v-applied" aria-labelledby="h-applied">
      <div className="mhead thead2"><h1 className="display" id="h-applied">Applied</h1><span className="count"><b>{sent.length}</b>sent</span>
        <span className="sp" /><button className="ghost2 tcsv" type="button" onClick={exportCsv}><IcDownload /><span>Export CSV</span></button>
        <button className="tadd" type="button" onClick={() => aref.current?.showModal()}><IcPlus /><span>Add an application</span></button></div>
      <div className="tkpis">
        <div className={`goal${done ? ' done' : ''}`} style={{ '--p': String(Math.min(1, week.length / goal)) }}>
          <div className="g-cup"><Cup p={100} w={58} cls="cup gcup" /></div>
          <div className="g-t"><b>{week.length} of {goal}</b><span className="g-l">sent this week</span><span className="g-sub">{done ? 'Goal reached. Well done.' : `${goal - week.length} more to reach your goal`}</span></div>
          <div className="g-r"><div className="wk" aria-label="Sent per day this week">{['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((l, i) => <span key={i} className={`wd${i === todayIdx ? ' today' : ''}${i > todayIdx ? ' fut' : ''}`} style={{ '--h': String(perDay[i]) }}><i /><b>{l}</b></span>)}</div>
            <div className="g-st" role="group" aria-label="Weekly goal"><button type="button" className="gs" aria-label="Lower the goal" onClick={() => setGoal((g) => Math.max(1, g - 1))}>−</button><span>Goal</span><button type="button" className="gs" aria-label="Raise the goal" onClick={() => setGoal((g) => Math.min(30, g + 1))}>+</button></div></div>
        </div>
        <div className="kpi"><b>{sent.length}</b><span>applications sent</span></div>
        <div className="kpi"><b>{ints}</b><span>interviews · <em>{sent.length ? Math.round((100 * ints) / sent.length) : 0}%</em> of sent</span></div>
        <div className="kpi ok"><b>{counts.offer}</b><span>{counts.offer === 1 ? 'offer' : 'offers'}</span></div>
        <button className="kpi warn" type="button" onClick={() => setFilt(filt === 'fu' ? 'all' : 'fu')}><b>{fuN}</b><span>to follow up</span></button>
      </div>
      <div className="tbar2">
        <div className="tchips" role="group" aria-label="Show">
          {chip('all', 'All', counts.all)}{chip('saved', 'Saved', counts.saved)}{chip('applied', 'Applied', counts.applied)}{chip('int', 'Interviewing', counts.int)}{chip('offer', 'Offer', counts.offer)}{chip('closed', 'Closed', counts.closed)}{chip('fu', 'Follow up', fuN, ' fuc')}
        </div>
        <label className="tsearch"><IcSearchSm /><input type="search" placeholder="Company, role or city" aria-label="Search your applications" value={q} onChange={(e) => setQ(e.target.value)} /></label>
      </div>
      <div className={`tw${shadow.l ? ' sl' : ''}${shadow.r ? ' sr' : ''}`} ref={twRef} onScroll={onScroll} tabIndex="0" role="region" aria-label="Your applications, scroll sideways for more columns">
        <table className="tt"><thead><tr>
          {HEAD.map((h, i) => {
            const k = SORTS[i];
            const aria = k ? (sort.k === k ? (sort.dir > 0 ? 'ascending' : 'descending') : 'none') : undefined;
            return <th scope="col" key={h} className={`h-${i}`} aria-sort={aria}>{k ? <button type="button" onClick={() => setSort({ k, dir: sort.k === k ? -sort.dir : k === 'co' ? 1 : -1 })}>{h}</button> : h}{(h === 'Days quiet' || h === 'Follow up?') && <> <span className="auto-t" title="Filled in for you">auto</span></>}</th>;
          })}
          <th scope="col" className="h-se"><span className="vh">What you sent</span></th>
        </tr></thead>
          <tbody>
            {visible.map((r) => {
              const qd = quiet(r); const fu = followUp(r); const g = grp(r.st); const over = r.nextd && r.nextd < TODAY() && g !== 'closed';
              return (
                <tr key={r.key} className={`tr${fu ? ' fu' : ''}${g === 'closed' ? ' closed' : ''}${g === 'offer' ? ' offer' : ''}${flash === r.key ? ' flash' : ''}`} tabIndex="0" onClick={() => open(r)} onKeyDown={(e) => { if (e.key === 'Enter' && e.target === e.currentTarget) open(r); }}>
                  <th scope="row" className="c-co" data-l="Company"><span className={`logo-c ${logoClass(r.co)}`} aria-hidden="true">{initials(r.co)}</span><span className="co-t"><b>{r.co}</b></span></th>
                  <td className="c-ro" data-l="Role">{r.role}</td>
                  <td className="c-ci" data-l="City">{r.city}</td>
                  <td className="c-li" data-l="Job link">{r.link && <a href={r.link} target="_blank" rel="noopener noreferrer" onClick={(e) => e.stopPropagation()}>{host(r.link)}<IcExt /></a>}</td>
                  <td className="c-so" data-l="Source">{r.src && <span className="src">{r.src}</span>}</td>
                  <td className="c-st" data-l="Status"><StatusSelect row={r} onChange={(v) => changeStatus(r, v)} /></td>
                  <td className="c-d c-ap" data-l="Date applied">{fdate(r.ap) || <i className="dash">—</i>}</td>
                  <td className="c-d" data-l="First interview">{fdate(r.fi) || <i className="dash">—</i>}</td>
                  <td className="c-d" data-l="Last activity">{fdate(r.last) || <i className="dash">—</i>}</td>
                  <td className="c-q auto" data-l="Days quiet">{qd ?? ''}</td>
                  <td className="c-f auto" data-l="Follow up?">{qd !== null && g !== 'closed' && g !== 'saved' ? (fu ? <span className="fub">Yes</span> : <span className="fno">No</span>) : ''}</td>
                  <td className="c-nx" data-l="Next step">{r.next}</td>
                  <td className={`c-d${over ? ' over' : ''}`} data-l="Next step date">{fdate(r.nextd)}</td>
                  <td className="c-ct" data-l="Contact">{r.contact && (/@/.test(r.contact) ? <a href={`mailto:${r.contact}`} onClick={(e) => e.stopPropagation()}>{r.contact}</a> : r.contact)}</td>
                  <td className="c-pa" data-l="Posted pay range">{r.pay}</td>
                  <td className="c-no" data-l="Notes"><span className="clamp">{r.notes}</span></td>
                  <td className="c-se"><SentCell r={r} onOpen={open} /></td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {rows && visible.length === 0 && <div className="tempty"><b>{all.length ? 'Nothing here' : 'No applications yet'}</b><span>{all.length ? 'No application matches this filter.' : 'Prepare one from your matches, or add one you sent yourself.'}</span></div>}
        {!rows && <div className="tempty"><span>Loading your applications…</span></div>}
      </div>
      <p className="tlegend"><span><i className="lg fu" />No reply for a while: follow up</span><span><i className="lg offer" />Offer</span><span><i className="lg closed" />Closed</span><span className="auto-t">auto</span> columns fill themselves in</p>

      <Details key={openRow?.key || 'none'} row={openRow} dref={dref} userId={user.id} say={say} onClose={() => setOpenRow(null)}
        onSave={async (next) => { await persist(openRow, next); say('Saved'); }} onDelete={remove} />

      <dialog className="tadd-d" ref={aref} aria-labelledby="ta-t" onClick={(e) => { if (e.target === e.currentTarget) e.currentTarget.close(); }}>
        <form className="ta-in" onSubmit={submitAdd}>
          <h2 className="display" id="ta-t">Add an application</h2>
          <p className="ta-lead">For an offer you found outside JobMatcher. Paste the link and we fill in what we can.</p>
          <div className="fld3"><label htmlFor="ta-link">Job link</label><input id="ta-link" type="url" placeholder="https://" autoComplete="off" value={add.link} onChange={(e) => { const v = e.target.value; const g = fromLink(v); setAdd((a) => ({ ...a, link: v, ...(g ? { src: g.src, co: g.co || a.co, role: g.role || a.role, city: g.city || a.city } : {}) })); }} /></div>
          <div className="tgrid">
            <div className="fld3"><label htmlFor="ta-co">Company</label><input id="ta-co" required value={add.co} onChange={(e) => setAdd({ ...add, co: e.target.value })} /></div>
            <div className="fld3"><label htmlFor="ta-ro">Role</label><input id="ta-ro" required value={add.role} onChange={(e) => setAdd({ ...add, role: e.target.value })} /></div>
            <div className="fld3"><label htmlFor="ta-ci">city</label><input id="ta-ci" value={add.city} onChange={(e) => setAdd({ ...add, city: e.target.value })} /></div>
            <div className="fld3"><label htmlFor="ta-src">Source</label><select id="ta-src" value={add.src} onChange={(e) => setAdd({ ...add, src: e.target.value })}>{SOURCES.map((s) => <option key={s}>{s}</option>)}</select></div>
            <div className="fld3"><label htmlFor="ta-st">Status</label><select id="ta-st" value={add.st} onChange={(e) => setAdd({ ...add, st: e.target.value })}>{STATUSES.map((s) => <option key={s}>{s}</option>)}</select></div>
            <div className="fld3"><label htmlFor="ta-ap">Date applied</label><input type="date" id="ta-ap" value={add.ap} onChange={(e) => setAdd({ ...add, ap: e.target.value })} /></div>
          </div>
          <div className="ta-f"><button className="ghost2" type="button" onClick={() => aref.current?.close()}>Cancel</button><button className="go" type="submit"><span className="s-go">Add to tracker</span></button></div>
        </form>
      </dialog>
    </section>
  );
}
