# Check your details: the CV as one drawn, editable page. Builds canvas boards and preview pages.
import sys, os
S = sys.argv[1]
A = f'{S}/auth'
src = open(f'{A}/auth2.py').read()
exec(src[src.index('def svg('):src.index('def signin(')])
CSS = open(f'{A}/auth2.css').read() + open(f'{A}/upload.css').read() + open(f'{A}/review.css').read()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Outfit:wght@400;500;600;700&amp;display=swap">'
PHONE = svg('<path d="M6 3h4l2 5-3 2a11 11 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 4 5a2 2 0 0 1 2-2z"></path>', w=16, cls='')
PIN = svg('<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"></path><circle cx="12" cy="10" r="2.5"></circle>', w=16, cls='')
MAIL_S = svg('<rect x="3" y="5" width="18" height="14" rx="3"></rect><path d="M4 7l8 6 8-6"></path>', w=16, cls='')
CHEV = svg('<path d="M9 6l6 6-6 6"></path>', w=18, cls='go-ic')
PLUS = svg('<path d="M12 5v14M5 12h14"></path>', w=14, cls='')
X = '×'

def chip(t, hit=False):
    return f'<span class="chip{" hit" if hit else ""}">{t}<button type="button" aria-label="Remove {t}">{X}</button></span>'

