# Profile v2: centred hero, three tabs on a swipeable sliding track, cleaned content.
import sys, os, re, shutil
S = sys.argv[1]
A = f'{S}/auth'
src = open(f'{A}/auth2.py').read()
exec(src[src.index('def svg('):src.index('def signin(')])
CSS = open(f'{A}/auth2.css').read() + open(f'{A}/dash2.css').read() + open(f'{A}/dash3.css').read() + open(f'{A}/profile.css').read() + open(f'{A}/profile2.css').read()
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
 'lock': I('<rect x="5" y="11" width="14" height="10" rx="2.5"></rect><path d="M8 11V8a4 4 0 0 1 8 0v3"></path>', 17),
 'pin': I('<path d="M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11z"></path><circle cx="12" cy="10" r="2.2"></circle>', 16),
}
def cup(p, w=24, lid=''):
    h = round(37 * p / 100, 1); y = round(50 - h, 1)
    return f'<svg class="cup" viewBox="0 0 48 56" width="{w}" height="{round(w*56/48)}" aria-hidden="true"><rect class="lvl"{lid} x="16" y="{y}" width="16" height="{h}" rx="1.5" fill="#FF7F45"></rect><rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" stroke-width="2.8"></rect><path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" stroke-width="2.8" stroke-linejoin="round"></path></svg>'
X = '×'
def chips(items, add=None, counts=None):
    out = []
    for i, t in enumerate(items):
        n = f'<span class="n" title="{counts[i]} of your matches ask for {t}">{counts[i]}</span>' if counts else ''
        out.append(f'<span class="chip">{t}{n}<button type="button" aria-label="Remove {t}">{X}</button></span>')
    if add:
        out.append(f'<span class="addc">+<input aria-label="{add}" placeholder="{add}"></span>')
    return '<div class="chips">' + ''.join(out) + '</div>'

JOBS = [('Data Analyst Intern', 'Attijariwafa bank', 'Feb to Jul 2025', ['Automated the weekly SQL reports for the retail credit team', 'Built Python jobs that load data for Power BI']),
        ('BI Assistant', 'OCP Group', 'Jul to Sep 2024', ['Cleaned and modelled production data in Python'])]
EDU = [('Master, Big Data and IoT', 'ENSAM Casablanca', '2024 to 2026'), ('Licence, Maths and Computer Science', 'FST Mohammedia', '2021 to 2024'), ('Power BI Data Analyst', 'Microsoft certification', '2025')]
def xp(rows, edu=False):
    li = []
    for r in rows:
        ul = '' if edu else '<ul>' + ''.join(f'<li>{b}</li>' for b in r[3]) + '</ul>'
        li.append(f'<li><div class="xh"><b>{r[0]}</b><span class="when">{r[2]}</span></div><span class="co">{r[1]}</span>{ul}</li>')
    return f'<ol class="xp{" edu" if edu else ""}">' + ''.join(li) + '</ol>'

