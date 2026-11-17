# Your matches (dashboard) inside the app shell. Canvas boards + main preview page + standalone preview.
import sys, os, re, shutil
S = sys.argv[1]
A = f'{S}/auth'
src = open(f'{A}/auth2.py').read()
exec(src[src.index('def svg('):src.index('def signin(')])
CSS = open(f'{A}/auth2.css').read() + open(f'{A}/dash.css').read()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Outfit:wght@400;500;600;700&amp;display=swap">'
I = lambda d, w=20: svg(d, w=w, cls='')
IC = {
 'home': I('<path d="M4 11l8-7 8 7v9H4z"></path><path d="M10 20v-5h4v5"></path>'),
 'search': I('<circle cx="11" cy="11" r="6.5"></circle><path d="M16 16l4 4"></path>'),
 'saved': I('<path d="M7 4h10v16l-5-4-5 4z"></path>'),
 'applied': I('<path d="M4 12l16-8-6 16-3-6z"></path>'),
 'profile': I('<circle cx="12" cy="8" r="4"></circle><path d="M4 20c1.5-4 4.5-6 8-6s6.5 2 8 6"></path>'),
 'upload': I('<path d="M12 16V4M7 9l5-5 5 5"></path><path d="M5 20h14"></path>'),
}
BOOK = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M7 4h10v16l-5-4-5 4z"></path></svg>'
TKS = '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
POTY = {91: (16.3, 33.7), 88: (17.4, 32.6), 84: (18.8, 31.2), 79: (20.6, 29.4), 76: (21.9, 28.1), 72: (23.3, 26.7), 69: (24.4, 25.6), 64: (26.2, 23.8), 61: (27.3, 22.7), 58: (28.5, 21.5)}
def pot(p, w=28):
    h = round(37 * p / 100, 1); y = round(50 - h, 1)
    return f'<svg viewBox="0 0 48 56" width="{w}" height="{round(w*56/48)}" aria-hidden="true"><rect class="lvl" x="16" y="{y}" width="16" height="{h}" rx="1.5" fill="#FF7F45"></rect><rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" stroke-width="2.8"></rect><path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" stroke-width="2.8" stroke-linejoin="round"></path></svg>'
JOBS = [  # title, company, city, source, score, type, level, tags[(t, hit)], posted, salary, logo-class
 ('Data Analyst', 'CIH Bank', 'Casablanca', 'LinkedIn', 88, 'Full-time', 'Junior', [('Python', 1), ('SQL', 1), ('Power BI', 1)], '1 day ago', '', 'l2'),
 ('BI Developer', 'OCP Group', 'Casablanca', 'ANAPEC', 84, 'Full-time', 'Junior', [('Power BI', 1), ('SQL', 1), ('SAP BW', 0)], '2 days ago', '11,000 to 14,000 MAD', 'l3'),
 ('Ingénieur BI junior', 'Maroc Telecom', 'Rabat', 'ANAPEC', 79, 'Full-time', 'Junior', [('SQL', 1), ('Tableau', 1), ('Talend', 0)], '3 days ago', '', 'l1'),
 ('Stage PFE Data Science', 'inwi', 'Casablanca', 'LinkedIn', 76, 'Internship', 'Intern', [('Python', 1), ('Pandas', 1), ('PyTorch', 0)], 'Today', '', 'l4'),
 ('Data Scientist junior', 'Capgemini', 'Rabat', 'LinkedIn', 72, 'Full-time', 'Junior', [('Python', 1), ('Spark', 1), ('Airflow', 0)], '4 days ago', '', 'l2'),
 ('Analyste de données', 'Marjane', 'Casablanca', 'Jobzyn', 69, 'Full-time', 'Junior', [('Excel', 1), ('SQL', 1), ('Looker', 0)], '5 days ago', '9,000 to 11,000 MAD', 'l1'),
 ('ML Engineer', 'Deloitte', 'Casablanca', 'LinkedIn', 64, 'Contract', 'Mid', [('Python', 1), ('Airflow', 0), ('Docker', 0)], '1 week ago', '', 'l3'),
 ('Data Engineer', 'Remote team', 'Remote', 'Jobzyn', 61, 'Full-time', 'Mid', [('Spark', 1), ('Airflow', 0), ('Kafka', 0)], '1 week ago', '', 'l4'),
 ('Consultant BI', 'Avanade', 'Casablanca', 'Jobzyn', 58, 'Contract', 'Junior', [('Power BI', 1), ('DAX', 1), ('Azure', 0)], '1 week ago', '', 'l2'),
]
def initials(c):
    w = [x for x in re.split(r'\s+', c) if x]
    return (w[0][0] + (w[1][0] if len(w) > 1 else w[0][1])).upper()
