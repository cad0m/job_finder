# JobMatcher auth pages v2: sign in (form + a CV being read by a magnifying glass) and sign up (the form is the top of a CV).
# Usage: auth2.py SCRATCH [coords.json]   coords = measured centres of the three highlighted skills inside .scan
import sys, os, json
S = sys.argv[1]
A = f'{S}/auth'
sys.path.insert(0, A)
import importlib.util
spec = importlib.util.spec_from_file_location('v1', f'{A}/auth.py.bak') if False else None
CSS = open(f'{A}/auth2.css').read()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Outfit:wght@400;500;600;700&amp;display=swap">'
coords = json.load(open(sys.argv[2])) if len(sys.argv) > 2 and os.path.exists(sys.argv[2]) else [[90, 330], [160, 330], [240, 330]]

def svg(inner, w=20, cls='ic', sw=2):
    return f'<svg class="{cls}" viewBox="0 0 24 24" width="{w}" height="{w}" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'
MAIL = svg('<rect x="3" y="5" width="18" height="14" rx="3"></rect><path d="M4 7l8 6 8-6"></path>')
LOCK = svg('<rect x="5" y="10" width="14" height="10" rx="3"></rect><path d="M8 10V7a4 4 0 0 1 8 0v3"></path>')
USER = svg('<circle cx="12" cy="8" r="4"></circle><path d="M4 20c1.5-4 4.5-6 8-6s6.5 2 8 6"></path>', w=30, cls='u')
EYE_ON = svg('<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"></path><circle cx="12" cy="12" r="3"></circle>', cls='e-on')
EYE_OFF = svg('<path d="M3 3l18 18"></path><path d="M10.6 6.1A9.8 9.8 0 0 1 12 6c6.5 0 10 6 10 6a17 17 0 0 1-3.2 3.9M6.6 7.6C3.9 9.4 2 12 2 12s3.5 6 10 6c1.6 0 3-.3 4.3-.9"></path><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"></path>', cls='e-off')
ARR = svg('<path d="M5 12h14M13 6l6 6-6 6"></path>', cls='arr', sw=2.4)
UP = svg('<path d="M12 16V4M7 9l5-5 5 5"></path><path d="M5 20h14"></path>', w=18, cls='')
TARGET = svg('<circle cx="12" cy="12" r="8"></circle><circle cx="12" cy="12" r="3"></circle>', w=18, cls='')
DOC = svg('<path d="M7 3h7l4 4v14H7z"></path><path d="M14 3v4h4M10 12h5M10 16h5"></path>', w=18, cls='')
TICK = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path pathLength="1" d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
TICK_W = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
GLOBE = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#1E1C2B" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z"></path></svg>'
PAUSE = '<label class="mp" title="Pause the animation"><input type="checkbox" aria-label="Pause the animation"><svg class="i-pause" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1.2" fill="#1E1C2B"></rect><rect x="14" y="5" width="4" height="14" rx="1.2" fill="#1E1C2B"></rect></svg><svg class="i-play" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="#1E1C2B"></path></svg></label>'

def host(name, extra=''):
    s = open(f'{S}/peeps-render/auth/host-{name}.svg').read().strip()
    return s.replace('<svg xmlns="http://www.w3.org/2000/svg" ', f'<svg class="host{extra}" aria-hidden="true" focusable="false" ', 1)
def words(text):
    return ' '.join(f'<span class="wd" style="--w: {i};">{w}</span>' for i, w in enumerate(text.split(' ')))
def eye(id_):
    return f'<button class="eye" type="button" data-for="{id_}" aria-pressed="false" aria-label="Show password">{EYE_ON}{EYE_OFF}</button>'
def header(logo, home):
    return f'''  <header class="ahdr">
    <a class="logo" href="{home}"><img src="{logo}" alt="" width="40" height="40"><span class="display">JobMatcher</span></a>
    <button class="lang" type="button" aria-label="Language: English. Also available in French and Arabic.">{GLOBE}<span>EN</span></button>
  </header>'''
def go(a, b, c, d):
    return f'<button class="go rise" style="--d: {d};" type="submit" data-state="idle"><span class="s-go">{a}{ARR}</span><span class="s-wait"><i class="spin"></i>{b}</span><span class="s-ok">{TICK_W}{c}</span></button>'

