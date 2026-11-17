# Step 2: add your CV. Builds canvas boards (one per state) and an interactive preview page.
import sys, os, re
S = sys.argv[1]
A = f'{S}/auth'
src = open(f'{A}/auth2.py').read()
# reuse the icon/helper definitions from the auth generator without running its build
helpers = src[src.index('def svg('):src.index('def signin(')]
helpers = helpers.replace("open(f'{S}/peeps-render", "open(f'{S}/peeps-render")
exec(helpers)
CSS = open(f'{A}/auth2.css').read() + open(f'{A}/upload.css').read()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Outfit:wght@400;500;600;700&amp;display=swap">'
UPDOC = '<svg viewBox="0 0 48 48" width="44" height="44" fill="none" stroke="#1E1C2B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 6h15l9 9v27H13z" fill="#FFFFFF"></path><path d="M28 6v9h9"></path><path d="M25 37V22M19 28l6-6 6 6" stroke="#FF7F45"></path></svg>'
CAMERA = svg('<path d="M4 8h3l2-3h6l2 3h3v11H4z"></path><circle cx="12" cy="13" r="3.5"></circle>', w=18, cls='')
FOLDER = svg('<path d="M3 7h6l2 2h10v10H3z"></path>', w=18, cls='')
XMARK = svg('<path d="M6 6l12 12M18 6L6 18"></path>', w=18, cls='')
WARN = svg('<path d="M12 4l9 16H3z"></path><path d="M12 10v4M12 17.5v.5"></path>', w=26, cls='')
TICK_S = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'

