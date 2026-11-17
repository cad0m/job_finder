# Prepare application v2: the CV is the hero on a lavender stage, a guide narrates, designs morph with view transitions.
import sys, os, re, shutil
S = sys.argv[1]
A = f'{S}/auth'
src = open(f'{A}/auth2.py').read()
exec(src[src.index('def svg('):src.index('def signin(')])
a1 = open(f'{A}/apply.py').read()
exec(a1[a1.index('TKS = '):a1.index('def sheet(')])
CSS = open(f'{A}/auth2.css').read() + open(f'{A}/apply.css').read() + open(f'{A}/apply2.css').read() + open(f'{A}/apply3.css').read() + open(f'{A}/apply4.css').read()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Outfit:wght@400;500;600;700&amp;display=swap">'
CVTXT = {
 'en': dict(loc='Casablanca, Morocco', H=['Profile', 'Experience', 'Education', 'Skills', 'Languages'],
   sum='Data analyst moving into data engineering. I build batch pipelines in {P} and {S}, model data in {Q} and hand clean tables to reporting teams. Master\'s student in Big Data and IoT.',
   j1=('Data Analyst Intern', 'Feb to Jul 2025', ['Automated the weekly {Q} reports for the retail credit team', 'Built {P} jobs that load data for twelve Power BI dashboards', 'Moved a slow Excel process to a {S} batch job']),
   j2=('BI Assistant', 'Jul to Sep 2024', ['Cleaned and modelled production data in {P}', 'Documented every data source used by the plant reports']),
   edu=[('Master, Big Data and IoT', 'ENSAM Casablanca, 2024 to 2026'), ('Licence, Maths and CS', 'FST Mohammedia, 2021 to 2024'), ('Certification', 'Microsoft Power BI Data Analyst, 2025')],
   lng='Arabic, native<br>French, fluent<br>English, professional'),
 'fr': dict(loc='Casablanca, Maroc', H=['Profil', 'Expérience', 'Formation', 'Compétences', 'Langues'],
   sum='Analyste de données qui évolue vers le data engineering. Je construis des pipelines batch en {P} et {S}, je modélise les données en {Q} et je livre des tables propres aux équipes de reporting. Étudiante en Master Big Data et IoT.',
   j1=('Stagiaire Data Analyst', 'févr. à juil. 2025', ['Automatisation des rapports {Q} hebdomadaires de l\'équipe crédit', 'Jobs {P} qui alimentent douze tableaux de bord Power BI', 'Migration d\'un traitement Excel lent vers un job {S}']),
   j2=('Assistante BI', 'juil. à sept. 2024', ['Nettoyage et modélisation des données de production en {P}', 'Documentation de toutes les sources des rapports de l\'usine']),
   edu=[('Master Big Data et IoT', 'ENSAM Casablanca, 2024 à 2026'), ('Licence Maths et Informatique', 'FST Mohammedia, 2021 à 2024'), ('Certification', 'Microsoft Power BI Data Analyst, 2025')],
   lng='Arabe, langue maternelle<br>Français, courant<br>Anglais, professionnel'),
}
def cv_inner(lang='en', marks=False):
    c = CVTXT[lang]
    m = (lambda x: f'<span class="mark">{x}</span>') if marks else (lambda x: x)
    f = lambda s: s.replace('{P}', m('Python')).replace('{S}', m('Spark')).replace('{Q}', m('SQL'))
    job = lambda j, co: f'<div class="j"><b>{j[0]}<span>{j[1]}</span></b><em>{co}</em><ul>' + ''.join(f'<li>{f(x)}</li>' for x in j[2]) + '</ul></div>'
    edu = ''.join(f'<p{" class=" + chr(34) + "crt" + chr(34) if i == 2 else ""}><b>{a}</b><br>{b}</p>' for i, (a, b) in enumerate(c['edu']))
    return f'''<div class="s h" style="grid-area:h"><span class="nm">Salma El Idrissi</span><span class="hl">Data Engineer</span></div>
      <div class="s ct" style="grid-area:ct">salma@example.com<br>+212 6 12 34 56 78<br>{c['loc']}<br>linkedin.com/in/salma-elidrissi</div>
      <div class="s sum" style="grid-area:sum"><h6>{c['H'][0]}</h6><p>{f(c['sum'])}</p></div>
      <div class="s exp" style="grid-area:exp"><h6>{c['H'][1]}</h6>{job(c['j1'], 'Attijariwafa bank, Casablanca')}{job(c['j2'], 'OCP Group, Casablanca')}</div>
      <div class="s edu" style="grid-area:edu"><h6>{c['H'][2]}</h6>{edu}</div>
      <div class="s skl" style="grid-area:skl"><h6>{c['H'][3]}</h6><p>{m("Python")} · {m("Spark")} · {m("SQL")} · Power BI · Pandas · Git · Excel · Tableau</p></div>
      <div class="s lng" style="grid-area:lng"><h6>{c['H'][4]}</h6><p>{c['lng']}</p></div>
      <div class="s side" style="grid-area:side"></div>'''
