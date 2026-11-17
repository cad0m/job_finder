# Applied = an application tracker with the same 16 columns as the user's Google Sheet.
# exec'd inside dash5.py after dash4_views.py; overrides applied_view() and adds TRACK_JS + tracker_dialogs().
import json as _json, datetime as _dt
TODAY = '2026-11-17'
HEAD = ['Company', 'Role', 'city', 'Job link', 'Source', 'Status', 'Date applied', 'First interview', 'Last activity', 'Days quiet', 'Follow up?', 'Next step', 'Next step date', 'Contact', 'Posted pay range', 'Notes']
STATUSES = ['Saved', 'Applied', 'Recruiter screen', 'Hiring manager', 'Final loop', 'Offer', 'Rejected', 'Withdrawn', 'No response']
SOURCES = ['LinkedIn', 'ANAPEC', 'Jobzyn', 'Job board', 'Company site', 'Referral', 'Other']
INT = ['Recruiter screen', 'Hiring manager', 'Final loop']; CLOSED = ['Rejected', 'Withdrawn', 'No response']
def R(co, role, city, link, src, st, ap='', fi='', last='', nxt='', nxd='', contact='', pay='', notes='', sent=None, lc='l1', own=None):
    return dict(co=co, role=role, city=city, link=link, src=src, st=st, ap=ap, fi=fi, last=last, next=nxt, nextd=nxd, contact=contact, pay=pay, notes=notes, sent=sent, lc=lc, own=own)
ROWS = [
 R('Bank of Africa', 'Stage PFE Big Data', 'Casablanca', 'https://www.jobzyn.com/fr/offre/bank-of-africa-pfe-big-data', 'Jobzyn', 'Applied', '2026-11-17', '', '2026-11-17', 'Wait for a reply', '2026-12-01', 'stages@bankofafrica.example', '', 'Prepared today with JobMatcher.', 'writing', 'l4'),
 R('OCP Group', 'BI Developer', 'Casablanca', 'https://www.anapec.org/offre/ocp-bi-developer', 'ANAPEC', 'Applied', '2026-11-16', '', '2026-11-16', '', '', '', '', 'Power BI and SQL. On site.', 'gen', 'l3'),
 R('Lydec', 'Data Analyst stagiaire', 'Casablanca', 'https://www.anapec.org/offre/lydec-data-analyst', 'ANAPEC', 'Applied', '2026-11-16', '', '2026-11-16', '', '', 'rh@lydec.example', '', '', 'gen', 'l2'),
 R('Attijariwafa bank', 'Data Engineer', 'Casablanca', 'https://www.linkedin.com/jobs/view/data-engineer-attijariwafa', 'LinkedIn', 'Recruiter screen', '2026-11-03', '2026-11-12', '2026-11-12', 'Send the SQL case study', '2026-11-19', 'talent@attijariwafa.example', '', 'Data platform team. Hybrid, 2 days remote.', 'gen', 'l1'),
 R('Deloitte Maroc', 'Data Analyst Consultant', 'Casablanca', 'https://www.linkedin.com/jobs/view/deloitte-data-analyst', 'LinkedIn', 'Final loop', '2026-10-24', '2026-11-06', '2026-11-13', 'Case interview with a partner', '2026-11-20', '', '', 'Bring the Power BI portfolio.', 'gen', 'l3'),
 R('Maroc Telecom', 'Ingénieur BI junior', 'Rabat', 'https://www.jobzyn.com/fr/offre/maroc-telecom-ingenieur-bi', 'Jobzyn', 'Hiring manager', '2026-10-20', '2026-10-30', '2026-11-04', 'Thank-you email after the interview', '2026-11-05', 'recrutement@iam.example', '8 000 to 10 000 MAD', 'Power BI and Oracle.', 'own', 'l2',
   own={'subject': 'Candidature Ingénieur BI junior, Salma El Idrissi', 'body': 'Bonjour,\n\nJe vous adresse ma candidature au poste d’Ingénieur BI junior. Vous trouverez mon CV en pièce jointe.\n\nCordialement,\nSalma El Idrissi', 'file': 'CV_Salma_El_Idrissi_BI.pdf'}),
 R('CIH Bank', 'Data Analyst', 'Casablanca', 'https://www.anapec.org/offre/cih-data-analyst', 'ANAPEC', 'Applied', '2026-10-28', '', '2026-10-28', '', '', 'rh@cihbank.example', '', 'Retail banking analytics.', 'gen', 'l2'),
 R('inwi', 'Stage PFE Data Science', 'Casablanca', 'https://www.linkedin.com/jobs/view/inwi-pfe-data-science', 'LinkedIn', 'Offer', '2026-10-14', '2026-10-22', '2026-11-14', 'Reply to the offer', '2026-11-21', 'stages@inwi.example', '6 000 MAD a month', '6-month PFE from February.', 'own', 'l4',
   own={'subject': 'Stage PFE Data Science, Salma El Idrissi', 'body': 'Hello,\n\nPlease find my CV attached for the PFE Data Science internship.\n\nBest regards,\nSalma', 'file': 'CV_Salma_El_Idrissi.pdf'}),
 R('Capgemini', 'Data Scientist junior', 'Rabat', 'https://www.jobzyn.com/fr/offre/capgemini-data-scientist', 'Jobzyn', 'Rejected', '2026-10-12', '', '2026-10-30', '', '', '', '', 'They asked for 2 years of experience.', 'own', 'l1', own={'subject': '', 'body': '', 'file': 'CV_Salma_El_Idrissi.pdf'}),
 R('Dislog Group', 'BI Analyst', 'Casablanca', 'https://www.linkedin.com/jobs/view/dislog-bi-analyst', 'LinkedIn', 'Withdrawn', '2026-10-05', '', '2026-10-16', '', '', '', '', 'Chose the inwi process instead.', 'gen', 'l3'),
 R('Marjane', 'Analyste de données', 'Casablanca', 'https://www.anapec.org/offre/marjane-analyste-donnees', 'ANAPEC', 'No response', '2026-09-30', '', '2026-09-30', '', '', '', '', '', 'own', 'l2', own={'subject': 'Candidature Analyste de données', 'body': '', 'file': 'CV_Salma_2026.pdf'}),
 R('Société Générale Maroc', 'Data Engineer Intern', 'Casablanca', 'https://www.jobzyn.com/fr/offre/sgma-data-engineer-intern', 'Jobzyn', 'Saved', '', '', '', 'Apply before the deadline', '2026-11-25', '', '', 'Deadline 25 November.', None, 'l1'),
 R('Orange Business', 'Data Platform Intern', 'Rabat', 'https://www.linkedin.com/jobs/view/orange-business-data-platform', 'LinkedIn', 'Saved', '', '', '', '', '', '', '', 'Spark and Kafka.', None, 'l2'),
]
for i, r in enumerate(ROWS): r['id'] = 'r%d' % i
D = lambda s: _dt.date.fromisoformat(s)
def quiet(r): return (D(TODAY) - D(r['last'])).days if r['last'] else None
def fu(r):
    q = quiet(r)
    return q is not None and ((r['st'] == 'Applied' and q >= 14) or (r['st'] in INT and q >= 10))
