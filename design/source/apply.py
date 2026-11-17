# Prepare application: setup, writing, ready. Builds canvas boards, the main preview page and the standalone preview.
import sys, os, re, shutil
S = sys.argv[1]
A = f'{S}/auth'
src = open(f'{A}/auth2.py').read()
exec(src[src.index('def svg('):src.index('def signin(')])
CSS = open(f'{A}/auth2.css').read() + open(f'{A}/apply.css').read()
CSS = CSS.replace('.sheet3{animation:dealt .9s var(--out) both}', '.sheet3{animation:dealt .9s var(--out) backwards}')
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Outfit:wght@400;500;600;700&amp;display=swap">'
TKS = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
BACK = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"></path></svg>'
DL = '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5"></path><path d="M5 20h14"></path></svg>'
EXT = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5H5V6h5"></path></svg>'
COPY = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2"></rect><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"></path></svg>'
MAIL = '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#1E1C2B" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3"></rect><path d="M4 7l8 6 8-6"></path></svg>'
def cup(p, w=24):
    h = round(37 * p / 100, 1); y = round(50 - h, 1)
    return f'<svg class="cup" viewBox="0 0 48 56" width="{w}" height="{round(w*56/48)}" aria-hidden="true"><rect class="lvl" x="16" y="{y}" width="16" height="{h}" rx="1.5" fill="#FF7F45"></rect><rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" stroke-width="2.8"></rect><path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" stroke-width="2.8" stroke-linejoin="round"></path></svg>'

def cvdoc(t, marks=False):
    m = (lambda x: f'<span class="mark">{x}</span>') if marks else (lambda x: x)
    return f'''<div class="cvd {t}" aria-hidden="true"><div class="in">
      <div class="s h" style="grid-area:h"><span class="nm">Salma El Idrissi</span><span class="hl">Data Engineer</span></div>
      <div class="s ct" style="grid-area:ct">salma@example.com<br>+212 6 12 34 56 78<br>Casablanca, Morocco<br>linkedin.com/in/salma-elidrissi</div>
      <div class="s sum" style="grid-area:sum"><h6>Profile</h6><p>Data analyst moving into data engineering. I build batch pipelines in {m("Python")} and {m("Spark")} and model data in {m("SQL")} for reporting teams.</p></div>
      <div class="s exp" style="grid-area:exp"><h6>Experience</h6>
        <div class="j"><b>Data Analyst Intern<span>Feb to Jul 2025</span></b><em>Attijariwafa bank, Casablanca</em><ul><li>Automated the weekly {m("SQL")} reports for the credit team</li><li>Built {m("Python")} jobs that load data for Power BI</li></ul></div>
        <div class="j"><b>BI Assistant<span>Jul to Sep 2024</span></b><em>OCP Group, Casablanca</em><ul><li>Cleaned and modelled production data in {m("Python")}</li></ul></div></div>
      <div class="s edu" style="grid-area:edu"><h6>Education</h6><p><b>Master, Big Data and IoT</b><br>ENSAM Casablanca, 2024 to 2026</p><p><b>Licence, Maths and CS</b><br>FST Mohammedia, 2021 to 2024</p></div>
      <div class="s skl" style="grid-area:skl"><h6>Skills</h6><p>{m("Python")} · {m("Spark")} · {m("SQL")} · Power BI · Pandas · Git · Excel</p></div>
      <div class="s lng" style="grid-area:lng"><h6>Languages</h6><p>Arabic, native<br>French, fluent<br>English, professional</p></div>
      <div class="s side" style="grid-area:side"></div>
    </div></div>'''

LETTER = '''<div class="ltr" aria-hidden="true"><div class="lin">
      <div class="from"><b>Salma El Idrissi</b><span>salma@example.com · +212 6 12 34 56 78 · Casablanca</span></div>
      <p>Casablanca, 17 November 2026</p>
      <p>Attijariwafa bank<br>Data platform team</p>
      <p>Dear hiring team,</p>
      <p>I am applying for the Data Engineer role on your data platform team. During my internship at Attijariwafa bank I automated the weekly SQL reports for the credit team and built Python jobs that load data for Power BI, so I already know how much the risk and marketing teams rely on clean, on-time data.</p>
      <p>I build batch pipelines in Python and Spark and model data in SQL. I have not used Airflow in production yet; I have scheduled jobs with cron and I am keen to learn it with your team.</p>
      <p>I would be glad to talk about how I can help move your core banking data into the analytics lake.</p>
      <p>Kind regards,<br>Salma El Idrissi</p>
    </div></div>'''