LETTER_FR = '''<div class="ltr" aria-hidden="true"><div class="lin">
      <div class="from"><b>Salma El Idrissi</b><span>salma@example.com · +212 6 12 34 56 78 · Casablanca</span></div>
      <p>Casablanca, le 17 novembre 2026</p>
      <p>Attijariwafa bank<br>Équipe data platform</p>
      <p>Madame, Monsieur,</p>
      <p>Je vous propose ma candidature au poste de Data Engineer au sein de votre équipe data platform. Pendant mon stage chez Attijariwafa bank, j'ai automatisé les rapports SQL hebdomadaires de l'équipe crédit et construit des jobs Python qui alimentent Power BI. Je sais donc combien les équipes risque et marketing dépendent de données propres et à jour.</p>
      <p>Je construis des pipelines batch en Python et Spark et je modélise les données en SQL. Je n'ai pas encore utilisé Airflow en production : j'ai planifié des jobs avec cron, et je serais heureuse de l'apprendre avec votre équipe.</p>
      <p>Je serais ravie d'échanger sur la façon dont je peux vous aider à amener vos données bancaires vers le data lake.</p>
      <p>Je vous prie d'agréer, Madame, Monsieur, mes salutations distinguées.<br>Salma El Idrissi</p>
    </div></div>'''
SUBJECT_FR = 'Candidature au poste de Data Engineer, Salma El Idrissi'
BODY_FR = '''Bonjour,

Je vous propose ma candidature au poste de Data Engineer au sein de votre équipe data platform. Vous trouverez ci-joint mon CV et une lettre de motivation.

Pendant mon stage chez Attijariwafa bank, j'ai automatisé des rapports SQL et construit des jobs Python pour Power BI. Je serais heureuse d'apporter cette expérience à votre équipe.

Cordialement,
Salma El Idrissi
+212 6 12 34 56 78'''
def mailbox(sub, body):
    return f'<div class="mrow"><span>To</span><b>The recruiter, from the original post</b><span></span></div><div class="mrow"><span>Subject</span><b id="msub">{sub}</b><button class="copy" type="button" data-copy="sub">{COPY}Copy</button></div><p class="mbody" id="mbody">{body}</p><div><button class="copy" type="button" data-copy="all">{COPY}Copy subject and message</button></div>'
def cvdoc(t, marks=False, lang='en'):
    return f'<div class="cvd {t}" aria-hidden="true"><div class="in">{cv_inner(lang, marks)}</div></div>'
def cvdoc_old(t, marks=False):
    m = (lambda x: f'<span class="mark">{x}</span>') if marks else (lambda x: x)
    return f'''<div class="cvd {t}" aria-hidden="true"><div class="in">
      <div class="s h" style="grid-area:h"><span class="nm">Salma El Idrissi</span><span class="hl">Data Engineer</span></div>
      <div class="s ct" style="grid-area:ct">salma@example.com<br>+212 6 12 34 56 78<br>Casablanca, Morocco<br>linkedin.com/in/salma-elidrissi</div>
      <div class="s sum" style="grid-area:sum"><h6>Profile</h6><p>Data analyst moving into data engineering. I build batch pipelines in {m("Python")} and {m("Spark")}, model data in {m("SQL")} and hand clean tables to reporting teams. Master's student in Big Data and IoT.</p></div>
      <div class="s exp" style="grid-area:exp"><h6>Experience</h6>
        <div class="j"><b>Data Analyst Intern<span>Feb to Jul 2025</span></b><em>Attijariwafa bank, Casablanca</em><ul><li>Automated the weekly {m("SQL")} reports for the retail credit team</li><li>Built {m("Python")} jobs that load data for twelve Power BI dashboards</li><li>Moved a slow Excel process to a {m("Spark")} batch job</li></ul></div>
        <div class="j"><b>BI Assistant<span>Jul to Sep 2024</span></b><em>OCP Group, Casablanca</em><ul><li>Cleaned and modelled production data in {m("Python")}</li><li>Documented every data source used by the plant reports</li></ul></div></div>
      <div class="s edu" style="grid-area:edu"><h6>Education</h6><p><b>Master, Big Data and IoT</b><br>ENSAM Casablanca, 2024 to 2026</p><p><b>Licence, Maths and CS</b><br>FST Mohammedia, 2021 to 2024</p><p class="crt"><b>Certification</b><br>Microsoft Power BI Data Analyst, 2025</p></div>
      <div class="s skl" style="grid-area:skl"><h6>Skills</h6><p>{m("Python")} · {m("Spark")} · {m("SQL")} · Power BI · Pandas · Git · Excel · Tableau</p></div>
      <div class="s lng" style="grid-area:lng"><h6>Languages</h6><p>Arabic, native<br>French, fluent<br>English, professional</p></div>
      <div class="s side" style="grid-area:side"></div>
    </div></div>'''
