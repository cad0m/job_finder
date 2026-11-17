# Profile inside the app shell: header with the cup as completeness, Overview / Experience / Job preferences / Settings.
import sys, os, re, shutil
S = sys.argv[1]
A = f'{S}/auth'
src = open(f'{A}/auth2.py').read()
exec(src[src.index('def svg('):src.index('def signin(')])
CSS = open(f'{A}/auth2.css').read() + open(f'{A}/dash2.css').read() + open(f'{A}/dash3.css').read() + open(f'{A}/profile.css').read()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Outfit:wght@400;500;600;700&amp;display=swap">'
I = lambda d, w=20, c='': svg(d, w=w, cls=c)
IC = {
 'home': I('<path d="M4 11l8-7 8 7v9H4z"></path><path d="M10 20v-5h4v5"></path>'),
 'saved': I('<path d="M7 4h10v16l-5-4-5 4z"></path>'),
 'applied': I('<path d="M4 12l16-8-6 16-3-6z"></path>'),
 'upload': I('<path d="M12 16V4M7 9l5-5 5 5"></path><path d="M5 20h14"></path>', 18),
 'chev': I('<path d="M9 6l6 6-6 6"></path>', 18, 'chev'),
 'cam': I('<path d="M4 8h3l2-3h6l2 3h3v11H4z"></path><circle cx="12" cy="13" r="3.5"></circle>', 18),
 'dl': I('<path d="M12 4v11M7 10l5 5 5-5"></path><path d="M5 20h14"></path>', 17),
 'out': I('<path d="M15 4h4v16h-4"></path><path d="M10 8l-4 4 4 4M6 12h10"></path>', 18),
}
def cup(p, w=24):
    h = round(37 * p / 100, 1); y = round(50 - h, 1)
    return f'<svg class="cup" viewBox="0 0 48 56" width="{w}" height="{round(w*56/48)}" aria-hidden="true"><rect class="lvl" x="16" y="{y}" width="16" height="{h}" rx="1.5" fill="#FF7F45"></rect><rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" stroke-width="2.8"></rect><path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" stroke-width="2.8" stroke-linejoin="round"></path></svg>'
X = '×'
def chips(items, ro=False, add=None, counts=None):
    out = []
    for i, t in enumerate(items):
        n = f'<span class="n">{counts[i]}</span>' if counts else ''
        out.append(f'<span class="chip ro">{t}{n}</span>' if ro else f'<span class="chip">{t}{n}<button type="button" aria-label="Remove {t}">{X}</button></span>')
    if add:
        out.append(f'<span class="addc">+<input aria-label="{add}" placeholder="{add}"></span>')
    return '<div class="chips">' + ''.join(out) + '</div>'