def card(k, j, hidden=False):
    t, co, city, srcn, sc, typ, lvl, tags, posted, sal, lc = j
    tg = ''.join(f'<span class="t{" hit" if h else " miss"}">{x}</span>' for x, h in tags)
    sal_h = f' · {sal}' if sal else ''
    return f'''          <article class="mc{" hid" if hidden else ""}" style="--k: {k};" data-type="{typ}" data-level="{lvl}" data-city="{city}" data-src="{srcn}" data-text="{(t + ' ' + co + ' ' + ' '.join(x for x, _ in tags)).lower()}">
            <div class="mc-top"><span class="logo-c {lc}" aria-hidden="true">{initials(co)}</span><span class="mc-t"><b>{t}</b><span>{co} · {city}</span></span><span class="sc" role="img" aria-label="{sc}% match">{pot(sc)}<span class="num">{sc}<small>%</small></span></span></div>
            <div class="tags">{tg}</div>
            <div class="mc-b"><span><span class="src-b">{srcn}</span> {posted}{sal_h}</span><span class="acts2"><button class="sbtn" type="button" aria-pressed="false" aria-label="Save {t} at {co}">{BOOK}</button><a class="view" href="#job">View</a></span></div>
          </article>
'''
def chips(name, opts):
    return f'<div class="fg" role="group" aria-label="{name}"><span>{name}</span>' + ''.join(f'<button class="fc" type="button" data-f="{name.lower()}" data-v="{o}" aria-pressed="{"true" if i == 0 else "false"}">{o}</button>' for i, o in enumerate(opts)) + '</div>'