ICONS = {
 't1': '<svg viewBox="0 0 20 20" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><rect x="3.5" y="2" width="13" height="16" rx="2"></rect><path d="M7 6h6M6.5 9h7M6.5 12h7M6.5 15h5"></path></svg>',
 't2': '<svg viewBox="0 0 20 20" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><rect x="3.5" y="2" width="13" height="16" rx="2"></rect><path d="M6 6h4.5M6 9h4.5M6 12h4.5M12.5 6h1.5M12.5 9h1.5"></path></svg>',
 't3': '<svg viewBox="0 0 20 20" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><rect x="3.5" y="2" width="13" height="16" rx="2"></rect><path d="M4.5 3h3.5v14H4.5z" fill="currentColor" stroke="none"></path><path d="M10.5 6h4M10.5 9h4M10.5 12h4"></path></svg>',
 't4': '<svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><text x="10" y="14.5" text-anchor="middle" font-family="Georgia, serif" font-size="12.5" font-weight="700" fill="currentColor">Aa</text></svg>',
 't5': '<svg viewBox="0 0 20 20" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><rect x="3.5" y="2" width="13" height="16" rx="2"></rect><path d="M4.5 6h3.5v11H4.5z" fill="currentColor" stroke="none" opacity=".35"></path><path d="M7 4.5h6M10.5 9h4M10.5 12h4"></path></svg>',
}
PREV = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"></path></svg>'
NEXT = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"></path></svg>'
ZOOM = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"></circle><path d="M16 16l4 4M11 8v6M8 11h6"></path></svg>'
CHEV2 = '<svg class="chev2" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"></path></svg>'
TKW = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#FFFFFF" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"></path></svg>'
GUIDE = open(f'{S}/peeps-render/auth/g3.svg').read().strip().replace('<svg xmlns="http://www.w3.org/2000/svg" ', '<svg class="guide" aria-hidden="true" focusable="false" ', 1)
MINIG = re.sub(r'viewBox="[^"]*"', 'viewBox="230 -30 470 470"', GUIDE.replace('class="guide"', 'class="guide-mini"', 1), count=1)
TIPS = {
 't1': ('Classic', 'One column', 'Classic is the safest template. It reads well in any office, from banks to public institutions.'),
 't2': ('Two columns', 'Light, airy', 'Two columns puts contact and skills on the right and gives your experience room.'),
 't3': ('Dark sidebar', 'Skills in view', 'Dark sidebar keeps your skills in view. Someone looking for Python sees it in a second.'),
 't4': ('Formal serif', 'Printed feel', 'Formal serif reads like a printed letter. A good fit for consulting and large groups.'),
 't5': ('Warm sidebar', 'Soft colours', 'Warm sidebar is soft and easy to read, even on a phone screen.'),
}
WRITE_TIPS = ['I am putting Python, Spark and SQL first, because the offer asks for them.', 'Now a letter to the data platform team, in your words.', 'A short email to send with both files.', 'Turning everything into PDFs.']
READY_TIP = 'All set. Read it once, then send it from your own email.'