def body(logo, links, tab='overview'):
    nav = [('home', 'Matches', links['dash'] + '#matches', '84'), ('saved', 'Saved', links['dash'] + '#saved', '3'), ('applied', 'Applied', links['dash'] + '#applied', '4')]
    navh = ''.join(f'<a class="nav-i" href="{h}">{IC[i]}<span>{t}</span><span class="b">{b}</span></a>' for i, t, h, b in nav)
    tabs = ''.join(f'<a href="{h}">{IC[i]}{t}</a>' for i, t, h, b in nav)
    T = [('overview', 'Overview'), ('experience', 'Experience'), ('prefs', 'Job preferences'), ('settings', 'Settings')]
    tabh = ''.join(f'<button class="ptab" role="tab" type="button" data-t="{k}" aria-selected="{"true" if k == tab else "false"}">{n}</button>' for k, n in T)
    on = lambda k: ' on' if k == tab else ''
    return f'''<div class="page">
<div class="app">
  <aside class="side" aria-label="Main">
    <a class="logo" href="{links['dash']}"><img src="{logo}" alt="" width="40" height="40"><span class="display">JobMatcher</span></a>
    {navh}
    <span class="sp"></span>
    <a class="newcv" href="{links['upload']}">{IC['upload']}<span>Upload a new CV</span></a>
    <a class="me on" href="#top" aria-current="page"><span class="s-av done" aria-hidden="true">SE</span><div><b>Salma El Idrissi</b><small>Your profile</small></div>{IC['chev']}</a>
  </aside>
  <main class="main">
    <div class="mtop"><a class="logo" href="{links['dash']}"><img src="{logo}" alt="" width="36" height="36"><span class="display">JobMatcher</span></a><span class="s-av done">SE</span></div>
    <section class="phead" aria-label="Your profile">
      <div class="pav"><span class="face" aria-hidden="true">SE</span><button class="cam" type="button" aria-label="Change your photo">{IC['cam']}</button><input type="file" id="photo" accept="image/*" hidden></div>
      <div class="pid">
        <h1 class="display" style="--d: 0;">Salma El Idrissi</h1>
        <p style="--d: 1;">Data analyst moving into data engineering · Casablanca</p>
        <span class="since" style="--d: 2;">Member since November 2026</span>
        <div class="pstats" style="--d: 3;"><a class="pst" href="{links['dash']}#applied"><b>4</b><span>applications</span></a><a class="pst" href="{links['dash']}#saved"><b id="ps-saved">3</b><span>saved offers</span></a><a class="pst" href="{links['dash']}#matches"><b>84</b><span>matches</span></a></div>
      </div>
      <div class="pcomp" style="--d: 4;"><span class="pc-v">{cup(85, 40)}85<small>%</small></span><div><b>Profile</b><p>Add your GitHub to reach 100%. <a href="#" data-goto="settings-links">Add it</a></p></div></div>
    </section>
    <div class="ptabs" role="tablist" aria-label="Profile sections"><span class="ind" aria-hidden="true"></span>{tabh}</div>

    <section class="tp{on('overview')}" data-p="overview" role="tabpanel">
      <div class="g2p">
        <div class="stack2">
          <div class="card" style="--k: 0;"><h3>About <a href="{links['review']}">Edit</a></h3><p class="body">Data analyst with two internships, in banking and in industry. I build Power BI dashboards and data pipelines in Python and SQL, and I am moving into data engineering.</p></div>
          <div class="card" style="--k: 1;"><h3>Skills <span style="letter-spacing: 0; text-transform: none; font-weight: 500;">How many of your matches ask for it</span></h3>{chips(['Python', 'SQL', 'Power BI', 'Spark', 'Excel', 'Tableau', 'Pandas', 'Git'], counts=[61, 58, 34, 22, 19, 11, 9, 8], add='Add a skill')}</div>
          <div class="card" style="--k: 2;"><h3>Certifications</h3>{chips(['Microsoft Power BI Data Analyst'], add='Add one')}</div>
        </div>
        <div class="stack2">
          <div class="card" style="--k: 1;"><h3>Your CV</h3><div class="cvf"><span class="ic3">PDF</span><span><b>CV_Salma_El_Idrissi.pdf</b><small>Read on 15 November 2026</small></span></div><div class="btnrow"><a class="pbtn ink" href="{links['upload']}">{IC['upload']}Update your CV</a><button class="pbtn line dlcv" type="button">{IC['dl']}Download</button></div></div>
          <div class="card" style="--k: 2;"><h3>Links</h3><div class="lnkrow"><span>LinkedIn</span><b>salma-elidrissi</b></div><div class="lnkrow miss"><span>GitHub</span><b>Not added</b><a class="add2" href="#" data-goto="settings-links">Add</a></div><div class="lnkrow miss"><span>Portfolio</span><b>Not added</b><a class="add2" href="#" data-goto="settings-links">Add</a></div></div>
          <div class="card" style="--k: 3;"><h3>Languages</h3>{chips(['Arabic · native', 'French · fluent', 'English · professional'], ro=True)}</div>
        </div>
      </div>
    </section>

    <section class="tp{on('experience')}" data-p="experience" role="tabpanel">
      <div class="g2p">
        <div class="card" style="--k: 0;"><h3>Experience and education <a href="{links['review']}">Edit your details</a></h3>
          <ol class="tl">
            <li><span class="when">Feb to Jul 2025</span><b>Data Analyst Intern</b><span class="co">Attijariwafa bank · Casablanca</span><ul><li>Automated the weekly SQL reports for the retail credit team</li><li>Built Python jobs that load data for Power BI</li></ul></li>
            <li><span class="when">Jul to Sep 2024</span><b>BI Assistant</b><span class="co">OCP Group · Casablanca</span><ul><li>Cleaned and modelled production data in Python</li></ul></li>
            <li class="edu"><span class="when">2024 to 2026</span><b>Master, Big Data and IoT</b><span class="co">ENSAM Casablanca</span></li>
            <li class="edu"><span class="when">2021 to 2024</span><b>Licence, Mathematics and Computer Science</b><span class="co">FST Mohammedia</span></li>
          </ol></div>
        <div class="stack2">
          <div class="card" style="--k: 1;"><h3>Level</h3><p class="body" style="font-size: 26px; font-family: Anton, sans-serif; line-height: 1;">Junior · 1 year</p><p class="body" style="font-size: 14px; color: var(--muted);">Used to pick offers at your level. You can change it in your details.</p></div>
          <div class="card" style="--k: 2;"><h3>New job or degree?</h3><p class="body" style="font-size: 14.5px;">Upload your latest CV and JobMatcher reads it again. You check everything before it is saved.</p><a class="pbtn ink" href="{links['upload']}" style="align-self: flex-start;">{IC['upload']}Update your CV</a></div>
        </div>
      </div>
    </section>

    <section class="tp{on('prefs')}" data-p="prefs" role="tabpanel">
      <div class="prefs">
        <div class="card score" style="--k: 0;"><span class="cupv2">{cup(60, 52).replace('class="lvl"', 'class="lvl" id="slvl"')}<span id="sval">60</span><small>%</small></span>
          <div><h3>Minimum match score</h3><input class="rng" type="range" id="rng" min="30" max="95" step="5" value="60" aria-label="Minimum match score"><div class="rng-l"><span>30%, more offers</span><span>95%, only close fits</span></div><p class="effect" id="effect"><b>52 of your 84 matches</b> are at 60% or more.</p></div></div>
        <div class="card" style="--k: 1;"><h3>Where you want to work</h3>{chips(['Casablanca', 'Rabat'], add='Add a city')}<div class="sw2"><span><b>Open to remote</b><small>Show remote offers too</small></span><label class="tog"><input type="checkbox" checked aria-label="Open to remote"><i></i></label></div></div>
        <div class="card" style="--k: 2;"><h3>Roles you want</h3>{chips(['Data Engineer', 'Data Analyst', 'BI Developer'], add='Add a role')}</div>
        <div class="card" style="--k: 3;"><h3>Industries</h3>{chips(['Banking', 'Telecom', 'Industry'], add='Add an industry')}</div>
        <div class="card" style="--k: 4;"><h3>Alerts</h3><div class="sw2"><span><b>Smart job alerts</b><small>An email when a new offer is above your score</small></span><label class="tog"><input type="checkbox" checked aria-label="Smart job alerts"><i></i></label></div></div>
      </div>
    </section>

    <section class="tp{on('settings')}" data-p="settings" role="tabpanel">
      <div class="stack2">
        <div class="card" style="--k: 0;"><h3>Account</h3><div class="sform"><div class="fld2"><label for="s-name">Display name</label><input id="s-name" value="Salma El Idrissi"></div><div class="fld2"><label for="s-loc">Location</label><input id="s-loc" value="Casablanca, Morocco"></div><div class="fld2"><label for="s-mail">Email</label><input id="s-mail" value="salma@example.com" readonly><small>Used to sign in. It cannot be changed here.</small></div><div class="fld2"><span style="font-size: 13px; font-weight: 600; color: var(--muted);">App language</span><div class="seg6" role="radiogroup" aria-label="App language"><label><input type="radio" name="al" checked>English</label><label><input type="radio" name="al">Français</label><label><input type="radio" name="al">العربية</label></div></div></div></div>
        <div class="card" id="settings-links" style="--k: 1;"><h3>Links on your CV</h3><div class="sform"><div class="fld2"><label for="s-li">LinkedIn</label><input id="s-li" value="linkedin.com/in/salma-elidrissi"></div><div class="fld2"><label for="s-gh">GitHub</label><input id="s-gh" placeholder="github.com/username"></div><div class="fld2"><label for="s-pf">Portfolio</label><input id="s-pf" placeholder="https://"></div></div></div>
        <div class="card" style="--k: 2;"><h3>Password</h3><div class="sform"><div class="fld2"><label for="s-p1">New password</label><input id="s-p1" type="password" placeholder="8 or more characters" autocomplete="new-password"></div><div class="fld2"><label for="s-p2">Confirm it</label><input id="s-p2" type="password" placeholder="Same password" autocomplete="new-password"></div></div></div>
        <div class="card" style="--k: 3;"><div class="leave"><p>Signed in as salma@example.com</p><a class="pbtn line" href="{links['signin']}">{IC['out']}Sign out</a></div></div>
      </div>
      <div class="savebar" id="savebar" role="status"><span>Unsaved changes</span><span class="btnrow"><button class="pbtn lite" type="button" id="undo">Undo</button><button class="pbtn wh" type="button" id="save">Save</button></span></div>
    </section>
    <p class="note">Example profile, to show how it looks.</p>
  </main>
  <nav class="tabs" aria-label="Main">{tabs}</nav>
</div>
<div class="toast" id="toast" role="status" hidden></div>
</div>'''