def grp(st): return 'saved' if st == 'Saved' else 'applied' if st == 'Applied' else 'int' if st in INT else 'offer' if st == 'Offer' else 'closed'
def fdate(s):
    if not s: return ''
    d = D(s); return f'{d.day} {d.strftime("%b")}'
def ini2(c):
    w = c.replace('é', 'e').split()
    return (w[0][0] + (w[1][0] if len(w) > 1 else w[0][1])).upper()
CHEV = '<svg class="ch" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"></path></svg>'
EXT2 = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9"></path><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"></path></svg>'
CLIP = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 11.5l-8 8a5 5 0 0 1-7-7l8.5-8.5a3.3 3.3 0 0 1 4.7 4.7L9.7 17.2a1.7 1.7 0 0 1-2.4-2.4l7.4-7.3"></path></svg>'
PLUS = '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"></path></svg>'
CSV_I = '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5"></path><path d="M5 20h14"></path></svg>'
SRCH = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"></circle><path d="M16 16l4 4"></path></svg>'
MARKI = '<svg viewBox="0 0 48 48" width="16" height="16" aria-hidden="true"><rect x="4" y="4" width="22" height="32" rx="4" fill="#CDBFFF" stroke="#1E1C2B" stroke-width="3.4"></rect><rect x="17" y="20" width="27" height="22" rx="5" fill="#FFFFFF" stroke="#1E1C2B" stroke-width="3.4"></rect><rect x="17" y="20" width="9" height="16" fill="#FF7F45"></rect></svg>'

def sent_cell(r, apply_href):
    s = r['sent']
    if s == 'gen': return f'<button class="sent gen" type="button" data-open="{r["id"]}" aria-label="See the CV, cover letter and email made with JobMatcher">{MARKI}3 files</button>'
    if s == 'own': return f'<button class="sent own" type="button" data-open="{r["id"]}" aria-label="See what you sent yourself">{CLIP}Yours</button>'
    if s == 'writing': return f'<span class="sent wr"><i class="spin sm"></i>Writing</span>'
    if r['st'] == 'Saved': return f'<a class="sent prep" href="{apply_href}">Prepare</a>'
    return f'<button class="sent add" type="button" data-open="{r["id"]}" aria-label="Add what you sent">{PLUS}Add</button>'

def stsel(r):
    opts = ''.join(f'<option{" selected" if s == r["st"] else ""}>{s}</option>' for s in STATUSES)
    return f'<span class="stw" data-g="{grp(r["st"])}"><select class="stsel" data-id="{r["id"]}" aria-label="Status for {r["role"]} at {r["co"]}">{opts}</select>{CHEV}</span>'

def trow(r, apply_href='#apply'):
    q = quiet(r); f = fu(r); g = grp(r['st'])
    over = r['nextd'] and r['nextd'] < TODAY and g not in ('closed',)
    host = r['link'].split('/')[2].replace('www.', '') if r['link'] else ''
    cls = 'tr' + (' fu' if f else '') + (' closed' if g == 'closed' else '') + (' offer' if g == 'offer' else '')
    cells = [
     f'<th scope="row" class="c-co" data-l="Company"><span class="logo-c {r["lc"]}" aria-hidden="true">{ini2(r["co"])}</span><span class="co-t"><b>{r["co"]}</b></span></th>',
     f'<td class="c-ro" data-l="Role">{r["role"]}</td>',
     f'<td class="c-ci" data-l="City">{r["city"]}</td>',
     f'<td class="c-li" data-l="Job link"><a href="{r["link"]}" target="_blank" rel="noopener">{host}{EXT2}</a></td>',
     f'<td class="c-so" data-l="Source"><span class="src">{r["src"]}</span></td>',
     f'<td class="c-st" data-l="Status">{stsel(r)}</td>',
     f'<td class="c-d c-ap" data-l="Date applied">{fdate(r["ap"]) or "<i class=dash>—</i>"}</td>',
     f'<td class="c-d" data-l="First interview">{fdate(r["fi"]) or "<i class=dash>—</i>"}</td>',
     f'<td class="c-d" data-l="Last activity">{fdate(r["last"]) or "<i class=dash>—</i>"}</td>',
     f'<td class="c-q auto" data-l="Days quiet">{"" if q is None else q}</td>',
     f'<td class="c-f auto" data-l="Follow up?">{("<span class=fub>Yes</span>" if f else "<span class=fno>No</span>") if q is not None and g != "closed" and g != "saved" else ""}</td>',
     f'<td class="c-nx" data-l="Next step">{r["next"]}</td>',
     f'<td class="c-d{" over" if over else ""}" data-l="Next step date">{fdate(r["nextd"])}</td>',
     '<td class="c-ct" data-l="Contact">' + (f'<a href="mailto:{r["contact"]}">{r["contact"]}</a>' if r['contact'] else '') + '</td>',
     f'<td class="c-pa" data-l="Posted pay range">{r["pay"]}</td>',
     f'<td class="c-no" data-l="Notes"><span class="clamp">{r["notes"]}</span></td>',
     f'<td class="c-se">{sent_cell(r, apply_href)}</td>',
    ]
    return f'<tr class="{cls}" data-id="{r["id"]}" data-g="{g}" tabindex="0">' + ''.join(cells) + '</tr>'