def body(logo, links, step='setup', tpl='t3'):
    rows = ''.join(f'''<label class="trow" style="--k: {i};"><input type="radio" name="tpl" value="{t}"{" checked" if t == tpl else ""}><span class="tth">{cvdoc(t)}</span><span><b>{n}{" <em>Suggested</em>" if t == "t3" else ""}</b><small>{d}</small></span><span class="tck">{TKW}</span></label>''' for i, (t, (n, d, _)) in enumerate(TIPS.items()))
    on = {'setup': 1, 'writing': 2, 'ready': 3}[step]
    def st(i, label):
        cls = 'on' if i == on else ('ok' if i < on else '')
        return f'<li class="{cls}" data-s="{i}"><b>{"✓" if i < on else i}</b><span>{label}</span></li>'
    tip = {'setup': TIPS[tpl][2], 'writing': WRITE_TIPS[0], 'ready': READY_TIP}[step]
    face = {'setup': 'open', 'writing': 'focus', 'ready': 'happy'}[step]
    return f'''<div class="page">
<div class="studio" id="studio" data-step="{step}" data-face="{face}">
  <header class="stop">
    <a class="back" href="{links['dash']}">{BACK}<span>Back to your matches</span></a>
    <ol class="psteps" aria-label="Progress">{st(1, 'Set up')}{st(2, 'Writing')}{st(3, 'Ready')}</ol>
    <div class="ochip"><span class="logo-c l1" aria-hidden="true">AB</span><span><b>Data Engineer</b><span>Attijariwafa bank</span></span><span class="cupv">{cup(91, 18)}91<small>%</small></span></div>
  </header>
  <div class="st2">
    <div class="ctrl">
      <section class="cpane c-setup" aria-labelledby="h1s">
        <div class="cscroll">
          <span class="kick2" style="--d: 0;">Step 1 of 3</span>
          <h1 class="display" id="h1s" style="--d: 1;">Choose a CV template.</h1>
          <p class="lead3" style="--d: 2;">Every template shows your real CV. Switch between them above the preview, or swipe it on a phone.</p>
          <div class="offer2" style="--d: 3;"><div class="o-h"><span><b>Data Engineer</b><small>Attijariwafa bank · Casablanca</small></span><span class="o-c">{cup(91, 22)}91<small>%</small></span></div>
            <span class="chips2"><span class="c2 hit">Python</span><span class="c2 hit">Spark</span><span class="c2 hit">SQL</span></span>
            <p>These go first, marked in orange on the CV. <b>Airflow is not on your CV</b>, so it will not be added.</p><a class="editl" href="{links['review']}">Something wrong in your CV? Edit your details</a></div>
          <div class="langsel" style="--d: 3;"><span class="ls-l">Language of your documents</span><div class="seg5" role="radiogroup" aria-label="Language of your documents"><label><input type="radio" name="dlang" value="en" checked><b>English</b><small>Like the offer</small></label><label><input type="radio" name="dlang" value="fr"><b>Français</b><small>CV, letter, email</small></label></div></div>
          <details class="lkd" style="--d: 4;"><summary><span>Links on your CV <small>· 1 of 3</small></span>{CHEV2}</summary>
            <div class="lnks">
              <div class="lk"><label for="ln-li">LinkedIn</label><div class="pre2"><span>linkedin.com/in/</span><input id="ln-li" value="salma-elidrissi"></div></div>
              <div class="lk"><label for="ln-gh">GitHub</label><div class="pre2"><span>github.com/</span><input id="ln-gh" placeholder="username"></div></div>
              <div class="lk"><label for="ln-pf">Portfolio</label><div class="pre2"><span>https://</span><input id="ln-pf" placeholder="yoursite.ma"></div></div>
            </div></details>
          <ul class="get" style="--d: 5;"><li><i>CV</i>A CV tailored to this offer</li><li><i>CL</i>A cover letter to the company</li><li><i>EM</i>An email to send with both</li></ul>
        </div>
        <div class="cta2" style="--d: 5;"><button class="go write" type="button"><span class="s-go">Write my application{ARR}</span></button><small>A CV, a cover letter and an email. About a minute.</small></div>
      </section>
      <section class="cpane c-writing" aria-labelledby="h1w" aria-live="polite">
        <div class="cscroll">
          <span class="kick2">Step 2 of 3</span>
          <h1 class="display" id="h1w">Writing your application.</h1>
          <div class="wcup"><span class="bigcup">{cup(100, 52).replace('class="lvl"', 'class="lvl" id="wlvl" style="transform-box: fill-box; transform-origin: 50% 100%; transform: scaleY(0);"')}<span id="wpct">0</span><small>%</small></span></div>
          <ol class="wsteps2" id="wsteps"><li class="now"><i></i><span>Tailoring your CV<small>Your matched skills go first</small></span></li><li><i></i><span>Writing the cover letter<small>Addressed to the data platform team</small></span></li><li><i></i><span>Drafting the email<small>Short, with both files attached</small></span></li><li><i></i><span>Making the PDFs<small>One page each</small></span></li></ol>
          <p class="lead2">You can leave; it will wait for you in <a href="{links['applied']}" style="color: var(--ink); font-weight: 600;">Applied</a>.</p>
        </div>
      </section>
      <section class="cpane c-ready" aria-labelledby="h1r">
        <div class="cscroll">
          <span class="kick2">Step 3 of 3</span>
          <h1 class="display" id="h1r">Ready to send.</h1>
          <div class="dlist" role="tablist" aria-label="Documents">
            <button class="ditem" role="tab" aria-selected="true" data-doc="cv"><span class="di">CV</span><span><b>CV</b><small>Salma_El_Idrissi_CV.pdf · 1 page</small></span><span class="dl2 dl" role="button" aria-label="Download the CV">{DL}</span></button>
            <button class="ditem" role="tab" aria-selected="false" data-doc="cl"><span class="di">CL</span><span><b>Cover letter</b><small>Salma_El_Idrissi_Letter.pdf · 1 page</small></span><span class="dl2 dl" role="button" aria-label="Download the cover letter">{DL}</span></button>
            <button class="ditem" role="tab" aria-selected="false" data-doc="em"><span class="di">EM</span><span><b>Email</b><small>Subject and message to copy</small></span><span class="dl2" aria-hidden="true">{COPY}</span></button>
          </div>
          <div class="racts2"><a class="go" href="{links['applied']}"><span class="s-go">Done{ARR}</span></a><button class="ghost3 dlall" type="button">{DL}Download all</button></div>
          <div class="ready-more"><button class="chdesign" type="button" id="chdesign">Change the template</button><button class="chdesign" type="button" id="again">Write it again</button></div>
        </div>
      </section>
    </div>
    <section class="stage3" id="stage" data-doc="cv" aria-label="Preview">
      <div class="tbar" role="group" aria-labelledby="tb-l"><div class="tb-l" id="tb-l"><b>CV template</b><span id="tpos">{list(TIPS).index(tpl) + 1} of 5</span></div><button class="arw" type="button" data-step="-1" aria-label="Previous template">{PREV}</button><div class="tstrip" role="radiogroup" aria-label="CV template">{''.join(f'<label class="tthumb"><input type="radio" name="tpl" value="{k}"{" checked" if k == tpl else ""}><span class="tt-doc">{cvdoc(k)}{"<em class=" + chr(34) + "sug" + chr(34) + ">Suggested</em>" if k == "t3" else ""}<i class="tt-ck">{TKW}</i></span><span class="tt-n">{v[0]}</span></label>' for k, v in TIPS.items())}</div><button class="arw" type="button" data-step="1" aria-label="Next template">{NEXT}</button></div>
      <div class="paper" id="paper">
        <div class="layer l-cv big" id="bigcv">{cvdoc(tpl, marks=True)}</div>
        <div class="layer l-cl">{LETTER}</div>
        <div class="layer l-em"><div class="mail">{mailbox(SUBJECT, BODY)}</div></div>
        <div class="pen" id="pen" aria-hidden="true"></div>
        <button class="zoomb" type="button" id="zoomb">{ZOOM}View full size</button>
        {GUIDE}
        <div class="bubble" role="status"><b>Your guide</b><span class="bt" id="tip">{tip}</span></div>
      </div>
      <div class="tipbar"><span class="mini-g">{MINIG}</span><p id="tip2">{tip}</p></div>
      <div class="pdfs" aria-hidden="true"><span>CV.pdf</span><span>Letter.pdf</span><span>Email</span></div>
      <div class="stamp2" aria-hidden="true">Ready<br>to<br>send</div>
    </section>
  <template id="cv-en">{cv_inner('en', True)}</template><template id="cv-fr">{cv_inner('fr', True)}</template>
  <template id="cl-en">{LETTER}</template><template id="cl-fr">{LETTER_FR}</template>
  <template id="em-en">{mailbox(SUBJECT, BODY)}</template><template id="em-fr">{mailbox(SUBJECT_FR, BODY_FR)}</template>
  <dialog class="zoom" id="zoom" aria-label="Your CV at full size"><div class="zbar"><b>Your CV</b><button class="zx" type="button" id="zx" aria-label="Close">×</button></div><div class="zbody"><div class="zdoc" id="zdoc"></div></div></dialog>
  </div>
  <div class="toast" id="toast" role="status" hidden></div>
</div>
</div>'''

