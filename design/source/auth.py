# Builds the JobMatcher sign-in and sign-up pages: canvas boards (.dc.html) and live preview pages (.html).
import re, sys, os
S = sys.argv[1]
A = f'{S}/auth'
CSS = open(f'{A}/auth.css').read()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Outfit:wght@400;500;600;700&amp;display=swap">'

def svg(inner, w=20, cls='ic', sw=2):
    return f'<svg class="{cls}" viewBox="0 0 24 24" width="{w}" height="{w}" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'
MAIL = svg('<rect x="3" y="5" width="18" height="14" rx="3"></rect><path d="M4 7l8 6 8-6"></path>')
LOCK = svg('<rect x="5" y="10" width="14" height="10" rx="3"></rect><path d="M8 10V7a4 4 0 0 1 8 0v3"></path>')
USER = svg('<circle cx="12" cy="8" r="4"></circle><path d="M4 20c1.5-4 4.5-6 8-6s6.5 2 8 6"></path>')
EYE_ON = svg('<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"></path><circle cx="12" cy="12" r="3"></circle>', cls='e-on')
EYE_OFF = svg('<path d="M3 3l18 18"></path><path d="M10.6 6.1A9.8 9.8 0 0 1 12 6c6.5 0 10 6 10 6a17 17 0 0 1-3.2 3.9M6.6 7.6C3.9 9.4 2 12 2 12s3.5 6 10 6c1.6 0 3-.3 4.3-.9"></path><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"></path>', cls='e-off')
ARR = svg('<path d="M5 12h14M13 6l6 6-6 6"></path>', cls='arr', sw=2.4)
TICK = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path pathLength="1" d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
TICK_W = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
GLOBE = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#1E1C2B" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z"></path></svg>'
PAUSE = '<label class="mp" title="Pause the animation"><input type="checkbox" aria-label="Pause the animation"><svg class="i-pause" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1.2" fill="#1E1C2B"></rect><rect x="14" y="5" width="4" height="14" rx="1.2" fill="#1E1C2B"></rect></svg><svg class="i-play" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="#1E1C2B"></path></svg></label>'
POT = {91: (16.3, 33.7), 76: (21.9, 28.1), 58: (28.5, 21.5)}
def pot(p, w=30):
    y, h = POT[p]
    return f'<svg viewBox="0 0 48 56" width="{w}" height="{round(w*56/48)}" aria-hidden="true"><rect class="lvl" x="16" y="{y}" width="16" height="{h}" rx="1.5" fill="#FF7F45"></rect><rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" stroke-width="2.8"></rect><path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" stroke-width="2.8" stroke-linejoin="round"></path></svg>'

def host(name):
    s = open(f'{S}/peeps-render/auth/host-{name}.svg').read().strip()
    s = s.replace('<svg xmlns="http://www.w3.org/2000/svg" ', '<svg class="host" aria-hidden="true" focusable="false" ', 1)
    return s

def words(text, start=0):
    out = []
    for i, w in enumerate(text.split(' ')):
        out.append(f'<span class="wd" style="--w: {i + start};">{w}</span>')
    return ' '.join(out)

def tags(lst):
    return ''.join(f'<span class="tag{" hit" if h else ""}">{t}</span>' for t, h in lst)

def field(id_, label, icon, typ, auto, ph, d, extra='', after='', right=''):
    lab = f'<span class="lbl"><label for="{id_}">{label}</label>{right}</span>' if right else f'<label class="lbl" for="{id_}">{label}</label>'
    eye = f'<button class="eye" type="button" data-for="{id_}" aria-pressed="false" aria-label="Show password">{EYE_ON}{EYE_OFF}</button>' if typ == 'password' else ''
    return f'''        <div class="fld rise" style="--d: {d};">
          {lab}
          <span class="ctl">{icon}<input id="{id_}" name="{id_}" type="{typ}" autocomplete="{auto}" placeholder="{ph}" required{extra}>{eye}</span>{after}
        </div>
'''