JS = r'''<script>
(() => {
  const tabs = [...document.querySelectorAll('.ptab')], panes = [...document.querySelectorAll('.tp')], toast = document.getElementById('toast'); let tt;
  const say = (t) => { toast.textContent = t; toast.hidden = false; toast.style.animation = 'none'; void toast.offsetWidth; toast.style.animation = ''; clearTimeout(tt); tt = setTimeout(() => { toast.hidden = true; }, 2800); };
  const order = tabs.map((t) => t.dataset.t);
  let show = (k) => {
    const from = order.indexOf(tabs.find((t) => t.getAttribute('aria-selected') === 'true').dataset.t), to = order.indexOf(k);
    tabs.forEach((t) => t.setAttribute('aria-selected', String(t.dataset.t === k)));
    panes.forEach((p) => { const on = p.dataset.p === k; p.classList.remove('on', 'enter-r', 'enter-l'); if (on) { void p.offsetWidth; p.classList.add('on', to >= from ? 'enter-r' : 'enter-l'); } });
  };
  const ind = document.querySelector('.ptabs .ind');
  const slide = () => { const s = tabs.find((t) => t.getAttribute('aria-selected') === 'true'); ind.style.width = s.offsetWidth + 'px'; ind.style.translate = s.offsetLeft + 'px 0'; s.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'smooth' }); };
  const show0 = show; show = (k) => { show0(k); slide(); };
  slide(); requestAnimationFrame(() => ind.classList.add('ready')); addEventListener('resize', slide); document.fonts.ready.then(slide);
  tabs.forEach((t) => t.addEventListener('click', () => show(t.dataset.t)));
  document.querySelector('.ptabs').addEventListener('keydown', (e) => { const i = order.indexOf(document.activeElement.dataset.t); if (i < 0) return; const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (!d) return; const n = tabs[(i + d + tabs.length) % tabs.length]; n.focus(); show(n.dataset.t); });
  document.querySelectorAll('[data-goto]').forEach((a) => a.addEventListener('click', (e) => { e.preventDefault(); show('settings'); setTimeout(() => { const c = document.getElementById(a.dataset.goto); c.scrollIntoView({ behavior: 'smooth', block: 'center' }); c.querySelector('#s-gh').focus({ preventScroll: true }); }, 350); }));
  /* score: the cup and the effect follow the slider */
  const rng = document.getElementById('rng'), sval = document.getElementById('sval'), slvl = document.getElementById('slvl'), eff = document.getElementById('effect');
  const fit = { 30: 84, 35: 82, 40: 79, 45: 74, 50: 68, 55: 60, 60: 52, 65: 41, 70: 31, 75: 22, 80: 14, 85: 8, 90: 4, 95: 1 };
  const upd = () => { const v = +rng.value; rng.style.setProperty('--f', ((v - 30) / 65 * 100) + '%'); sval.textContent = v; slvl.style.scale = `1 ${v / 60}`; slvl.style.transformBox = 'fill-box'; slvl.style.transformOrigin = '50% 100%'; eff.innerHTML = `<b>${fit[v]} of your 84 matches</b> are at ${v}% or more.`; };
  rng.addEventListener('input', upd); upd();
  rng.addEventListener('change', () => say('Saved. Your matches now start at ' + rng.value + '%.'));
  document.querySelectorAll('.tog input').forEach((c) => c.addEventListener('change', () => say(c.getAttribute('aria-label') + (c.checked ? ' on' : ' off'))));
  /* chips */
  const wire = (c) => { const b = c.querySelector('button'); if (b) b.addEventListener('click', () => { c.classList.add('out'); setTimeout(() => c.remove(), 260); }); };
  document.querySelectorAll('.chip').forEach(wire);
  document.querySelectorAll('.addc input').forEach((i) => i.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' || !i.value.trim()) return; e.preventDefault();
    const c = document.createElement('span'); c.className = 'chip new'; c.textContent = i.value.trim();
    const x = document.createElement('button'); x.type = 'button'; x.textContent = '×'; x.setAttribute('aria-label', 'Remove ' + i.value.trim()); c.append(x);
    i.parentElement.before(c); wire(c); i.value = '';
  }));
  /* settings: a save bar appears when something changes */
  const bar = document.getElementById('savebar'), inputs = [...document.querySelectorAll('[data-p="settings"] input')];
  const init = new Map(inputs.map((i) => [i, i.type === 'radio' ? i.checked : i.value]));
  const dirty = () => inputs.some((i) => (i.type === 'radio' ? i.checked : i.value) !== init.get(i));
  inputs.forEach((i) => i.addEventListener('input', () => bar.classList.toggle('on', dirty())));
  inputs.forEach((i) => i.addEventListener('change', () => bar.classList.toggle('on', dirty())));
  new MutationObserver(() => document.body.classList.toggle('dirty', bar.classList.contains('on'))).observe(bar, { attributes: true });
  document.getElementById('undo').addEventListener('click', () => { inputs.forEach((i) => { if (i.type === 'radio') i.checked = init.get(i); else i.value = init.get(i); }); bar.classList.remove('on'); });
  document.getElementById('save').addEventListener('click', () => {
    const p1 = document.getElementById('s-p1').value, p2 = document.getElementById('s-p2').value;
    if (p1 && p1.length < 8) { say('Use 8 or more characters for the password.'); return; }
    if (p1 !== p2) { say('The two passwords are not the same.'); return; }
    inputs.forEach((i) => init.set(i, i.type === 'radio' ? i.checked : i.value)); bar.classList.remove('on'); say('Saved');
  });
  document.querySelector('.cam').addEventListener('click', () => document.getElementById('photo').click());
  document.getElementById('photo').addEventListener('change', (e) => { const f = e.target.files[0]; if (!f) return; const r = new FileReader(); r.onload = () => { const face = document.querySelector('.pav .face'); face.textContent = ''; face.style.background = `center / cover url(${r.result})`; say('Photo updated'); }; r.readAsDataURL(f); });
  document.querySelector('.dlcv').addEventListener('click', () => say('Downloads start here in the app. This preview has no files.'));
})();
</script>'''

