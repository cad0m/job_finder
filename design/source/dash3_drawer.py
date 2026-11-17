import json as _json
DETAIL = {
 'b': dict(t='Data Engineer', co='Attijariwafa bank', city='Casablanca', src='Jobzyn', sc=91, typ='Full-time', lvl='Junior', sal='12,000 to 15,000 MAD a month', posted='2 days ago', lc='l1',
   have=['Python', 'Spark', 'SQL'], miss=['Airflow'],
   about='Join the data platform team that moves banking data from the core systems into the analytics lake used by the risk and marketing teams.',
   do=['Build and run batch pipelines in Python and Spark', 'Model lake data for the reporting teams', 'Watch the daily jobs and fix data quality issues'],
   ask=['A degree in computer science, data or a related field', 'Python and SQL', 'Spark, ideally in production', 'Airflow or another scheduler is a plus']),
}
ROWS = [
 dict(sal='', about='CIH Bank is growing its analytics team to support retail banking decisions with clear, reliable reporting.', do=['Build Power BI dashboards for the retail teams', 'Write SQL to prepare monthly figures', 'Explain results to business owners'], ask=['Python and SQL', 'Power BI', 'One internship in data is enough'], miss=[]),
 dict(sal='11,000 to 14,000 MAD a month', about='OCP Group needs a BI developer to bring plant and logistics data into one reporting layer.', do=['Design data models for production reporting', 'Build Power BI reports with the plant teams', 'Document every data source'], ask=['Power BI and SQL', 'SAP BW is a plus', 'French and English'], miss=['SAP BW']),
 dict(sal='', about='Maroc Telecom is hiring a junior BI engineer in Rabat to work on customer and network dashboards.', do=['Prepare data with SQL and Talend', 'Maintain Tableau dashboards', 'Check data quality every week'], ask=['SQL', 'Tableau', 'Talend or another ETL tool'], miss=['Talend']),
 dict(sal='', about='A six-month end-of-studies internship in the inwi data science team, on churn prediction.', do=['Explore customer data with Pandas', 'Train and compare models', 'Present your results to the team'], ask=['Last year of a Master or engineering school', 'Python and Pandas', 'PyTorch or scikit-learn'], miss=['PyTorch']),
 dict(sal='', about='Capgemini Rabat is looking for a junior data scientist for client projects in banking and insurance.', do=['Build models in Python and Spark', 'Turn notebooks into scheduled jobs', 'Work with consultants on client sites'], ask=['Python and Spark', 'Airflow is a plus', 'Good written French'], miss=['Airflow']),
 dict(sal='9,000 to 11,000 MAD a month', about='Marjane wants an analyst to follow sales and stock across its stores.', do=['Build weekly sales reports', 'Answer questions from store managers', 'Automate Excel reports with SQL'], ask=['Excel and SQL', 'Looker is a plus', 'Retail experience is a plus'], miss=['Looker']),
 dict(sal='', about='Deloitte is staffing a six-month contract on a machine learning platform for a client.', do=['Package models in Docker', 'Build training pipelines with Airflow', 'Write clear technical notes'], ask=['Python', 'Docker', 'Airflow', 'Two years of experience'], miss=['Docker', 'Airflow']),
 dict(sal='', about='A remote data team needs an engineer to run streaming pipelines.', do=['Run Spark and Kafka pipelines', 'Schedule jobs in Airflow', 'Keep costs under control'], ask=['Spark', 'Kafka', 'Airflow'], miss=['Kafka', 'Airflow']),
 dict(sal='', about='Avanade is looking for a BI consultant for Power BI projects on Azure.', do=['Gather client needs', 'Build Power BI models and DAX measures', 'Deploy reports on Azure'], ask=['Power BI and DAX', 'Azure is a plus', 'Client-facing French'], miss=['Azure']),
]
for k, j in enumerate(JOBS):
    t_, co, city, srcn, sc, typ, lvl, m, tot, posted, new, lc = j
    d = ROWS[k]
    DETAIL[str(k)] = dict(t=t_, co=co, city=city, src=srcn, sc=sc, typ=typ, lvl=lvl, sal=d['sal'], posted=posted, lc=lc, have=m, miss=d['miss'], about=d['about'], do=d['do'], ask=d['ask'])