def stats():
    sent = [r for r in ROWS if r['ap']]; ints = [r for r in ROWS if r['fi']]
    wk = [r for r in ROWS if r['ap'] and '2026-11-16' <= r['ap'] <= '2026-11-22']
    return dict(sent=len(sent), ints=len(ints), rate=round(100 * len(ints) / len(sent)) if sent else 0, offers=sum(r['st'] == 'Offer' for r in ROWS), fu=sum(fu(r) for r in ROWS), week=len(wk), total=len(ROWS),
                g={k: sum(grp(r['st']) == k for r in ROWS) for k in ('saved', 'applied', 'int', 'offer', 'closed')})

def applied_view():
    s = stats(); goal = 5; p = min(100, round(100 * s['week'] / goal))
    days = ['M', 'T', 'W', 'T', 'F', 'S', 'S']; per = {0: 2, 1: 1}
    bars = ''.join(f'<span class="wd{" today" if i == 1 else ""}{" fut" if i > 1 else ""}" style="--h: {per.get(i, 0)};"><i></i><b>{d}</b></span>' for i, d in enumerate(days))
    head = ''.join(f'<th scope="col" class="h-{i}"{" aria-sort=\"none\" data-sort=\"" + k + "\"" if k else ""}>{"<button type=button>" + h + "</button>" if k else h}{" <span class=auto-t title=\"Filled in for you\">auto</span>" if h in ("Days quiet", "Follow up?") else ""}</th>' for i, (h, k) in enumerate(zip(HEAD, ['co', '', '', '', '', 'st', 'ap', 'fi', 'last', 'q', '', '', 'nextd', '', '', ''])))
    chips = [('all', 'All', s['total']), ('saved', 'Saved', s['g']['saved']), ('applied', 'Applied', s['g']['applied']), ('int', 'Interviewing', s['g']['int']), ('offer', 'Offer', s['g']['offer']), ('closed', 'Closed', s['g']['closed'])]
    chiph = ''.join(f'<button class="tchip" type="button" data-f="{k}" data-g="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}<em class="tn-{k}">{c}</em></button>' for k, n, c in chips)
    rows = ''.join(trow(r) for r in ROWS)
    return f'''<section class="view v-applied" data-v="applied" aria-labelledby="h-applied">
      <div class="mhead thead2"><h1 class="display" id="h-applied">Applied</h1><span class="count"><b class="n-sent">{s['sent']}</b>sent</span>
        <span class="sp"></span><button class="ghost2 tcsv" type="button" id="tcsv">{CSV_I}<span>Export CSV</span></button><button class="tadd" type="button" id="tadd">{PLUS}<span>Add an application</span></button></div>
      <div class="tkpis">
        <div class="goal" id="goal" style="--p: {p / 100};">
          <div class="g-cup">{cup(100, 58, "cup gcup")}</div>
          <div class="g-t"><b><span id="g-n">{s['week']}</span> of <span id="g-goal">{goal}</span></b><span class="g-l">sent this week</span><span class="g-sub" id="g-sub">{goal - s['week']} more to reach your goal</span></div>
          <div class="g-r"><div class="wk" aria-label="Sent per day this week">{bars}</div><div class="g-st" role="group" aria-label="Weekly goal"><button type="button" class="gs" data-d="-1" aria-label="Lower the goal">−</button><span>Goal</span><button type="button" class="gs" data-d="1" aria-label="Raise the goal">+</button></div></div>
        </div>
        <div class="kpi"><b class="n-sent">{s['sent']}</b><span>applications sent</span></div>
        <div class="kpi"><b class="n-ints">{s['ints']}</b><span>interviews · <em class="n-rate">{s['rate']}%</em> of sent</span></div>
        <div class="kpi ok"><b class="n-offers">{s['offers']}</b><span>offer</span></div>
        <button class="kpi warn" type="button" data-f="fu"><b class="n-fu">{s['fu']}</b><span>to follow up</span></button>
      </div>
      <div class="tbar2">
        <div class="tchips" role="group" aria-label="Show">{chiph}<button class="tchip fuc" type="button" data-f="fu" aria-pressed="false">Follow up<em class="n-fu">{s['fu']}</em></button></div>
        <label class="tsearch">{SRCH}<input type="search" id="tq" placeholder="Company, role or city" aria-label="Search your applications"></label>
      </div>
      <div class="tw" id="tw" tabindex="0" role="region" aria-label="Your applications, scroll sideways for more columns">
        <table class="tt" id="tt"><thead><tr>{head}<th scope="col" class="h-se"><span class="vh">What you sent</span></th></tr></thead><tbody id="tbody">{rows}</tbody></table>
        <div class="tempty" id="tempty" hidden><b>Nothing here</b><span>No application matches this filter.</span></div>
      </div>
      <p class="tlegend"><span><i class="lg fu"></i>No reply for a while: follow up</span><span><i class="lg offer"></i>Offer</span><span><i class="lg closed"></i>Closed</span><span class="auto-t">auto</span> columns fill themselves in</p>
    </section>'''

