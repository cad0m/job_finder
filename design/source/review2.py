# Check your details v2: your file on the left, everything JobMatcher read on the right, one screen on desktop.
import sys, os, re, shutil
S = sys.argv[1]
A = f'{S}/auth'
src = open(f'{A}/auth2.py').read()
exec(src[src.index('def svg('):src.index('def signin(')])
CSS = open(f'{A}/auth2.css').read() + open(f'{A}/upload.css').read() + open(f'{A}/review.css').read() + open(f'{A}/review2.css').read()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Outfit:wght@400;500;600;700&amp;display=swap">'
PLUS = svg('<path d="M12 5v14M5 12h14"></path>', w=14, cls='')
CHEV = svg('<path d="M9 6l6 6-6 6"></path>', w=18, cls='chev')
CHEV2 = svg('<path d="M6 9l6 6 6-6"></path>', w=18, cls='chev2')
DOC_I = svg('<path d="M7 3h7l4 4v14H7z"></path><path d="M14 3v4h4"></path>', w=20, cls='')
TK = '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
X = '×'
NEED = '<span class="need-tag">Check</span>'

def chip(t):
    return f'<span class="chip">{t}<button type="button" aria-label="Remove {t}">{X}</button></span>'

def docmock():
    return '''<div class="doc" aria-hidden="true">
          <div class="db d-name">SALMA EL IDRISSI</div>
          <div class="db d-role">Data Analyst</div>
          <div class="db d-contact">salma@example.com · Casablanca, Morocco · linkedin.com/in/salma-elidrissi</div>
          <div class="db d-rule"></div>
          <div class="db d-sum"><div class="d-h">Profile</div><div class="d-p">Data analyst with two internships, in banking and in industry. I build Power BI dashboards and data pipelines in Python and SQL.</div></div>
          <div class="db d-exp"><div class="d-h">Experience</div>
            <div class="d-job">Data Analyst Intern, Attijariwafa bank<span>Feb 2025 to Jul 2025</span></div>
            <div class="d-li">Built Power BI dashboards for the retail credit team</div><div class="d-li">Automated the weekly SQL reports</div><div class="d-gap"></div>
            <div class="d-job">BI Assistant, OCP Group<span>Jul 2024 to</span></div>
            <div class="d-li">Cleaned and modelled production data in Python</div></div>
          <div class="db d-edu"><div class="d-h">Education</div><div class="d-p"><b>Master, Big Data and IoT</b>, ENSAM Casablanca<br><b>Licence, Mathematics and Computer Science</b>, FST Mohammedia</div></div>
          <div class="db d-skl"><div class="d-h">Skills</div><div class="d-p">Python, SQL, Power BI, Excel, Tableau, Spark, Pandas, Git</div></div>
          <div class="db d-lng"><div class="d-h">Languages</div><div class="d-p">Arabic (native), French (fluent), English (professional)</div></div>
          <div class="db d-crt"><div class="d-h">Certifications</div><div class="d-p">Microsoft Certified: Power BI Data Analyst Associate</div></div>
          <div class="hl"></div>
        </div>'''

