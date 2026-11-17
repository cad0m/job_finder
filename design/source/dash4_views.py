# Saved and Applied views, shared by dash4.py (exec'd after dash3_drawer.py so DETAIL, cup, ini, BOOK, TKS, ARR exist).
SAVED0 = [('b', '2 days ago'), ('1', '3 days ago'), ('3', 'today')]
DL_I = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5"></path><path d="M5 20h14"></path></svg>'
RETRY_I = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12a8 8 0 1 1-2.3-5.7"></path><path d="M20 4v5h-5"></path></svg>'
SPIN = '<i class="spin sm"></i>'

def srow(key, ago):
    j = DETAIL[key]
    return f'''<article class="row srow" data-key="{key}">
          <a class="stretch" href="#job" data-i="{key}" aria-label="{j['t']} at {j['co']}, {j['sc']}% match"></a>
          <span class="logo-c {j['lc']}" aria-hidden="true">{ini(j['co'])}</span>
          <span class="r-t"><b>{j['t']}<span class="ar" aria-hidden="true">→</span></b><span>{j['co']} · {j['city']} · {j['src']}</span></span>
          <span class="r-d">Saved {ago}</span>
          <span class="r-sc">{cup(j['sc'], 22)}<b>{j['sc']}<small>%</small></b></span>
          <a class="mini-go" href="#apply">Prepare</a>
          <button class="save" type="button" data-k="{key}" aria-pressed="true" aria-label="Remove {j['t']} from saved">{BOOK}</button>
        </article>'''

def docs(which=('cv', 'cl', 'em'), off=()):
    names = {'cv': ('CV', 'Tailored to this offer'), 'cl': ('Cover letter', 'Addressed to the company'), 'em': ('Email', 'Ready to send with both')}
    out = []
    for k in ('cv', 'cl', 'em'):
        n, sub = names[k]
        if k in off:
            out.append(f'<div class="doc off"><i class="dic">{n[:2].upper()}</i><span><b>{n}</b><small>Not written</small></span></div>')
        elif k in which:
            out.append(f'<button class="doc" type="button" data-doc="{n}"><i class="dic">{n[:2].upper()}</i><span><b>{n}</b><small>{sub} · PDF</small></span>{DL_I}</button>')
    return '<div class="docs">' + ''.join(out) + '</div>'

def apcard(key, st, when, extra=''):
    j = DETAIL[key]
    head = f'''<div class="ap-h"><span class="logo-c {j['lc']}" aria-hidden="true">{ini(j['co'])}</span><span class="r-t"><b>{j['t']}</b><span>{j['co']} · {j['city']}</span></span><span class="r-sc">{cup(j['sc'], 22)}<b>{j['sc']}<small>%</small></b></span></div>'''
    if st == 'ready':
        pill = f'<span class="stp ok"><i>{TKS}</i>Ready</span>'
        body = docs() + f'<div class="ap-f"><button class="go dlall" type="button"><span class="s-go">{DL_I}Download all</span></button><a class="lnk2" href="#job" data-i="{key}">View offer</a><a class="lnk2" href="#source">Original post</a></div>'
    elif st == 'gen':
        pill = f'<span class="stp gen">{SPIN}Writing your documents</span>'
        body = '''<ol class="gsteps" aria-label="Progress"><li class="done"><i></i>Tailoring your CV</li><li class="now"><i></i>Writing the cover letter</li><li><i></i>Drafting the email</li></ol><div class="gbar"><i></i></div><p class="gnote">This takes about a minute. You can leave this page.</p>'''
    else:
        pill = '<span class="stp bad">Needs you</span>'
        body = docs(which=('cv', 'em'), off=('cl',)) + f'<p class="err">The cover letter could not be written for this offer. Your CV and email are ready.</p><div class="ap-f"><button class="go retry" type="button"><span class="s-go">{RETRY_I}Try the cover letter again</span></button><a class="lnk2" href="#job" data-i="{key}">View offer</a></div>'
    return f'<article class="ap" data-st="{st}" data-key="{key}" style="--k: {extra or 0};">{head}<div class="ap-st">{pill}<span class="when">{when}</span></div>{body}</article>'