def pane_profile(links):
    return f'''<section class="tp" data-p="profile" role="tabpanel" aria-label="Profile">
      <div class="g2p">
        <div class="stack2">
          <div class="card"><h2>About <a href="{links['review']}">Edit</a></h2><p class="body">Data analyst with two internships, in banking and in industry. I build Power BI dashboards and data pipelines in Python and SQL, and I am moving into data engineering.</p></div>
          <div class="card"><h2>Experience <a href="{links['review']}">Edit</a></h2>{xp(JOBS)}</div>
          <div class="card"><h2>Education <a href="{links['review']}">Edit</a></h2>{xp(EDU, True)}</div>
        </div>
        <div class="stack2">
          <div class="card"><h2>Your CV</h2><div class="cvf"><span class="ic3">PDF</span><span><b>CV_Salma_El_Idrissi.pdf</b><small>Read on 15 November 2026</small></span></div><div class="btnrow"><a class="pbtn ink" href="{links['upload']}">{IC['upload']}Update</a><button class="pbtn line dlcv" type="button">{IC['dl']}Download</button></div></div>
          <div class="card"><h2>Skills <span class="hint">in your matches</span></h2>{chips(['Python', 'SQL', 'Power BI', 'Spark', 'Excel', 'Tableau', 'Pandas', 'Git'], counts=[61, 58, 34, 22, 19, 11, 9, 8], add='Add a skill')}</div>
          <div class="card" id="links"><h2>Links</h2>
            <div class="lnkrow"><span>LinkedIn</span><b>salma-elidrissi</b></div>
            <div class="lnkrow miss" id="gh"><span>GitHub</span><b>Not added</b><button class="add2" type="button">Add</button><input class="lin2" placeholder="github.com/username" aria-label="GitHub"></div>
            <div class="lnkrow miss"><span>Portfolio</span><b>Not added</b><button class="add2" type="button">Add</button><input class="lin2" placeholder="https://" aria-label="Portfolio"></div>
          </div>
        </div>
      </div>
    </section>'''

def pane_prefs():
    return f'''<section class="tp" data-p="prefs" role="tabpanel" aria-label="Preferences">
      <div class="prefs">
        <div class="card score"><span class="cupv2">{cup(60, 56, ' id="slvl"')}<span id="sval">60</span><small>%</small></span>
          <div><h2>Minimum match score</h2><input class="rng" type="range" id="rng" min="30" max="95" step="5" value="60" aria-label="Minimum match score"><div class="rng-l"><span>More offers</span><span>Only close fits</span></div><p class="effect" id="effect"><b>52 of your 84 matches</b> are at 60% or more.</p>
          <div class="sw2"><span><b>Email me new offers above this score</b></span><label class="tog"><input type="checkbox" checked aria-label="Email me new offers above this score"><i></i></label></div></div></div>
        <div class="card"><h2>Cities</h2>{chips(['Casablanca', 'Rabat'], add='Add a city')}<div class="sw2"><span><b>Remote offers too</b></span><label class="tog"><input type="checkbox" checked aria-label="Remote offers too"><i></i></label></div></div>
        <div class="card"><h2>Roles</h2>{chips(['Data Engineer', 'Data Analyst', 'BI Developer'], add='Add a role')}</div>
        <div class="card"><h2>Industries</h2>{chips(['Banking', 'Telecom', 'Industry'], add='Add an industry')}</div>
      </div>
    </section>'''

def pane_account(links):
    return f'''<section class="tp" data-p="account" role="tabpanel" aria-label="Account">
      <div class="stack2 acc">
        <div class="card"><h2>Account</h2><div class="sform"><div class="fld2"><label for="s-name">Name</label><input id="s-name" value="Salma El Idrissi" autocomplete="name"></div><div class="fld2"><label for="s-loc">City</label><input id="s-loc" value="Casablanca" autocomplete="address-level2"></div><div class="fld2 wide"><label for="s-mail">Email</label><input id="s-mail" value="salma@example.com" readonly><small>You sign in with it, so it cannot be changed here.</small></div></div></div>
        <div class="card pw" id="pw"><div class="pw-h"><span><h2>Password</h2><small>Changed 3 months ago</small></span><button class="pbtn ink" type="button" id="pw-open" aria-expanded="false" aria-controls="pw-f">{IC['lock']}Change password</button></div>
          <div class="pw-f" id="pw-f"><div class="pw-in"><div class="sform"><div class="fld2"><label for="s-p1">New password</label><input id="s-p1" type="password" placeholder="8 or more characters" autocomplete="new-password"></div><div class="fld2"><label for="s-p2">Type it again</label><input id="s-p2" type="password" placeholder="Same password" autocomplete="new-password"></div></div><p class="pw-msg" id="pw-msg" aria-live="polite"></p><div class="btnrow"><button class="pbtn ink" type="button" id="pw-save">Update password</button><button class="pbtn line" type="button" id="pw-cancel">Cancel</button></div></div></div></div>
        <a class="pbtn line signout" href="{links['signin']}">{IC['out']}Sign out</a>
      </div>
    </section>'''