def body(logo, home, filled=False, upload_href='#upload'):
    ph = ' value="+212 6 12 34 56 78"' if filled else ''
    end2 = ' value="Sep 2024"' if filled else ''
    junior = ' checked' if filled else ''
    need = '<span class="need-tag">Check</span>'
    skills = ''.join(chip(t, h) for t, h in [('Python', 1), ('SQL', 1), ('Power BI', 1), ('Excel', 0), ('Tableau', 0), ('Spark', 0), ('Pandas', 0), ('Git', 0)])
    langs = ''.join(chip(t) for t in ['Arabic · Native', 'French · Fluent', 'English · Professional'])
    def job(n, title, company, start, end, bullets, end_need=False):
        endf = f'<span class="f req" id="f-end{n}" style="margin:0"><input class="e d" id="end{n}" aria-label="End date, {company}" placeholder="End date"{end2 if end_need else f" value={chr(34)}{end}{chr(34)}"}>{need}</span>' if end_need else f'<input class="e d" aria-label="End date, {company}" value="{end}">'
        bl = ''.join(f'<li><textarea class="e b1" rows="1" aria-label="Responsibility">{b}</textarea></li>' for b in bullets)
        return f'''            <div class="job">
              <div class="jrow"><input class="e t" aria-label="Job title" value="{title}"></div>
              <div class="jmeta"><input class="e" aria-label="Company" value="{company}"><input class="e d" aria-label="Start date, {company}" value="{start}"><span>to</span>{endf}</div>
              <ul class="bul">{bl}</ul>
              <button class="rm" type="button" aria-label="Remove this job">{X}</button>
            </div>
'''
    return f'''<div class="page">
<div class="auth signup review" id="auth">
{header(logo, home)}
  <section class="intro">
    <ol class="steps rise" style="--d: 0;" aria-label="Getting started">
      <li class="st ok"><b>✓</b>Account</li><li class="bar ok" aria-hidden="true"></li><li class="st on" aria-current="step"><b>2</b>Your CV</li><li class="bar" aria-hidden="true"></li><li class="st"><b>3</b>Matches</li>
    </ol>
    <div class="head">
      <h1 class="display atitle">{words('Check your details.')}</h1>
      <p class="asub rise" style="--d: 1;">This is what JobMatcher read from your CV. Click any line to change it. Your matches are built from this page.</p>
    </div>
    <div class="todo" style="--d: 2;">
      <a class="ti ti-phone" href="#f-phone"><span class="tb">{TICK}</span><span class="tx"><b>Add your phone number</b><small>It was not on your CV</small></span>{CHEV}</a>
      <a class="ti ti-lvl" href="#lvl"><span class="tb">{TICK}</span><span class="tx"><b>Confirm your level</b><small>JobMatcher suggests Junior</small></span>{CHEV}</a>
      <a class="ti ti-end" href="#f-end2"><span class="tb">{TICK}</span><span class="tx"><b>When did the OCP Group job end?</b><small>The end date is missing</small></span>{CHEV}</a>
      <div class="todo-h"><span class="sw"><span class="sa">Things to check</span><span class="sb">All set</span></span><span class="todo-n" aria-hidden="true"></span></div>
    </div>
    <div class="save" style="--d: 3;">
      <button class="go save-go" type="button" data-state="idle"><span class="s-go">Looks good, find my jobs{ARR}</span><span class="s-wait"><i class="spin"></i>Saving your details…</span><span class="s-ok">{TICK_W}Saved</span></button>
      <p class="back"><a href="{upload_href}">Upload a different CV</a></p>
    </div>
  </section>
  <footer class="afoot"><span>© 2026 JobMatcher</span><a href="{home}">Back to the home page</a></footer>
  <div class="desk">
    <div class="aura a1" aria-hidden="true"></div><div class="aura a2" aria-hidden="true"></div>
    <div class="fwrap">
    {host('signup', ' host-m')}
    <div class="sheet cvdoc">
      <div class="kicker"><span>Curriculum vitae</span><em>Read from CV_Salma_El_Idrissi.pdf</em></div>
      <div class="stamp" aria-hidden="true">Ready<br>for<br>matches</div>
      <header class="cv-h" style="--t: 0;">
        <span class="s-av done" aria-hidden="true">SE</span>
        <div class="cv-nm"><input class="e big" aria-label="Full name" value="Salma El Idrissi"><span class="loc">{PIN}<input class="e" aria-label="Location" value="Casablanca, Morocco"></span></div>
      </header>
      <div class="cv-cols">
        <aside class="cv-side">
          <section class="blk" style="--t: 1;"><h3>Contact</h3>
            <span class="f">{MAIL_S}<input class="e" type="email" aria-label="Email" value="salma@example.com"></span>
            <span class="f req" id="f-phone">{PHONE}<input class="e" id="phone" type="tel" aria-label="Phone number" placeholder="Add your phone"{ph}>{need}</span>
          </section>
          <fieldset class="blk lvl" id="lvl" style="--t: 2; border: 0; margin-inline: -8px; min-width: 0;"><legend class="vh">Level</legend><h3>Level {need}</h3>
            <div class="seg"><label><input type="radio" name="lvl" value="junior"{junior}>Junior</label><label><input type="radio" name="lvl" value="mid">Mid-level</label><label><input type="radio" name="lvl" value="senior">Senior</label><label><input type="radio" name="lvl" value="lead">Lead</label></div>
            <p class="hintx">JobMatcher suggests <b>Junior</b> from your CV.</p>
          </fieldset>
          <section class="blk" style="--t: 3;"><h3>Experience</h3>
            <div class="step"><button type="button" aria-label="One year less" data-step="-1">−</button><output id="yrs" aria-live="polite">1</output><span id="yrs-l">year in total</span><button type="button" aria-label="One year more" data-step="1">+</button></div>
          </section>
          <section class="blk" style="--t: 4;"><h3>Languages</h3>
            <div class="chips" data-list="lang">{langs}<span class="addchip">{PLUS}<input aria-label="Add a language" placeholder="Add"></span></div>
          </section>
        </aside>
        <div class="cv-main">
          <section class="blk" style="--t: 1;"><h3>Summary</h3>
            <textarea class="e" rows="3" aria-label="Summary">Data analyst with two internships, in banking and in industry. I build Power BI dashboards and data pipelines in Python and SQL.</textarea>
          </section>
          <section class="blk" style="--t: 2;"><h3>Experience <button class="add" type="button" id="addjob">{PLUS}Add a job</button></h3>
{job(1, 'Data Analyst Intern', 'Attijariwafa bank', 'Feb 2025', 'Jul 2025', ['Built Power BI dashboards for the retail credit team', 'Automated the weekly SQL reports'])}{job(2, 'BI Assistant', 'OCP Group', 'Jul 2024', '', ['Cleaned and modelled production data in Python'], end_need=True)}          </section>
          <section class="blk" style="--t: 3;"><h3>Education <button class="add" type="button">{PLUS}Add</button></h3>
            <div class="edu"><input class="e t" aria-label="Degree" value="Master, Big Data and IoT"><span class="sub"><input class="e" aria-label="School" value="ENSAM Casablanca"><input class="e d" aria-label="Years" value="2024 to 2026"></span><button class="rm" type="button" aria-label="Remove this degree">{X}</button></div>
            <div class="edu"><input class="e t" aria-label="Degree" value="Licence, Mathematics and Computer Science"><span class="sub"><input class="e" aria-label="School" value="FST Mohammedia"><input class="e d" aria-label="Years" value="2021 to 2024"></span><button class="rm" type="button" aria-label="Remove this degree">{X}</button></div>
          </section>
          <section class="blk" style="--t: 4;"><h3>Skills</h3>
            <div class="chips" data-list="skill">{skills}<span class="addchip">{PLUS}<input aria-label="Add a skill" placeholder="Add a skill"></span></div>
          </section>
        </div>
      </div>
    </div>
    <div class="mbar"><button class="mleft" type="button" id="nextcheck"><span class="todo-n" aria-hidden="true"></span><span class="sw"><span class="sa">to check</span><span class="sb">All set</span></span></button><button class="go save-go" type="button" data-state="idle"><span class="s-go">Find my jobs{ARR}</span><span class="s-wait"><i class="spin"></i>Saving…</span><span class="s-ok">{TICK_W}Saved</span></button></div>
    </div>
    {PAUSE}
  </div>
</div>
</div>'''