def body(logo, home, filled=False, upload_href='#upload'):
    ph = ' value="+212 6 12 34 56 78"' if filled else ''
    end2 = ' value="Sep 2024"' if filled else ''
    jun = ' checked' if filled else ''
    skills = ''.join(chip(t) for t in ['Python', 'SQL', 'Power BI', 'Excel', 'Tableau', 'Spark', 'Pandas', 'Git'])
    langs = ''.join(chip(t) for t in ['Arabic · Native', 'French · Fluent', 'English · Professional'])
    certs = chip('Microsoft Certified: Power BI Data Analyst Associate')
    def job(n, title, company, start, end, duties, need_end=False):
        endv = end2 if need_end else f' value="{end}"'
        req = ' req' if need_end else ''
        endid = f' id="end{n}"'
        dl = ''.join(f'<li><textarea class="in" rows="1" aria-label="Duty">{d}</textarea></li>' for d in duties)
        return f'''              <details class="jc"{' open' if need_end else ''}><summary class="jsum"><b>{title}</b><span>{company} · {start} to {end or '…'}</span>{CHEV2}</summary><div class="jc-b">
                <button class="rm" type="button" aria-label="Remove this job">{X}</button>
                <div class="g4">
                  <div class="fl"><label for="jt{n}">Job title</label><input class="in" id="jt{n}" value="{title}"></div>
                  <div class="fl"><label for="jco{n}">Company</label><input class="in" id="jco{n}" value="{company}"></div>
                  <div class="dd">
                    <div class="fl"><label for="js{n}">Start</label><input class="in" id="js{n}" value="{start}"></div>
                    <div class="fl{req}" id="f-end{n}"><label for="end{n}"><span>End</span>{NEED if need_end else ''}</label><input class="in"{endid} aria-label="End date" placeholder="Month year"{endv}></div>
                  </div>
                </div>
                {'<p class="help" style="margin-top:-6px;">The end date is missing from your CV.</p>' if need_end else ''}
                <label class="now"><input type="checkbox" class="nowbox">I still work here</label>
                <div class="fl"><span class="lb">What you did</span><ul class="duties">{dl}</ul><button class="lnk addduty" type="button">Add a line</button></div>
              </div></details>
'''
    rail = [('profile', 'Profile', '', True), ('contact', 'Contact and links', '', True), ('exp', 'Experience', '2', True), ('edu', 'Education', '2', False), ('skills', 'Skills', '8', False), ('lang', 'Languages', '3', False), ('cert', 'Certifications', '1', False)]
    railh = ''.join(f'<a class="rl-{k}{" need" if n else ""}" href="#s-{k}" style="--t: {i};"><span class="st">{TK}</span>{t}<span class="c">{c}</span></a>' for i, (k, t, c, n) in enumerate(rail))
    jump = ''.join(f'<a class="j-{k}{" need" if n else ""}" href="#s-{k}">{t}</a>' for k, t, c, n in rail)
    marks = '<i class="tk tk-phone"></i><i class="tk tk-lvl"></i><i class="tk tk-end"></i>'
    return f'''<div class="page">
<div class="auth rv2" id="auth">
  <div class="rbar">
    <a class="logo" href="{home}"><img src="{logo}" alt="" width="40" height="40"><span class="display">JobMatcher</span></a>
    <ol class="steps" aria-label="Getting started">
      <li class="st ok"><b>✓</b>Account</li><li class="bar ok" aria-hidden="true"></li><li class="st on" aria-current="step"><b>2</b>Your CV</li><li class="bar" aria-hidden="true"></li><li class="st"><b>3</b>Matches</li>
    </ol>
    {marks}<button class="cnt nextcheck" type="button"><span class="todo-n" aria-hidden="true"></span><span class="sw"><span class="sa">to check</span><span class="sb">All set</span></span></button>
    <button class="go save-go" type="button" data-state="idle"><span class="s-go">Save and find my jobs{ARR}</span><span class="s-wait"><i class="spin"></i>Saving…</span><span class="s-ok">{TICK_W}Saved</span></button>
  </div>
  <div class="rmain">
    <section class="src" aria-label="Your file">
      <div class="aura a1" aria-hidden="true"></div><div class="aura a2" aria-hidden="true"></div>
      <div class="src-h"><span><b>Your file</b><small>CV_Salma_El_Idrissi.pdf · page 1 of 1</small></span><a href="{upload_href}">Replace file</a></div>
      <div class="doc-wrap">
        {docmock()}
      </div>
    </section>
    <section class="data" aria-label="What JobMatcher read">
      <nav class="rail" aria-label="Sections"><p class="rl">Sections</p>{railh}<p class="tip"><b>Point at a section</b> to see where it came from in your file.</p></nav>
      <div class="scroll" id="scroll">
        <div class="stamp" aria-hidden="true">Ready<br>for<br>matches</div>
        <div class="dhead">
          <h1 class="display">{words('Check your details.')}</h1>
          <p>This is everything JobMatcher read from your CV. Compare it with your file, fix anything that is off, then save. Your matches are built from this.</p>
        </div>
        <details class="mfile"><summary>{DOC_I}<span>Compare with your file<small>CV_Salma_El_Idrissi.pdf</small></span>{CHEV}</summary><div class="mdoc">{docmock()}</div></details>
        <nav class="jump" aria-label="Sections">{jump}</nav>
        <details class="rs" id="s-profile" style="--t: 1;" open><summary class="rs-h"><h2>Profile</h2><span class="pv"></span>{CHEV2}</summary><div class="rs-b">
          <div class="g2">
            <div class="fl full"><label for="fn">Full name</label><input class="in big" id="fn" value="Salma El Idrissi"></div>
            <div class="fl"><label for="loc">Location</label><input class="in" id="loc" value="Casablanca, Morocco"></div>
            <div class="fl"><span class="lb">Years of experience</span><div class="stepper"><button type="button" data-step="-1" aria-label="One year less">−</button><output id="yrs" aria-live="polite">1 year</output><button type="button" data-step="1" aria-label="One year more">+</button></div></div>
            <div class="fl full lv" id="lvl"><span class="lb"><span>Level</span>{NEED}</span>
              <div class="seg4" role="radiogroup" aria-label="Level"><label class="sug"><input type="radio" name="lvl" value="junior"{jun}>Junior</label><label><input type="radio" name="lvl" value="mid">Mid-level</label><label><input type="radio" name="lvl" value="senior">Senior</label><label><input type="radio" name="lvl" value="lead">Lead</label></div>
              <p class="help">JobMatcher suggests Junior from your CV. Pick the level you want to be matched at.</p></div>
            <div class="fl full"><label for="sum">Summary</label><textarea class="in" id="sum" rows="3">Data analyst with two internships, in banking and in industry. I build Power BI dashboards and data pipelines in Python and SQL.</textarea></div>
          </div>
        </div></details>
        <details class="rs" id="s-contact" style="--t: 2;" open><summary class="rs-h"><h2>Contact and links</h2><span class="pv"></span>{CHEV2}</summary><div class="rs-b">
          <div class="g2">
            <div class="fl"><label for="em">Email</label><input class="in" id="em" type="email" value="salma@example.com"></div>
            <div class="fl req" id="f-phone"><label for="phone"><span>Phone</span>{NEED}</label><input class="in" id="phone" type="tel" placeholder="+212 6 00 00 00 00"{ph}><p class="help">Not found in your CV. Recruiters use it to reach you.</p></div>
            <div class="fl"><label for="li">LinkedIn</label><div class="pre"><span>linkedin.com/in/</span><input class="in" id="li" value="salma-elidrissi"></div></div>
            <div class="fl"><label for="gh">GitHub <span class="opt">optional</span></label><div class="pre"><span>github.com/</span><input class="in" id="gh" placeholder="username"></div></div>
            <div class="fl full"><label for="pf">Portfolio or website <span class="opt">optional</span></label><input class="in" id="pf" type="url" placeholder="https://"></div>
          </div>
        </div></details>
        <details class="rs" id="s-exp" style="--t: 3;" open><summary class="rs-h"><h2>Experience</h2><span class="c">2 jobs</span><span class="pv"></span>{CHEV2}</summary><div class="rs-b">
{job(1, 'Data Analyst Intern', 'Attijariwafa bank', 'Feb 2025', 'Jul 2025', ['Built Power BI dashboards for the retail credit team', 'Automated the weekly SQL reports'])}{job(2, 'BI Assistant', 'OCP Group', 'Jul 2024', '', ['Cleaned and modelled production data in Python'], need_end=True)}        <div class="addrow"><button class="add" type="button" id="addjob">{PLUS}Add a job</button></div></div></details>
        <details class="rs" id="s-edu" style="--t: 4;"><summary class="rs-h"><h2>Education</h2><span class="c">2</span><span class="pv">Master, Big Data and IoT · Licence, Mathematics and Computer Science</span>{CHEV2}</summary><div class="rs-b">
          <div class="edu2"><div class="fl"><label for="dg1">Degree</label><input class="in" id="dg1" value="Master, Big Data and IoT"></div><div class="fl"><label for="sc1">School</label><input class="in" id="sc1" value="ENSAM Casablanca"></div><button class="rm" type="button" aria-label="Remove this degree">{X}</button></div>
          <div class="edu2"><div class="fl"><label for="dg2">Degree</label><input class="in" id="dg2" value="Licence, Mathematics and Computer Science"></div><div class="fl"><label for="sc2">School</label><input class="in" id="sc2" value="FST Mohammedia"></div><button class="rm" type="button" aria-label="Remove this degree">{X}</button></div>
        <div class="addrow"><button class="add" type="button" id="addedu">{PLUS}Add</button></div></div></details>
        <details class="rs" id="s-skills" style="--t: 5;"><summary class="rs-h"><h2>Skills</h2><span class="c">8</span><span class="pv">Python, SQL, Power BI +5</span>{CHEV2}</summary><div class="rs-b">
          <div class="chips">{skills}<span class="addchip">{PLUS}<input aria-label="Add a skill" placeholder="Add a skill"></span></div>
        </div></details>
        <details class="rs" id="s-lang" style="--t: 6;"><summary class="rs-h"><h2>Languages</h2><span class="c">3</span><span class="pv">Arabic, French, English</span>{CHEV2}</summary><div class="rs-b">
          <div class="chips">{langs}<span class="addchip">{PLUS}<input aria-label="Add a language" placeholder="Add a language"></span></div>
        </div></details>
        <details class="rs" id="s-cert" style="--t: 7;"><summary class="rs-h"><h2>Certifications</h2><span class="c">1</span><span class="pv">Power BI Data Analyst Associate</span>{CHEV2}</summary><div class="rs-b">
          <div class="chips">{certs}<span class="addchip">{PLUS}<input aria-label="Add a certification" placeholder="Add a certification"></span></div>
        </div></details>
      </div>
    </section>
  </div>
  <div class="mbar"><button class="mleft nextcheck" type="button"><span class="todo-n" aria-hidden="true"></span><span class="sw"><span class="sa">to check</span><span class="sb">All set</span></span></button><button class="go save-go" type="button" data-state="idle"><span class="s-go">Find my jobs{ARR}</span><span class="s-wait"><i class="spin"></i>Saving…</span><span class="s-ok">{TICK_W}Saved</span></button></div>
</div>
</div>'''

