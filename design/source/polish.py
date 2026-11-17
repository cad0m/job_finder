# Post-build polish from the frontend audit. Idempotent: run after any generator.
import sys, glob, os, re
S = sys.argv[1]
MARK = '/*audit-polish*/'
CSS = MARK + '''
.get li i{font-size:11px !important}
:focus-visible{outline:2px solid #1E1C2B;outline-offset:3px}
.zz,.zz *{animation-play-state:paused !important}
.mtop a{text-decoration:none}
.chip button{position:relative}
.chip button::after{content:"";position:absolute;inset:-7px}
.card :is(h2,h3) a{padding:8px 2px;margin:-8px -2px}
.rm{width:36px !important;height:36px !important;right:-10px !important;top:0 !important}
.need-tag{font-size:11.5px !important}
.fp-msg{margin:6px 0 0;font-size:13.5px;line-height:19px;color:#5E5C6E}
.fp-msg.bad{color:#C2410C;font-weight:600}
.fp-msg:empty{display:none}
@media (max-width:900px){
.mtop{margin-bottom:20px !important}
.tt-n{font-size:11.5px !important}
.ditem .di,.ditem .di i{font-size:11px !important}
.fnav a{display:inline-block;padding:10px 0}
.lkd,.editl{min-height:32px}
.lbl a{display:inline-block;padding:6px 0}
}
'''
PAUSE = '''<script>/*audit-polish*/(() => { if (!('IntersectionObserver' in window)) return; const io = new IntersectionObserver((es) => es.forEach((e) => e.target.classList.toggle('zz', !e.isIntersecting)), { rootMargin: '120px' }); document.querySelectorAll('body section, body aside.host, .hero, .stage').forEach((s) => io.observe(s)); })();</script>'''
FORGOT = '''<script>/*audit-polish*/(() => { const a = document.querySelector('a[href="#forgot"]'); if (!a) return; const f = a.closest('.fld'); const m = document.createElement('p'); m.className = 'fp-msg'; m.setAttribute('role', 'status'); f.append(m);
  a.addEventListener('click', (e) => { e.preventDefault(); const em = document.getElementById('email'); if (!em.value || !em.checkValidity()) { m.className = 'fp-msg bad'; m.textContent = 'Type your email above first, then press Forgot password again.'; em.focus(); return; } m.className = 'fp-msg'; m.textContent = 'We sent a reset link to ' + em.value + '. Check your inbox.'; }); })();</script>'''

def polish(path):
    t = open(path).read(); o = t
    name = os.path.basename(path) if 'preview' in path else os.path.basename(os.path.dirname(path))
    if MARK not in t:
        i = t.rfind('</style>')
        if i > 0: t = t[:i] + CSS + t[i:]
    # landmarks and lang
    if t.startswith('<!doctype') and '<html>' in t[:200]: t = t.replace('<html>', '<html lang="en">', 1)
    if 'Grow into' in t and '<div class="page" lang="en"' not in t: t = t.replace('<div class="page" style=', '<div class="page" lang="en" style=', 1)
    if '<main' not in t and 'role="main"' not in t:
        t = re.sub(r'(<body[^>]*>\s*<div)', r'\1 role="main"', t, count=1) if '<body' in t else re.sub(r'(</style>\s*(?:<[^d][^>]*>\s*)*?<div)', r'\1 role="main"', t, count=1)
    # labels
    t = t.replace('id="cvcam" accept', 'id="cvcam" aria-label="Take a photo of your CV" accept')
    t = re.sub(r'<a class="back" href="([^"]*)">', r'<a class="back" href="\1" aria-label="Back to your matches">', t)
    t = t.replace('<div class="chips rv" style=', '<div class="chips rv" tabindex="0" aria-label="Popular searches" style=', 1)
    # flows
    if name in ('signin.html',) or (name == 'signin' ):
        t = t.replace("location.href = 'upload.html'", "location.href = 'dashboard.html'")
    if 'href="#forgot"' in t and 'fp-msg' not in t.split(MARK, 1)[-1].split('</style>', 1)[-1]:
        t = t.replace('</body>', FORGOT + '\n</body>') if '</body>' in t else t + FORGOT
    if ('class="hero' in t or 'href="#forgot"' in t or 'class="host' in t) and "classList.toggle('zz'" not in t:
        t = t.replace('</body>', PAUSE + '\n</body>') if '</body>' in t else t + PAUSE
    if t != o: open(path, 'w').write(t); return True
    return False

files = glob.glob(f'{S}/preview/*.html') + glob.glob(f'{S}/*-standalone/index.html')
print(sum(polish(f) for f in files), 'files polished')