APPS = [('0', 'ready', 'Prepared yesterday'), ('1', 'gen', 'Started a few seconds ago'), ('3', 'ready', 'Prepared 3 days ago'), ('5', 'fail', 'Tried 4 days ago')]

def saved_view(static=False):
    rows = ''.join(srow(k, a) for k, a in SAVED0)
    return f'''<section class="view v-saved" data-v="saved" aria-labelledby="h-saved">
      <div class="mhead"><h1 class="display" id="h-saved">Saved</h1><span class="count"><b class="n-saved">{len(SAVED0)}</b>offers</span></div>
      <div class="list" id="slist">
        {rows}
      </div>
      <div class="sempty" id="sempty" hidden><svg viewBox="0 0 48 56" width="64" height="75" aria-hidden="true"><rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" stroke-width="2.8"></rect><path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" stroke-width="2.8" stroke-linejoin="round"></path></svg><b>Nothing saved yet</b><span>Tap the bookmark on any offer to keep it here.</span><a class="go" href="#matches"><span class="s-go">See your matches{ARR}</span></a></div>
    </section>'''

def applied_view():
    cards = ''.join(apcard(k, s, w, str(i)) for i, (k, s, w) in enumerate(APPS))
    seg = '<div class="seg3" role="group" aria-label="Show"><button type="button" class="s3" data-s="all" aria-pressed="true">All <em>4</em></button><button type="button" class="s3" data-s="ready" aria-pressed="false">Ready <em class="n-ready">2</em></button><button type="button" class="s3" data-s="gen" aria-pressed="false">In progress <em class="n-gen">1</em></button><button type="button" class="s3" data-s="fail" aria-pressed="false">Needs you <em>1</em></button></div>'
    return f'''<section class="view v-applied" data-v="applied" aria-labelledby="h-applied">
      <div class="mhead"><h1 class="display" id="h-applied">Applied</h1><span class="count"><b>4</b>applications</span></div>
      {seg}
      <div class="aps" id="aps">{cards}</div>
      <template id="tpl-ready">{apcard('1', 'ready', 'Prepared just now')}</template>
    </section>'''