JS = r'''<script>
(() => {
  const yrs = document.getElementById('yrs'); let y = 1;
  document.querySelectorAll('[data-step]').forEach((b) => b.addEventListener('click', () => { y = Math.max(0, Math.min(40, y + +b.dataset.step)); yrs.textContent = y + (y === 1 ? ' year' : ' years'); }));
  const wire = (c) => { const b = c.querySelector('button'); if (b) b.addEventListener('click', () => { c.classList.add('out'); setTimeout(() => c.remove(), 260); }); };
  document.querySelectorAll('.chip').forEach(wire);
  document.querySelectorAll('.addchip input').forEach((i) => i.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' || !i.value.trim()) return; e.preventDefault();
    const c = document.createElement('span'); c.className = 'chip in-new'; c.textContent = i.value.trim();
    const x = document.createElement('button'); x.type = 'button'; x.textContent = '×'; x.setAttribute('aria-label', 'Remove ' + i.value.trim()); c.append(x);
    i.parentElement.before(c); wire(c); i.value = '';
  }));
  const rmw = (b) => b.addEventListener('click', () => { const r = b.closest('.jc, .edu2'); r.style.transition = 'opacity .25s'; r.style.opacity = '0'; setTimeout(() => r.remove(), 260); });
  document.querySelectorAll('.rm').forEach(rmw);
  const dutyw = (b) => b.addEventListener('click', () => { const ul = b.previousElementSibling; const li = document.createElement('li'); li.innerHTML = '<textarea class="in" rows="1" aria-label="Duty" placeholder="What you did"></textarea>'; ul.append(li); li.firstChild.focus(); });
  document.querySelectorAll('.addduty').forEach(dutyw);
  const noww = (c) => c.addEventListener('change', () => { const e = c.closest('.jc').querySelector('[aria-label="End date"]'); if (c.checked) { e.dataset.prev = e.value; e.value = 'Present'; e.disabled = true; } else { e.disabled = false; e.value = e.dataset.prev || ''; } e.dispatchEvent(new Event('input')); });
  document.querySelectorAll('.nowbox').forEach(noww);
  let n = 10;
  document.getElementById('addjob').addEventListener('click', () => {
    const j = document.querySelector('.jc').cloneNode(true); n++;
    j.querySelectorAll('input:not([type=checkbox]), textarea').forEach((i) => { i.value = ''; if (i.id) i.id = i.id.replace(/\d+$/, n); });
    j.querySelectorAll('label[for]').forEach((l) => { l.htmlFor = l.htmlFor.replace(/\d+$/, n); });
    j.querySelectorAll('.duties li:not(:first-child)').forEach((l) => l.remove()); j.querySelector('.nowbox').checked = false;
    document.querySelector('#s-exp .addrow').before(j); j.open = true; rmw(j.querySelector('.rm')); dutyw(j.querySelector('.addduty')); noww(j.querySelector('.nowbox')); j.querySelector('input').focus();
  });
  document.getElementById('addedu').addEventListener('click', () => {
    const r = document.querySelector('.edu2').cloneNode(true); n++;
    r.querySelectorAll('input').forEach((i) => { i.value = ''; i.id = i.id.replace(/\d+$/, n); }); r.querySelectorAll('label[for]').forEach((l) => { l.htmlFor = l.htmlFor.replace(/\d+$/, n); });
    document.querySelector('#s-edu .addrow').before(r); rmw(r.querySelector('.rm')); r.querySelector('input').focus();
  });
  const sc = document.getElementById('scroll');
  if (matchMedia('(min-width: 901px)').matches) document.querySelectorAll('details.rs, details.jc').forEach((d) => { d.open = true; });
  document.querySelectorAll('.rail a, .jump a').forEach((a) => a.addEventListener('click', (e) => {
    const t = document.querySelector(a.getAttribute('href')); if (!t) return; e.preventDefault(); if (t.tagName === 'DETAILS') t.open = true;
    t.scrollIntoView({ behavior: 'smooth', block: 'start' }); const f = t.querySelector('input, textarea'); setTimeout(() => f && f.focus({ preventScroll: true }), 450);
  }));
  document.querySelectorAll('.nextcheck').forEach((b) => b.addEventListener('click', () => {
    const f = [...document.querySelectorAll('.fl.req, .fl.lv')].find((x) => x.matches('.req:has(.in:placeholder-shown), .lv:not(:has(input:checked))'));
    if (f) { f.closest('details.rs') && (f.closest('details.rs').open = true); f.closest('details.jc') && (f.closest('details.jc').open = true); f.scrollIntoView({ behavior: 'smooth', block: 'center' }); const i = f.querySelector('.in, input'); setTimeout(() => i && i.focus({ preventScroll: true }), 450); }
  }));
  document.querySelectorAll('.save-go').forEach((g) => g.addEventListener('click', () => {
    if (g.dataset.state !== 'idle') return; document.querySelectorAll('.save-go').forEach((x) => { x.dataset.state = 'wait'; });
    setTimeout(() => { document.querySelectorAll('.save-go').forEach((x) => { x.dataset.state = 'ok'; }); if (location.pathname.endsWith('review.html')) setTimeout(() => { location.href = 'dashboard.html'; }, 1100); }, 1300);
  }));
})();
</script>'''