JS = r'''<script>
(() => {
  const yrs = document.getElementById('yrs'), yl = document.getElementById('yrs-l');
  document.querySelectorAll('[data-step]').forEach((b) => b.addEventListener('click', () => {
    const v = Math.max(0, Math.min(40, (+yrs.value || +yrs.textContent) + +b.dataset.step)); yrs.textContent = v; yl.textContent = v === 1 ? 'year in total' : 'years in total';
  }));
  const wire = (c) => { const b = c.querySelector('button'); if (b) b.addEventListener('click', () => { c.classList.add('out'); setTimeout(() => c.remove(), 260); }); };
  document.querySelectorAll('.chip').forEach(wire);
  document.querySelectorAll('.addchip input').forEach((i) => i.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' || !i.value.trim()) return; e.preventDefault();
    const c = document.createElement('span'); c.className = 'chip'; c.textContent = i.value.trim();
    const x = document.createElement('button'); x.type = 'button'; x.textContent = '×'; x.setAttribute('aria-label', 'Remove ' + i.value.trim()); c.append(x);
    i.parentElement.before(c); wire(c); i.value = '';
  }));
  document.querySelectorAll('.rm').forEach((b) => b.addEventListener('click', () => { const r = b.parentElement; r.style.transition = 'opacity .25s'; r.style.opacity = '0'; setTimeout(() => r.remove(), 260); }));
  document.getElementById('addjob').addEventListener('click', () => {
    const j = document.querySelector('.job').cloneNode(true); j.querySelectorAll('input, textarea').forEach((i) => { i.value = ''; i.placeholder = i.getAttribute('aria-label').split(',')[0]; });
    j.querySelectorAll('.bul li:not(:first-child)').forEach((l) => l.remove());
    document.getElementById('addjob').closest('section').append(j); j.querySelector('input').focus();
    j.querySelector('.rm').addEventListener('click', () => j.remove());
  });
  document.querySelectorAll('.ti').forEach((a) => a.addEventListener('click', () => { setTimeout(() => { const t = document.querySelector(a.getAttribute('href')); const i = t && t.querySelector('input'); if (i) i.focus({ preventScroll: true }); }, 350); }));
  document.getElementById('nextcheck').addEventListener('click', () => {
    const f = [...document.querySelectorAll('.req, .lvl')].find((x) => x.matches('.req:has(input:placeholder-shown), .lvl:not(:has(input:checked))'));
    if (f) { f.scrollIntoView({ behavior: 'smooth', block: 'center' }); const i = f.querySelector('input'); setTimeout(() => i && i.focus({ preventScroll: true }), 400); }
  });
  document.querySelectorAll('.save-go').forEach((g) => g.addEventListener('click', () => {
    if (g.dataset.state !== 'idle') return; document.querySelectorAll('.save-go').forEach((x) => { x.dataset.state = 'wait'; });
    setTimeout(() => document.querySelectorAll('.save-go').forEach((x) => { x.dataset.state = 'ok'; }), 1300);
  }));
})();
</script>'''

