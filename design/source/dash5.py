# Your matches v2: simpler shell (Matches, Saved, Applied; profile on the name card), one search bar with a filter panel,
# a focused best match and a scannable list. Builds canvas boards, the main preview page and the standalone preview.
import sys, os, re, shutil
S = sys.argv[1]
A = f'{S}/auth'
src = open(f'{A}/auth2.py').read()
exec(src[src.index('def svg('):src.index('def signin(')])
CSS = open(f'{A}/auth2.css').read() + open(f'{A}/dash2.css').read() + open(f'{A}/dash3.css').read() + open(f'{A}/dash4.css').read() + open(f'{A}/tracker.css').read()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Outfit:wght@400;500;600;700&amp;display=swap">'
I = lambda d, w=20, c='': svg(d, w=w, cls=c)
IC = {
 'home': I('<path d="M4 11l8-7 8 7v9H4z"></path><path d="M10 20v-5h4v5"></path>'),
 'saved': I('<path d="M7 4h10v16l-5-4-5 4z"></path>'),
 'applied': I('<path d="M4 12l16-8-6 16-3-6z"></path>'),
 'upload': I('<path d="M12 16V4M7 9l5-5 5 5"></path><path d="M5 20h14"></path>', 18),
 'search': I('<circle cx="11" cy="11" r="6.5"></circle><path d="M16 16l4 4"></path>'),
 'filter': I('<path d="M4 6h16M7 12h10M10 18h4"></path>', 18),
 'chev': I('<path d="M9 6l6 6-6 6"></path>', 18, 'chev'),
}
BOOK = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M7 4h10v16l-5-4-5 4z"></path></svg>'
TKS = '<svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
JOBS = [  # title, company, city, source, score, type, level, matched, total, posted, new, logo
 ('Data Analyst', 'CIH Bank', 'Casablanca', 'LinkedIn', 88, 'Full-time', 'Junior', ['Python', 'SQL', 'Power BI'], 3, '1 day ago', True, 'l2'),
 ('BI Developer', 'OCP Group', 'Casablanca', 'ANAPEC', 84, 'Full-time', 'Junior', ['Power BI', 'SQL'], 3, '2 days ago', False, 'l3'),
 ('Ingénieur BI junior', 'Maroc Telecom', 'Rabat', 'ANAPEC', 79, 'Full-time', 'Junior', ['SQL', 'Tableau'], 3, '3 days ago', False, 'l1'),
 ('Stage PFE Data Science', 'inwi', 'Casablanca', 'LinkedIn', 76, 'Internship', 'Intern', ['Python', 'Pandas'], 3, 'Today', True, 'l4'),
 ('Data Scientist junior', 'Capgemini', 'Rabat', 'LinkedIn', 72, 'Full-time', 'Junior', ['Python', 'Spark'], 3, '4 days ago', False, 'l2'),
 ('Analyste de données', 'Marjane', 'Casablanca', 'Jobzyn', 69, 'Full-time', 'Junior', ['Excel', 'SQL'], 3, '5 days ago', False, 'l1'),
 ('ML Engineer', 'Deloitte', 'Casablanca', 'LinkedIn', 64, 'Contract', 'Mid', ['Python'], 3, '1 week ago', False, 'l3'),
 ('Data Engineer', 'Remote team', 'Remote', 'Jobzyn', 61, 'Full-time', 'Mid', ['Spark'], 3, '1 week ago', False, 'l4'),
 ('Consultant BI', 'Avanade', 'Casablanca', 'Jobzyn', 58, 'Contract', 'Junior', ['Power BI', 'DAX'], 3, '1 week ago', False, 'l2'),
]
def cup(p, w=24, cls='cup'):
    h = round(37 * p / 100, 1); y = round(50 - h, 1)
    return f'<svg class="{cls}" viewBox="0 0 48 56" width="{w}" height="{round(w*56/48)}" aria-hidden="true"><rect class="lvl" x="16" y="{y}" width="16" height="{h}" rx="1.5" fill="#FF7F45"></rect><rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" stroke-width="2.8"></rect><path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" stroke-width="2.8" stroke-linejoin="round"></path></svg>'
def ini(c):
    w = c.split()
    return (w[0][0] + (w[1][0] if len(w) > 1 else w[0][1])).upper()