DCs = open(f'{A}/upload.py').read()
DC = DCs[DCs.index("DC = '''") + 8:DCs.index("'''", DCs.index("DC = '''") + 8)]
LOGO = 'data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%2048%2048%22%20width=%2248%22%20height=%2248%22%20fill=%22none%22%20stroke-linecap=%22round%22%20stroke-linejoin=%22round%22%3E%3Cdefs%3E%3CclipPath%20id=%22jmc%22%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22/%3E%3C/clipPath%3E%3C/defs%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20fill=%22%23CDBFFF%22/%3E%3Cpath%20d=%22M27.5%2020V17Q27.5%2014.5%2030%2014.5H35Q37.5%2014.5%2037.5%2017V20%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FFFFFF%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FF7F45%22%20clip-path=%22url%28%23jmc%29%22/%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Cpath%20d=%22M9.5%2011H19M9.5%2015.5H15%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.4%22/%3E%3Cpath%20d=%22M17%2029.5H44%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.2%22/%3E%3C/svg%3E'
P = f'{S}/nabta-canvas/project'
PH = int(sys.argv[2]) if len(sys.argv) > 2 else 2400
open(f'{P}/Review.dc.html', 'w').write(DC.format(title='JobMatcher check your details', fonts=FONTS, css=CSS, body=body(LOGO, '#home'), w=1440, h=900))
open(f'{P}/ReviewDone.dc.html', 'w').write(DC.format(title='JobMatcher check your details, all set', fonts=FONTS, css=CSS, body=body(LOGO, '#home', filled=True), w=1440, h=900))
open(f'{P}/ReviewPhone.dc.html', 'w').write(DC.format(title='JobMatcher check your details, phone width', fonts=FONTS, css='body{margin:0;background:#F6F5FB}\n',
     body=f'<div style="width: 390px; background: #F6F5FB;">\n  <dc-import name="Review" hint-size="390px,{PH}px"></dc-import>\n</div>', w=390, h=PH))
def page(home, upload_href, title, logo='assets/nabta-mark.svg'):
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
{body(logo, home, upload_href=upload_href)}
{JS}
</body>
</html>
'''
open(f'{S}/preview/review.html', 'w').write(page('index.html', 'upload.html', 'JobMatcher Check Your Details'))
full = page('#top', '#top', 'JobMatcher Check Your Details')
head = re.search(r'<head>(.*?)</head>', full, re.S).group(1)
head = re.sub(r'<meta charset="utf-8">|<meta name="viewport"[^>]*>', '', head).strip()
t = re.search(r'<title>.*?</title>', head).group(0); head = head.replace(t, '').strip()
bod = re.search(r'<body>(.*)</body>', full, re.S).group(1).strip()
open(f'{S}/review-standalone/index.html', 'w').write(t + '\n' + head + '\n' + bod + '\n')
print('ok')