def signin(logo, home, other, avatar):
    finds = [('Data Analyst', 'Attijariwafa bank · Casablanca', 91), ('BI Developer', 'OCP Group · Rabat', 84), ('Stage PFE Data', 'inwi · Casablanca', 76)]
    skills = [('Python', 0), ('Excel', None), ('SQL', 1), ('Tableau', None), ('Power BI', 2), ('Arabic', None), ('French', None)]
    sk = ''.join(f'<span class="sk"{f" data-k={chr(34)}{k}{chr(34)} style={chr(34)}--hit: hit{k}; --dot: dot{k};{chr(34)}" if k is not None else ""}>{t}</span>' for t, k in skills)
    return f'''<div class="page">
<div class="auth signin" id="auth">
{header(logo, home)}
  <main class="aform">
    <div class="head">
      <h1 class="display atitle">{words('Welcome back.')}</h1>
      <p class="asub rise" style="--d: 0;">Sign in to see your matches and the applications you have prepared.</p>
    </div>
    <div class="fwrap">
      <p class="mchip" aria-hidden="true"><span class="mc-ic"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"></circle><path d="M15.5 15.5L20 20"></path></svg></span><span class="mc-sk">Python</span><span class="mc-ar">→</span><span><b>Data Analyst</b> · 91%</span></p>
      {host('signin', ' host-m')}
    <form id="authform" action="#" method="post">
      <div class="fld rise" style="--d: 1;">
        <label class="lbl" for="email">Email</label>
        <span class="ctl">{MAIL}<input id="email" name="email" type="email" autocomplete="email" placeholder="you@example.com" required></span>
      </div>
      <div class="fld rise" style="--d: 2;">
        <span class="lbl"><label for="password">Password</label><a href="#forgot">Forgot password?</a></span>
        <span class="ctl">{LOCK}<input id="password" name="password" type="password" autocomplete="current-password" placeholder="Your password" required>{eye('password')}</span>
      </div>
      <label class="chk rise" style="--d: 3;"><input type="checkbox" id="keep" name="keep" checked><span class="box">{TICK}</span>Keep me signed in on this device</label>
      {go('Sign in', 'Signing in…', 'Welcome back', 4)}
    </form>
    </div>
    <p class="switch rise" style="--d: 5;">New to JobMatcher? <a href="{other}">Create an account</a></p>
  </main>
  <footer class="afoot"><span>© 2026 JobMatcher</span><a href="{home}">Back to the home page</a></footer>
  <aside class="stage" aria-label="How JobMatcher reads your CV">
    <div class="aura a1" aria-hidden="true"></div><div class="aura a2" aria-hidden="true"></div>
    <div class="st-in">
      <span class="st-chip"><i class="live"></i><span>New offers every day<span class="hide-sm"> from ANAPEC, Jobzyn and LinkedIn</span></span></span>
      <h2 class="display st-title">Your CV in. The right jobs out.</h2>
    </div>
    <div class="scan" aria-hidden="true">
      <div class="cv">
        <div class="cv-top"><span class="cv-av"><img src="{avatar}" alt=""></span><span><span class="cv-name">Salma El Idrissi</span><span class="cv-role">Data analyst · Casablanca</span></span></div>
        <span class="cv-sec">Experience</span>
        <i class="ln" style="--w: 92%;"></i><i class="ln" style="--w: 76%;"></i><i class="ln" style="--w: 84%;"></i>
        <span class="cv-sec">Skills</span>
        <div class="cv-skills">{sk}</div>
        <span class="cv-sec">Education</span>
        <i class="ln" style="--w: 70%;"></i><i class="ln" style="--w: 52%;"></i>
      </div>
      <div class="finds">
''' + ''.join(f'''        <div class="find{' top' if i == 0 else ''}" style="--pop: pop{i};"><span class="pct">{p}<small>%</small></span><span style="min-width: 0;"><span class="t1">{t}</span><span class="t2">{c}</span></span></div>
''' for i, (t, c, p) in enumerate(finds)) + f'''      </div>
      <div class="loupe"><i class="lens"></i><i class="handle"></i></div>
    </div>
    {host('signin')}
    {PAUSE}
  </aside>
</div>
</div>'''