SUBJECT = 'Application for the Data Engineer role, Salma El Idrissi'
BODY = '''Hello,

I am applying for the Data Engineer role on your data platform team. You will find my CV and a cover letter attached.

During my internship at Attijariwafa bank I automated SQL reporting and built Python jobs for Power BI. I would be glad to bring that experience to your team.

Thank you for your time,
Salma El Idrissi
+212 6 12 34 56 78'''

TPLS = [('t1', 'Classic', 'One column'), ('t2', 'Clean', 'Two columns'), ('t3', 'Sidebar', 'Dark side'), ('t4', 'Serif', 'Formal'), ('t5', 'Soft', 'Warm side')]

def sheet(cls, tag, n_lines, chips=False):
    lines = [('t', None)] + [(None, w) for w in [92, 78, 86, 64, None, 90, 72, 84, 58, None, 80, 70, 88][:n_lines]]
    out = []
    k = 0
    for c, w in lines:
        if c == 't': out.append('<i class="t"></i>')
        elif w is None: out.append('<i class="sp"></i>')
        else:
            out.append(f'<i style="--w: {w}%; position: relative;"><i class="wr" style="--n: {k}; position: absolute; inset: 0; width: 100%;"></i></i>'); k += 1
    ch = '<span class="chips3"><span style="--n: 0;">Python</span><span style="--n: 1;">Spark</span><span style="--n: 2;">SQL</span></span>' if chips else ''
    return f'<div class="sheet3 {cls}"><span class="tg">{tag}</span>{"".join(out[:3])}{ch}{"".join(out[3:])}<span class="pdf">PDF</span></div>'