def page(kind, logo, home, other):
    if kind == 'signin':
        head = f'''      <div class="head">
        <h1 class="display atitle">{words('Welcome back.')}</h1>
        <p class="asub rise" style="--d: 0;">Sign in to see your matches and the applications you have prepared.</p>
      </div>'''
        fields = field('email', 'Email', MAIL, 'email', 'email', 'you@example.com', 1) + \
                 field('password', 'Password', LOCK, 'password', 'current-password', 'Your password', 2, right='<a href="#forgot">Forgot password?</a>') + \
                 f'''        <label class="chk rise" style="--d: 3;"><input type="checkbox" id="keep" name="keep" checked><span class="box">{TICK}</span>Keep me signed in on this device</label>
'''
        btn = ('Sign in', 'Signing in…', 'Welcome back')
        switch = f'New to JobMatcher? <a href="{other}">Create an account</a>'
        chip = '<i class="live"></i><span>New offers every day<span class="hide-sm"> from ANAPEC, Jobzyn and LinkedIn</span></span>'
        title = 'Pick up where you left off.'
        aside_label = 'What you find after signing in'
        deck = [('Data Engineer', 'Attijariwafa bank · Casablanca', 91, [('Python', 1), ('Spark', 1), ('Airflow', 1)], '0s'),
                ('Ingénieur BI junior', 'OCP Group · Rabat', 76, [('SQL', 1), ('Power BI', 1), ('SAP BW', 0)], '-6s'),
                ('Stage PFE Data Science', 'inwi · Casablanca', 58, [('Python', 1), ('PyTorch', 0), ('MLflow', 0)], '-3s')]
        visual = '    <div class="deck card-free" aria-hidden="true">\n' + ''.join(
            f'''      <div class="dk card" style="--dd: {dd}; --to: {p};">
        <div class="dk-top"><span class="score">{pot(p)}<span class="display pct"><span class="num">{p}</span></span><small style="font-size: 14px; font-weight: 600;">%</small></span><span style="min-width: 0;"><span class="t1">{t}</span><span class="t2">{c}</span></span></div>
        <div style="display: flex; flex-wrap: wrap; gap: 6px;">{tags(tg)}</div>
      </div>
''' for t, c, p, tg, dd in deck) + '    </div>\n'
        mini = f'<div class="mini card" aria-hidden="true">{pot(91, 22)}<span class="sw" style="font-size: 14px; font-weight: 600;"><span class="sa">91% · Data Engineer</span><span class="sb">76% · Ingénieur BI junior</span><span class="sc">58% · Stage PFE Data Science</span></span></div>'
        name = 'signin'
    else:
        head = f'''      <ol class="steps rise" style="--d: 0; margin: 0; padding: 0; list-style: none;" aria-label="Getting started">
        <li class="st on" aria-current="step"><b>1</b>Account</li><li class="bar" aria-hidden="true"></li><li class="st"><b>2</b>Your CV</li><li class="bar" aria-hidden="true"></li><li class="st"><b>3</b>Matches</li>
      </ol>
      <div class="head">
        <h1 class="display atitle">{words('Create your account.')}</h1>
        <p class="asub rise" style="--d: 0;">Next, you add your CV and see the offers that fit you.</p>
      </div>'''
        fields = field('name', 'Full name', USER, 'text', 'name', 'Your full name', 1) + \
                 field('email', 'Email', MAIL, 'email', 'email', 'you@example.com', 2) + \
                 field('password', 'Password', LOCK, 'password', 'new-password', 'At least 8 characters', 3, extra=' minlength="8" aria-describedby="pw-hint"',
                       after='\n          <div class="meter" data-s="0" aria-hidden="true"><i></i><i></i><i></i><i></i></div>\n          <p class="hint" id="pw-hint">Use 8 or more characters. A number or a symbol makes it stronger.</p>')
        btn = ('Create account', 'Creating your account…', 'Account created')
        switch = f'Already have an account? <a href="{other}">Sign in</a>'
        chip = '<i class="live"></i><span>Three steps<span class="hide-sm">, then your first matches</span></span>'
        title = 'Three steps to your first application.'
        aside_label = 'What happens after you create your account'
        rows = [('Create your account', 'Name, email and a password', ''),
                ('Add your CV', 'A PDF or a photo, up to 10 MB', '<span class="pl-bar"><i></i></span>'),
                ('See your matches', 'Best fit first', '<span class="pl-chips"><span class="tag hit" style="--c: 0;">91%</span><span class="tag" style="--c: 1;">76%</span><span class="tag" style="--c: 2;">58%</span></span>')]
        visual = f'''    <div class="plan card" aria-hidden="true">
      <div class="plan-h"><i class="live"></i><span class="sw"><span class="sa">Setting up your search</span><span class="sb">All set. Your matches are ready.</span></span></div>
''' + ''.join(f'''      <div class="pl" style="--hl: hl{k}; --dot: dot{k}; --ck: ck{k};"><span class="pl-ic">{k + 1}<i class="dot"></i>{TICK_W.replace('<path ', '<path pathLength="1" ')}</span><span class="pl-tx"><span class="t1">{t}</span><span class="t2">{d}</span>{x}</span></div>
''' for k, (t, d, x) in enumerate(rows)) + '    </div>\n'
        mini = '<div class="mini card" aria-hidden="true"><span class="sw" style="font-size: 14px; font-weight: 600;"><span class="sa">Step 1 · Create your account</span><span class="sb">Step 2 · Add your CV</span><span class="sc">Step 3 · See your matches</span></span></div>'
        name = 'signup'
    return f'''<div class="page">
<div class="auth" id="auth">
  <header class="ahdr">
    <a class="logo" href="{home}"><img src="{logo}" alt="" width="40" height="40"><span class="display">JobMatcher</span></a>
    <button class="lang" type="button" aria-label="Language: English. Also available in French and Arabic.">{GLOBE}<span>EN</span></button>
  </header>
  <main class="aform">
{head}
    <form id="authform" action="#" method="post">
{fields}        <button class="go rise" style="--d: 5;" type="submit" data-state="idle"><span class="s-go">{btn[0]}{ARR}</span><span class="s-wait"><i class="spin"></i>{btn[1]}</span><span class="s-ok">{TICK_W}{btn[2]}</span></button>
    </form>
    <p class="switch rise" style="--d: 6;">{switch}</p>
  </main>
  <footer class="afoot"><span>© 2026 JobMatcher</span><a href="{home}">Back to the home page</a></footer>
  <aside class="stage" aria-label="{aside_label}">
    <div class="aura a1" aria-hidden="true"></div><div class="aura a2" aria-hidden="true"></div>
    <div class="st-in">
      <span class="st-chip" style="--d: 0;">{chip}</span>
      <h2 class="display st-title" style="--d: 1;">{title}</h2>
      {mini}
    </div>
{visual}    {host(name)}
    {PAUSE}
  </aside>
</div>
</div>'''