JS = r'''<script>
(() => {
  const st = document.getElementById('studio'), stage = document.getElementById('stage'), big = document.getElementById('bigcv'), tip = document.getElementById('tip');
  const TIPS = __TIPS__, WT = __WT__, RT = __RT__;
  const toast = document.getElementById('toast'); let tt;
  const paper = document.getElementById('paper'), radios = [...document.querySelectorAll('input[name="tpl"]')];
  const pick = (d) => { const i = radios.findIndex((r) => r.checked); const n = radios[(i + d + radios.length) % radios.length]; n.checked = true; n.dispatchEvent(new Event('change')); n.closest('.dpill').scrollIntoView({ inline: 'center', block: 'nearest', behavior: 'smooth' }); };
  document.querySelectorAll('.arw').forEach((b) => b.addEventListener('click', () => pick(+b.dataset.step)));
  let sx = null; paper.addEventListener('pointerdown', (e) => { sx = e.clientX; });
  paper.addEventListener('pointerup', (e) => { if (sx !== null && st.dataset.step === 'setup' && Math.abs(e.clientX - sx) > 50) pick(e.clientX < sx ? 1 : -1); sx = null; });
  const zoom = document.getElementById('zoom');
  document.getElementById('zoomb').addEventListener('click', () => { const d = stage.dataset.doc === 'cl' ? document.querySelector('.l-cl .ltr') : big.querySelector('.cvd'); document.getElementById('zdoc').innerHTML = d.outerHTML; zoom.showModal(); });
  document.getElementById('zx').addEventListener('click', () => zoom.close());
  const pen = document.getElementById('pen'); const runPen = () => { pen.classList.remove('run'); void pen.offsetWidth; pen.classList.add('run'); };

  const say = (t) => { toast.textContent = t; toast.hidden = false; toast.style.animation = 'none'; void toast.offsetWidth; toast.style.animation = ''; clearTimeout(tt); tt = setTimeout(() => { toast.hidden = true; }, 3000); };
  let ft;
  const tip2 = document.getElementById('tip2'), gd = document.querySelector('.paper .guide');
  const speak = (text, after = 'open') => { [tip, tip2].forEach((x) => { x.textContent = text; x.classList.remove('swap'); void x.offsetWidth; x.classList.add('swap'); }); if (gd) { gd.classList.remove('nod'); void gd.getBoundingClientRect(); gd.classList.add('nod'); } st.dataset.face = 'talk'; clearTimeout(ft); ft = setTimeout(() => { st.dataset.face = after; }, 900); };
  const setStep = (s) => {
    st.dataset.step = s; const n = { setup: 1, writing: 2, ready: 3 }[s];
    document.querySelectorAll('.psteps li').forEach((li) => { const i = +li.dataset.s; li.className = i === n ? 'on' : i < n ? 'ok' : ''; li.querySelector('b').textContent = i < n ? '✓' : i; });
  };
  const tpl = () => document.querySelector('input[name="tpl"]:checked').value;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const setDoc = (d) => { const go = () => { stage.dataset.doc = d; }; go(); document.querySelectorAll('.ditem').forEach((x) => x.setAttribute('aria-selected', String(x.dataset.doc === d))); };
  /* switching designs: every section glides to its place in the new layout */
  document.querySelectorAll('input[name="tpl"]').forEach((r) => r.addEventListener('change', () => {
    const doc = big.querySelector('.cvd'); const t = r.value;
    const apply = () => { doc.className = 'cvd ' + t; };
    if (document.startViewTransition && !reduce) document.startViewTransition(apply); else { apply(); doc.classList.add('flash'); setTimeout(() => doc.classList.remove('flash'), 600); }
    if (stage.dataset.doc !== 'cv') setDoc('cv');
    paper.classList.remove('lift'); void paper.offsetWidth; paper.classList.add('lift');
    speak(TIPS[t]);
  }));
  /* writing: the CV builds, the letter and the email follow, the cup fills */
  const steps = [...document.querySelectorAll('#wsteps li')], pct = document.getElementById('wpct'), lvl = document.getElementById('wlvl');
  const write = () => {
    setStep('writing'); setDoc('cv'); st.classList.add('writing-on'); st.classList.remove('marks-on');
    document.querySelectorAll('.big .cvd .s, .l-cl .lin > *, .l-em .mail > *, .pdfs span').forEach((x) => x.classList.remove('shw'));
    steps.forEach((li, i) => { li.className = i === 0 ? 'now' : ''; });
    speak(WT[0], 'focus'); runPen();
    const T = reduce ? 800 : 9400, t0 = performance.now();
    const tick = (now) => { const p = Math.min(1, (now - t0) / T); pct.textContent = Math.round(p * 100); lvl.style.transform = `scaleY(${p})`; if (p < 1 && st.dataset.step === 'writing') requestAnimationFrame(tick); };
    requestAnimationFrame(tick);
    const at = (ms, fn) => setTimeout(() => { if (st.dataset.step === 'writing') fn(); }, reduce ? Math.min(ms, 700) : ms);
    const secs = ['.h', '.ct', '.sum', '.exp', '.edu', '.skl', '.lng', '.side'];
    secs.forEach((s, i) => at(250 + i * 330, () => big.querySelector('.cvd ' + s).classList.add('shw')));
    at(2700, () => st.classList.add('marks-on'));
    at(3700, () => { setDoc('cl'); setTimeout(runPen, 350); steps[0].className = 'done'; steps[1].className = 'now'; speak(WT[1], 'focus'); });
    [...document.querySelectorAll('.l-cl .lin > *')].forEach((x, i) => at(4000 + i * 280, () => x.classList.add('shw')));
    at(6500, () => { setDoc('em'); setTimeout(runPen, 350); steps[1].className = 'done'; steps[2].className = 'now'; speak(WT[2], 'focus'); });
    [...document.querySelectorAll('.l-em .mail > *')].forEach((x, i) => at(6800 + i * 280, () => x.classList.add('shw')));
    at(8000, () => { setDoc('cv'); steps[2].className = 'done'; steps[3].className = 'now'; speak(WT[3], 'focus'); });
    [...document.querySelectorAll('.pdfs span')].forEach((x, i) => at(8300 + i * 300, () => x.classList.add('shw')));
    at(9600, () => { steps[3].className = 'done'; st.classList.remove('writing-on'); st.classList.add('marks-on'); setStep('ready'); speak(RT, 'happy'); });
  };
  document.querySelectorAll('.write').forEach((b) => b.addEventListener('click', write));
  document.querySelectorAll('.ditem').forEach((d) => d.addEventListener('click', (e) => {
    if (e.target.closest('.dl')) { e.stopPropagation(); say('Downloads start here in the app. This preview has no files.'); return; }
    setDoc(d.dataset.doc);
    if (matchMedia('(max-width: 900px)').matches) stage.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }));
  document.querySelector('.dlall').addEventListener('click', () => say('Downloads start here in the app. This preview has no files.'));
  document.getElementById('chdesign').addEventListener('click', () => { setStep('setup'); setDoc('cv'); speak(TIPS[tpl()]); });
  const text = { sub: () => document.getElementById('msub').textContent, body: () => document.getElementById('mbody').textContent };
  text.all = () => 'Subject: ' + text.sub() + '\n\n' + text.body();
  const wireCopy = () => document.querySelectorAll('[data-copy]').forEach((b) => { if (b.dataset.w) return; b.dataset.w = '1'; b.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(text[b.dataset.copy]()); say('Copied'); } catch (e) { const r = document.createRange(); r.selectNodeContents(document.getElementById(b.dataset.copy === 'sub' ? 'msub' : 'mbody')); getSelection().removeAllRanges(); getSelection().addRange(r); say('Selected. Press Ctrl+C to copy.'); }
    b.classList.add('ok'); setTimeout(() => b.classList.remove('ok'), 1500);
  }); });
  wireCopy();
  st.classList.add('marks-on');

  /* the chooser shows its position; language swaps every document, morphing the CV */
  const tpos = document.getElementById('tpos');
  radios.forEach((r, i) => r.addEventListener('change', () => { tpos.textContent = (i + 1) + ' of ' + radios.length; }));
  const LANG_TIPS = { en: 'Your CV, letter and email will be in English, like the offer.', fr: 'Switched to French. Your CV, letter and email will all be in French.' };
  document.querySelectorAll('input[name="dlang"]').forEach((r) => r.addEventListener('change', () => {
    const L = r.value;
    const swap = () => {
      big.querySelector('.cvd .in').innerHTML = document.getElementById('cv-' + L).innerHTML;
      document.querySelector('.l-cl').innerHTML = document.getElementById('cl-' + L).innerHTML;
      document.querySelector('.l-em .mail').innerHTML = document.getElementById('em-' + L).innerHTML;
      document.documentElement.lang = L;
    };
    if (document.startViewTransition && !reduce) document.startViewTransition(swap); else swap();
    wireCopy(); speak(LANG_TIPS[L]);
  }));
  document.getElementById('again').addEventListener('click', write);
  document.querySelector('.psteps li[data-s="1"]').addEventListener('click', () => { if (st.dataset.step === 'ready') { setStep('setup'); setDoc('cv'); speak(TIPS[tpl()]); } });
})();
</script>'''
import json as _j
JS = JS.replace('__TIPS__', _j.dumps({k: v[2] for k, v in TIPS.items()})).replace('__WT__', _j.dumps(WRITE_TIPS)).replace('__RT__', _j.dumps(READY_TIP))