def body(logo, home, links):
    nav = [('home', 'Matches', links['dash'], True, ''), ('search', 'Search', '#search', False, ''), ('saved', 'Saved', '#saved', False, '3'), ('applied', 'Applied', '#applied', False, '1'), ('profile', 'Profile', '#profile', False, '')]
    navh = ''.join(f'<a class="nav-i{" on" if on else ""}" href="{h}"{" aria-current=\"page\"" if on else ""}>{IC[i]}<span>{t}</span>{f"<em class={chr(34)}b{chr(34)}>{b}</em>" if b else ""}</a>' for i, t, h, on, b in nav).replace('<em class="b">', '<span class="b">').replace('</em>', '</span>')
    tabs = ''.join(f'<a class="{"on" if on else ""}" href="{h}">{IC[i]}{t}</a>' for i, t, h, on, b in nav)
    cards = ''.join(card(k, j, hidden=k >= 6) for k, j in enumerate(JOBS))
    return f'''<div class="page">
<div class="app" id="app">
  <aside class="side" aria-label="Main">
    <a class="logo" href="{home}"><img src="{logo}" alt="" width="40" height="40"><span class="display">JobMatcher</span></a>
    {navh}
    <span class="sp"></span>
    <a class="newcv" href="{links['upload']}">{IC['upload']}<span><b>Upload a new CV</b>Your matches update after you check it.</span></a>
    <div class="me"><span class="s-av done" aria-hidden="true">SE</span><div><b>Salma El Idrissi</b><small>Junior · Casablanca</small></div></div>
  </aside>
  <main class="main">
    <div class="mtop"><a class="logo" href="{home}"><img src="{logo}" alt="" width="36" height="36"><span class="display">JobMatcher</span></a><span class="s-av done" aria-hidden="true">SE</span></div>
    <div class="top">
      <div class="hi"><small style="--d: 0;">Good morning, Salma.</small><h1 class="display" style="--d: 1;">Your matches.</h1><p style="--d: 2;"><b>84 offers</b> fit your CV. The best fit comes first.</p></div>
      <label class="srch" style="--d: 3;">{IC['search']}<input type="search" id="q" placeholder="Search by role, company or skill" aria-label="Search your matches"></label>
    </div>
    <div class="fbar" style="--d: 4;">
      {chips('Type', ['All', 'Full-time', 'Internship', 'Contract'])}
      {chips('Level', ['All', 'Intern', 'Junior', 'Mid'])}
      {chips('City', ['All', 'Casablanca', 'Rabat', 'Remote'])}
      {chips('Source', ['All', 'ANAPEC', 'Jobzyn', 'LinkedIn'])}
      <button class="clear" type="button" id="clear">Clear</button>
    </div>
    <div class="grid">
      <div class="feed">
        <article class="topm">
          <div class="aura a1" aria-hidden="true"></div>
          <span class="tag1"><i class="live"></i>Your best match today</span>
          <div class="bigscore" role="img" aria-label="91% match">{pot(91, 54)}<span class="num"><span class="n">91</span><small>%</small></span><span class="lb">Match</span></div>
          <h2>Data Engineer</h2>
          <span class="co">Attijariwafa bank · Casablanca · Jobzyn · posted 2 days ago</span>
          <div class="why"><b>Why it fits you</b>
            <span><i class="tk">{TKS}</i>3 of the 4 skills it asks for are on your CV: Python, Spark, SQL</span>
            <span><i class="tk">{TKS}</i>It is a junior role, like you</span>
            <span><i class="tk">{TKS}</i>It is in Casablanca, where you live</span>
            <span class="gap"><i class="tk"></i>It also asks for Airflow, which is not on your CV</span>
          </div>
          <div class="acts"><a class="go" href="{links['apply']}" style="text-decoration: none; color: #FFFFFF;"><span class="s-go">Prepare application{ARR}</span></a><button class="ibtn" type="button" aria-pressed="false" aria-label="Save Data Engineer at Attijariwafa bank">{BOOK}</button><a class="txtl" href="#job">View the offer</a></div>
          {host('signin')}
        </article>
        <div class="lhead"><h3>More matches</h3><span id="shown">Showing 6 of 84</span></div>
        <div class="cards" id="cards">
{cards}        </div>
        <div class="empty" id="empty"><h4>No matches with these filters</h4><p>Try another city or level, or clear the filters to see all 84 offers that fit your CV.</p><button class="more" type="button" id="clear2">Clear the filters</button></div>
        <button class="more" type="button" id="more">Show more matches</button>
        <p class="note">Example offers, to show how matches look.</p>
      </div>
      <aside class="aside" aria-label="Your week">
        <section class="pbox" style="--d: 0;"><h4>This week</h4><div class="stats"><div class="stat"><b>24</b><span>new offers</span></div><div class="stat"><b id="savedn">3</b><span>saved</span></div><div class="stat"><b>1</b><span>applied</span></div></div></section>
        <section class="pbox tip" style="--d: 1;"><h4>Make your matches better</h4><p><b>4 of your matches</b> ask for Airflow. If you have used it, add it to your profile and those offers move up.</p><div class="row"><a class="pill2" href="{links['review']}">Add Airflow</a><button class="pill2 pill3" type="button">Not now</button></div></section>
        <section class="pbox" style="--d: 2;"><h4>Where your matches come from</h4><div class="srcs2"><div class="srow"><span>LinkedIn</span><i style="--w: 46%;"></i><b>39</b></div><div class="srow"><span>ANAPEC</span><i style="--w: 31%;"></i><b>26</b></div><div class="srow"><span>Jobzyn</span><i style="--w: 23%;"></i><b>19</b></div></div></section>
      </aside>
    </div>
  </main>
  <nav class="tabs" aria-label="Main">{tabs}</nav>
</div>
</div>'''