def signup(logo, home, other):
    return f'''<div class="page">
<div class="auth signup" id="auth">
{header(logo, home)}
  <section class="intro">
    <ol class="steps rise" style="--d: 0;" aria-label="Getting started">
      <li class="st on" aria-current="step"><b>1</b>Account</li><li class="bar" aria-hidden="true"></li><li class="st"><b>2</b>Your CV</li><li class="bar" aria-hidden="true"></li><li class="st"><b>3</b>Matches</li>
    </ol>
    <div class="head">
      <h1 class="display atitle">{words('Create your account.')}</h1>
      <p class="asub rise" style="--d: 1;">Your account is the top of your CV. Fill it in here, then add the rest from your CV file.</p>
    </div>
    <ul class="next rise" style="--d: 2;">
      <li><span class="ni">{UP}</span>Upload a PDF or a photo of your CV</li>
      <li><span class="ni">{TARGET}</span>See the offers that fit you, best first</li>
      <li><span class="ni">{DOC}</span>Get a tailored CV, cover letter and email</li>
    </ul>
  </section>
  <footer class="afoot"><span>© 2026 JobMatcher</span><a href="{home}">Back to the home page</a></footer>
  <div class="desk">
    <div class="aura a1" aria-hidden="true"></div><div class="aura a2" aria-hidden="true"></div>
    <div class="fwrap">
    {host('signup', ' host-m')}
    <form class="sheet" id="authform" action="#" method="post">
      <div class="kicker"><span>Curriculum vitae</span></div>
      <div class="stamp" aria-hidden="true">Ready<br>for<br>matches</div>
      <div class="s-head">
        <span class="s-av" id="av" aria-hidden="true">{USER}</span>
        <div class="s-name"><label for="name">Full name</label><input id="name" name="name" type="text" autocomplete="name" placeholder="Your full name" required></div>
      </div>
      <div class="s-sec">
        <span class="sl">Contact</span>
        <div class="fld"><label class="lbl" for="email">Email</label><span class="ctl">{MAIL}<input id="email" name="email" type="email" autocomplete="email" placeholder="you@example.com" required></span></div>
      </div>
      <div class="s-sec">
        <span class="sl">Private</span>
        <div class="fld">
          <label class="lbl" for="password">Password</label>
          <span class="ctl">{LOCK}<input id="password" name="password" type="password" autocomplete="new-password" placeholder="At least 8 characters" required minlength="8" aria-describedby="pw-hint">{eye('password')}</span>
          <div class="meter" data-s="0" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
          <p class="hint" id="pw-hint">8 or more characters. A number or a symbol makes it stronger.</p>
        </div>
      </div>
      <p class="next-m">Experience and skills come from your CV in step 2.</p>
      <div class="s-sec ghost" aria-hidden="true">
        <span class="sl">Experience</span>
        <div style="display: flex; flex-direction: column; gap: 7px; padding-top: 4px;"><i class="ln" style="--w: 88%;"></i><i class="ln" style="--w: 64%;"></i><span class="gnote">Filled in from your CV in step 2.</span></div>
      </div>
      <div class="s-sec ghost" aria-hidden="true" style="border-bottom: 0;">
        <span class="sl">Skills</span>
        <div style="display: flex; flex-wrap: wrap; gap: 6px;"><i class="gpill" style="width: 64px;"></i><i class="gpill" style="width: 48px;"></i><i class="gpill" style="width: 80px;"></i><i class="gpill" style="width: 56px;"></i></div>
      </div>
      <div class="s-foot">
        {go('Create account', 'Creating your account…', 'Account created', 0).replace(' rise', '')}
        <p class="switch">Already have an account? <a href="{other}">Sign in</a></p>
      </div>
    </form>
    </div>
    {host('signup')}
    {PAUSE}
  </div>
</div>
</div>'''

def keyframes():
    (x0, y0), out = (coords[3] if len(coords) > 3 else [330, 470]), []
    p = coords[:3]
    out.append('.loupe{--x0:%dpx;--y0:%dpx}' % (x0, y0))
    out.append('@keyframes glide{0%%{translate:%dpx %dpx}8%%,30%%{translate:%dpx %dpx}38%%,58%%{translate:%dpx %dpx}66%%,86%%{translate:%dpx %dpx}94%%,100%%{translate:%dpx %dpx}}' % (x0, y0, *p[0], *p[1], *p[2], x0, y0))
    for k, a in enumerate([10, 38, 66]):
        out.append(f'@keyframes hit{k}{{0%,{a}%{{opacity:0}}{a + 3}%,88%{{opacity:1}}94%,100%{{opacity:0}}}}')
        out.append(f'@keyframes dot{k}{{0%,{a}%{{scale:0}}{a + 4}%,88%{{scale:1}}94%,100%{{scale:0}}}}')
        out.append(f'@keyframes pop{k}{{0%,{a + 3}%{{opacity:0;translate:-28px 0;scale:.86}}{a + 9}%,88%{{opacity:1;translate:0 0;scale:1}}94%,100%{{opacity:0;translate:18px 0;scale:.96}}}}')
    return '\n'.join(out) + '\n'