T = [('profile', 'Profile'), ('prefs', 'Preferences'), ('account', 'Account')]
def body(logo, links, tab='profile', static=False):
    nav = [('home', 'Matches', links['dash'] + '#matches', '84'), ('saved', 'Saved', links['dash'] + '#saved', '3'), ('applied', 'Applied', links['dash'] + '#applied', '4')]
    navh = ''.join(f'<a class="nav-i" href="{h}">{IC[i]}<span>{t}</span><span class="b">{b}</span></a>' for i, t, h, b in nav)
    tabs = ''.join(f'<a href="{h}">{IC[i]}{t}</a>' for i, t, h, b in nav)
    tabh = ''.join(f'<button class="ptab" role="tab" type="button" id="tab-{k}" data-t="{k}" aria-selected="{"true" if k == tab else "false"}">{n}</button>' for k, n in T)
    P = {'profile': pane_profile(links), 'prefs': pane_prefs(), 'account': pane_account(links)}
    panes = P[tab] if static else ''.join(P[k] for k, _ in T)
    return f'''<div class="page" id="top">
<div class="app">
  <aside class="side" aria-label="Main">
    <a class="logo" href="{links['dash']}"><img src="{logo}" alt="" width="40" height="40"><span class="display">JobMatcher</span></a>
    {navh}
    <span class="sp"></span>
    <a class="newcv" href="{links['upload']}">{IC['upload']}<span>Upload a new CV</span></a>
    <a class="me on" href="#top" aria-current="page"><span class="s-av done" aria-hidden="true">SE</span><div><b>Salma El Idrissi</b><small>Your profile</small></div>{IC['chev']}</a>
  </aside>
  <main class="main{' static' if static else ''}">
    <div class="mtop"><a class="logo" href="{links['dash']}"><img src="{logo}" alt="" width="36" height="36"><span class="display">JobMatcher</span></a></div>
    <section class="hero" aria-label="Your profile">
      <span class="halo" aria-hidden="true"><i></i><i></i></span>
      <div class="pav"><span class="face" aria-hidden="true">SE</span><button class="cam" type="button" aria-label="Change your photo">{IC['cam']}</button><input type="file" id="photo" accept="image/*" hidden></div>
      <h1 class="display">Salma El Idrissi</h1>
      <p class="hl">Data analyst moving into data engineering<span>{IC['pin']}Casablanca</span></p>
      <div class="hbar">
        <a class="hs comp" href="#links" data-goto="gh">{cup(85, 30, ' id="hlvl"')}<span><b><em data-n="85">85</em>%</b><small id="comp-l">Add GitHub</small></span></a>
        <a class="hs" href="{links['dash']}#applied"><b data-n="11">11</b><small>applied</small></a>
        <a class="hs" href="{links['dash']}#saved"><b data-n="3">3</b><small>saved</small></a>
        <a class="hs" href="{links['dash']}#matches"><b data-n="84">84</b><small>matches</small></a>
      </div>
    </section>
    <div class="ptabs" role="tablist" aria-label="Profile sections"><span class="ind" aria-hidden="true"></span>{tabh}</div>
    <div class="track" id="track">{panes}</div>
  </main>
  <nav class="tabs" aria-label="Main">{tabs}</nav>
</div>
<div class="savebar" id="savebar" role="status"><span>Unsaved changes</span><span class="btnrow"><button class="pbtn lite" type="button" id="undo">Undo</button><button class="pbtn wh" type="button" id="save">Save</button></span></div>
<div class="toast" id="toast" role="status" hidden></div>
</div>'''