def row(k, j, hidden=False):
    t, co, city, srcn, sc, typ, lvl, m, tot, posted, new, lc = j
    full = ' full' if len(m) == tot else ''
    return f'''          <article class="row{" hid" if hidden else ""}" style="--k: {k};" data-type="{typ}" data-level="{lvl}" data-city="{city}" data-src="{srcn}" data-text="{(t + ' ' + co + ' ' + ' '.join(m)).lower()}">
            <a class="stretch" href="#job" data-i="{k}" aria-label="{t} at {co}, {sc}% match"></a>
            <span class="logo-c {lc}" aria-hidden="true">{ini(co)}</span>
            <span class="r-t"><b>{t}<span class="ar" aria-hidden="true">→</span></b><span>{co} · {city} · {srcn}</span></span>
            <span class="r-sk"><span class="k{full}">{len(m)}/{tot}</span><span class="names">{", ".join(m)}</span></span>
            <span class="r-d{" new" if new else ""}">{posted}</span>
            <span class="r-sc">{cup(sc, 22)}<b>{sc}<small>%</small></b></span>
            <button class="save" type="button" data-k="{k}" aria-pressed="{'true' if str(k) in ('1', '3') else 'false'}" aria-label="Save {t} at {co}">{BOOK}</button>
          </article>
'''
exec(open(f'{A}/dash3_drawer.py').read())
exec(open(f'{A}/dash4_views.py').read())
exec(open(f'{A}/tracker.py').read())
TD_STATIC = None
DRAWER_DATA = '<script type="application/json" id="jobdata">' + _json.dumps({'order': ORDER, 'jobs': {k: dict(v, html=dbody(v), ini=ini(v['co']), cup=cup(v['sc'], 22)) for k, v in DETAIL.items()}}) + '</script>'
GROUPS = [('Type', 'type', ['Any', 'Full-time', 'Internship', 'Contract']), ('Level', 'level', ['Any', 'Intern', 'Junior', 'Mid']), ('City', 'city', ['Any', 'Casablanca', 'Rabat', 'Remote']), ('Source', 'src', ['Any', 'ANAPEC', 'Jobzyn', 'LinkedIn'])]
def panel(static=False, preset=None):
    preset = preset or {}
    g = ''.join(f'<div class="fgp"><span>{lab}</span><div class="seg">' + ''.join(f'<button class="opt2" type="button" data-f="{key}" data-v="{o}" aria-pressed="{"true" if preset.get(key, "Any") == o else "false"}">{o}</button>' for o in opts) + '</div></div>' for lab, key, opts in GROUPS)
    attr = ' class="fp static"' if static else ' class="fp" popover id="fp"'
    close = '' if static else ' popovertarget="fp" popovertargetaction="hide"'
    return f'''<div{attr} aria-label="Filters">
          <div class="fp-h"><b>Filters</b><button class="fp-x" type="button"{close} aria-label="Close filters">×</button></div>
          {g}
          <div class="fp-f"><button class="lnk" type="button" id="fp-reset">Reset</button><button class="go" type="button" id="fp-apply"{close}><span class="s-go" id="fp-count">Show {"2" if preset else "84"} offers</span></button></div>
        </div>'''