def plan_keyframes():
    out = []
    hl = ['0%,26%{opacity:1}31%,96%{opacity:0}100%{opacity:1}', '0%,30%{opacity:0}34%,56%{opacity:1}61%,100%{opacity:0}', '0%,60%{opacity:0}64%,88%{opacity:1}93%,100%{opacity:0}']
    for k, t in enumerate([20, 52, 80]):
        out.append(f'@keyframes hl{k}{{{hl[k]}}}')
        out.append(f'@keyframes dot{k}{{0%,{t}%{{scale:0}}{t + 5}%,94%{{scale:1}}98%,100%{{scale:0}}}}')
        out.append(f'@keyframes ck{k}{{0%,{t + 3}%{{stroke-dashoffset:1}}{t + 10}%,94%{{stroke-dashoffset:0}}98%,100%{{stroke-dashoffset:1}}}}')
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
    hint.textContent = !v || v.length < 8 ? 'Use 8 or more characters. A number or a symbol makes it stronger.' : s < 3 ? 'Good start. Add a number or a symbol to make it stronger.' : 'Strong password.';
  });
  const form = document.getElementById('authform'), go = form.querySelector('.go');
  form.addEventListener('submit', (e) => {
    e.preventDefault(); if (go.dataset.state !== 'idle') return;
    go.dataset.state = 'wait';
    setTimeout(() => { go.dataset.state = 'ok'; root.classList.add('done'); document.getElementById('demo-note').hidden = false; }, 1300);
  });
  form.addEventListener('invalid', () => { go.classList.remove('shake'); void go.offsetWidth; go.classList.add('shake'); }, true);
})();
</script>'''

css = CSS + plan_keyframes()
os.makedirs(f'{S}/nabta-canvas/project', exist_ok=True)
LOGO_BLOB = 'data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%2048%2048%22%20width=%2248%22%20height=%2248%22%20fill=%22none%22%20stroke-linecap=%22round%22%20stroke-linejoin=%22round%22%3E%3Cdefs%3E%3CclipPath%20id=%22jmc%22%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22/%3E%3C/clipPath%3E%3C/defs%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20fill=%22%23CDBFFF%22/%3E%3Cpath%20d=%22M27.5%2020V17Q27.5%2014.5%2030%2014.5H35Q37.5%2014.5%2037.5%2017V20%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FFFFFF%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FF7F45%22%20clip-path=%22url%28%23jmc%29%22/%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Cpath%20d=%22M9.5%2011H19M9.5%2015.5H15%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.4%22/%3E%3Cpath%20d=%22M17%2029.5H44%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.2%22/%3E%3C/svg%3E'
for kind, Name, title in (('signin', 'SignIn', 'JobMatcher sign in'), ('signup', 'SignUp', 'JobMatcher sign up')):
    other = '#signup' if kind == 'signin' else '#signin'
    body = page(kind, LOGO_BLOB, '#home', other)
    dc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
{css}</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":900}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{}};
  }}
}}
</script>
</body>
</html>
'''
    open(f'{S}/nabta-canvas/project/{Name}.dc.html', 'w').write(dc)
    phone = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}, phone width</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
body{{margin:0;background:#F6F5FB}}
</style>
</helmet>
<div style="width: 390px; background: #F6F5FB;">
  <dc-import name="{Name}" hint-size="390px,960px"></dc-import>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":390,"height":960}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{}};
  }}
}}
</script>
</body>
</html>
'''
    open(f'{S}/nabta-canvas/project/{Name}Phone.dc.html', 'w').write(phone)
    # live preview page (its own document inside the preview artifact)
    pv_other = 'signup.html' if kind == 'signin' else 'signin.html'
    pbody = page(kind, 'assets/nabta-mark.svg', 'index.html', pv_other).replace('href="#forgot"', 'href="#forgot"')
    pbody = pbody.replace('</form>', '</form>\n    <p class="note" id="demo-note" hidden>This is a design preview, so nothing was sent.</p>', 1)
    prev = f'''<!doctype html>
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
'''
    open(f'{S}/preview/{kind}.html', 'w').write(prev)
print('ok')