DCs = open(f'{A}/upload.py').read()
DC = DCs[DCs.index("DC = '''") + 8:DCs.index("'''", DCs.index("DC = '''") + 8)]
LOGO = 'data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%2048%2048%22%20width=%2248%22%20height=%2248%22%20fill=%22none%22%20stroke-linecap=%22round%22%20stroke-linejoin=%22round%22%3E%3Cdefs%3E%3CclipPath%20id=%22jmc%22%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22/%3E%3C/clipPath%3E%3C/defs%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20fill=%22%23CDBFFF%22/%3E%3Cpath%20d=%22M27.5%2020V17Q27.5%2014.5%2030%2014.5H35Q37.5%2014.5%2037.5%2017V20%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FFFFFF%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FF7F45%22%20clip-path=%22url%28%23jmc%29%22/%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Cpath%20d=%22M9.5%2011H19M9.5%2015.5H15%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.4%22/%3E%3Cpath%20d=%22M17%2029.5H44%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.2%22/%3E%3C/svg%3E'
P = f'{S}/nabta-canvas/project'
CL = {'dash': '#dashboard', 'upload': '#upload', 'review': '#review', 'signin': '#signin'}
for nm, tab, h in (('Profile', 'overview', 1100), ('ProfilePrefs', 'prefs', 1100), ('ProfileSettings', 'settings', 1200)):
    open(f'{P}/{nm}.dc.html', 'w').write(DC.format(title=f'JobMatcher profile, {tab}', fonts=FONTS, css=CSS, body=body(LOGO, CL, tab), w=1440, h=h))