def body(logo, home, links, show_panel=False, show_details=False, view='matches'):
    nav = [('home', 'Matches', '#matches', 'matches', '84'), ('saved', 'Saved', '#saved', 'saved', '<b class="n-saved">3</b>'), ('applied', 'Applied', '#applied', 'applied', '<b class="n-sent">11</b>')]
    navh = ''.join(f'<a class="nav-i{" on" if v == view else ""}" href="{h}" data-nav="{v}"{" aria-current=\"page\"" if v == view else ""}>{IC[i]}<span>{t}</span><span class="b">{b}</span></a>' for i, t, h, v, b in nav)
    tabs = ''.join(f'<a class="{"on" if v == view else ""}" href="{h}" data-nav="{v}">{IC[i]}{t}</a>' for i, t, h, v, b in nav)
    rows = ''.join(row(k, j, hidden=k >= 6) for k, j in enumerate(JOBS))
    preset = {'city': 'Rabat'} if show_panel else None
    act = '<button class="achip" type="button" data-f="city">Rabat<i>×</i></button><button class="reset" type="button">Clear all</button>' if show_panel else ''
    return f'''<div class="page">
<div class="app" id="app" data-view="{view}">
  <aside class="side" aria-label="Main">
    <a class="logo" href="{home}"><img src="{logo}" alt="" width="40" height="40"><span class="display">JobMatcher</span></a>
    {navh}
    <span class="sp"></span>
    <a class="newcv" href="{links['upload']}">{IC['upload']}<span>Upload a new CV</span></a>
    <a class="me" href="#profile" aria-label="Your profile"><span class="s-av done" aria-hidden="true">SE</span><div><b>Salma El Idrissi</b><small>View profile</small></div>{IC['chev']}</a>
  </aside>
  <main class="main">
    <div class="mtop"><a class="logo" href="{home}"><img src="{logo}" alt="" width="36" height="36"><span class="display">JobMatcher</span></a><a class="avl" href="#profile" aria-label="Your profile"><span class="s-av done">SE</span></a></div>
    <section class="view v-matches" data-v="matches" aria-label="Your matches">
    <div class="mhead" style="--d: 0;"><h1 class="display">Your matches</h1><span class="count"><b id="cnt">84</b>offers</span></div>
    <div class="sbar" style="--d: 1;">{IC['search']}<input type="search" id="q" placeholder="Search a role, company or skill" aria-label="Search your matches"><button class="fbtn" type="button" popovertarget="fp" aria-label="Filters">{IC['filter']}<span class="lbl">Filters</span><span class="n" id="fn"{"" if show_panel else " hidden"}>1</span></button></div>
    <div class="act" id="act"{"" if show_panel else " hidden"}>{act}</div>
    {panel(static=True, preset=preset) if show_panel else panel()}
    <article class="best">
      <div class="cupbig" role="img" aria-label="91% match">{cup(91, 70, "cup big")}<span class="v"><b>91<small>%</small></b><span>match</span></span></div>
      <div class="b-m">
        <span class="kick" style="--d: 0;"><i class="live"></i>Best match today</span>
        <h2 style="--d: 1;"><a class="blink" href="#job" data-i="b">Data Engineer</a></h2>
        <span class="co" style="--d: 2;">Attijariwafa bank · Casablanca</span>
        <div class="facts" style="--d: 3;"><span class="fact"><i class="ok">{TKS}</i>3 of 4 skills</span><span class="fact"><i class="ok">{TKS}</i>Junior</span><span class="fact"><i class="ok">{TKS}</i>Casablanca</span><span class="fact miss">Missing: Airflow</span></div>
      </div>
      <div class="b-r" style="--d: 4;"><a class="go" href="{links['apply']}"><span class="s-go">Prepare application{ARR}</span></a><div class="sub"><button class="ghost2 bsave" type="button" data-k="b" aria-pressed="true" aria-label="Save Data Engineer at Attijariwafa bank">{BOOK}Save</button><a class="ghost2" href="#job" data-i="b">View offer</a></div></div>
    </article>
    <div class="lh"><h3>Next best matches</h3><span id="shown">Sorted by match</span></div>
    <div class="list" id="list">
{rows}      <div class="empty" id="empty"><b>Nothing here</b><span>No offers match these filters.</span><button type="button" id="clear2">Clear filters</button></div>
    </div>
    <button class="more" type="button" id="more">Show more</button>
    <p class="note">Example offers, to show how matches look.</p>
    </section>
    {saved_view()}
    {applied_view()}
  </main>
  {srow_tpl()}
  <div class="toast" id="toast" role="status" hidden></div>
  {drawer(show_details)}
  {tracker_dialogs(TD_STATIC)}
  <nav class="tabs" aria-label="Main">{tabs}</nav>
</div>
</div>'''