def tracker_dialogs(static_id=None):
    stopts = ''.join(f'<option>{x}</option>' for x in STATUSES); sropts = ''.join(f'<option>{x}</option>' for x in SOURCES)
    attrs = ' class="dw td static" open' if static_id else ' class="dw td" id="td" closedby="any" aria-labelledby="td-t"'
    tag = 'div' if static_id else 'dialog'
    bd = '<div class="dwbd" aria-hidden="true"></div>' if static_id else ''
    return f'''{bd}<{tag}{attrs}>
    <form class="dw-in td-in" id="tdf" method="dialog">
      <header class="td-top"><span class="logo-c l1" id="td-logo" aria-hidden="true">AB</span><span class="td-h"><b id="td-t">Role</b><span id="td-co">Company · City</span></span><button class="dw-ib dw-x" type="button" id="td-x" aria-label="Close">{CLOSE_I}</button></header>
      <div class="td-body">
        <div class="td-stat"><label class="stw big" id="td-stw"><select id="td-st" aria-label="Status">{stopts}</select>{CHEV}</label><span class="td-q" id="td-q"></span></div>
        <div class="td-fu" id="td-fu" hidden><b>No reply for <span id="td-fud">20</span> days.</b><span>A short, polite follow-up often gets an answer.</span><button class="lnk3" type="button" id="td-fub">Plan a follow-up</button></div>
        <section class="td-sec"><h3>What you sent</h3>
          <div class="seg7" role="radiogroup" aria-label="What you sent"><label><input type="radio" name="tds" value="gen" checked>Made with JobMatcher</label><label><input type="radio" name="tds" value="own">Your own</label></div>
          <div class="tds-p p-gen">
            <div class="tdocs" id="td-docs"><button class="tdoc" type="button" data-doc="CV"><i>CV</i><span><b>CV</b><small>Tailored to this offer</small></span>{CSV_I}</button><button class="tdoc" type="button" data-doc="Cover letter"><i>CL</i><span><b>Cover letter</b><small>Addressed to the company</small></span>{CSV_I}</button><button class="tdoc" type="button" data-doc="Email"><i>EM</i><span><b>Email</b><small>Subject and message</small></span>{CSV_I}</button></div>
            <div class="tmail" id="td-mail"><span class="tm-s"><small>Subject</small><b id="td-msub">Data Engineer application, Salma El Idrissi</b></span><p id="td-mbody">Hello,\n\nI am applying for the role…</p></div>
            <div class="tnone" id="td-none" hidden><span>Nothing was made with JobMatcher for this offer.</span><a class="lnk3" href="#apply" id="td-prep">Prepare it with JobMatcher</a></div>
          </div>
          <div class="tds-p p-own">
            <div class="fld3"><label for="td-osub">Subject</label><input id="td-osub" placeholder="The subject of your email"></div>
            <div class="fld3"><label for="td-obody">Message</label><textarea id="td-obody" rows="5" placeholder="Paste the email or message you sent"></textarea></div>
            <div class="tfile"><input type="file" id="td-ofile" accept=".pdf,.doc,.docx,image/*" class="vh"><label for="td-ofile" class="tf-b">{CLIP}<span id="td-ofn">Attach the CV you sent</span></label></div>
          </div>
        </section>
        <section class="td-sec"><h3>Tracking</h3>
          <div class="tgrid"><div class="fld3"><label for="td-ap">Date applied</label><input type="date" id="td-ap"></div><div class="fld3"><label for="td-fi">First interview</label><input type="date" id="td-fi"></div><div class="fld3"><label for="td-last">Last activity</label><input type="date" id="td-last"></div><div class="fld3"><label for="td-nextd">Next step date</label><input type="date" id="td-nextd"></div><div class="fld3 wide"><label for="td-next">Next step</label><input id="td-next" placeholder="Send the case study, call back, wait…"></div></div>
        </section>
        <section class="td-sec"><h3>Offer</h3>
          <div class="tgrid"><div class="fld3 wide"><label for="td-link">Job link</label><span class="lk"><input id="td-link" type="url"><a id="td-open" href="#" target="_blank" rel="noopener" aria-label="Open the job post">{EXT2}</a></span></div><div class="fld3"><label for="td-src">Source</label><select id="td-src">{sropts}</select></div><div class="fld3"><label for="td-city">city</label><input id="td-city"></div><div class="fld3"><label for="td-ct">Contact</label><input id="td-ct"></div><div class="fld3"><label for="td-pay">Posted pay range</label><input id="td-pay"></div><div class="fld3 wide"><label for="td-notes">Notes</label><textarea id="td-notes" rows="3"></textarea></div></div>
        </section>
      </div>
      <footer class="td-foot"><button class="tdel" type="button" id="td-del">Delete</button><button class="go td-save" type="submit" id="td-save"><span class="s-go">Save changes</span></button></footer>
    </form>
  </{tag}>
  <dialog class="tadd-d" id="ta" closedby="any" aria-labelledby="ta-t">
    <form class="ta-in" id="taf" method="dialog">
      <h2 class="display" id="ta-t">Add an application</h2>
      <p class="ta-lead">For an offer you found outside JobMatcher. Paste the link and we fill in what we can.</p>
      <div class="fld3"><label for="ta-link">Job link</label><input id="ta-link" type="url" placeholder="https://" autocomplete="off"></div>
      <div class="tgrid"><div class="fld3"><label for="ta-co">Company</label><input id="ta-co" required></div><div class="fld3"><label for="ta-ro">Role</label><input id="ta-ro" required></div><div class="fld3"><label for="ta-ci">city</label><input id="ta-ci"></div><div class="fld3"><label for="ta-src">Source</label><select id="ta-src">{sropts}</select></div><div class="fld3"><label for="ta-st">Status</label><select id="ta-st">{stopts.replace("<option>Applied</option>", "<option selected>Applied</option>")}</select></div><div class="fld3"><label for="ta-ap">Date applied</label><input type="date" id="ta-ap" value="{TODAY}"></div></div>
      <div class="ta-f"><button class="ghost2" type="button" id="ta-x">Cancel</button><button class="go" type="submit"><span class="s-go">Add to tracker</span></button></div>
    </form>
  </dialog>'''