JS = r'''<script>
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const toast = document.getElementById('toast'); let tt;
  const say = (t) => { toast.textContent = t; toast.hidden = false; toast.style.animation = 'none'; void toast.offsetWidth; toast.style.animation = ''; clearTimeout(tt); tt = setTimeout(() => { toast.hidden = true; }, 2600); };

  /* tabs: one horizontal track; the pill and the panes follow the scroll, so a swipe and a click feel the same */
  const track = document.getElementById('track'), panes = [...track.children], tabs = [...document.querySelectorAll('.ptab')], ind = document.querySelector('.ptabs .ind'), bar0 = document.querySelector('.ptabs');
  let cur = 0, raf = 0;
  const pos = () => track.scrollLeft / track.clientWidth;
  const place = (x) => {
    x = Math.max(0, Math.min(tabs.length - 1, x));
    const i = Math.floor(x), f = x - i, a = tabs[i], b = tabs[Math.min(i + 1, tabs.length - 1)];
    ind.style.width = (a.offsetWidth + (b.offsetWidth - a.offsetWidth) * f) + 'px';
    ind.style.translate = (a.offsetLeft + (b.offsetLeft - a.offsetLeft) * f) + 'px 0';
    const n = Math.round(x); tabs.forEach((t, k) => t.setAttribute('aria-selected', String(k === n)));
    if (!reduce) panes.forEach((p, k) => { const d = Math.min(1, Math.abs(k - x)); p.style.opacity = 1 - d * .75; p.style.scale = 1 - d * .05; });
  };
  const fitH = (k = cur) => { track.style.height = panes[k].offsetHeight + 'px'; };
  const settle = () => { cur = Math.round(pos()); place(cur); fitH(); panes.forEach((p, k) => { p.inert = k !== cur; }); };
  track.addEventListener('scroll', () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(() => place(pos())); }, { passive: true });
  if ('onscrollend' in window) track.addEventListener('scrollend', settle); else { let st; track.addEventListener('scroll', () => { clearTimeout(st); st = setTimeout(settle, 120); }, { passive: true }); }
  const go = (k) => {
    if (k === cur && Math.abs(pos() - k) < .01) return;
    panes[k].inert = false; fitH(k);
    const top = bar0.getBoundingClientRect().top; if (top < 0 || top > innerHeight * .6) scrollTo({ top: scrollY + top - 8, behavior: reduce ? 'auto' : 'smooth' });
    track.scrollTo({ left: k * track.clientWidth, behavior: reduce ? 'auto' : 'smooth' });
  };
  tabs.forEach((t, k) => t.addEventListener('click', () => go(k)));
  bar0.addEventListener('keydown', (e) => { const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (!d) return; const k = (cur + d + tabs.length) % tabs.length; tabs[k].focus(); go(k); });
  new ResizeObserver(() => fitH()).observe(panes[0]); panes.slice(1).forEach((p) => new ResizeObserver(() => { if (panes[cur] === p) fitH(); }).observe(p));
  addEventListener('resize', () => { track.scrollLeft = cur * track.clientWidth; place(cur); fitH(); });
  document.fonts.ready.then(() => { place(0); fitH(); requestAnimationFrame(() => ind.classList.add('ready')); });
  place(0); fitH(); panes.forEach((p, k) => { p.inert = k !== 0; });

  /* hero numbers count up once */
  if (!reduce) document.querySelectorAll('[data-n]').forEach((el) => { const n = +el.dataset.n, t0 = performance.now() + 350; const step = (t) => { const k = Math.min(1, Math.max(0, (t - t0) / 900)); el.textContent = Math.round(n * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(step); }; el.textContent = '0'; requestAnimationFrame(step); });

  /* "Add your GitHub": go to the Profile tab and open the GitHub field */
  const openLink = (row) => { row.classList.add('editing'); const i = row.querySelector('input'); setTimeout(() => i.focus({ preventScroll: true }), 50); };
  document.querySelectorAll('[data-goto]').forEach((a) => a.addEventListener('click', (e) => { e.preventDefault(); go(0); const row = document.getElementById(a.dataset.goto); setTimeout(() => { row.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' }); openLink(row); }, cur === 0 ? 0 : 450); }));
  document.querySelectorAll('.lnkrow .add2').forEach((b) => b.addEventListener('click', () => openLink(b.parentElement)));
  document.querySelectorAll('.lin2').forEach((i) => {
    const done = () => { const row = i.parentElement, v = i.value.trim(); row.classList.remove('editing'); if (!v) return; row.classList.remove('miss'); row.querySelector('b').textContent = v.replace(/^https?:\/\//, ''); row.querySelector('.add2').textContent = 'Edit'; row.classList.add('just'); say('Link saved');
      if (row.id === 'gh') { document.getElementById('comp-l').textContent = 'complete'; const h = document.getElementById('hlvl'); h.style.transition = 'scale .9s cubic-bezier(.16,1,.3,1)'; h.style.scale = '1 ' + (100 / 85); const em = document.querySelector('.comp em'); em.textContent = '100'; } };
    i.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); done(); } if (e.key === 'Escape') { i.value = ''; i.parentElement.classList.remove('editing'); } });
    i.addEventListener('blur', done);
  });

  /* score: the cup and the effect follow the slider */
  const rng = document.getElementById('rng'), sval = document.getElementById('sval'), slvl = document.getElementById('slvl'), eff = document.getElementById('effect');
  const fit = { 30: 84, 35: 82, 40: 79, 45: 74, 50: 68, 55: 60, 60: 52, 65: 41, 70: 31, 75: 22, 80: 14, 85: 8, 90: 4, 95: 1 };
  const upd = () => { const v = +rng.value; rng.style.setProperty('--f', ((v - 30) / 65 * 100) + '%'); sval.textContent = v; slvl.style.scale = `1 ${v / 60}`; eff.innerHTML = `<b>${fit[v]} of your 84 matches</b> are at ${v}% or more.`; };
  rng.addEventListener('input', upd); upd();
  rng.addEventListener('change', () => say('Saved. Matches start at ' + rng.value + '%'));
  document.querySelectorAll('.prefs .tog input').forEach((c) => c.addEventListener('change', () => say(c.checked ? 'Turned on' : 'Turned off')));

  /* chips */
  const wire = (c) => { const b = c.querySelector('button'); if (b) b.addEventListener('click', () => { c.classList.add('out'); setTimeout(() => c.remove(), 260); }); };
  document.querySelectorAll('.chip').forEach(wire);
  document.querySelectorAll('.addc input').forEach((i) => i.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' || !i.value.trim()) return; e.preventDefault();
    const c = document.createElement('span'); c.className = 'chip new'; c.textContent = i.value.trim();
    const x = document.createElement('button'); x.type = 'button'; x.textContent = '×'; x.setAttribute('aria-label', 'Remove ' + i.value.trim()); c.append(x);
    i.parentElement.before(c); wire(c); i.value = '';
  }));

  /* account: a save bar rises only when something changed */
  const bar = document.getElementById('savebar'), inputs = [...document.querySelectorAll('[data-p="account"] input:not([readonly]):not([type="password"])')];
  const init = new Map(inputs.map((i) => [i, i.value]));
  const sync = () => { const d = inputs.some((i) => i.value !== init.get(i)); bar.classList.toggle('on', d); document.body.classList.toggle('dirty', d); };
  inputs.forEach((i) => i.addEventListener('input', sync));
  document.getElementById('undo').addEventListener('click', () => { inputs.forEach((i) => { i.value = init.get(i); }); sync(); });
  document.getElementById('save').addEventListener('click', () => { inputs.forEach((i) => init.set(i, i.value)); sync(); say('Saved'); });
  /* password: opens in place, checks as you type */
  const pw = document.getElementById('pw'), pwo = document.getElementById('pw-open'), p1 = document.getElementById('s-p1'), p2 = document.getElementById('s-p2'), msg = document.getElementById('pw-msg');
  const pwSet = (open) => { pw.classList.toggle('open', open); pwo.setAttribute('aria-expanded', String(open)); pw.querySelector('.pw-f').inert = !open; if (open) setTimeout(() => p1.focus({ preventScroll: true }), 120); else { p1.value = p2.value = ''; msg.textContent = ''; msg.className = 'pw-msg'; } };
  pwSet(false);
  pwo.addEventListener('click', () => pwSet(true));
  document.getElementById('pw-cancel').addEventListener('click', () => pwSet(false));
  const check = () => { if (!p1.value) return ''; if (p1.value.length < 8) return 'Use 8 or more characters.'; if (p2.value && p2.value !== p1.value) return 'The two passwords are not the same.'; return ''; };
  [p1, p2].forEach((i) => i.addEventListener('input', () => { const m = check(); msg.textContent = m; msg.className = 'pw-msg' + (m ? ' bad' : ''); }));
  document.getElementById('pw-save').addEventListener('click', () => {
    const m = check() || (!p1.value ? 'Type a new password.' : p1.value !== p2.value ? 'Type the same password twice.' : '');
    if (m) { msg.textContent = m; msg.className = 'pw-msg bad'; pw.classList.remove('shake'); void pw.offsetWidth; pw.classList.add('shake'); return; }
    pwSet(false); pw.querySelector('.pw-h small').textContent = 'Changed just now'; say('Password updated');
  });

  document.querySelector('.cam').addEventListener('click', () => document.getElementById('photo').click());
  document.getElementById('photo').addEventListener('change', (e) => { const f = e.target.files[0]; if (!f) return; const r = new FileReader(); r.onload = () => { const face = document.querySelector('.pav .face'); face.textContent = ''; face.style.background = `center / cover url(${r.result})`; say('Photo updated'); }; r.readAsDataURL(f); });
  document.querySelector('.dlcv').addEventListener('click', () => say('Downloads start here in the app'));
})();
</script>'''