JS = r'''<script>
(() => {
  const rows = [...document.querySelectorAll('#list .row')], q = document.getElementById('q'), more = document.getElementById('more'), empty = document.getElementById('empty');
  const cnt = document.getElementById('cnt'), fn = document.getElementById('fn'), act = document.getElementById('act'), fpc = document.getElementById('fp-count');
  const sel = { type: 'Any', level: 'Any', city: 'Any', src: 'Any' }; let draft = { ...sel }; let limit = 6;
  const match = (r, s, text) => (s.type === 'Any' || r.dataset.type === s.type) && (s.level === 'Any' || r.dataset.level === s.level) && (s.city === 'Any' || r.dataset.city === s.city) && (s.src === 'Any' || r.dataset.src === s.src) && (!text || r.dataset.text.includes(text));
  const active = (s) => Object.entries(s).filter(([, v]) => v !== 'Any');
  const total = (s, text) => (active(s).length || text) ? rows.filter((r) => match(r, s, text)).length : 84;
  const render = () => {
    const text = q.value.trim().toLowerCase(); let n = 0;
    rows.forEach((r) => { const ok = match(r, sel, text); const show = ok && n < limit; if (ok) n++; const was = !r.classList.contains('hid'); r.classList.toggle('hid', !show); if (show && !was) { r.classList.remove('shown'); void r.offsetWidth; r.classList.add('shown'); } });
    empty.classList.toggle('on', n === 0); more.hidden = n <= limit; cnt.textContent = total(sel, text);
    const a = active(sel); fn.hidden = !a.length; fn.textContent = a.length; act.hidden = !a.length;
    act.innerHTML = a.map(([k, v]) => `<button class="achip" type="button" data-f="${k}">${v}<i>×</i></button>`).join('') + (a.length ? '<button class="reset" type="button">Clear all</button>' : '');
  };
  const syncPanel = () => { document.querySelectorAll('.opt2').forEach((b) => b.setAttribute('aria-pressed', String(draft[b.dataset.f] === b.dataset.v))); fpc.textContent = 'Show ' + total(draft, q.value.trim().toLowerCase()) + ' offers'; };
  document.querySelectorAll('.opt2').forEach((b) => b.addEventListener('click', () => { draft[b.dataset.f] = b.dataset.v; syncPanel(); }));
  const fp = document.getElementById('fp');
  if (fp) fp.addEventListener('toggle', (e) => { if (e.newState === 'open') { draft = { ...sel }; syncPanel(); } });
  document.getElementById('fp-apply').addEventListener('click', () => { Object.assign(sel, draft); limit = 6; render(); });
  document.getElementById('fp-reset').addEventListener('click', () => { Object.keys(draft).forEach((k) => { draft[k] = 'Any'; }); syncPanel(); });
  act.addEventListener('click', (e) => { const c = e.target.closest('.achip'); if (c) sel[c.dataset.f] = 'Any'; else if (e.target.closest('.reset')) Object.keys(sel).forEach((k) => { sel[k] = 'Any'; }); else return; render(); });
  document.getElementById('clear2').addEventListener('click', () => { Object.keys(sel).forEach((k) => { sel[k] = 'Any'; }); q.value = ''; render(); });
  q.addEventListener('input', () => { limit = 6; render(); });
  more.addEventListener('click', () => { limit += 6; render(); });
  const data = JSON.parse(document.getElementById('jobdata').textContent), dw = document.getElementById('dw'), dbody = document.getElementById('dw-body');
  const pos = document.getElementById('dw-pos'), dsave = document.getElementById('dw-save'); let cur = null;
  const order = () => app.dataset.view === 'saved' ? [...document.querySelectorAll('#slist .srow')].map((r) => r.dataset.key) : ['b', ...rows.filter((r) => !r.classList.contains('hid')).map((r) => r.querySelector('.stretch').dataset.i)];
  const saveBtn = (i) => i === 'b' ? document.querySelector('.bsave') : rows[+i].querySelector('.save');
  const show = (i, dir) => {
    cur = i; dbody.innerHTML = data.jobs[i].html; dbody.scrollTop = 0;
    const o = order(); pos.textContent = (o.indexOf(i) + 1) + ' of ' + o.length;
    document.getElementById('dw-prev').disabled = o.indexOf(i) <= 0; document.getElementById('dw-next').disabled = o.indexOf(i) >= o.length - 1;
    dsave.setAttribute('aria-pressed', String(saved.has(i)));
    document.querySelectorAll('.row').forEach((r) => r.classList.toggle('sel', r.querySelector('.stretch').dataset.i === i));
    if (dir) { dw.dataset.dir = dir; dw.classList.remove('swap'); void dw.offsetWidth; dw.classList.add('swap'); }
  };
  const open = (i) => { show(i); if (!dw.open) { dw.classList.remove('swap'); dw.showModal(); } };
  const step = (d) => { const o = order(); const k = o.indexOf(cur) + d; if (k >= 0 && k < o.length) show(o[k], d > 0 ? 'next' : 'prev'); };
  document.getElementById('dw-prev').addEventListener('click', () => step(-1));
  document.getElementById('dw-next').addEventListener('click', () => step(1));
  document.getElementById('dw-close').addEventListener('click', () => dw.close());
  dw.addEventListener('click', (e) => { if (e.target === dw) dw.close(); });
  dw.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') step(1); if (e.key === 'ArrowLeft') step(-1); });
  dw.addEventListener('close', () => document.querySelectorAll('.row').forEach((r) => r.classList.remove('sel')));
  dsave.addEventListener('click', () => toggleSave(cur, dsave));
''' + VIEW_JS + TRACK_JS + r'''})();
</script>'''