TRACK_DATA = '<script type="application/json" id="trackdata">' + _json.dumps({'today': TODAY, 'head': HEAD, 'statuses': STATUSES, 'rows': ROWS}).replace('</', '<\\/') + '</script>'

TRACK_JS = r"""
  /* ---------- Applied: a tracker with the same columns as the Google Sheet ---------- */
  (() => {
  const TD = JSON.parse(document.getElementById('trackdata').textContent), TODAY = TD.today;
  const rows = TD.rows, INT = ['Recruiter screen', 'Hiring manager', 'Final loop'], CLOSED = ['Rejected', 'Withdrawn', 'No response'];
  const tbody = document.getElementById('tbody'), tempty = document.getElementById('tempty');
  const tpl = document.createElement('template');
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const day = (s) => new Date(s + 'T00:00:00');
  const quiet = (r) => r.last ? Math.round((day(TODAY) - day(r.last)) / 864e5) : null;
  const fu = (r) => { const q = quiet(r); return q !== null && ((r.st === 'Applied' && q >= 14) || (INT.includes(r.st) && q >= 10)); };
  const grp = (st) => st === 'Saved' ? 'saved' : st === 'Applied' ? 'applied' : INT.includes(st) ? 'int' : st === 'Offer' ? 'offer' : 'closed';
  const fdate = (s) => s ? day(s).toLocaleDateString('en-GB', { day: 'numeric', month: 'short' }) : '';
  const ini = (c) => { const w = c.replace('é', 'e').split(' '); return (w[0][0] + (w[1] ? w[1][0] : w[0][1])).toUpperCase(); };
  const ICONS = { chev: document.querySelector('.stw .ch').outerHTML, ext: document.querySelector('.c-li a svg').outerHTML, clip: document.querySelector('.tf-b svg').outerHTML, mark: (document.querySelector('.sent.gen svg') || {}).outerHTML || '', plus: document.querySelector('#tadd svg').outerHTML };
  const sentCell = (r) => r.sent === 'gen' ? `<button class="sent gen" type="button" data-open="${r.id}" aria-label="See the CV, cover letter and email made with JobMatcher">${ICONS.mark}3 files</button>`
    : r.sent === 'own' ? `<button class="sent own" type="button" data-open="${r.id}" aria-label="See what you sent yourself">${ICONS.clip}Yours</button>`
    : r.sent === 'writing' ? '<span class="sent wr"><i class="spin sm"></i>Writing</span>'
    : r.st === 'Saved' ? `<a class="sent prep" href="${document.getElementById('td-prep').getAttribute('href')}">Prepare</a>`
    : `<button class="sent add" type="button" data-open="${r.id}" aria-label="Add what you sent">${ICONS.plus}Add</button>`;
  const rowHTML = (r) => {
    const q = quiet(r), f = fu(r), g = grp(r.st), over = r.nextd && r.nextd < TODAY && g !== 'closed';
    let host = ''; try { host = r.link ? new URL(r.link).hostname.replace('www.', '') : ''; } catch (e) { host = r.link; }
    const d = (s) => fdate(s) || '<i class="dash">—</i>';
    const opts = TD.statuses.map((s) => `<option${s === r.st ? ' selected' : ''}>${s}</option>`).join('');
    return `<tr class="tr${f ? ' fu' : ''}${g === 'closed' ? ' closed' : ''}${g === 'offer' ? ' offer' : ''}" data-id="${r.id}" data-g="${g}" tabindex="0">`
      + `<th scope="row" class="c-co" data-l="Company"><span class="logo-c ${r.lc || 'l1'}" aria-hidden="true">${esc(ini(r.co))}</span><span class="co-t"><b>${esc(r.co)}</b></span></th>`
      + `<td class="c-ro" data-l="Role">${esc(r.role)}</td><td class="c-ci" data-l="City">${esc(r.city)}</td>`
      + `<td class="c-li" data-l="Job link">${r.link ? `<a href="${esc(r.link)}" target="_blank" rel="noopener">${esc(host)}${ICONS.ext}</a>` : ''}</td>`
      + `<td class="c-so" data-l="Source"><span class="src">${esc(r.src)}</span></td>`
      + `<td class="c-st" data-l="Status"><span class="stw" data-g="${g}"><select class="stsel" data-id="${r.id}" aria-label="Status for ${esc(r.role)} at ${esc(r.co)}">${opts}</select>${ICONS.chev}</span></td>`
      + `<td class="c-d c-ap" data-l="Date applied">${d(r.ap)}</td><td class="c-d" data-l="First interview">${d(r.fi)}</td><td class="c-d" data-l="Last activity">${d(r.last)}</td>`
      + `<td class="c-q auto" data-l="Days quiet">${q === null ? '' : q}</td>`
      + `<td class="c-f auto" data-l="Follow up?">${q !== null && g !== 'closed' && g !== 'saved' ? (f ? '<span class="fub">Yes</span>' : '<span class="fno">No</span>') : ''}</td>`
      + `<td class="c-nx" data-l="Next step">${esc(r.next)}</td><td class="c-d${over ? ' over' : ''}" data-l="Next step date">${fdate(r.nextd)}</td>`
      + `<td class="c-ct" data-l="Contact">${r.contact ? `<a href="mailto:${esc(r.contact)}">${esc(r.contact)}</a>` : ''}</td>`
      + `<td class="c-pa" data-l="Posted pay range">${esc(r.pay)}</td><td class="c-no" data-l="Notes"><span class="clamp">${esc(r.notes)}</span></td>`
      + `<td class="c-se">${sentCell(r)}</td></tr>`;
  };
  let filt = 'all', q = '', sortK = null, sortDir = 1;
  const visible = (r) => (filt === 'all' || (filt === 'fu' ? fu(r) : grp(r.st) === filt)) && (!q || (r.co + ' ' + r.role + ' ' + r.city).toLowerCase().includes(q));
  const render = (flashId) => {
    let list = rows.filter(visible);
    if (sortK) list = [...list].sort((a, b) => { const va = sortK === 'q' ? (quiet(a) ?? -1) : (a[sortK] || ''), vb = sortK === 'q' ? (quiet(b) ?? -1) : (b[sortK] || ''); return (va > vb ? 1 : va < vb ? -1 : 0) * sortDir; });
    tbody.innerHTML = list.map(rowHTML).join('');
    tempty.hidden = list.length > 0;
    if (flashId) { const tr = tbody.querySelector(`[data-id="${flashId}"]`); if (tr) tr.classList.add('flash'); }
    counts();
  };
  /* goal + numbers */
  let goal = 5; const gEl = document.getElementById('goal');
  const counts = () => {
    const sent = rows.filter((r) => r.ap), ints = rows.filter((r) => r.fi), wk = rows.filter((r) => r.ap && r.ap >= '2026-11-16' && r.ap <= '2026-11-22').length;
    const set = (c, v) => document.querySelectorAll(c).forEach((n) => { if (n.textContent !== String(v)) { n.textContent = v; n.classList.remove('bump'); void n.offsetWidth; n.classList.add('bump'); } });
    set('.n-sent', sent.length); set('.n-ints', ints.length); set('.n-rate', (sent.length ? Math.round(100 * ints.length / sent.length) : 0) + '%'); set('.n-offers', rows.filter((r) => r.st === 'Offer').length);
    set('.n-fu', rows.filter(fu).length); set('.tn-all', rows.length);
    ['saved', 'applied', 'int', 'offer', 'closed'].forEach((g) => set('.tn-' + g, rows.filter((r) => grp(r.st) === g).length));
    const was = gEl.classList.contains('done');
    set('#g-n', wk); set('#g-goal', goal); gEl.style.setProperty('--p', Math.min(1, wk / goal));
    const done = wk >= goal; gEl.classList.toggle('done', done);
    document.getElementById('g-sub').textContent = done ? 'Goal reached. Well done.' : (goal - wk) + ' more to reach your goal';
    if (done && !was && counts.ready) say('Weekly goal reached: ' + wk + ' applications sent');
    const today = document.querySelector('.wd.today'); if (today) today.style.setProperty('--h', rows.filter((r) => r.ap === TODAY).length);
  };
  document.querySelectorAll('.gs').forEach((b) => b.addEventListener('click', () => { goal = Math.max(1, Math.min(30, goal + +b.dataset.d)); counts(); }));
  /* filters, search, sort */
  const setF = (f) => { filt = f; document.querySelectorAll('.tchip').forEach((c) => c.setAttribute('aria-pressed', String(c.dataset.f === f))); render(); };
  document.querySelectorAll('.tchip, .kpi[data-f]').forEach((c) => c.addEventListener('click', () => setF(filt === c.dataset.f && c.dataset.f !== 'all' ? 'all' : c.dataset.f)));
  document.getElementById('tq').addEventListener('input', (e) => { q = e.target.value.trim().toLowerCase(); render(); });
  document.querySelectorAll('th[data-sort] button').forEach((b) => b.addEventListener('click', () => {
    const th = b.parentElement, k = th.dataset.sort; sortDir = sortK === k ? -sortDir : (k === 'co' ? 1 : -1); sortK = k;
    document.querySelectorAll('th[data-sort]').forEach((x) => x.setAttribute('aria-sort', x === th ? (sortDir > 0 ? 'ascending' : 'descending') : 'none')); render();
  }));
  /* status right in the table */
  const applyStatus = (r, st) => {
    const g0 = grp(r.st); r.st = st; r.last = TODAY;
    if (st !== 'Saved' && !r.ap) r.ap = TODAY;
    if (INT.includes(st) && !r.fi) r.fi = TODAY;
    return g0 !== grp(st);
  };
  tbody.addEventListener('change', (e) => {
    const s = e.target.closest('.stsel'); if (!s) return;
    const r = rows.find((x) => x.id === s.dataset.id); applyStatus(r, s.value);
    const tr = s.closest('tr'); tpl.innerHTML = rowHTML(r); const nr = tpl.content.firstElementChild; nr.classList.add('flash'); tr.replaceWith(nr); counts();
    say(`${r.co}: ${r.st}` + (r.st === 'Offer' ? '. Congratulations!' : ''));
  });
  /* the row opens the details */
  const dlg = document.getElementById('td'); let cur = null;
  const $ = (id) => document.getElementById(id);
  const fill = (r) => {
    cur = r; $('td-t').textContent = r.role; $('td-co').textContent = r.co + (r.city ? ' · ' + r.city : ''); $('td-logo').textContent = ini(r.co); $('td-logo').className = 'logo-c ' + (r.lc || 'l1');
    $('td-st').value = r.st; $('td-stw').dataset.g = grp(r.st);
    const qd = quiet(r); $('td-q').textContent = qd === null ? '' : (qd === 0 ? 'Active today' : `Quiet for ${qd} day${qd > 1 ? 's' : ''}`);
    $('td-fu').hidden = !fu(r); $('td-fud').textContent = qd;
    ['ap', 'fi', 'last', 'nextd', 'next', 'city', 'pay', 'notes'].forEach((k) => { $('td-' + k).value = r[k] || ''; });
    $('td-link').value = r.link || ''; $('td-open').href = r.link || '#'; $('td-src').value = r.src || 'Other'; $('td-ct').value = r.contact || '';
    const gen = r.sent === 'gen' || r.sent === 'writing';
    document.querySelector(`input[name="tds"][value="${gen || !r.own && r.sent !== 'own' ? 'gen' : 'own'}"]`).checked = true;
    $('td-docs').hidden = !gen; $('td-mail').hidden = !gen; $('td-none').hidden = gen;
    $('td-msub').textContent = `${r.role} application, Salma El Idrissi`;
    $('td-mbody').textContent = `Hello,\n\nI am applying for the ${r.role} role at ${r.co}. You will find my CV and a cover letter attached.\n\nDuring my internship at Attijariwafa bank I automated SQL reports and built Python jobs for Power BI. I would be glad to bring this to your team.\n\nBest regards,\nSalma El Idrissi`;
    const o = r.own || {}; $('td-osub').value = o.subject || ''; $('td-obody').value = o.body || ''; $('td-ofn').textContent = o.file || 'Attach the CV you sent';
    document.querySelector('.tfile').classList.toggle('has', !!o.file);
  };
  const openRow = (id) => { const r = rows.find((x) => x.id === id); if (!r) return; fill(r); dlg.showModal(); dlg.querySelector('.td-body').scrollTop = 0; };
  tbody.addEventListener('click', (e) => {
    if (e.target.closest('select, a, .stw')) return;
    const b = e.target.closest('[data-open]'); const tr = e.target.closest('tr'); if (!tr) return;
    openRow(tr.dataset.id); if (b && b.classList.contains('add')) setTimeout(() => { document.querySelector('input[name="tds"][value="own"]').checked = true; $('td-osub').focus(); }, 250);
  });
  tbody.addEventListener('keydown', (e) => { if (e.key === 'Enter' && e.target.matches('tr')) openRow(e.target.dataset.id); });
  $('td-x').addEventListener('click', () => dlg.close());
  $('td-st').addEventListener('change', (e) => { $('td-stw').dataset.g = grp(e.target.value); });
  $('td-ofile').addEventListener('change', (e) => { const f = e.target.files[0]; if (f) { $('td-ofn').textContent = f.name; document.querySelector('.tfile').classList.add('has'); } });
  $('td-fub').addEventListener('click', () => { const d = new Date(day(TODAY).getTime() + 2 * 864e5).toISOString().slice(0, 10); $('td-next').value = 'Send a short follow-up email'; $('td-nextd').value = d; $('td-next').focus(); });
  document.querySelectorAll('.tdoc').forEach((b) => b.addEventListener('click', () => say('Downloads start here in the app. This preview has no files.')));
  $('tdf').addEventListener('submit', (e) => {
    const r = cur; if (!r) return;
    const st = $('td-st').value; if (st !== r.st) applyStatus(r, st);
    ['ap', 'fi', 'last', 'nextd', 'next', 'city', 'pay', 'notes'].forEach((k) => { r[k] = $('td-' + k).value.trim(); });
    r.link = $('td-link').value.trim(); r.src = $('td-src').value; r.contact = $('td-ct').value.trim();
    const os = $('td-osub').value.trim(), ob = $('td-obody').value.trim(), of = document.querySelector('.tfile').classList.contains('has') ? $('td-ofn').textContent : '';
    if ((os || ob || of) && r.sent !== 'gen' && r.sent !== 'writing') { r.own = { subject: os, body: ob, file: of }; r.sent = 'own'; }
    else if (os || ob || of) r.own = { subject: os, body: ob, file: of };
    render(r.id); say('Saved');
  });
  $('td-del').addEventListener('click', () => {
    const i = rows.indexOf(cur), r = cur; rows.splice(i, 1); dlg.close(); render();
    say(`Deleted ${r.co}<button type="button" class="undo" id="tundo">Undo</button>`);
    $('tundo').addEventListener('click', () => { rows.splice(i, 0, r); render(r.id); toast.hidden = true; });
  });
  /* add an application, filled from the link when we can */
  const ta = $('ta'), cap = (s) => s.replace(/\b\w/g, (c) => c.toUpperCase());
  $('tadd').addEventListener('click', () => { $('taf').reset(); $('ta-ap').value = TODAY; ta.showModal(); setTimeout(() => $('ta-link').focus(), 60); });
  $('ta-x').addEventListener('click', () => ta.close());
  $('ta-link').addEventListener('input', (e) => {
    let u; try { u = new URL(e.target.value.trim()); } catch (err) { return; }
    const h = u.hostname, slug = decodeURIComponent(u.pathname.split('/').filter(Boolean).pop() || '').toLowerCase();
    const src = /linkedin/.test(h) ? 'LinkedIn' : /anapec/.test(h) ? 'ANAPEC' : /jobzyn/.test(h) ? 'Jobzyn' : /rekrute|emploi|joblia|indeed|marocannonces/.test(h) ? 'Job board' : 'Company site';
    const put = (id, v) => { if (!v) return; const el = $(id); el.value = v; el.classList.remove('auto-f'); void el.offsetWidth; el.classList.add('auto-f'); };
    put('ta-src', src);
    const m = slug.match(/^(.+?)-recrute-(?:une?-|des-|\d+-)?(.+?)(?:-a-|-au-|-en-)([a-z-]+?)(?:-\d+)?$/);
    if (m) { put('ta-co', cap(m[1].replace(/-/g, ' '))); put('ta-ro', cap(m[2].replace(/-/g, ' '))); put('ta-ci', cap(m[3].split('-')[0])); }
    else { const w = slug.split('-').filter((x) => x && !/^\d+$/.test(x)); if (w.length > 1) { put('ta-co', cap(w[0])); put('ta-ro', cap(w.slice(1).join(' '))); } }
  });
  $('taf').addEventListener('submit', () => {
    const r = { id: 'n' + Date.now(), co: $('ta-co').value.trim(), role: $('ta-ro').value.trim(), city: $('ta-ci').value.trim(), link: $('ta-link').value.trim(), src: $('ta-src').value, st: $('ta-st').value, ap: $('ta-st').value === 'Saved' ? '' : $('ta-ap').value, fi: '', last: TODAY, next: '', nextd: '', contact: '', pay: '', notes: '', sent: null, lc: 'l' + (1 + rows.length % 4) };
    if (INT.includes(r.st)) r.fi = TODAY;
    rows.unshift(r); setF('all'); render(r.id); say(`Added ${r.co}<button type="button" class="undo" data-open2="${r.id}">Add what you sent</button>`);
    const b = document.querySelector('[data-open2]'); if (b) b.addEventListener('click', () => { toast.hidden = true; openRow(r.id); document.querySelector('input[name="tds"][value="own"]').checked = true; });
  });
  /* export with the exact sheet header */
  $('tcsv').addEventListener('click', async () => {
    const c = (v) => { v = v == null ? '' : String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
    const lines = [TD.head.map(c).join(',')].concat(rows.map((r) => { const qd = quiet(r); return [r.co, r.role, r.city, r.link, r.src, r.st, r.ap, r.fi, r.last, qd ?? '', qd === null ? '' : (fu(r) ? 'Yes' : 'No'), r.next, r.nextd, r.contact, r.pay, r.notes].map(c).join(','); }));
    const data = '﻿' + lines.join('\n'), name = 'job-applications.csv';
    const dl = window.claude && window.claude.use ? await window.claude.use('downloads').catch(() => null) : null;
    if (dl) {
      try { await dl.save({ filename: name, data }); say('Saved ' + name + '. Import it into Google Sheets.'); }
      catch (err) { if (err && err.code === 'rate_limited') say('A save is already waiting for you.'); else if (!err || err.code !== 'declined') say('Saving files is not available here.'); }
      return;
    }
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([data], { type: 'text/csv' })); a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    say('Downloaded ' + name + '. Import it into Google Sheets.');
  });
  /* the application being written today finishes while you look */
  let wrote = false;
  const finishWriting = () => { if (wrote) return; wrote = true; setTimeout(() => { const r = rows.find((x) => x.sent === 'writing'); if (!r) return; r.sent = 'gen'; const tr = tbody.querySelector(`[data-id="${r.id}"]`); if (tr) { tpl.innerHTML = rowHTML(r); const nr = tpl.content.firstElementChild; nr.classList.add('flash'); tr.replaceWith(nr); } say(`Your documents for ${r.role} are ready<button type="button" class="undo" data-open3="${r.id}">See them</button>`); const b = document.querySelector('[data-open3]'); if (b) b.addEventListener('click', () => { toast.hidden = true; openRow(r.id); }); }, 4200); };
  const watch = () => { if (document.getElementById('app').dataset.view === 'applied') finishWriting(); };
  addEventListener('hashchange', watch); watch();
  /* scroll shadows on the table */
  const tw = document.getElementById('tw'); const sh = () => { tw.classList.toggle('sl', tw.scrollLeft > 4); tw.classList.toggle('sr', tw.scrollLeft < tw.scrollWidth - tw.clientWidth - 4); };
  tw.addEventListener('scroll', sh, { passive: true }); addEventListener('resize', sh); sh();
  counts(); counts.ready = true;
  })();
"""