DCs = open(f'{A}/upload.py').read()
DC = DCs[DCs.index("DC = '''") + 8:DCs.index("'''", DCs.index("DC = '''") + 8)]
LOGO = 'data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%2048%2048%22%20width=%2248%22%20height=%2248%22%20fill=%22none%22%20stroke-linecap=%22round%22%20stroke-linejoin=%22round%22%3E%3Cdefs%3E%3CclipPath%20id=%22jmc%22%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22/%3E%3C/clipPath%3E%3C/defs%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20fill=%22%23CDBFFF%22/%3E%3Cpath%20d=%22M27.5%2020V17Q27.5%2014.5%2030%2014.5H35Q37.5%2014.5%2037.5%2017V20%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FFFFFF%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20fill=%22%23FF7F45%22%20clip-path=%22url%28%23jmc%29%22/%3E%3Crect%20x=%224%22%20y=%224%22%20width=%2222%22%20height=%2232%22%20rx=%224%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Crect%20x=%2217%22%20y=%2220%22%20width=%2227%22%20height=%2222%22%20rx=%225%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.6%22/%3E%3Cpath%20d=%22M9.5%2011H19M9.5%2015.5H15%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.4%22/%3E%3Cpath%20d=%22M17%2029.5H44%22%20stroke=%22%231E1C2B%22%20stroke-width=%222.2%22/%3E%3C/svg%3E'
P = f'{S}/nabta-canvas/project'
CL = {'dash': '#matches', 'applied': '#applied', 'review': '#review'}
def board(step):
    b = body(LOGO, CL, step=step)
    b = b.replace('<div class="studio"', '<div class="studio marks-on"', 1)
    if step == 'writing':
        b = b.replace('<div class="studio marks-on"', '<div class="studio writing-on"', 1)
        for s in ('h', 'ct', 'sum', 'exp'):
            b = b.replace(f'<div class="s {s}" style="grid-area:{s}">', f'<div class="s {s} shw" style="grid-area:{s}">', 1)
        b = b.replace('<span id="wpct">0</span>', '<span id="wpct">24</span>').replace('transform: scaleY(0);', 'transform: scaleY(.24);')
    if step == 'ready':
        b = b.replace('<div class="studio marks-on"', '<div class="studio marks-on"', 1)
    return b