open(f'{P}/ProfilePhone.dc.html', 'w').write(DC.format(title='JobMatcher profile, phone width', fonts=FONTS, css='body{margin:0;background:#F6F5FB}\n',
     body='<div style="width: 390px; background: #F6F5FB;">\n  <dc-import name="Profile" hint-size="390px,2000px"></dc-import>\n</div>', w=390, h=2000))
def page(links, title):
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
{body('assets/nabta-mark.svg', links)}
{JS}
</body>
</html>
'''
open(f'{S}/preview/profile.html', 'w').write(page({'dash': 'dashboard.html', 'upload': 'upload.html', 'review': 'review.html', 'signin': 'signin.html'}, 'JobMatcher Profile'))
os.makedirs(f'{S}/profile-standalone/assets', exist_ok=True)
shutil.copy(f'{S}/preview/assets/nabta-mark.svg', f'{S}/profile-standalone/assets/nabta-mark.svg')
full = page({'dash': '#top', 'upload': '#top', 'review': '#top', 'signin': '#top'}, 'JobMatcher Profile').replace('href="#top#', 'href="#')
head = re.search(r'<head>(.*?)</head>', full, re.S).group(1)
head = re.sub(r'<meta charset="utf-8">|<meta name="viewport"[^>]*>', '', head).strip()
t = re.search(r'<title>.*?</title>', head).group(0); head = head.replace(t, '').strip()
bod = re.search(r'<body>(.*)</body>', full, re.S).group(1).strip()
open(f'{S}/profile-standalone/index.html', 'w').write(t + '\n' + head + '\n' + bod + '\n')
print('ok')