VIEW_JS = r"""
  /* views: Matches, Saved and Applied share one page; the hash names the view */
  const app = document.getElementById('app');
  const setView = (v) => {
    if (!['matches', 'saved', 'applied'].includes(v)) v = 'matches';
    if (app.dataset.view !== v) { app.dataset.view = v; window.scrollTo({ top: 0 }); }
    document.querySelectorAll('[data-nav]').forEach((a) => { const on = a.dataset.nav === v; a.classList.toggle('on', on); on ? a.setAttribute('aria-current', 'page') : a.removeAttribute('aria-current'); });
    if (v === 'applied') startGen();
  };
  addEventListener('hashchange', () => setView(location.hash.slice(1)));
  /* saved: one list of keys, shown everywhere */
  const saved = new Map([['b', '2 days ago'], ['1', '3 days ago'], ['3', 'today']]);
  const slist = document.getElementById('slist'), sempty = document.getElementById('sempty');
  const toast = document.getElementById('toast'); let tt;
  const say = (html) => { toast.innerHTML = html; toast.hidden = false; toast.classList.remove('in'); void toast.offsetWidth; toast.classList.add('in'); clearTimeout(tt); tt = setTimeout(() => { toast.hidden = true; }, 5000); };
  const syncSaved = () => {
    document.querySelectorAll('[data-k]').forEach((b) => b.setAttribute('aria-pressed', String(saved.has(b.dataset.k))));
    document.querySelectorAll('.n-saved').forEach((n) => { n.textContent = saved.size; });
    sempty.hidden = saved.size > 0; slist.hidden = saved.size === 0;
    if (cur) dsave.setAttribute('aria-pressed', String(saved.has(cur)));
  };
  const srowHTML = (k, ago) => { const j = data.jobs[k]; return document.getElementById('tpl-srow').innerHTML.replaceAll('__K__', k).replaceAll('__T__', j.t).replaceAll('__CO__', j.co).replaceAll('__CITY__', j.city).replaceAll('__SRC__', j.src).replaceAll('__LC__', j.lc).replaceAll('__INI__', j.ini).replaceAll('__SC__', j.sc).replaceAll('__AGO__', ago).replace('__CUP__', j.cup); };
  const toggleSave = (k, el) => {
    if (saved.has(k)) {
      const ago = saved.get(k); saved.delete(k);
      const r = slist.querySelector(`[data-key="${k}"]`); if (r) { r.classList.add('gone'); setTimeout(() => { r.remove(); syncSaved(); }, 320); }
      say(`Removed from saved<button type="button" class="undo" data-undo="${k}" data-ago="${ago}">Undo</button>`);
    } else {
      saved.set(k, 'just now'); slist.insertAdjacentHTML('afterbegin', srowHTML(k, 'just now')); slist.firstElementChild.classList.add('shown');
      say('Saved<a class="undo" href="#saved">See saved</a>');
    }
    if (el) { el.classList.remove('popd'); void el.offsetWidth; el.classList.add('popd'); }
    syncSaved();
  };
  document.addEventListener('click', (e) => {
    const u = e.target.closest('[data-undo]');
    if (u) { const k = u.dataset.undo; saved.set(k, u.dataset.ago); slist.insertAdjacentHTML('afterbegin', srowHTML(k, u.dataset.ago)); slist.firstElementChild.classList.add('shown'); syncSaved(); toast.hidden = true; return; }
    const s = e.target.closest('[data-k]'); if (s) { e.preventDefault(); toggleSave(s.dataset.k, s); return; }
    const d = e.target.closest('.doc, .dlall'); if (d) { say('Downloads start here in the app. This preview has no files.'); return; }
    const a = e.target.closest('[data-i]'); if (a) { e.preventDefault(); open(a.dataset.i); }
  });
  /* applied: filter by status, and finish the one in progress */
  document.querySelectorAll('.s3').forEach((b) => b.addEventListener('click', () => {
    document.querySelectorAll('.s3').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    document.querySelectorAll('.ap').forEach((c) => { const ok = b.dataset.s === 'all' || c.dataset.st === b.dataset.s; c.hidden = !ok; if (ok) { c.classList.remove('shown'); void c.offsetWidth; c.classList.add('shown'); } });
  }));
  let genStarted = false;
  const startGen = () => {
    if (genStarted) return; genStarted = true;
    const card = document.querySelector('.ap[data-st="gen"]'); if (!card) return;
    const steps = [...card.querySelectorAll('.gsteps li')];
    setTimeout(() => { steps[1].className = 'done'; steps[2].className = 'now'; card.style.setProperty('--g', '.72'); }, 2600);
    setTimeout(() => { steps[2].className = 'done'; card.style.setProperty('--g', '1'); }, 5000);
    setTimeout(() => {
      const t = document.getElementById('tpl-ready').content.firstElementChild.cloneNode(true); t.classList.add('flip'); card.replaceWith(t);
      document.querySelector('.n-ready').textContent = '3'; document.querySelector('.n-gen').textContent = '0';
      say('Your application for BI Developer is ready<button type="button" class="undo" onclick="this.closest(\'.toast\').hidden=true">OK</button>');
    }, 5900);
  };
  syncSaved(); setView(location.hash.slice(1));
"""

def srow_tpl():
    return ('<template id="tpl-srow"><article class="row srow" data-key="__K__"><a class="stretch" href="#job" data-i="__K__" aria-label="__T__ at __CO__"></a><span class="logo-c __LC__" aria-hidden="true">__INI__</span>'
            '<span class="r-t"><b>__T__<span class="ar" aria-hidden="true">→</span></b><span>__CO__ · __CITY__ · __SRC__</span></span><span class="r-d">Saved __AGO__</span>'
            f'<span class="r-sc">__CUP__<b>__SC__<small>%</small></b></span><a class="mini-go" href="#apply">Prepare</a><button class="save" type="button" data-k="__K__" aria-pressed="true" aria-label="Remove __T__ from saved">{BOOK}</button></article></template>')