def body(logo, home, state, preview=False):
    skills = ['Python', 'SQL', 'Power BI', 'Excel', 'Tableau', 'Spark', 'Pandas', 'Git']
    chips = ''.join(f'<span class="c rv-i" style="--t: 2; --k: {i};">{s}</span>' for i, s in enumerate(skills))
    sample = '\n          <button class="sample" type="button" id="sample">Preview with a sample CV</button>' if preview else ''
    return f'''<div class="page">
<div class="auth signup up" id="auth" data-state="{state}">
{header(logo, home)}
  <section class="intro">
    <ol class="steps rise" style="--d: 0;" aria-label="Getting started">
      <li class="st ok"><b>✓</b>Account</li><li class="bar ok" aria-hidden="true"></li><li class="st on" aria-current="step"><b>2</b>Your CV</li><li class="bar" aria-hidden="true"></li><li class="st"><b>3</b>Matches</li>
    </ol>
    <div class="head">
      <h1 class="display atitle">{words('Add your CV.')}</h1>
      <p class="asub rise" style="--d: 1;">JobMatcher reads it and fills in the rest of your sheet. You check everything before it is saved.</p>
    </div>
    <ul class="next rise" style="--d: 2;">
      <li><span class="ni">{DOC}</span>A PDF, or a photo or scan in JPEG, PNG or WEBP, up to 10 MB</li>
      <li><span class="ni">{TARGET}</span>Experience, skills, education and languages are read for you</li>
      <li><span class="ni">{UP}</span>Then you see the offers that fit you, best first</li>
    </ul>
  </section>
  <footer class="afoot"><span>© 2026 JobMatcher</span><a href="{home}">Back to the home page</a></footer>
  <div class="desk">
    <div class="aura a1" aria-hidden="true"></div><div class="aura a2" aria-hidden="true"></div>
    <div class="fwrap">
    <div class="sheet" id="sheet">
      <div class="kicker"><span>Curriculum vitae</span></div>
      <div class="stamp read" aria-hidden="true">CV<br>read</div>
      <div class="s-head">
        <span class="s-av done" aria-hidden="true">SE</span>
        <div class="s-name"><span class="s-nm">Salma El Idrissi</span><span class="s-me">salma@example.com</span></div>
      </div>
      <div class="zone" aria-live="polite">
        <label class="drop" data-z="empty" for="cvfile" id="drop">
          <span class="drop-ic">{UPDOC}</span>
          <p class="drop-t"><span class="d-desk">Drop your CV here</span><span class="d-phone">Choose your CV</span></p>
          <p class="drop-s">PDF, JPEG, PNG or WEBP, up to 10 MB</p>
          <span class="drop-b"><span class="pill ink">{FOLDER}Choose a file</span><button class="pill line cam" type="button" id="camb">{CAMERA}Take a photo</button></span>{sample}
        </label>
        <input class="vh" type="file" id="cvfile" accept=".pdf,.jpg,.jpeg,.png,.webp,application/pdf,image/jpeg,image/png,image/webp">
        <input class="vh" type="file" id="cvcam" accept="image/*" capture="environment">
        <div class="picked" data-z="file">
          <div class="fchip" style="--k: 0;"><span class="fdoc">CV<b id="fext">PDF</b></span><span style="min-width: 0;"><span class="fname" id="fname">CV_Salma_El_Idrissi.pdf</span><span class="fsize" id="fsize">412 KB</span></span><button class="fx" type="button" id="fremove" aria-label="Remove this file">{XMARK}</button></div>
          <button class="go" type="button" id="read" style="--k: 1;" data-state="idle"><span class="s-go">Read my CV{ARR}</span></button>
          <p class="alt" style="--k: 2;">Wrong file? <button type="button" id="again">Choose another one</button></p>
        </div>
        <div class="cvbody" data-z="read">
          <div class="scanl" aria-hidden="true"></div>
          <div class="sec"><span class="sl">Experience</span><div class="cell"><div class="ph" style="--t: 1;" aria-hidden="true"><i style="width: 92%;"></i><i style="width: 70%;"></i></div><div class="job rv-i" style="--t: 1; --k: 0;"><b>Data Analyst Intern · Attijariwafa bank</b><span>2025</span></div><div class="job rv-i" style="--t: 1; --k: 1;"><b>BI Assistant · OCP Group</b><span>2024</span></div></div></div>
          <div class="sec"><span class="sl">Skills</span><div class="cell"><div class="ph" style="--t: 2;" aria-hidden="true"><i style="width: 84%;"></i><i style="width: 56%;"></i></div><div class="chips">{chips}</div></div></div>
          <div class="sec"><span class="sl">Education</span><div class="cell"><div class="ph" style="--t: 3;" aria-hidden="true"><i style="width: 76%;"></i></div><div class="edu rv-i" style="--t: 3;"><b>Master, Big Data and IoT</b><span>ENSAM Casablanca</span></div></div></div>
          <div class="sec"><span class="sl">Languages</span><div class="cell"><div class="ph" style="--t: 3.6;" aria-hidden="true"><i style="width: 50%;"></i></div><div class="chips"><span class="c rv-i" style="--t: 3.6; --k: 0;">Arabic</span><span class="c rv-i" style="--t: 3.6; --k: 1;">French</span><span class="c rv-i" style="--t: 3.6; --k: 2;">English</span></div></div></div>
          <p class="status"><i class="spin"></i><span class="sw"><span>Reading your CV…</span><span>Finding your experience…</span><span>Listing your skills…</span><span>Almost done…</span></span></p>
        </div>
        <div class="donebar" data-z="done">
          <p class="found"><span class="ok">{TICK_S}</span><b>Found 2 jobs, 8 skills, 1 degree and 3 languages.</b></p>
          <a class="go" href="#review"><span class="s-go">Check your details{ARR}</span></a>
          <p class="alt">Not your best version? <button type="button" id="redo">Upload a different file</button></p>
        </div>
        <div class="oops" data-z="error" role="alert">
          <span class="oops-ic" style="--k: 0;">{WARN}</span>
          <h3 style="--k: 1;">We could not read this file</h3>
          <p id="errmsg" style="--k: 2;">Use a PDF, or a clear photo of your CV in JPEG, PNG or WEBP, up to 10 MB.</p>
          <button class="pill ink" type="button" id="retry" style="--k: 3;">{FOLDER}Choose another file</button>
        </div>
      </div>
    </div>
    </div>
    {PAUSE}
  </div>
</div>
</div>'''