DCs = open(f'{A}/upload.py').read()
DC = DCs[DCs.index("DC = '''") + 8:DCs.index("'''", DCs.index("DC = '''") + 8)]
LOGO = 'data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%2048%2048%22%20width=%2248%22%20height=%2248%22%20fill=%22none%22%20stroke-linecap=%22round%22%20stroke-linejoin=%22round%22%3E%3Cdefs%3E%3CclipPath%20id=%22jmc%22%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22/%3E%3C/clipPath%3E%3C/defs%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20fill=%22%23CDBFFF%22/%3E%3Cpath%20d=%22M27.5%2020V17Q27.5%2014.5%2030%2014.5H35Q37.5%2014.5%2037.5%2017V20%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FFFFFF%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FF7F45%22%20clip-path=%22url%28%23jmc%29%22/%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Cpath%20d=%22M9.5%2011H19M9.5%2015.5H15%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.4%22/%3E%3Cpath%20d=%22M17%2029.5H44%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.2%22/%3E%3C/svg%3E'
P = f'{S}/nabta-canvas/project'
CL = {'dash': '#dashboard', 'upload': '#upload', 'review': '#review', 'signin': '#signin'}
for nm, tab, h in (('Profile', 'profile', 1300), ('ProfilePrefs', 'prefs', 1000), ('ProfileSettings', 'account', 1000)):
    open(f'{P}/{nm}.dc.html', 'w').write(DC.format(title=f'JobMatcher profile, {tab}', fonts=FONTS, css=CSS, body=body(LOGO, CL, tab, static=True), w=1440, h=h))
open(f'{P}/ProfilePhone.dc.html', 'w').write(DC.format(title='JobMatcher profile, phone width', fonts=FONTS, css='body{margin:0;background:#F6F5FB}\n',
     body='<div style="width: 390px; background: #F6F5FB;">\n  <dc-import name="Profile" hint-size="390px,2300px"></dc-import>\n</div>', w=390, h=2300))
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
