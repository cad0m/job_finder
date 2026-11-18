import { Link } from 'react-router-dom';
import './Landing.css';
import { LandingPeekArt } from './LandingArt';

/* Generated from index.html by design/tools/html2react.py, then wired by hand. */
export default function LandingMarkup() {
  return (
    <div className="jm-landing"><div role="main" className="page" style={{ color: "#1E1C2B", fontFamily: "Outfit, 'Noto Sans Arabic', system-ui, sans-serif" }}>

  
  <div className="hdr">
  <header className="wrap" style={{ paddingBlock: "14px", display: "flex", alignItems: "center", justifyContent: "space-between", gap: "20px" }}>
    <a href="#top" style={{ display: "flex", alignItems: "center", gap: "10px", textDecoration: "none" }}>
      <img src="/jm/nabta-mark.svg" alt="" style={{ width: "42px", height: "42px" }} decoding="async" />
      <span className="display" style={{ fontSize: "32px", lineHeight: "1" }}>JobMatcher</span>
    </a>
    <nav className="nav" aria-label="Page sections" style={{ display: "flex", gap: "6px", padding: "6px", borderRadius: "999px", background: "#FFFFFF", fontSize: "16px", fontWeight: "500" }}>
      <a href="#how" style={{ padding: "10px 18px", borderRadius: "999px", textDecoration: "none" }}>How it works</a>
      <a href="#search" style={{ padding: "10px 18px", borderRadius: "999px", textDecoration: "none" }}>Search</a>
      <a href="#matches" style={{ padding: "10px 18px", borderRadius: "999px", textDecoration: "none" }}>Matches</a>
      <a href="#sources" style={{ padding: "10px 18px", borderRadius: "999px", textDecoration: "none" }}>Sources</a>
      <a href="#faq" style={{ padding: "10px 18px", borderRadius: "999px", textDecoration: "none" }}>Questions</a>
    </nav>
    <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
      <button className="lang" aria-label="Language: English. Also available in French and Arabic."><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#1E1C2B" strokeWidth="2" aria-hidden="true"><circle cx="12" cy="12" r="9" /><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z" /></svg><span className="lbl">EN</span></button>
      <Link className="signin" to="/signin" style={{ display: "inline-flex", alignItems: "center", minHeight: "48px", padding: "0 16px", textDecoration: "none", fontSize: "16px", fontWeight: "500" }}>Sign in</Link>
      <Link className="btn-ink hdr-cta" to="/signup" style={{ minHeight: "48px", padding: "0 22px", fontSize: "16px" }}><span>Upload your CV</span></Link>
    </div>
  </header>
  </div>

  
  <div className="wrap" style={{ paddingTop: "8px" }}>
    <section id="top" className="hero" style={{ position: "relative", overflow: "clip", display: "flex", flexWrap: "wrap", alignItems: "center", gap: "56px 64px", padding: "64px 64px 64px", borderRadius: "40px", background: "#E9E5FF" }}>

      <div style={{ position: "relative", flex: "1.25 1 460px", minWidth: "0", display: "flex", flexDirection: "column", gap: "28px" }}>
        <span className="in" style={{ "--d": "0", alignSelf: "flex-start", display: "inline-flex", alignItems: "center", gap: "8px", minHeight: "36px", whiteSpace: "nowrap", padding: "0 16px 0 6px", borderRadius: "999px", background: "#FFFFFF", fontSize: "15px", fontWeight: "500" }}><span style={{ display: "grid", placeItems: "center", width: "26px", height: "26px", borderRadius: "50%", background: "#1E1C2B", color: "#FFFFFF", fontSize: "13px", fontWeight: "700" }}>3</span><span>job boards, one search<span className="hide-sm">: ANAPEC, Jobzyn, LinkedIn</span></span></span>
        <h1 className="display hero-h1" style={{ fontSize: "clamp(60px, 7.2vw, 100px)", lineHeight: "0.92" }}><span className="wd" style={{ "--w": "0" }}>Grow</span> <span className="wd" style={{ "--w": "1" }}>into</span> <br className="br br-keep" /><span className="wd" style={{ "--w": "2" }}>your</span> <span className="uline"><span className="wd" style={{ "--w": "3" }}>next</span> <span className="wd" style={{ "--w": "4" }}>job.</span><svg className="swash" viewBox="0 0 300 24" preserveAspectRatio="none" aria-hidden="true"><path d="M4 17C70 7 170 5 296 13" pathLength="1" fill="none" stroke="#FF7F45" strokeWidth="7" strokeLinecap="round" /></svg></span></h1>
        <p className="lead in" style={{ "--d": "2", maxWidth: "500px", color: "#1E1C2B" }}>Upload your CV once. JobMatcher ranks the offers that fit you and drafts the CV, cover letter and email for the ones you pick.</p>
        <div className="cta in" style={{ "--d": "3", display: "flex", flexWrap: "wrap", alignItems: "center", gap: "12px" }}>
          <Link className="btn-ink" to="/signup">Upload your CV<svg className="nudge lp" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#FFFFFF" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" /></svg></Link>
          <a className="btn-line" href="#search">Search without a CV</a>
        </div>
        <div className="in" style={{ "--d": "4", display: "flex", flexWrap: "wrap", alignItems: "center", gap: "14px" }}>
          <div className="faces" aria-hidden="true"><img src="/jm/peep-cv-match.svg" alt="" width="820" height="1181" decoding="async" /><img src="/jm/peep-code.svg" alt="" width="1050" height="1209" decoding="async" /><img src="/jm/peep-full-time.svg" alt="" width="832" height="1305" decoding="async" /><img src="/jm/peep-senior.svg" alt="" width="847" height="1189" decoding="async" /></div>
          <p style={{ margin: "0", maxWidth: "300px", fontSize: "15px", lineHeight: "22px", color: "#1E1C2B" }}>Made for students, graduates and professionals across Morocco.</p>
        </div>
      </div>

      
      <div className="demo" style={{ position: "relative", flex: "1 1 360px", minWidth: "0", maxWidth: "430px", margin: "96px auto 0" }}>
        <div className="aura a1 lp" aria-hidden="true" /><div className="aura a2 lp" aria-hidden="true" />
        <LandingPeekArt />
        <div className="burst" aria-hidden="true" style={{ position: "absolute", zIndex: "4", top: "-44px", right: "-26px", display: "grid", placeItems: "center", width: "112px", height: "112px", background: "#FFFFFF", clipPath: "polygon(50.0% 0.0%, 59.1% 10.0%, 71.7% 5.0%, 75.6% 17.9%, 89.1% 18.8%, 86.9% 32.2%, 98.7% 38.9%, 91.0% 50.0%, 98.7% 61.1%, 86.9% 67.8%, 89.1% 81.2%, 75.6% 82.1%, 71.7% 95.0%, 59.1% 90.0%, 50.0% 100.0%, 40.9% 90.0%, 28.3% 95.0%, 24.4% 82.1%, 10.9% 81.2%, 13.1% 67.8%, 1.3% 61.1%, 9.0% 50.0%, 1.3% 38.9%, 13.1% 32.2%, 10.9% 18.8%, 24.4% 17.9%, 28.3% 5.0%, 40.9% 10.0%)", fontSize: "14.5px", fontWeight: "700", lineHeight: "1.1", textAlign: "center", color: "#1E1C2B" }}><span style={{ transform: "rotate(-12deg)" }}>One CV,<br />every offer</span></div>

        <div className="card-in" style={{ position: "relative", zIndex: "2", padding: "14px", borderRadius: "40px", background: "#FFFFFF", display: "flex", flexDirection: "column", gap: "6px" }}>
          <div role="tablist" style={{ display: "flex", margin: "0 6px 6px", borderBottom: "1.5px solid #DAD6EA" }}>
            <button role="tab" aria-selected="true" style={{ flex: "1 1 0", padding: "12px 8px", marginBottom: "-1.5px", border: "0", borderBottom: "2.5px solid #1E1C2B", background: "none", color: "#1E1C2B", font: "600 16px/20px Outfit, system-ui, sans-serif" }}>Jobs</button>
            <button role="tab" aria-selected="false" style={{ flex: "1 1 0", padding: "12px 8px", marginBottom: "-1.5px", border: "0", borderBottom: "2.5px solid transparent", background: "none", color: "#5E5C6E", font: "500 16px/20px Outfit, system-ui, sans-serif" }}>Internships</button>
          </div>
          <div style={{ padding: "18px 16px 12px", borderRadius: "20px", background: "#F6F5FB", display: "flex", flexDirection: "column", gap: "12px" }}>
            <h2 className="display" style={{ fontSize: "32px", lineHeight: "1.08" }}>What position?</h2>
            <label style={{ position: "relative", display: "block" }}>
              <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" style={{ position: "absolute", left: "15px", top: "16px", fill: "none", stroke: "#1E1C2B", strokeWidth: "2.2" }}><circle cx="10.5" cy="10.5" r="6.5" /><path d="M15.5 15.5L20 20" strokeLinecap="round" /></svg>
              <input className="hero-in" type="search" placeholder="Type a job title…" aria-label="Job title" style={{ width: "100%", height: "52px", boxSizing: "border-box", padding: "0 16px 0 46px", border: "1.5px solid #8B89A0", borderRadius: "16px", background: "#FFFFFF", color: "#1E1C2B", font: "400 16px/24px Outfit, system-ui, sans-serif" }} />
            <span className="dq" aria-hidden="true"><span className="dq-ph lp">Type a job title…</span><span className="dq-t lp">Data Engineer</span><i className="dq-c lp" /></span></label>
            <div className="hq" style={{ display: "flex", flexDirection: "column", gap: "12px" }}><p style={{ margin: "2px 0 -4px", fontSize: "14px", lineHeight: "20px", color: "#5E5C6E" }}>Quick search</p>
            <Link className="item" to="/signup"><span className="tile"><img src="/jm/peep-cv-match.svg" alt="" width="820" height="1181" decoding="async" /></span><span><span className="t1">CV Match</span><span className="t2">Offers picked from your CV</span></span></Link>
            <a className="item" href="#search"><span className="tile"><img src="/jm/peep-data.svg" alt="" width="1050" height="1149" decoding="async" /></span><span><span className="t1">Stage PFE</span><span className="t2">End-of-studies internships</span></span></a></div>
          </div>
          <button className="row r1 lp" style={{ background: "#F6F5FB" }}>Where?<b className="sw"><span className="sa lp">Any location</span><span className="sb lp" aria-hidden="true">Casablanca</span></b></button>
          <button className="row r2 lp" style={{ "--o": ".72s", background: "#F6F5FB" }}>Experience level?<b className="sw"><span className="sa lp">All levels</span><span className="sb lp" aria-hidden="true">Junior</span></b></button>
          <button className="row" style={{ background: "#F6F5FB" }}>Job type?<b>Any type</b></button>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: "12px", padding: "8px 2px 0" }}>
            <a href="#top" style={{ display: "inline-flex", alignItems: "center", minHeight: "54px", padding: "0 18px", textDecoration: "none", fontSize: "17px", fontWeight: "500" }}>Back</a>
            <a className="btn-ink xbtn lp" href="#matches"><span>Explore <b className="count lp" style={{ "--n": "280", fontWeight: "700" }}><span className="num">280</span></b> jobs</span></a>
          </div>
        </div>
        <div className="mt lp" aria-hidden="true">
          <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
            <span style={{ display: "inline-flex", alignItems: "center", gap: "6px" }}><svg viewBox="0 0 48 56" width="32" height="38"><rect className="mt-lvl lp" x="16" y="16.3" width="16" height="33.7" rx="1.5" fill="#FF7F45" /><rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" strokeWidth="2.8" /><path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" strokeWidth="2.8" strokeLinejoin="round" /></svg><span className="display mt-pct lp" style={{ fontSize: "30px", lineHeight: "1" }}><span className="num">91</span></span><small style={{ fontSize: "14px", fontWeight: "600" }}>%</small></span>
            <span style={{ minWidth: "0" }}><span className="t1">Data Engineer</span><span className="t2">Attijariwafa bank · Casablanca</span></span>
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}><span className="tag hit">Python</span><span className="tag hit">Spark</span><span className="tag hit">Airflow</span></div>
          <span className="mt-go"><b className="sw" style={{ justifyItems: "center" }}><span className="sa lp" style={{ "--o": "4.8s" }}>Prepare application</span><span className="sb lp" style={{ "--o": "4.8s", display: "inline-flex", alignItems: "center", gap: "6px" }}><svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#FFFFFF" strokeWidth="2.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5" /></svg>Application pack ready</span></b></span>
        </div>
      </div>
      <label className="mp" title="Pause the animation"><input type="checkbox" id="mpause" aria-label="Pause the animation" /><svg className="i-pause" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1.2" fill="#1E1C2B" /><rect x="14" y="5" width="4" height="14" rx="1.2" fill="#1E1C2B" /></svg><svg className="i-play" viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="#1E1C2B" /></svg></label>
    </section>
  </div>

  
  <div className="wrap" style={{ paddingTop: "28px" }}>
    <div className="chips rv" tabIndex="0" aria-label="Popular searches" style={{ display: "flex", flexWrap: "wrap", alignItems: "center", justifyContent: "center", gap: "10px" }}>
      <span style={{ flex: "none", fontSize: "15px", color: "#5E5C6E", marginRight: "6px" }}>People search for</span>
      <span className="search-chip"><img src="/jm/peep-data.svg" alt="" width="1050" height="1149" decoding="async" loading="lazy" />Data Engineer</span>
      <span className="search-chip"><img src="/jm/peep-code.svg" alt="" width="1050" height="1209" decoding="async" loading="lazy" />Développeur full-stack</span>
      <span className="search-chip"><img src="/jm/peep-intern.svg" alt="" width="861" height="1228" decoding="async" loading="lazy" />Stage PFE</span>
      <span className="search-chip"><img src="/jm/peep-design.svg" alt="" width="778" height="1247" decoding="async" loading="lazy" />UI/UX Designer</span>
      <span className="search-chip"><img src="/jm/peep-remote.svg" alt="" width="795" height="1151" decoding="async" loading="lazy" />Remote</span>
    </div>
  </div>

  
  <section id="how" className="wrap sec story">
    <div className="story-intro">
      <h2 className="display h2 split" style={{ maxWidth: "560px" }}><span className="w" style={{ "--w": "0" }}>From</span> <span className="w" style={{ "--w": "1" }}>one</span> <span className="w" style={{ "--w": "2" }}>CV</span> <span className="w" style={{ "--w": "3" }}>to</span> <span className="w" style={{ "--w": "4" }}>a</span> <span className="w" style={{ "--w": "5" }}>sent</span> <span className="w" style={{ "--w": "6" }}>application.</span></h2>
      <p className="lead rv" style={{ "--i": "1", maxWidth: "400px" }}>Upload once, then pick the offers worth your time. JobMatcher reads, ranks and drafts. You check and send.</p>
    </div>
    <ol className="stack">
      <li className="scard" style={{ "--i": "0" }}>
        <div className="scard-txt">
          <span className="display snum" aria-hidden="true">1</span>
          <h3 className="sh3">Upload your CV</h3>
          <p className="sp" style={{ margin: "0", fontSize: "17px", lineHeight: "26px", color: "#5E5C6E" }}>A PDF or a photo. You check what JobMatcher read before anything is saved.</p>
          <div className="smeta"><span className="tag">PDF</span><span className="tag">JPEG</span><span className="tag">PNG</span><span className="tag">WEBP</span><span className="smuted">up to 10 MB</span></div>
        </div>
        <img className="simg" src="/jm/peep-cv-match.svg" alt="" width="820" height="1181" decoding="async" loading="lazy" />
      </li>
      <li className="scard" style={{ "--i": "1" }}>
        <div className="scard-txt">
          <span className="display snum" aria-hidden="true">2</span>
          <h3 className="sh3">See what fits you</h3>
          <p className="sp" style={{ margin: "0", fontSize: "17px", lineHeight: "26px", color: "#5E5C6E" }}>Every offer gets a match score against your CV. The best fits come first.</p>
          <div className="smeta"><span className="tag hit">91%</span><span className="tag">76%</span><span className="tag">58%</span><span className="smuted">best fit first</span></div>
        </div>
        <img className="simg" src="/jm/peep-data.svg" alt="" width="1050" height="1149" decoding="async" loading="lazy" />
      </li>
      <li className="scard" style={{ "--i": "2" }}>
        <div className="scard-txt">
          <span className="display snum" aria-hidden="true">3</span>
          <h3 className="sh3">Apply with a ready pack</h3>
          <p className="sp" style={{ margin: "0", fontSize: "17px", lineHeight: "26px", color: "#5E5C6E" }}>A tailored CV, a cover letter and an email for the offer you pick.</p>
          <div className="smeta"><span className="tag hit">CV</span><span className="tag hit">Cover letter</span><span className="tag hit">Email</span></div>
        </div>
        <img className="simg" src="/jm/peep-design.svg" alt="" width="778" height="1247" decoding="async" loading="lazy" />
      </li>
    </ol>
  </section>

  
  <section id="search" className="wrap sec">
    <div className="panel2" style={{ padding: "72px 56px", borderRadius: "40px", background: "#FFFFFF", display: "flex", flexDirection: "column", gap: "40px" }}>
      <div style={{ display: "flex", flexWrap: "wrap", alignItems: "flex-end", justifyContent: "space-between", gap: "20px" }}>
        <h2 className="display h2 split" style={{ maxWidth: "620px" }}><span className="w" style={{ "--w": "0" }}>Four</span> <span className="w" style={{ "--w": "1" }}>short</span> <span className="w" style={{ "--w": "2" }}>questions.</span> <span style={{ display: "inline-block" }}><span className="w" style={{ "--w": "3" }}>Skip</span> <span className="w" style={{ "--w": "4" }}>any</span> <span className="w" style={{ "--w": "5" }}>of</span> <span className="w" style={{ "--w": "6" }}>them.</span></span></h2>
        <p className="lead rv" style={{ "--i": "1", maxWidth: "400px" }}>Each answer narrows the list, and the count on the button updates as you go. With a CV, the first one is answered for you.</p>
      </div>
      <div className="qgrid rail rail-q rail-b">
        <div className="qcard" style={{ "--i": "0" }}>
          <h3 className="display qtitle">What position?</h3>
          <label className="field"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="#1E1C2B" strokeWidth="2.2"><circle cx="10.5" cy="10.5" r="6.5" /><path d="M15.5 15.5L20 20" strokeLinecap="round" /></svg><input type="search" placeholder="Type a job title…" aria-label="Job title" /></label>
          <p className="glabel">Quick search</p>
          <Link className="item item-w" to="/signup"><span className="tile"><img src="/jm/peep-cv-match.svg" alt="" width="820" height="1181" decoding="async" loading="lazy" /></span><span><span className="t1">CV Match</span><span className="t2">Offers picked from your CV</span></span></Link>
          <p className="glabel">Popular roles</p>
          <div className="rolechips">
            <a className="rolechip" href="#search"><img src="/jm/peep-data.svg" alt="" width="1050" height="1149" decoding="async" loading="lazy" />Data Engineer</a>
            <a className="rolechip" href="#search"><img src="/jm/peep-intern.svg" alt="" width="861" height="1228" decoding="async" loading="lazy" />Stage PFE</a>
            <a className="rolechip" href="#search"><img src="/jm/peep-code.svg" alt="" width="1050" height="1209" decoding="async" loading="lazy" />Développeur full-stack</a>
            <a className="rolechip" href="#search"><img src="/jm/peep-design.svg" alt="" width="778" height="1247" decoding="async" loading="lazy" />UI/UX Designer</a>
          </div>
        </div>
        <div className="qcard" style={{ "--i": "1" }}>
          <h3 className="display qtitle">Where?</h3>
          <label className="field"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="#1E1C2B" strokeWidth="2.2"><circle cx="10.5" cy="10.5" r="6.5" /><path d="M15.5 15.5L20 20" strokeLinecap="round" /></svg><input type="search" placeholder="Type a city…" aria-label="City" /></label>
          <p className="glabel">Quick search</p>
          <a className="item item-w" href="#search"><span className="tile"><img src="/jm/peep-nearby.svg" alt="" width="840" height="1174" decoding="async" loading="lazy" /></span><span><span className="t1">Nearby</span><span className="t2">Find a job around you</span></span></a>
          <a className="item item-w" href="#search"><span className="tile"><img src="/jm/peep-remote.svg" alt="" width="795" height="1151" decoding="async" loading="lazy" /></span><span><span className="t1">Remote</span><span className="t2">Work from anywhere in Morocco</span></span></a>
          <a className="item item-w" href="#search"><span className="tile"><img src="/jm/peep-relocate.svg" alt="" width="1083" height="2890" decoding="async" loading="lazy" /></span><span><span className="t1">Relocate</span><span className="t2">Ready for a new city</span></span></a>
        </div>
        <div className="qcard" style={{ "--i": "0" }}>
          <h3 className="display qtitle">Experience level?</h3>
          <div className="tiles4">
            <button className="opt" aria-pressed="false" style={{ background: "#FFFFFF" }}><img src="/jm/peep-intern.svg" alt="" width="861" height="1228" decoding="async" loading="lazy" />Intern<span style={{ fontSize: "13px", fontWeight: "400", color: "#5E5C6E" }}>0–1 years</span></button>
            <button className="opt" aria-pressed="true"><img src="/jm/peep-code.svg" alt="" width="1050" height="1209" decoding="async" loading="lazy" />Junior<span style={{ fontSize: "13px", fontWeight: "400", color: "#5E5C6E" }}>2–3 years</span></button>
            <button className="opt" aria-pressed="false" style={{ background: "#FFFFFF" }}><img src="/jm/peep-mid.svg" alt="" width="840" height="1184" decoding="async" loading="lazy" />Mid-level<span style={{ fontSize: "13px", fontWeight: "400", color: "#5E5C6E" }}>4–6 years</span></button>
            <button className="opt" aria-pressed="false" style={{ background: "#FFFFFF" }}><img src="/jm/peep-senior.svg" alt="" width="847" height="1189" decoding="async" loading="lazy" />Senior<span style={{ fontSize: "13px", fontWeight: "400", color: "#5E5C6E" }}>7+ years</span></button>
          </div>
        </div>
        <div className="qcard" style={{ "--i": "1" }}>
          <h3 className="display qtitle">Job type?</h3>
          <div className="tiles4">
            <button className="opt" aria-pressed="true"><img src="/jm/peep-full-time.svg" alt="" width="832" height="1305" decoding="async" loading="lazy" />Full-time</button>
            <button className="opt" aria-pressed="false" style={{ background: "#FFFFFF" }}><img src="/jm/peep-part-time.svg" alt="" width="1353" height="2064" decoding="async" loading="lazy" />Part-time</button>
            <button className="opt" aria-pressed="false" style={{ background: "#FFFFFF" }}><img src="/jm/peep-contract.svg" alt="" width="1094" height="2899" decoding="async" loading="lazy" />Contract</button>
            <button className="opt" aria-pressed="false" style={{ background: "#FFFFFF" }}><img src="/jm/peep-apply.svg" alt="" width="820" height="1162" decoding="async" loading="lazy" />Internship</button>
          </div>
        </div>
      </div>
      <div className="dots dots-b" aria-hidden="true" style={{ "--travel": "32px" }}><i className="on" /><i /><i /><i /><b /></div>
    </div>
  </section>

  
  <section id="matches" className="wrap sec" style={{ display: "flex", flexWrap: "wrap", gap: "48px", alignItems: "stretch" }}>
    <div style={{ flex: "1 1 380px", minWidth: "0", alignSelf: "stretch", display: "flex", flexDirection: "column", gap: "20px" }}>
      <h2 className="display h2 split"><span className="w" style={{ "--w": "0" }}>Your</span> <span className="w" style={{ "--w": "1" }}>matches,</span> <span className="w" style={{ "--w": "2" }}>best</span> <span className="w" style={{ "--w": "3" }}>fit</span> <span className="w" style={{ "--w": "4" }}>first.</span></h2>
      <p className="lead rv" style={{ "--i": "1", maxWidth: "440px" }}>The pot fills with how well an offer matches your CV. Skills you already have get an orange dot, so you see why at a glance.</p>
      <img src="/jm/peep-full-time.svg" alt="" className="m-peep" style={{ height: "250px", width: "auto", maxWidth: "100%", marginTop: "auto", alignSelf: "flex-start" }} width="832" height="1305" decoding="async" loading="lazy" />
    </div>
    <div className="rv" style={{ flex: "1.3 1 520px", minWidth: "0", padding: "14px", borderRadius: "40px", background: "#E9E5FF", display: "flex", flexDirection: "column", gap: "8px" }}>
      <div className="mcard" style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: "14px 20px", padding: "20px 22px", borderRadius: "28px", background: "#FFFFFF" }}>
        <span style={{ display: "inline-flex", alignItems: "center", gap: "10px", width: "104px" }} role="img" aria-label="91% match"><svg viewBox="0 0 48 56" width="40" height="46" aria-hidden="true"><rect className="lvl" x="16" y="16.3" width="16" height="33.7" rx="1.5" fill="#FF7F45" /><rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" strokeWidth="2.8" /><path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" strokeWidth="2.8" strokeLinejoin="round" /></svg><span className="display pct" style={{ "--p": "91", fontSize: "34px", lineHeight: "1" }}><span className="num">91</span><small style={{ fontFamily: "Outfit, sans-serif", fontSize: "15px", fontWeight: "600" }}>%</small></span></span>
        <div style={{ flex: "1 1 240px", minWidth: "0" }}>
          <span className="t1" style={{ fontSize: "19px" }}>Data Engineer</span><span className="t2">Attijariwafa bank · Casablanca · Jobzyn</span>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "6px", marginTop: "10px" }}><span className="tag hit">Python</span><span className="tag hit">Spark</span><span className="tag hit">Airflow</span><span className="tag">Scala</span></div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "6px 16px", marginTop: "14px", paddingTop: "12px", borderTop: "1px solid #DAD6EA" }}><span style={{ fontSize: "14px", fontWeight: "700" }}>Why it fits you</span><span className="why"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#1E1C2B" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path className="ck" pathLength="1" d="M5 12.5l4.5 4.5L19 7.5" /></svg>3 of 4 skills on your CV</span><span className="why"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#1E1C2B" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path className="ck" pathLength="1" d="M5 12.5l4.5 4.5L19 7.5" /></svg>Junior level, like you</span><span className="why"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#1E1C2B" strokeWidth="2.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path className="ck" pathLength="1" d="M5 12.5l4.5 4.5L19 7.5" /></svg>In Casablanca</span></div>
        </div>
        <Link className="btn-ink" to="/signup" style={{ minHeight: "46px", padding: "0 20px", fontSize: "15px" }}>Prepare application</Link>
      </div>
      <div className="mcard" style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: "14px 20px", padding: "18px 22px", borderRadius: "28px", background: "#FFFFFF" }}>
        <span style={{ display: "inline-flex", alignItems: "center", gap: "10px", width: "104px" }} role="img" aria-label="76% match"><svg viewBox="0 0 48 56" width="40" height="46" aria-hidden="true"><rect className="lvl" x="16" y="21.9" width="16" height="28.1" rx="1.5" fill="#FF7F45" /><rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" strokeWidth="2.8" /><path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" strokeWidth="2.8" strokeLinejoin="round" /></svg><span className="display pct" style={{ "--p": "76", fontSize: "34px", lineHeight: "1" }}><span className="num">76</span><small style={{ fontFamily: "Outfit, sans-serif", fontSize: "15px", fontWeight: "600" }}>%</small></span></span>
        <div style={{ flex: "1 1 240px", minWidth: "0" }}>
          <span className="t1" style={{ fontSize: "19px" }}>Ingénieur BI junior</span><span className="t2">OCP Group · Rabat · ANAPEC</span>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "6px", marginTop: "10px" }}><span className="tag hit">SQL</span><span className="tag hit">Power BI</span><span className="tag">SAP BW</span></div>
        </div>
      </div>
      <div className="mcard" style={{ display: "flex", flexWrap: "wrap", alignItems: "center", gap: "14px 20px", padding: "18px 22px", borderRadius: "28px", background: "#FFFFFF" }}>
        <span style={{ display: "inline-flex", alignItems: "center", gap: "10px", width: "104px" }} role="img" aria-label="58% match"><svg viewBox="0 0 48 56" width="40" height="46" aria-hidden="true"><rect className="lvl" x="16" y="28.5" width="16" height="21.5" rx="1.5" fill="#FF7F45" /><rect x="6" y="6" width="36" height="8" rx="3" fill="none" stroke="#1E1C2B" strokeWidth="2.8" /><path d="M9 14 L12 50 Q12.4 53 15 53 L33 53 Q35.6 53 36 50 L39 14" fill="none" stroke="#1E1C2B" strokeWidth="2.8" strokeLinejoin="round" /></svg><span className="display pct" style={{ "--p": "58", fontSize: "34px", lineHeight: "1" }}><span className="num">58</span><small style={{ fontFamily: "Outfit, sans-serif", fontSize: "15px", fontWeight: "600" }}>%</small></span></span>
        <div style={{ flex: "1 1 240px", minWidth: "0" }}>
          <span className="t1" style={{ fontSize: "19px" }}>Stage PFE Data Science</span><span className="t2">inwi · Casablanca · LinkedIn</span>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "6px", marginTop: "10px" }}><span className="tag hit">Python</span><span className="tag">PyTorch</span><span className="tag">MLflow</span></div>
        </div>
      </div>
      <p style={{ margin: "4px 10px 2px", fontSize: "14px", color: "#1E1C2B" }}>Example offers, to show how matches look.</p>
    </div>
  </section>

  
  <section id="sources" className="wrap sec" style={{ display: "flex", flexDirection: "column", gap: "40px" }}>
    <div style={{ display: "flex", flexWrap: "wrap", alignItems: "flex-end", justifyContent: "space-between", gap: "20px" }}>
      <h2 className="display h2 split" style={{ maxWidth: "680px" }}><span className="w" style={{ "--w": "0" }}>Three</span> <span className="w" style={{ "--w": "1" }}>job</span> <span className="w" style={{ "--w": "2" }}>boards,</span> <span className="w" style={{ "--w": "3" }}>one</span> <span className="w" style={{ "--w": "4" }}>list.</span></h2>
      <p className="lead rv" style={{ "--i": "1", maxWidth: "400px" }}>Collected every day, cleaned up, and kept with a link to the original post.</p>
    </div>
    <div className="srcs" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(min(100%, 300px), 1fr))", gap: "16px" }}>
      <div className="cvg" style={{ "--i": "0", "--sx": "-72px", "--sy": "0px", display: "flex", flexDirection: "column", gap: "10px", padding: "30px 28px", borderRadius: "28px", background: "#FFFFFF" }}><span className="display" style={{ fontSize: "44px", lineHeight: "1" }}>ANAPEC</span><span style={{ fontSize: "17px", lineHeight: "26px", color: "#5E5C6E" }}>The national employment agency, public and private sector offers.</span></div>
      <div className="cvg" style={{ "--i": "1", "--sx": "0px", "--sy": "56px", display: "flex", flexDirection: "column", gap: "10px", padding: "30px 28px", borderRadius: "28px", background: "#FFFFFF" }}><span className="display" style={{ fontSize: "44px", lineHeight: "1" }}>Jobzyn</span><span style={{ fontSize: "17px", lineHeight: "26px", color: "#5E5C6E" }}>A Moroccan job board for local and remote roles.</span></div>
      <div className="cvg" style={{ "--i": "2", "--sx": "72px", "--sy": "0px", display: "flex", flexDirection: "column", gap: "10px", padding: "30px 28px", borderRadius: "28px", background: "#FFFFFF" }}><span className="display" style={{ fontSize: "44px", lineHeight: "1" }}>LinkedIn</span><span style={{ fontSize: "17px", lineHeight: "26px", color: "#5E5C6E" }}>Public job posts located in Morocco.</span></div>
    </div>
  </section>

  
  <section id="faq" className="wrap sec" style={{ display: "flex", flexDirection: "column", gap: "40px" }}>
    <div style={{ display: "flex", flexWrap: "wrap", alignItems: "flex-end", justifyContent: "space-between", gap: "20px" }}>
      <h2 className="display h2 split" style={{ maxWidth: "620px" }}><span className="w" style={{ "--w": "0" }}>Questions</span> <span className="w" style={{ "--w": "1" }}>people</span> <span className="w" style={{ "--w": "2" }}>ask.</span></h2>
      <p className="lead rv" style={{ "--i": "1", maxWidth: "400px" }}>Short answers before you upload anything.</p>
    </div>
    <div className="faq">
      <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
        <details className="rv" style={{ "--i": "0" }} open><summary>Can I search without uploading a CV?<span className="pm" aria-hidden="true"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#1E1C2B" strokeWidth="2.6" strokeLinecap="round"><path d="M12 5v14M5 12h14" /></svg></span></summary><p>Yes. Describe the job you want in your own words, or answer the four questions, and JobMatcher ranks offers by how close they are. Upload a CV when you want scores based on your experience.</p></details>
        <details className="rv" style={{ "--i": "1" }}><summary>Which files can I upload?<span className="pm" aria-hidden="true"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#1E1C2B" strokeWidth="2.6" strokeLinecap="round"><path d="M12 5v14M5 12h14" /></svg></span></summary><p>A PDF, or a photo or scan of your CV in JPEG, PNG or WEBP, up to 10 MB. You review and correct what was read before it is saved.</p></details>
        <details className="rv" style={{ "--i": "2" }}><summary>Does it include internships and Stage PFE?<span className="pm" aria-hidden="true"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#1E1C2B" strokeWidth="2.6" strokeLinecap="round"><path d="M12 5v14M5 12h14" /></svg></span></summary><p>Yes. Use the Internships tab, or set your experience level to Intern.</p></details>
        <details className="rv" style={{ "--i": "3" }}><summary>What is in the application pack?<span className="pm" aria-hidden="true"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#1E1C2B" strokeWidth="2.6" strokeLinecap="round"><path d="M12 5v14M5 12h14" /></svg></span></summary><p>A CV reordered around the offer in the template you choose, a cover letter addressed to the company, and an email to send with both. Read and adjust them before you apply.</p></details>
      </div>
    </div>
  </section>

  
  <section id="upload" className="wrap sec" style={{ paddingBottom: "80px" }}>
    <div className="panel grow" style={{ position: "relative", overflow: "clip", display: "flex", flexDirection: "column", alignItems: "center", gap: "24px", padding: "80px 40px 0", borderRadius: "40px", background: "#1E1C2B", color: "#FFFFFF", textAlign: "center" }}>
      <div aria-hidden="true" style={{ position: "absolute", width: "360px", height: "360px", borderRadius: "50%", background: "#2B2840", left: "-120px", top: "-140px" }} />
            <h2 className="display h2 split" style={{ position: "relative", maxWidth: "760px", color: "#FFFFFF" }}><span className="w" style={{ "--w": "0" }}>Every</span> <span className="w" style={{ "--w": "1" }}>stage</span> <span className="w" style={{ "--w": "2" }}>is</span> <span className="w" style={{ "--w": "3" }}>a</span> <span className="w" style={{ "--w": "4" }}>good</span> <span className="w" style={{ "--w": "5" }}>place</span> <span className="w" style={{ "--w": "6" }}>to</span> <span className="w" style={{ "--w": "7" }}>start.</span></h2>
      <p className="lead" style={{ position: "relative", maxWidth: "520px", color: "#E9E5FF" }}>From a first internship to a senior role. Upload a PDF or a photo of your CV, up to 10 MB.</p>
      <Link className="rv" to="/signup" style={{ "--i": "2", position: "relative", display: "inline-flex", alignItems: "center", gap: "10px", minHeight: "56px", padding: "0 30px", borderRadius: "999px", background: "#FFFFFF", color: "#1E1C2B", textDecoration: "none", fontSize: "17px", fontWeight: "600" }}>Upload your CV<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#1E1C2B" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" /></svg></Link>
      <div className="stages" style={{ position: "relative", display: "grid", gridTemplateColumns: "repeat(4, minmax(0, 1fr))", alignItems: "end", gap: "clamp(4px, 2vw, 24px)", width: "100%", maxWidth: "900px", boxSizing: "border-box", marginTop: "28px", padding: "24px 20px 0", borderRadius: "40px 40px 0 0", background: "#F6F5FB" }}>
        <figure className="fig" style={{ "--i": "0", margin: "0", display: "flex", flexDirection: "column", alignItems: "center", gap: "2px" }}><img src="/jm/peep-stage-1.svg" alt="" style={{ height: "clamp(130px, 22vw, 260px)", width: "auto", maxWidth: "100%" }} width="1083" height="3055" decoding="async" loading="lazy" /><figcaption style={{ whiteSpace: "nowrap", padding: "6px 0 16px", fontSize: "15px", fontWeight: "600", color: "#1E1C2B" }}>Intern</figcaption></figure>
        <figure className="fig" style={{ "--i": "1", margin: "0", display: "flex", flexDirection: "column", alignItems: "center", gap: "2px" }}><img src="/jm/peep-stage-2.svg" alt="" style={{ height: "clamp(130px, 22vw, 260px)", width: "auto", maxWidth: "100%" }} width="1846" height="2405" decoding="async" loading="lazy" /><figcaption style={{ whiteSpace: "nowrap", padding: "6px 0 16px", fontSize: "15px", fontWeight: "600", color: "#1E1C2B" }}>Junior</figcaption></figure>
        <figure className="fig" style={{ "--i": "2", margin: "0", display: "flex", flexDirection: "column", alignItems: "center", gap: "2px" }}><img src="/jm/peep-stage-3.svg" alt="" style={{ height: "clamp(130px, 22vw, 260px)", width: "auto", maxWidth: "100%" }} width="1094" height="2899" decoding="async" loading="lazy" /><figcaption style={{ whiteSpace: "nowrap", padding: "6px 0 16px", fontSize: "15px", fontWeight: "600", color: "#1E1C2B" }}>Mid-level</figcaption></figure>
        <figure className="fig" style={{ "--i": "3", margin: "0", display: "flex", flexDirection: "column", alignItems: "center", gap: "2px" }}><img src="/jm/peep-stage-4.svg" alt="" style={{ height: "clamp(130px, 22vw, 260px)", width: "auto", maxWidth: "100%" }} width="1348" height="2665" decoding="async" loading="lazy" /><figcaption style={{ whiteSpace: "nowrap", padding: "6px 0 16px", fontSize: "15px", fontWeight: "600", color: "#1E1C2B" }}>Senior</figcaption></figure>
      </div>
    </div>
  </section>

  
  <footer className="wrap" style={{ paddingBottom: "44px", display: "flex", flexWrap: "wrap", alignItems: "center", justifyContent: "space-between", gap: "18px", fontSize: "15px", color: "#5E5C6E" }}>
    <a href="#top" style={{ display: "flex", alignItems: "center", gap: "8px", textDecoration: "none" }}>
      <img src="/jm/nabta-mark.svg" alt="" style={{ width: "34px", height: "34px" }} decoding="async" loading="lazy" />
      <span className="display" style={{ fontSize: "26px", lineHeight: "1" }}>JobMatcher</span>
    </a>
    <nav className="fnav" aria-label="Footer" style={{ display: "flex", flexWrap: "wrap", gap: "22px" }}>
      <Link to="/signin" style={{ color: "#5E5C6E", textDecoration: "none" }}>Sign in</Link>
      <Link to="/signup" style={{ color: "#5E5C6E", textDecoration: "none" }}>Create an account</Link>
      <a href="#faq" style={{ color: "#5E5C6E", textDecoration: "none" }}>Questions</a>
      <a href="https://github.com/cad0m/job_finder" style={{ color: "#5E5C6E", textDecoration: "none" }}>Source on GitHub</a>
    </nav>
    <span>© 2026 JobMatcher</span>
  </footer>

</div></div>
  );
}