JS = '''<script>
(() => {
  const root = document.getElementById('auth');
  document.querySelectorAll('.eye').forEach((b) => b.addEventListener('click', () => {
    const i = document.getElementById(b.dataset.for); const show = i.type === 'password';
    i.type = show ? 'text' : 'password'; b.setAttribute('aria-pressed', String(show));
    b.setAttribute('aria-label', show ? 'Hide password' : 'Show password'); i.focus();
  }));
  const pw = document.getElementById('password'), meter = document.querySelector('.meter'), hint = document.getElementById('pw-hint');
  if (meter && pw) pw.addEventListener('input', () => {
    const v = pw.value; let s = 0;
    if (v.length >= 8) s++; if (/[0-9]/.test(v)) s++; if (/[^A-Za-z0-9]/.test(v)) s++; if (v.length >= 12) s++;
    if (v.length < 8) s = Math.min(s, 1); if (!v) s = 0;
    meter.dataset.s = String(s);
    hint.textContent = !v || v.length < 8 ? '8 or more characters. A number or a symbol makes it stronger.' : s < 3 ? 'Good start. Add a number or a symbol to make it stronger.' : 'Strong password.';
  });
  const name = document.getElementById('name'), av = document.getElementById('av');
  if (name && av) { const icon = av.innerHTML; name.addEventListener('input', () => {
    const ini = name.value.trim().split(/\\s+/).filter(Boolean).slice(0, 2).map((w) => w[0].toUpperCase()).join('');
    if (ini) { av.textContent = ini; av.classList.add('has'); } else { av.innerHTML = icon; av.classList.remove('has'); }
  }); }
  const form = document.getElementById('authform'), go = form.querySelector('.go');
  form.addEventListener('submit', (e) => {
    e.preventDefault(); if (go.dataset.state !== 'idle') return;
    go.dataset.state = 'wait';
    setTimeout(() => { go.dataset.state = 'ok'; root.classList.add('done'); document.getElementById('demo-note').hidden = false; if (document.getElementById('name')) setTimeout(() => { location.href = 'upload.html'; }, 1500); }, 1300);
  });
  form.addEventListener('invalid', () => { go.classList.remove('shake'); void go.offsetWidth; go.classList.add('shake'); }, true);
})();
</script>'''

css = CSS + keyframes()
LOGO_BLOB = 'data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%2048%2048%22%20width=%2248%22%20height=%2248%22%20fill=%22none%22%20stroke-linecap=%22round%22%20stroke-linejoin=%22round%22%3E%3Cdefs%3E%3CclipPath%20id=%22jmc%22%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22/%3E%3C/clipPath%3E%3C/defs%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20fill=%22%23CDBFFF%22/%3E%3Cpath%20d=%22M27.5%2020V17Q27.5%2014.5%2030%2014.5H35Q37.5%2014.5%2037.5%2017V20%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FFFFFF%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FF7F45%22%20clip-path=%22url%28%23jmc%29%22/%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Cpath%20d=%22M9.5%2011H19M9.5%2015.5H15%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.4%22/%3E%3Cpath%20d=%22M17%2029.5H44%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.2%22/%3E%3C/svg%3E'
AV_BLOB = '/_blob/508ad66c55ac8d5772119087ddc19fb2'
DC = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{fonts}
<style>
{css}</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{}};
  }}
}}
</script>
</body>
</html>
'''
for kind, Name, title, ph in (('signin', 'SignIn', 'JobMatcher sign in', 860), ('signup', 'SignUp', 'JobMatcher sign up', 1110)):
    other = '#signup' if kind == 'signin' else '#signin'
    body = signin(LOGO_BLOB, '#home', other, AV_BLOB) if kind == 'signin' else signup(LOGO_BLOB, '#home', other)
    open(f'{S}/nabta-canvas/project/{Name}.dc.html', 'w').write(DC.format(title=title, fonts=FONTS, css=css, body=body, w=1440, h=900))
    phone = f'<div style="width: 390px; background: #F6F5FB;">\n  <dc-import name="{Name}" hint-size="390px,{ph}px"></dc-import>\n</div>'
    open(f'{S}/nabta-canvas/project/{Name}Phone.dc.html', 'w').write(DC.format(title=title + ', phone width', fonts=FONTS, css='body{margin:0;background:#F6F5FB}\n', body=phone, w=390, h=ph))
    pv_other = 'signup.html' if kind == 'signin' else 'signin.html'
    pbody = signin('assets/nabta-mark.svg', 'index.html', pv_other, 'assets/peep-cv-match.svg') if kind == 'signin' else signup('assets/nabta-mark.svg', 'index.html', pv_other)
    note = '<p class="note" id="demo-note" hidden>This is a design preview, so nothing was sent.</p>'
    pbody = pbody.replace('</form>\n    </div>\n    <p class="switch rise"', '</form>\n    </div>\n    ' + note + '\n    <p class="switch rise"', 1) if kind == 'signin' else pbody.replace('<p class="switch">', note + '\n        <p class="switch">', 1)
    assert 'demo-note' in pbody
    open(f'{S}/preview/{kind}.html', 'w').write(f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title.replace('JobMatcher s', 'JobMatcher S')}</title>
{FONTS}
<style>
{css}</style>
</head>
<body>
{pbody}
{JS}
</body>
</html>
''')
print('ok', coords)