DCs = open(f'{A}/upload.py').read()
DC = DCs[DCs.index("DC = '''") + 8:DCs.index("'''", DCs.index("DC = '''") + 8)]
LOGO = 'data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%2048%2048%22%20width=%2248%22%20height=%2248%22%20fill=%22none%22%20stroke-linecap=%22round%22%20stroke-linejoin=%22round%22%3E%3Cdefs%3E%3CclipPath%20id=%22jmc%22%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22/%3E%3C/clipPath%3E%3C/defs%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20fill=%22%23CDBFFF%22/%3E%3Cpath%20d=%22M27.5%2020V17Q27.5%2014.5%2030%2014.5H35Q37.5%2014.5%2037.5%2017V20%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FFFFFF%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FF7F45%22%20clip-path=%22url%28%23jmc%29%22/%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Cpath%20d=%22M9.5%2011H19M9.5%2015.5H15%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.4%22/%3E%3Cpath%20d=%22M17%2029.5H44%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.2%22/%3E%3C/svg%3E'
P = f'{S}/nabta-canvas/project'
H = int(sys.argv[2]) if len(sys.argv) > 2 else 1100
PH = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
CL = {'dash': '#matches', 'upload': '#upload', 'apply': '#apply'}
open(f'{P}/Dashboard.dc.html', 'w').write(DC.format(title='JobMatcher your matches', fonts=FONTS, css=CSS, body=body(LOGO, '#home', CL), w=1440, h=H))
open(f'{P}/DashboardFilters.dc.html', 'w').write(DC.format(title='JobMatcher your matches, filters', fonts=FONTS, css=CSS, body=body(LOGO, '#home', CL, show_panel=True), w=1440, h=H + 420))
open(f'{P}/DashboardDetails.dc.html', 'w').write(DC.format(title='JobMatcher your matches, offer open', fonts=FONTS, css=CSS, body=body(LOGO, '#home', CL, show_details=True), w=1440, h=900))
open(f'{P}/Saved.dc.html', 'w').write(DC.format(title='JobMatcher saved offers', fonts=FONTS, css=CSS, body=body(LOGO, '#home', CL, view='saved'), w=1440, h=900))
open(f'{P}/Applied.dc.html', 'w').write(DC.format(title='JobMatcher application tracker', fonts=FONTS, css=CSS, body=body(LOGO, '#home', CL, view='applied'), w=1440, h=1100))
TD_STATIC = 'r5'
open(f'{P}/AppliedSent.dc.html', 'w').write(DC.format(title='JobMatcher application tracker, what you sent', fonts=FONTS, css=CSS + TD_STATIC_CSS, body=body(LOGO, '#home', CL, view='applied'), w=1440, h=900))
TD_STATIC = None
for nm in ('Saved', 'Applied'):
    open(f'{P}/{nm}Phone.dc.html', 'w').write(DC.format(title=f'JobMatcher {nm.lower()}, phone width', fonts=FONTS, css='body{margin:0;background:#F6F5FB}\n', body=f'<div style="width: 390px; background: #F6F5FB;">\n  <dc-import name="{nm}" hint-size="390px,1500px"></dc-import>\n</div>', w=390, h=1500))
open(f'{P}/DashboardPhone.dc.html', 'w').write(DC.format(title='JobMatcher your matches, phone width', fonts=FONTS, css='body{margin:0;background:#F6F5FB}\n',
     body=f'<div style="width: 390px; background: #F6F5FB;">\n  <dc-import name="Dashboard" hint-size="390px,{PH}px"></dc-import>\n</div>', w=390, h=PH))
def page(home, links, title):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
{FONTS}
<style>
{CSS}</style>
</head>
<body>
{body('assets/nabta-mark.svg', home, links)}
{DRAWER_DATA}
{TRACK_DATA}
{JS}
</body>
</html>
'''
open(f'{S}/preview/dashboard.html', 'w').write(page('index.html', {'dash': 'dashboard.html', 'upload': 'upload.html', 'apply': 'apply.html'}, 'JobMatcher Your Matches').replace('href="#apply"', 'href="apply.html"').replace('href="#profile"', 'href="profile.html"'))
full = page('#top', {'dash': '#top', 'upload': '#top', 'apply': '#top'}, 'JobMatcher Your Matches')
head = re.search(r'<head>(.*?)</head>', full, re.S).group(1)
head = re.sub(r'<meta charset="utf-8">|<meta name="viewport"[^>]*>', '', head).strip()
t = re.search(r'<title>.*?</title>', head).group(0); head = head.replace(t, '').strip()
bod = re.search(r'<body>(.*)</body>', full, re.S).group(1).strip()
open(f'{S}/dash-standalone/index.html', 'w').write(t + '\n' + head + '\n' + bod + '\n')
print('ok')