JS = r'''<script>
(() => {
  const cards = [...document.querySelectorAll('.mc')], q = document.getElementById('q'), more = document.getElementById('more'), empty = document.getElementById('empty'), shown = document.getElementById('shown');
  const f = { type: 'All', level: 'All', city: 'All', source: 'All' }; let limit = 6;
  const apply = () => {
    const text = q.value.trim().toLowerCase(); let n = 0, vis = 0;
    cards.forEach((c) => {
      const ok = (f.type === 'All' || c.dataset.type === f.type) && (f.level === 'All' || c.dataset.level === f.level) && (f.city === 'All' || c.dataset.city === f.city) && (f.source === 'All' || c.dataset.src === f.source) && (!text || c.dataset.text.includes(text));
      const show = ok && n < limit; if (ok) n++; const was = !c.classList.contains('hid');
      c.classList.toggle('hid', !show); if (show && !was) { c.classList.remove('shown'); void c.offsetWidth; c.classList.add('shown'); } if (show) vis++;
    });
    empty.classList.toggle('on', n === 0); more.hidden = n <= limit; shown.textContent = n === 0 ? 'No matches' : 'Showing ' + vis + ' of ' + (text || Object.values(f).some((v) => v !== 'All') ? n : 84);
  };
  document.querySelectorAll('.fc').forEach((b) => b.addEventListener('click', () => {
    f[b.dataset.f] = b.dataset.v; b.parentElement.querySelectorAll('.fc').forEach((x) => x.setAttribute('aria-pressed', String(x === b))); limit = 6; apply();
  }));
  const clear = () => { Object.keys(f).forEach((k) => { f[k] = 'All'; }); document.querySelectorAll('.fg').forEach((g) => g.querySelectorAll('.fc').forEach((x, i) => x.setAttribute('aria-pressed', String(i === 0)))); q.value = ''; limit = 6; apply(); };
  document.getElementById('clear').addEventListener('click', clear); document.getElementById('clear2').addEventListener('click', clear);
  q.addEventListener('input', apply);
  more.addEventListener('click', () => { limit += 6; apply(); });
  const savedn = document.getElementById('savedn');
  document.querySelectorAll('.sbtn, .ibtn').forEach((b) => b.addEventListener('click', () => {
    const on = b.getAttribute('aria-pressed') !== 'true'; b.setAttribute('aria-pressed', String(on)); b.classList.remove('popd'); void b.offsetWidth; b.classList.add('popd');
    savedn.textContent = +savedn.textContent + (on ? 1 : -1);
  }));
})();
</script>'''

DCs = open(f'{A}/upload.py').read()
DC = DCs[DCs.index("DC = '''") + 8:DCs.index("'''", DCs.index("DC = '''") + 8)]
LOGO = 'data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%2048%2048%22%20width=%2248%22%20height=%2248%22%20fill=%22none%22%20stroke-linecap=%22round%22%20stroke-linejoin=%22round%22%3E%3Cdefs%3E%3CclipPath%20id=%22jmc%22%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22/%3E%3C/clipPath%3E%3C/defs%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20fill=%22%23CDBFFF%22/%3E%3Cpath%20d=%22M27.5%2020V17Q27.5%2014.5%2030%2014.5H35Q37.5%2014.5%2037.5%2017V20%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FFFFFF%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FF7F45%22%20clip-path=%22url%28%23jmc%29%22/%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Cpath%20d=%22M9.5%2011H19M9.5%2015.5H15%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.4%22/%3E%3Cpath%20d=%22M17%2029.5H44%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.2%22/%3E%3C/svg%3E'
P = f'{S}/nabta-canvas/project'
H = int(sys.argv[2]) if len(sys.argv) > 2 else 1300
PH = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
canvas_links = {'dash': '#matches', 'upload': '#upload', 'apply': '#apply', 'review': '#review'}
open(f'{P}/Dashboard.dc.html', 'w').write(DC.format(title='JobMatcher your matches', fonts=FONTS, css=CSS, body=body(LOGO, '#home', canvas_links), w=1440, h=H))
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
{JS}
</body>
</html>
'''
open(f'{S}/preview/dashboard.html', 'w').write(page('index.html', {'dash': 'dashboard.html', 'upload': 'upload.html', 'apply': '#apply', 'review': 'review.html'}, 'JobMatcher Your Matches'))
os.makedirs(f'{S}/dash-standalone/assets', exist_ok=True)
shutil.copy(f'{S}/preview/assets/nabta-mark.svg', f'{S}/dash-standalone/assets/nabta-mark.svg')
full = page('#top', {'dash': '#top', 'upload': '#top', 'apply': '#top', 'review': '#top'}, 'JobMatcher Your Matches')
head = re.search(r'<head>(.*?)</head>', full, re.S).group(1)
head = re.sub(r'<meta charset="utf-8">|<meta name="viewport"[^>]*>', '', head).strip()
t = re.search(r'<title>.*?</title>', head).group(0); head = head.replace(t, '').strip()
bod = re.search(r'<body>(.*)</body>', full, re.S).group(1).strip()
open(f'{S}/dash-standalone/index.html', 'w').write(t + '\n' + head + '\n' + bod + '\n')
print('ok')