def body(logo, home, links, step='setup', tpl='t3'):
    tcards = ''.join(f'''<label class="tpl" style="--k: {i};"><input type="radio" name="tpl" value="{t}"{" checked" if t == tpl else ""}><span class="frame">{"<span class=" + chr(34) + "rec" + chr(34) + ">Recommended</span>" if t == "t3" else ""}{cvdoc(t)}<span class="chk2">{TKS}</span></span><span class="nm2">{n}<small>{d}</small></span></label>''' for i, (t, n, d) in enumerate(TPLS))
    on = {'setup': 1, 'writing': 2, 'ready': 3}[step]
    def st(i, label):
        cls = 'on' if i == on else ('ok' if i < on else '')
        return f'<li class="{cls}" data-s="{i}"><b>{"✓" if i < on else i}</b><span>{label}</span></li>'
    return f'''<div class="page">
<div class="studio" id="studio" data-step="{step}">
  <header class="stop">
    <a class="back" href="{links['dash']}">{BACK}<span>Back to your matches</span></a>
    <ol class="psteps" aria-label="Progress">{st(1, 'Set up')}{st(2, 'Writing')}{st(3, 'Ready')}</ol>
    <div class="ochip"><span class="logo-c l1" aria-hidden="true">AB</span><span><b>Data Engineer</b><span>Attijariwafa bank</span></span><span class="cupv">{cup(91, 18)}91<small>%</small></span></div>
  </header>
  <main class="stage-w">
    <section class="pane p-setup" aria-labelledby="h-setup">
      <div class="setup">
        <div>
          <div class="sh"><h1 class="display" id="h-setup" style="--d: 0;">Prepare your application.</h1><p style="--d: 1;">Pick a design for your CV. JobMatcher writes the CV, a cover letter and an email for this offer.</p></div>
          <div class="blk2" style="--d: 2;"><h2>CV design <span>All five fit on one page</span></h2><div class="tpls" role="radiogroup" aria-label="CV design">{tcards}</div></div>
          <div class="blk2" style="--d: 3;"><h2>Links on your CV <span>From your profile</span></h2>
            <div class="lnks">
              <div class="lk"><label for="ln-li">LinkedIn</label><div class="pre2"><span>linkedin.com/in/</span><input id="ln-li" value="salma-elidrissi"></div></div>
              <div class="lk"><label for="ln-gh">GitHub</label><div class="pre2"><span>github.com/</span><input id="ln-gh" placeholder="username"></div></div>
              <div class="lk"><label for="ln-pf">Portfolio</label><div class="pre2"><span>https://</span><input id="ln-pf" placeholder="yoursite.ma"></div></div>
            </div></div>
        </div>
        <aside class="forit" style="--d: 2;" aria-label="For this offer">
          <span class="k">For this offer</span>
          <div class="fo-h"><div><h3>Data Engineer</h3><p>Attijariwafa bank · Casablanca</p></div><span class="fo-cup">{cup(91, 34)}91<small>%</small></span></div>
          <div class="hl2"><b>JobMatcher puts these first</b><span class="chips2"><span class="c2 hit">Python</span><span class="c2 hit">Spark</span><span class="c2 hit">SQL</span></span><p class="honest"><b>Airflow is not on your CV</b>, so it will not be added. Your letter says you are keen to learn it.</p></div>
          <ul class="get"><li><i>CV</i>A CV tailored to this offer</li><li><i>CL</i>A cover letter to the company</li><li><i>EM</i>An email to send with both</li></ul>
          <button class="go write" type="button"><span class="s-go">Write my application{ARR}</span></button>
        </aside>
      </div>
    </section>
    <section class="pane p-writing" aria-labelledby="h-writing" aria-live="polite">
      <div class="writing">
        <h1 class="display" id="h-writing">Writing your application.</h1>
        <div class="desk3" id="desk3">{sheet('s-cl', 'Cover letter', 13)}{sheet('s-em', 'Email', 8)}{sheet('s-cv', 'CV', 13, chips=True)}</div>
        <div class="wfoot">
          <span class="bigcup" id="bigcup">{cup(100, 46).replace('class="lvl"', 'class="lvl" id="wlvl"')}<span id="wpct">0</span><small>%</small></span>
          <div><ol class="wsteps" id="wsteps"><li class="now"><i></i>Tailoring your CV</li><li><i></i>Writing the cover letter</li><li><i></i>Drafting the email</li><li><i></i>Making the PDFs</li></ol></div>
        </div>
        <p class="wnote">This takes about a minute. You can leave; it will wait for you in <a href="{links['applied']}">Applied</a>.</p>
      </div>
    </section>
    <section class="pane p-ready" aria-labelledby="h-ready">
      <div class="rhead" style="--d: 0;"><div><h1 class="display" id="h-ready">Your application is ready.</h1><p>Read it once, then send it from your own email.</p></div>
        <div class="racts"><button class="ghost3 dlall" type="button">{DL}Download all</button><a class="go" href="{links['applied']}"><span class="s-go">Done{ARR}</span></a></div></div>
      <div class="ready">
        <div class="dtabs" role="tablist" aria-label="Documents">
          <button class="dtab" role="tab" aria-selected="true" data-tab="cv" style="--d: 1;"><span class="th" id="thcv">{cvdoc(tpl)}</span><span><b>CV</b><small>PDF · 1 page</small></span></button>
          <button class="dtab" role="tab" aria-selected="false" data-tab="cl" style="--d: 2;"><span class="th">{LETTER}</span><span><b>Cover letter</b><small>PDF · 1 page</small></span></button>
          <button class="dtab" role="tab" aria-selected="false" data-tab="em" style="--d: 3;"><span class="th mi">{MAIL}</span><span><b>Email</b><small>Subject and message</small></span></button>
          <button class="chdesign" type="button" id="chdesign">Change the CV design</button>
        </div>
        <div class="viewer" style="--d: 2;">
          <div class="stamp2" aria-hidden="true">Ready<br>to<br>send</div>
          <div class="vpane on" data-pane="cv"><div class="vbar"><b>CV · Salma_El_Idrissi_CV.pdf</b><span class="vb"><button class="vbtn dl" type="button">{DL}Download</button><button class="vbtn dl" type="button">{EXT}Open</button></span></div><div class="vdoc" id="vcv">{cvdoc(tpl)}</div></div>
          <div class="vpane" data-pane="cl"><div class="vbar"><b>Cover letter · Salma_El_Idrissi_Letter.pdf</b><span class="vb"><button class="vbtn dl" type="button">{DL}Download</button><button class="vbtn dl" type="button">{EXT}Open</button></span></div><div class="vdoc">{LETTER}</div></div>
          <div class="vpane" data-pane="em"><div class="vbar"><b>Email</b><span class="vb"><button class="vbtn copy" type="button" data-copy="all">{COPY}Copy all</button></span></div>
            <div class="mail"><div class="mrow"><span>To</span><b>The recruiter, from the original post</b><span></span></div><div class="mrow"><span>Subject</span><b id="msub">{SUBJECT}</b><button class="copy" type="button" data-copy="sub">{COPY}Copy</button></div><p class="mbody" id="mbody">{BODY}</p><div><button class="copy" type="button" data-copy="body">{COPY}Copy the message</button></div></div></div>
        </div>
      </div>
    </section>
  </main>
  <div class="mbar2"><button class="go write" type="button"><span class="s-go">Write my application{ARR}</span></button></div>
  <div class="toast" id="toast" role="status" hidden></div>
</div>
</div>'''