ORDER = ['b'] + [str(k) for k in range(len(JOBS))]
CLOSE_I = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"></path></svg>'
PREV_I = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"></path></svg>'
NEXT_I = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"></path></svg>'
EXT_I = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5H5V6h5"></path></svg>'
def dbody(j):
    have = ''.join(f'<span class="t hit">{x}</span>' for x in j['have'])
    miss = ''.join(f'<span class="t miss">{x}</span>' for x in j['miss'])
    n_have, n_all = len(j['have']), len(j['have']) + len(j['miss'])
    facts = f'<span class="fact"><i class="ok">{TKS}</i>{n_have} of {n_all} skills</span><span class="fact"><i class="ok">{TKS}</i>{j["lvl"]}</span>' + (f'<span class="fact"><i class="ok">{TKS}</i>{j["city"]}</span>' if j['city'] in ('Casablanca', 'Remote') else f'<span class="fact miss">{j["city"]}, not your city</span>') + ''.join(f'<span class="fact miss">Missing: {x}</span>' for x in j['miss'][:1])
    li = lambda xs: ''.join(f'<li>{x}</li>' for x in xs)
    sal = j['sal'] or 'Not given'
    return f'''<div class="dw-hero" style="--i: 0;"><span class="logo-c {j['lc']}" aria-hidden="true">{ini(j['co'])}</span><span><b>{j['co']}</b><span>{j['city']} · posted {j['posted']}</span></span></div>
        <h2 class="dw-t" id="dw-t" style="--i: 1;">{j['t']}</h2>
        <div class="dw-tags" style="--i: 2;"><span class="t">{j['typ']}</span><span class="t">{j['lvl']}</span><span class="t">{j['city']}</span><span class="src-b">{j['src']}</span></div>
        <section class="dw-match" style="--i: 3;"><div class="cupbig sm" role="img" aria-label="{j['sc']}% match">{cup(j['sc'], 52, 'cup big')}<span class="v"><b>{j['sc']}<small>%</small></b><span>match</span></span></div><div class="facts">{facts}</div></section>
        <section class="dw-s" style="--i: 4;"><h3>Skills it asks for</h3><div class="dw-sk">{have}{miss}</div><p class="dw-n">The ones with a dot are on your CV.</p></section>
        <section class="dw-s" style="--i: 5;"><h3>About the role</h3><p>{j['about']}</p></section>
        <section class="dw-s" style="--i: 6;"><h3>What you will do</h3><ul>{li(j['do'])}</ul></section>
        <section class="dw-s" style="--i: 7;"><h3>What they ask for</h3><ul>{li(j['ask'])}</ul></section>
        <section class="dw-grid" style="--i: 8;"><div><span>Salary</span><b>{sal}</b></div><div><span>Contract</span><b>{j['typ']}</b></div><div><span>Level</span><b>{j['lvl']}</b></div><div><span>Source</span><b>{j['src']}</b></div></section>'''
def drawer(static=False):
    j = DETAIL['b']
    attrs = ' class="dw static" open' if static else ' class="dw" id="dw" closedby="any" aria-labelledby="dw-t"'
    tag = 'div' if static else 'dialog'
    bd = '<div class="dwbd" aria-hidden="true"></div>' if static else ''
    return f'''{bd}<{tag}{attrs}>
    <div class="dw-in">
      <header class="dw-top"><button class="dw-ib" type="button" id="dw-prev" aria-label="Previous offer">{PREV_I}</button><button class="dw-ib" type="button" id="dw-next" aria-label="Next offer">{NEXT_I}</button><span class="dw-pos" id="dw-pos">1 of {len(ORDER)}</span><button class="dw-ib dw-x" type="button" id="dw-close" aria-label="Close">{CLOSE_I}</button></header>
      <div class="dw-body" id="dw-body">
        {dbody(j)}
      </div>
      <footer class="dw-foot"><a class="go" href="#apply" id="dw-apply"><span class="s-go">Prepare application{ARR}</span></a><button class="dw-save" type="button" id="dw-save" aria-pressed="false" aria-label="Save this offer">{BOOK}</button><a class="dw-ext" href="#source" id="dw-ext">{EXT_I}<span>Original post</span></a></footer>
    </div>
  </{tag}>'''
DRAWER_DATA = '<script type="application/json" id="jobdata">' + _json.dumps({'order': ORDER, 'jobs': {k: dict(v, html=dbody(v)) for k, v in DETAIL.items()}}) + '</script>'