TD_STATIC_CSS = '.dw.td.static{translate:none !important;display:block}\n'
_td_dialogs = tracker_dialogs
def tracker_dialogs(static_id=None):
    h = _td_dialogs(static_id)
    if not static_id: return h
    r = next(x for x in ROWS if x['id'] == static_id); q = quiet(r); o = r.get('own') or {}
    rep = [('id="td-t">Role<', f'id="td-t">{r["role"]}<'), ('id="td-co">Company · City<', f'id="td-co">{r["co"]} · {r["city"]}<'),
           ('id="td-logo" aria-hidden="true">AB<', f'id="td-logo" aria-hidden="true">{ini2(r["co"])}<'), ('class="logo-c l1" id="td-logo"', f'class="logo-c {r["lc"]}" id="td-logo"'),
           ('<label class="stw big" id="td-stw">', f'<label class="stw big" id="td-stw" data-g="{grp(r["st"])}">'), (f'<option>{r["st"]}</option>', f'<option selected>{r["st"]}</option>'),
           ('id="td-q"></span>', f'id="td-q">Quiet for {q} days</span>'), ('id="td-fu" hidden', 'id="td-fu"' if fu(r) else 'id="td-fu" hidden'), ('id="td-fud">20<', f'id="td-fud">{q}<'),
           ('value="gen" checked>', 'value="gen">'), ('value="own">Your own', 'value="own" checked>Your own'),
           ('id="td-osub" placeholder', f'id="td-osub" value="{o.get("subject", "")}" placeholder'), ('placeholder="Paste the email or message you sent"></textarea>', f'placeholder="Paste the email or message you sent">{o.get("body", "")}</textarea>'),
           ('<div class="tfile">', '<div class="tfile has">' if o.get('file') else '<div class="tfile">'), ('id="td-ofn">Attach the CV you sent<', f'id="td-ofn">{o.get("file") or "Attach the CV you sent"}<')]
    for k in ('ap', 'fi', 'last', 'nextd'): rep.append((f'type="date" id="td-{k}">', f'type="date" id="td-{k}" value="{r[k]}">'))
    for k, v in (('next', r['next']), ('city', r['city']), ('ct', r['contact']), ('pay', r['pay']), ('link', r['link'])): rep.append((f'id="td-{k}"', f'id="td-{k}" value="{v}"'))
    rep.append(('<textarea id="td-notes" rows="3"></textarea>', f'<textarea id="td-notes" rows="3">{r["notes"]}</textarea>'))
    so = ''.join(f'<option>{x}</option>' for x in SOURCES); rep.append(('<select id="td-src">' + so, '<select id="td-src">' + so.replace(f'<option>{r["src"]}</option>', f'<option selected>{r["src"]}</option>')))
    for a, b in rep:
        assert a in h, a; h = h.replace(a, b, 1)
    return h.split('<dialog class="tadd-d"')[0]