JS = r'''<script>
(() => {
  const st = document.getElementById('studio'), desk = document.getElementById('desk3'), steps = [...document.querySelectorAll('#wsteps li')];
  const pct = document.getElementById('wpct'), lvl = document.getElementById('wlvl'), toast = document.getElementById('toast'); let tt;
  const say = (t) => { toast.textContent = t; toast.hidden = false; toast.style.animation = 'none'; void toast.offsetWidth; toast.style.animation = ''; clearTimeout(tt); tt = setTimeout(() => { toast.hidden = true; }, 3200); };
  const setStep = (s) => {
    st.dataset.step = s; scrollTo({ top: 0, behavior: 'smooth' }); const n = { setup: 1, writing: 2, ready: 3 }[s];
    document.querySelectorAll('.psteps li').forEach((li) => { const i = +li.dataset.s; li.className = i === n ? 'on' : i < n ? 'ok' : ''; li.querySelector('b').textContent = i < n ? '✓' : i; });
  };
  const tpl = () => document.querySelector('input[name="tpl"]:checked').value;
  const applyTpl = () => { document.querySelectorAll('#vcv .cvd, #thcv .cvd').forEach((d) => { d.className = 'cvd ' + tpl(); }); };
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const write = () => {
    applyTpl(); setStep('writing');
    desk.className = 'desk3'; desk.querySelectorAll('.sheet3').forEach((s) => s.classList.remove('on3'));
    steps.forEach((li, i) => { li.className = i === 0 ? 'now' : ''; });
    const T = reduce ? 600 : 8200, t0 = performance.now();
    const tick = (now) => { const p = Math.min(1, (now - t0) / T); pct.textContent = Math.round(p * 100); lvl.style.transform = `scaleY(${p})`; if (p < 1 && st.dataset.step === 'writing') requestAnimationFrame(tick); };
    lvl.style.transformBox = 'fill-box'; lvl.style.transformOrigin = '50% 100%'; requestAnimationFrame(tick);
    const at = (ms, fn) => setTimeout(() => { if (st.dataset.step === 'writing') fn(); }, reduce ? Math.min(ms, 500) : ms);
    at(150, () => desk.querySelector('.s-cv').classList.add('on3'));
    at(2400, () => { desk.classList.add('ph2'); desk.querySelector('.s-cl').classList.add('on3'); steps[0].className = 'done'; steps[1].className = 'now'; });
    at(4500, () => { desk.classList.remove('ph2'); desk.classList.add('ph3'); desk.querySelector('.s-em').classList.add('on3'); steps[1].className = 'done'; steps[2].className = 'now'; });
    at(6300, () => { desk.classList.remove('ph3'); desk.classList.add('ph4'); steps[2].className = 'done'; steps[3].className = 'now'; });
    at(8300, () => { steps[3].className = 'done'; setStep('ready'); showTab('cv'); });
  };
  document.querySelectorAll('.write').forEach((b) => b.addEventListener('click', write));
  const showTab = (k) => {
    document.querySelectorAll('.dtab').forEach((t) => t.setAttribute('aria-selected', String(t.dataset.tab === k)));
    document.querySelectorAll('.vpane').forEach((p) => p.classList.toggle('on', p.dataset.pane === k));
  };
  document.querySelectorAll('.dtab').forEach((t) => t.addEventListener('click', () => showTab(t.dataset.tab)));
  document.getElementById('chdesign').addEventListener('click', () => setStep('setup'));
  document.querySelectorAll('.dl, .dlall').forEach((b) => b.addEventListener('click', () => say('Downloads start here in the app. This preview has no files.')));
  const text = { sub: () => document.getElementById('msub').textContent, body: () => document.getElementById('mbody').textContent };
  text.all = () => 'Subject: ' + text.sub() + '\n\n' + text.body();
  document.querySelectorAll('[data-copy]').forEach((b) => b.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(text[b.dataset.copy]()); say('Copied'); } catch (e) { const r = document.createRange(); r.selectNodeContents(document.getElementById(b.dataset.copy === 'sub' ? 'msub' : 'mbody')); getSelection().removeAllRanges(); getSelection().addRange(r); say('Selected. Press Ctrl+C to copy.'); }
    b.classList.add('ok'); setTimeout(() => b.classList.remove('ok'), 1500);
  }));
})();
</script>'''