JS = r'''<script>
(() => {
  const root = document.getElementById('auth'), input = document.getElementById('cvfile'), cam = document.getElementById('cvcam'), drop = document.getElementById('drop');
  const ok = ['application/pdf', 'image/jpeg', 'image/png', 'image/webp'], set = (s) => { root.dataset.state = s; };
  const size = (b) => b > 1048576 ? (b / 1048576).toFixed(1) + ' MB' : Math.max(1, Math.round(b / 1024)) + ' KB';
  const take = (f) => {
    if (!f) return;
    if (!ok.includes(f.type)) { document.getElementById('errmsg').textContent = 'This file type is not supported. Use a PDF, or a photo of your CV in JPEG, PNG or WEBP.'; return set('error'); }
    if (f.size > 10 * 1048576) { document.getElementById('errmsg').textContent = 'This file is larger than 10 MB. Try a smaller PDF, or a photo of your CV.'; return set('error'); }
    document.getElementById('fname').textContent = f.name; document.getElementById('fsize').textContent = size(f.size);
    document.getElementById('fext').textContent = (f.name.split('.').pop() || 'PDF').toUpperCase().slice(0, 4); set('file');
  };
  [input, cam].forEach((i) => i.addEventListener('change', () => { take(i.files[0]); i.value = ''; }));
  ['dragenter', 'dragover'].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); set('drag'); }));
  drop.addEventListener('dragleave', (e) => { if (!drop.contains(e.relatedTarget)) set('empty'); });
  drop.addEventListener('drop', (e) => { e.preventDefault(); set('empty'); take(e.dataTransfer.files[0]); });
  const pick = () => input.click();
  document.getElementById('camb').addEventListener('click', (e) => { e.preventDefault(); cam.click(); });
  ['again', 'retry', 'redo'].forEach((id) => document.getElementById(id).addEventListener('click', () => { set('empty'); pick(); }));
  document.getElementById('fremove').addEventListener('click', () => set('empty'));
  const s = document.getElementById('sample'); if (s) s.addEventListener('click', (e) => { e.preventDefault(); set('file'); });
  document.getElementById('read').addEventListener('click', () => { set('reading'); setTimeout(() => set('done'), 4800); });
})();
</script>'''

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
LOGO = 'data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%2048%2048%22%20width=%2248%22%20height=%2248%22%20fill=%22none%22%20stroke-linecap=%22round%22%20stroke-linejoin=%22round%22%3E%3Cdefs%3E%3CclipPath%20id=%22jmc%22%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22/%3E%3C/clipPath%3E%3C/defs%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20fill=%22%23CDBFFF%22/%3E%3Cpath%20d=%22M27.5%2020V17Q27.5%2014.5%2030%2014.5H35Q37.5%2014.5%2037.5%2017V20%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FFFFFF%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FF7F45%22%20clip-path=%22url%28%23jmc%29%22/%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Cpath%20d=%22M9.5%2011H19M9.5%2015.5H15%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.4%22/%3E%3Cpath%20d=%22M17%2029.5H44%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.2%22/%3E%3C/svg%3E'
P = f'{S}/nabta-canvas/project'
for Name, state, title in (('Upload', 'empty', 'JobMatcher add your CV'), ('UploadReading', 'reading', 'JobMatcher add your CV, reading'), ('UploadDone', 'done', 'JobMatcher add your CV, read')):
    open(f'{P}/{Name}.dc.html', 'w').write(DC.format(title=title, fonts=FONTS, css=CSS, body=body(LOGO, '#home', state), w=1440, h=900))
ph = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
open(f'{P}/UploadPhone.dc.html', 'w').write(DC.format(title='JobMatcher add your CV, phone width', fonts=FONTS, css='body{margin:0;background:#F6F5FB}\n',
     body=f'<div style="width: 390px; background: #F6F5FB;">\n  <dc-import name="Upload" hint-size="390px,{ph}px"></dc-import>\n</div>', w=390, h=ph))
pv = body('assets/nabta-mark.svg', 'index.html', 'empty', preview=True).replace('href="#review"', 'href="review.html" id="toreview"')
open(f'{S}/preview/upload.html', 'w').write(f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>JobMatcher Add Your CV</title>
{FONTS}
<style>
{CSS}</style>
</head>
<body>
{pv}
{JS}
</body>
</html>
''')
print('ok')