DC = open(f'{A}/upload.py').read()
DC = DC[DC.index("DC = '''") + 8:DC.index("'''", DC.index("DC = '''") + 8)]
LOGO = 'data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%2048%2048%22%20width=%2248%22%20height=%2248%22%20fill=%22none%22%20stroke-linecap=%22round%22%20stroke-linejoin=%22round%22%3E%3Cdefs%3E%3CclipPath%20id=%22jmc%22%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22/%3E%3C/clipPath%3E%3C/defs%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20fill=%22%23CDBFFF%22/%3E%3Cpath%20d=%22M27.5%2020V17Q27.5%2014.5%2030%2014.5H35Q37.5%2014.5%2037.5%2017V20%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FFFFFF%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FF7F45%22%20clip-path=%22url%28%23jmc%29%22/%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Cpath%20d=%22M9.5%2011H19M9.5%2015.5H15%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.4%22/%3E%3Cpath%20d=%22M17%2029.5H44%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.2%22/%3E%3C/svg%3E'
P = f'{S}/nabta-canvas/project'
H = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
PH = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
open(f'{P}/Review.dc.html', 'w').write(DC.format(title='JobMatcher check your details', fonts=FONTS, css=CSS, body=body(LOGO, '#home'), w=1440, h=H))
open(f'{P}/ReviewDone.dc.html', 'w').write(DC.format(title='JobMatcher check your details, all set', fonts=FONTS, css=CSS, body=body(LOGO, '#home', filled=True), w=1440, h=H))
open(f'{P}/ReviewPhone.dc.html', 'w').write(DC.format(title='JobMatcher check your details, phone width', fonts=FONTS, css='body{margin:0;background:#F6F5FB}\n',
     body=f'<div style="width: 390px; background: #F6F5FB;">\n  <dc-import name="Review" hint-size="390px,{PH}px"></dc-import>\n</div>', w=390, h=PH))
def page(home, upload_href, title):
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
{body('assets/nabta-mark.svg', home, upload_href=upload_href)}
{JS}
</body>
</html>
'''
open(f'{S}/preview/review.html', 'w').write(page('index.html', 'upload.html', 'JobMatcher Check Your Details'))
os.makedirs(f'{S}/review-standalone/assets', exist_ok=True)
import re, shutil
shutil.copy(f'{S}/preview/assets/nabta-mark.svg', f'{S}/review-standalone/assets/nabta-mark.svg')
full = page('#top', '#top', 'JobMatcher Check Your Details')
head = re.search(r'<head>(.*?)</head>', full, re.S).group(1)
head = re.sub(r'<meta charset="utf-8">|<meta name="viewport"[^>]*>', '', head).strip()
bod = re.search(r'<body>(.*)</body>', full, re.S).group(1).strip()
t = re.search(r'<title>.*?</title>', head).group(0); head = head.replace(t, '').strip()
open(f'{S}/review-standalone/index.html', 'w').write(t + '\n' + head + '\n' + bod + '\n')
print('ok')