DCs = open(f'{A}/upload.py').read()
DC = DCs[DCs.index("DC = '''") + 8:DCs.index("'''", DCs.index("DC = '''") + 8)]
LOGO = 'data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%2048%2048%22%20width=%2248%22%20height=%2248%22%20fill=%22none%22%20stroke-linecap=%22round%22%20stroke-linejoin=%22round%22%3E%3Cdefs%3E%3CclipPath%20id=%22jmc%22%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22/%3E%3C/clipPath%3E%3C/defs%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20fill=%22%23CDBFFF%22/%3E%3Cpath%20d=%22M27.5%2020V17Q27.5%2014.5%2030%2014.5H35Q37.5%2014.5%2037.5%2017V20%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FFFFFF%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FF7F45%22%20clip-path=%22url%28%23jmc%29%22/%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Cpath%20d=%22M9.5%2011H19M9.5%2015.5H15%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.4%22/%3E%3Cpath%20d=%22M17%2029.5H44%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.2%22/%3E%3C/svg%3E'
P = f'{S}/nabta-canvas/project'
CL = {'dash': '#matches', 'applied': '#applied'}
def frozen_writing(b):
    b = b.replace('<div class="desk3" id="desk3">', '<div class="desk3 ph2" id="desk3">').replace('class="sheet3 s-cv"', 'class="sheet3 s-cv on3"').replace('class="sheet3 s-cl"', 'class="sheet3 s-cl on3"')
    b = b.replace('<span id="wpct">0</span>', '<span id="wpct">46</span>').replace('class="lvl" id="wlvl"', 'class="lvl" id="wlvl" style="transform-box: fill-box; transform-origin: 50% 100%; transform: scaleY(.46);"')
    return b.replace('<li class="now"><i></i>Tailoring your CV</li><li><i></i>Writing the cover letter</li>', '<li class="done"><i></i>Tailoring your CV</li><li class="now"><i></i>Writing the cover letter</li>')
for nm, step, h in (('Apply', 'setup', 1000), ('ApplyWriting', 'writing', 900), ('ApplyReady', 'ready', 1100)):
    b = body(LOGO, '#home', CL, step=step)
    if step == 'writing': b = frozen_writing(b)
    open(f'{P}/{nm}.dc.html', 'w').write(DC.format(title=f'JobMatcher prepare application, {step}', fonts=FONTS, css=CSS, body=b, w=1440, h=h))
open(f'{P}/ApplyPhone.dc.html', 'w').write(DC.format(title='JobMatcher prepare application, phone width', fonts=FONTS, css='body{margin:0;background:#F6F5FB}\n',
     body='<div style="width: 390px; background: #F6F5FB;">\n  <dc-import name="Apply" hint-size="390px,1700px"></dc-import>\n</div>', w=390, h=1700))
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
{body('assets/nabta-mark.svg', '#', links)}
{JS}
</body>
</html>
'''
open(f'{S}/preview/apply.html', 'w').write(page({'dash': 'dashboard.html', 'applied': 'dashboard.html#applied'}, 'JobMatcher Prepare Application'))
os.makedirs(f'{S}/apply-standalone/assets', exist_ok=True)
shutil.copy(f'{S}/preview/assets/nabta-mark.svg', f'{S}/apply-standalone/assets/nabta-mark.svg')
full = page({'dash': '#top', 'applied': '#top'}, 'JobMatcher Prepare Application')
head = re.search(r'<head>(.*?)</head>', full, re.S).group(1)
head = re.sub(r'<meta charset="utf-8">|<meta name="viewport"[^>]*>', '', head).strip()
t = re.search(r'<title>.*?</title>', head).group(0); head = head.replace(t, '').strip()
bod = re.search(r'<body>(.*)</body>', full, re.S).group(1).strip()
open(f'{S}/apply-standalone/index.html', 'w').write(t + '\n' + head + '\n' + bod + '\n')
print('ok')