for nm, step in (('Apply', 'setup'), ('ApplyWriting', 'writing'), ('ApplyReady', 'ready')):
    open(f'{P}/{nm}.dc.html', 'w').write(DC.format(title=f'JobMatcher prepare application, {step}', fonts=FONTS, css=CSS, body=board(step), w=1440, h=900))
open(f'{P}/ApplyPhone.dc.html', 'w').write(DC.format(title='JobMatcher prepare application, phone width', fonts=FONTS, css='body{margin:0;background:#F6F5FB}\n',
     body='<div style="width: 390px; background: #F6F5FB;">\n  <dc-import name="Apply" hint-size="390px,1150px"></dc-import>\n</div>', w=390, h=1150))
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
open(f'{S}/preview/apply.html', 'w').write(page({'dash': 'dashboard.html', 'applied': 'dashboard.html#applied', 'review': 'review.html'}, 'JobMatcher Prepare Application'))
full = page({'dash': '#top', 'applied': '#top', 'review': '#top'}, 'JobMatcher Prepare Application')
head = re.search(r'<head>(.*?)</head>', full, re.S).group(1)
head = re.sub(r'<meta charset="utf-8">|<meta name="viewport"[^>]*>', '', head).strip()
t = re.search(r'<title>.*?</title>', head).group(0); head = head.replace(t, '').strip()
bod = re.search(r'<body>(.*)</body>', full, re.S).group(1).strip()
open(f'{S}/apply-standalone/index.html', 'w').write(t + '\n' + head + '\n' + bod + '\n')
print('ok')
