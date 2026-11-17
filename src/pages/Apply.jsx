import { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import { useAuth } from '../hooks/useAuth';
import { supabase } from '../lib/supabaseClient';
import { supabaseDB } from '../services/supabaseDB';
import { edgeFunctions } from '../services/edgeFunctions';
import './Apply.css';

/* ─────────────────────────────────────────────
   SUB-COMPONENTS
───────────────────────────────────────────── */

const NoCvBanner = () => (
  <div className="no-cv-banner">
    <div className="ap-glass no-cv-banner__card">
      <span className="material-symbols-outlined no-cv-banner__icon">upload_file</span>
      <h2 className="no-cv-banner__title">Upload your CV first</h2>
      <p className="no-cv-banner__body">
        The application documents are written from your CV. Upload it, then come back to this offer.
      </p>
      <Link to="/upload" className="no-cv-banner__btn">
        <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>upload</span>
        Upload your CV
      </Link>
    </div>
  </div>
);

const JobHeader = ({ jobDetails }) => (
  <div className="ap-glass job-header">
    {jobDetails?.logo_url ? (
      <img src={jobDetails.logo_url} alt={jobDetails.company_name} className="job-header__logo" />
    ) : (
      <div className="job-header__icon">
        <span className="material-symbols-outlined">work</span>
      </div>
    )}
    <div>
      <p className="job-header__kicker">Application for</p>
      <h1 className="job-header__title">{jobDetails?.title || 'Loading…'}</h1>
      <p className="job-header__company">{jobDetails?.company_name || ''}</p>
    </div>
  </div>
);

const StepIndicator = ({ currentStep }) => (
  <div className="step-indicator">
    <div className="step-indicator__item">
      <div className={`step-indicator__circle ${currentStep === 1 ? 'active' : 'completed'}`}>
        {currentStep > 1
          ? <span className="material-symbols-outlined" style={{ fontSize: '16px' }}>check</span>
          : '1'
        }
      </div>
      <span className={`step-indicator__label ${currentStep === 1 ? 'active' : ''}`}>Set up</span>
    </div>
    <div className="step-indicator__connector">
      <div className={`step-indicator__connector-fill ${currentStep === 2 ? 'active' : ''}`} />
    </div>
    <div className="step-indicator__item">
      <div className={`step-indicator__circle ${currentStep === 2 ? 'active' : ''}`}>2</div>
      <span className={`step-indicator__label ${currentStep === 2 ? 'active' : ''}`}>Your documents</span>
    </div>
  </div>
);

const TEMPLATES = [1, 2, 3, 4, 5];

const TemplateSelector = ({ selectedTemplate, onSelectTemplate }) => {
  const [imgErrors, setImgErrors] = useState({});
  const handleImgError = (idx) => setImgErrors(prev => ({ ...prev, [idx]: true }));
  const selectedNum = selectedTemplate?.replace('template', '').replace('.tex', '');

  return (
    <div className="template-section">
      <h2 className="section-label">Choose a CV template</h2>
      <div className="template-scroll-row">
        {TEMPLATES.map((i) => {
          const key = `template${i}.tex`;
          const isSelected = selectedTemplate === key;
          return (
            <div
              key={key}
              className={`template-card ${isSelected ? 'selected' : ''}`}
              onClick={() => onSelectTemplate(key)}
              role="button"
              aria-label={`Select Template ${i}`}
              tabIndex={0}
              onKeyDown={(e) => e.key === 'Enter' && onSelectTemplate(key)}
            >
              {imgErrors[i] ? (
                <div className="template-card__placeholder">
                  <span className="material-symbols-outlined">description</span>
                </div>
              ) : (
                <img
                  src={`/assets/cv-images/template${i}.jpg`}
                  alt={`Template ${i}`}
                  onError={() => handleImgError(i)}
                />
              )}
              <div className="template-card__label">Template {i}</div>
              {isSelected && (
                <div className="template-card__check">
                  <span className="material-symbols-outlined" style={{ fontSize: '14px', fontVariationSettings: "'FILL' 1" }}>check</span>
                </div>
              )}
            </div>
          );
        })}
      </div>
      <p className="template-selected-info">
        Selected: <span>Template {selectedNum}</span>
      </p>
    </div>
  );
};

const SOCIAL_FIELDS = [
  { id: 'linkedin-url', field: 'linkedin_url', label: 'LinkedIn URL', type: 'url', placeholder: 'https://linkedin.com/in/…', full: true },
  { id: 'github-label', field: 'github_label', label: 'GitHub name shown on the CV', type: 'text', placeholder: 'e.g. johndoe' },
  { id: 'github-url', field: 'github_url', label: 'GitHub URL', type: 'url', placeholder: 'https://github.com/…' },
  { id: 'portfolio-label', field: 'portfolio_label', label: 'Portfolio name shown on the CV', type: 'text', placeholder: 'e.g. mysite.io' },
  { id: 'portfolio-url', field: 'portfolio_url', label: 'Portfolio URL', type: 'url', placeholder: 'https://…' },
];

const SocialLinksForm = ({ socialLinks, onChange }) => {
  const update = (field) => (e) => onChange(prev => ({ ...prev, [field]: e.target.value }));

  return (
    <div className="social-section">
      <h2 className="section-label">Links to put on your CV <span className="section-label__hint">Optional</span></h2>
      <div className="ap-glass social-form">
        {SOCIAL_FIELDS.map(({ id, field, label, type, placeholder, full }) => (
          <div key={id} className={`social-field ${full ? 'social-field--full' : ''}`}>
            <label htmlFor={id} className="label">{label}</label>
            <input
              id={id}
              type={type}
              placeholder={placeholder}
              value={socialLinks[field]}
              onChange={update(field)}
              className="field"
            />
          </div>
        ))}
      </div>
    </div>
  );
};

const PHASE_CONTENT = {
  thinking: {
    headline: 'Writing your documents',
    sub: 'Matching your experience to what the offer asks for.',
  },
  compiling: {
    headline: 'Building the PDFs',
    sub: 'Laying out your CV, cover letter and email.',
  },
  default: {
    headline: 'Preparing your application',
    sub: 'Keep this page open while your documents are written.',
  },
};

const GeneratingLoader = ({ phase }) => {
  const content = PHASE_CONTENT[phase] || PHASE_CONTENT.default;
  const isThinkingDone = phase === 'compiling';
  const isCompiling = phase === 'compiling';

  return (
    <div className="generating-loader">
      <div className="orbital-container">
        <div className="orbital-ring orbital-ring-outer" />
        <div className="orbital-ring orbital-ring-middle" />
        <div className="orbital-dot" />
      </div>

      <h2 className="generating-headline">{content.headline}</h2>
      <p className="generating-sub">{content.sub}</p>

      <div className="generating-steps">
        {/* Step 1: AI Tailoring */}
        <div className={`gen-step ${isThinkingDone ? 'gen-step--done' : phase === 'thinking' ? 'gen-step--active' : 'gen-step--pending'}`}>
          <span className="material-symbols-outlined gen-step__icon" style={{ fontVariationSettings: "'FILL' 1" }}>
            {isThinkingDone ? 'check_circle' : phase === 'thinking' ? 'edit_note' : 'radio_button_unchecked'}
          </span>
          Writing the content
        </div>
        {/* Step 2: Compiling */}
        <div className={`gen-step ${isCompiling ? 'gen-step--active' : 'gen-step--pending'}`}>
          <span className={`material-symbols-outlined gen-step__icon ${isCompiling ? 'spin-icon' : ''}`}>
            {isCompiling ? 'sync' : 'radio_button_unchecked'}
          </span>
          Building the PDFs
        </div>
        {/* Step 3: Upload */}
        <div className="gen-step gen-step--pending">
          <span className="material-symbols-outlined gen-step__icon">radio_button_unchecked</span>
          Saving your documents
        </div>
      </div>
    </div>
  );
};

const ErrorBanner = ({ message, onRetry }) => (
  <div className="ap-glass error-banner">
    <span className="material-symbols-outlined error-banner__icon">error_outline</span>
    <div>
      <p className="error-banner__title">The documents could not be generated</p>
      <p className="error-banner__msg">{message}</p>
      <button className="error-banner__retry" onClick={onRetry}>Try again</button>
    </div>
  </div>
);

const PdfPreview = ({ url, label }) => {
  const [failed, setFailed] = useState(false);
  if (!url || failed) {
    return (
      <div className="iframe-fallback">
        <span className="material-symbols-outlined" style={{ fontSize: '2rem' }}>picture_as_pdf</span>
        <p>{url ? 'No preview for this file' : 'This document was not generated'}</p>
        {url && (
          <a href={url} target="_blank" rel="noreferrer">
            <span className="material-symbols-outlined" style={{ fontSize: '16px', verticalAlign: 'middle' }}>open_in_new</span>
            {' '}View {label}
          </a>
        )}
      </div>
    );
  }
  return (
    <iframe
      src={url}
      title={label}
      onError={() => setFailed(true)}
    />
  );
};

const EmailPreview = ({ dataEmail, emailUrl }) => {
  const handleDownload = () => {
    if (!dataEmail) return;
    const content = typeof dataEmail === 'string'
      ? dataEmail
      : `Subject: ${dataEmail.subject || ''}\n\n${dataEmail.body || JSON.stringify(dataEmail, null, 2)}`;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'cold_email.txt';
    document.body.appendChild(a); a.click();
    document.body.removeChild(a); URL.revokeObjectURL(url);
  };

  const subject = typeof dataEmail === 'object' ? dataEmail?.subject : null;
  const body = typeof dataEmail === 'object' ? dataEmail?.body : (typeof dataEmail === 'string' ? dataEmail : null);

  return (
    <div className="email-preview-outer">
      <div className="email-preview-inner">
        {subject && (
          <div className="email-preview__header">
            <div className="email-preview__subject-label">Subject</div>
            <div className="email-preview__subject">{subject}</div>
          </div>
        )}
        {body ? (
          <div className="email-preview__body">{body}</div>
        ) : dataEmail ? (
          <pre className="email-preview__raw">{JSON.stringify(dataEmail, null, 2)}</pre>
        ) : (
          <div className="iframe-fallback" style={{ height: '200px' }}>
            <span className="material-symbols-outlined" style={{ fontSize: '2rem' }}>alternate_email</span>
            <p>The email was not generated</p>
          </div>
        )}
      </div>
    </div>
  );
};

const StepTwoResults = ({ pack, onDownloadAll }) => {
  const navigate = useNavigate();
  const handleEmailDownload = () => {
    if (!pack.data_email) return;
    const content = typeof pack.data_email === 'string'
      ? pack.data_email
      : `Subject: ${pack.data_email.subject || ''}\n\n${pack.data_email.body || JSON.stringify(pack.data_email, null, 2)}`;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'cold_email.txt';
    document.body.appendChild(a); a.click();
    document.body.removeChild(a); URL.revokeObjectURL(url);
  };

  return (
    <div>
      {/* Success Banner */}
      <div className="ap-glass success-banner">
        <div className="success-banner__left">
          <span className="material-symbols-outlined success-banner__icon" style={{ fontSize: '2rem', fontVariationSettings: "'FILL' 1" }}>
            check_circle
          </span>
          <div>
            <p className="success-banner__title">Your application is ready</p>
            <p className="success-banner__sub">Read each document before you send it. Download them one by one, or all together.</p>
          </div>
        </div>
        <button className="download-all-btn" onClick={onDownloadAll} id="download-all-btn">
          <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>download</span>
          Download all
        </button>
      </div>

      {/* 3-Column Grid */}
      <div className="results-grid">
        {/* CV */}
        <div className="result-col">
          <div className="result-col__header">
            <h3 className="result-col__title">
              <span className="material-symbols-outlined col-icon-cv" style={{ fontVariationSettings: "'FILL' 1" }}>badge</span>
              Curriculum Vitae
            </h3>
            <button
              className="result-col__download-btn"
              onClick={() => pack.cv_url && window.open(pack.cv_url, '_blank')}
              title="Download CV"
              id="download-cv-btn"
            >
              <span className="material-symbols-outlined" style={{ fontSize: '20px' }}>file_download</span>
            </button>
          </div>
          <div className="ap-glass result-preview-panel">
            <PdfPreview url={pack.cv_url} label="CV" />
          </div>
        </div>

        {/* Cover Letter */}
        <div className="result-col">
          <div className="result-col__header">
            <h3 className="result-col__title">
              <span className="material-symbols-outlined col-icon-letter" style={{ fontVariationSettings: "'FILL' 1" }}>article</span>
              Cover Letter
            </h3>
            <button
              className="result-col__download-btn"
              onClick={() => pack.cover_letter_url && window.open(pack.cover_letter_url, '_blank')}
              title="Download cover letter"
              id="download-letter-btn"
            >
              <span className="material-symbols-outlined" style={{ fontSize: '20px' }}>file_download</span>
            </button>
          </div>
          <div className="ap-glass result-preview-panel">
            <PdfPreview url={pack.cover_letter_url} label="Cover letter" />
          </div>
        </div>

        {/* Cold Email */}
        <div className="result-col">
          <div className="result-col__header">
            <h3 className="result-col__title">
              <span className="material-symbols-outlined col-icon-email" style={{ fontVariationSettings: "'FILL' 1" }}>alternate_email</span>
              Cold Email
            </h3>
            <button
              className="result-col__download-btn"
              onClick={handleEmailDownload}
              title="Download email"
              id="download-email-btn"
            >
              <span className="material-symbols-outlined" style={{ fontSize: '20px' }}>file_download</span>
            </button>
          </div>
          <div className="ap-glass result-preview-panel">
            <EmailPreview dataEmail={pack.data_email} emailUrl={pack.email_url} />
          </div>
        </div>
      </div>

      <div className="back-btn-wrap">
        <button className="back-btn" onClick={() => navigate('/dashboard')} id="back-to-jobs-btn">
          Back to your matches
        </button>
      </div>
    </div>
  );
};

/* ─────────────────────────────────────────────
   MAIN COMPONENT
───────────────────────────────────────────── */
const Apply = () => {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const { user, session, loading: authLoading } = useAuth();

  const [step, setStep] = useState(1);
  const [cvExists, setCvExists] = useState(null); // null=checking, true, false
  const [jobDetails, setJobDetails] = useState(null);
  const [selectedTemplate, setSelectedTemplate] = useState('template1.tex');
  const [socialLinks, setSocialLinks] = useState({
    linkedin_url: '',
    github_label: '',
    github_url: '',
    portfolio_label: '',
    portfolio_url: '',
  });
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationPhase, setGenerationPhase] = useState('');
  const [generatedPack, setGeneratedPack] = useState(null);
  const [error, setError] = useState(null);

  /* ── On-mount: auth guard + CV check + job fetch + social prefill ── */
  useEffect(() => {
    if (authLoading) return;
    if (!user) { navigate('/signin'); return; }

    const userId = user.id;

    const fetchAll = async () => {
      try {
        const [cvResult, jobResult, socialsResult] = await Promise.all([
          // CV check
          supabase
            .from('candidates')
            .select('id, cv_storage_path')
            .eq('user_id', userId)
            .limit(1)
            .maybeSingle(),
          // Job details
          supabaseDB.getJobById(jobId),
          // Social links prefill
          supabaseDB.getLastApplicationSocials(userId),
        ]);

        // CV gate
        const candidate = cvResult.data;
        if (!candidate || !candidate.cv_storage_path) {
          setCvExists(false);
        } else {
          setCvExists(true);
        }

        // Job details
        if (jobResult) {
          setJobDetails({
            title: jobResult.title,
            company_name: jobResult.company,
            logo_url: jobResult.logo_url,
          });
        }

        // Prefill socials
        if (socialsResult) {
          setSocialLinks(prev => ({
            ...prev,
            linkedin_url: socialsResult.linkedin_url || '',
            github_url: socialsResult.github_url || '',
            portfolio_url: socialsResult.portfolio_url || '',
          }));
        }
      } catch (err) {
        console.error('Apply mount fetch error:', err);
        setCvExists(false);
      }
    };

    fetchAll();
  }, [authLoading, user, jobId, navigate]);

  /* ── Generation handler ── */
  const handleGenerate = useCallback(async () => {
    if (!selectedTemplate || !user) return;
    setIsGenerating(true);
    setError(null);

    try {
      // Phase 1: THINKING — generate CV content
      setGenerationPhase('thinking');
      const cvContent = await edgeFunctions.invokeGenerateCv({
        user_id: user.id,
        job_id: parseInt(jobId, 10),
        linkedin_url: socialLinks.linkedin_url,
        github_label: socialLinks.github_label,
        github_url: socialLinks.github_url,
        portfolio_label: socialLinks.portfolio_label,
        portfolio_url: socialLinks.portfolio_url,
      });

      const { data_cv, data_letter, data_email } = cvContent;

      // Phase 2: COMPILING — generate PDFs
      setGenerationPhase('compiling');
      const pdfResult = await edgeFunctions.invokeGeneratePdf({
        user_id: user.id,
        job_id: parseInt(jobId, 10),
        template_id: selectedTemplate,
        data_cv,
        data_letter,
        data_email,
      });

      const { files } = pdfResult;

      // Save the application record
      try {
        const candidateData = await supabaseDB.getCandidateProfile(user.id);
        if (candidateData) {
          await supabaseDB.saveJobApplication({
            user_id: user.id,
            job_id: jobId,
            candidate_id: candidateData.id,
            template_id: selectedTemplate,
            linkedin_url: socialLinks.linkedin_url,
            github_url: socialLinks.github_url,
            portfolio_url: socialLinks.portfolio_url,
            cv_url: files?.cv,
            cover_letter_url: files?.cover_letter,
            email_url: files?.email,
            data_cv,
            data_letter,
            data_email,
            status: 'ready',
          });
        }
      } catch (saveErr) {
        console.warn('Failed to save application record (non-fatal):', saveErr);
      }

      setGeneratedPack({
        cv_url: files?.cv,
        cover_letter_url: files?.cover_letter,
        email_url: files?.email,
        data_email,
      });

      setStep(2);
    } catch (err) {
      console.error('Generation flow error:', err);
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setIsGenerating(false);
      setGenerationPhase('');
    }
  }, [selectedTemplate, user, jobId, socialLinks]);

  const handleDownloadAll = useCallback(() => {
    if (!generatedPack) return;
    if (generatedPack.cv_url) window.open(generatedPack.cv_url, '_blank');
    if (generatedPack.cover_letter_url) window.open(generatedPack.cover_letter_url, '_blank');
    if (generatedPack.email_url) window.open(generatedPack.email_url, '_blank');
  }, [generatedPack]);

  /* ── Render ── */
  if (authLoading || cvExists === null) {
    return (
      <div className="apply-page-wrapper">
        <Sidebar />
        <main className="apply-main-content">
          <div className="page-loading">
            <span className="material-symbols-outlined" style={{ animation: 'spin-cw 1.5s linear infinite', fontSize: '24px' }}>sync</span>
            Loading…
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="apply-page-wrapper">
      <Sidebar />
      <main className="apply-main-content">

        {/* ── CV Gate ── */}
        {cvExists === false && <NoCvBanner />}

        {/* ── Normal flow ── */}
        {cvExists === true && (
          <>
            <JobHeader jobDetails={jobDetails} />
            <StepIndicator currentStep={step} />

            {/* Error state */}
            {error && !isGenerating && (
              <ErrorBanner message={error} onRetry={() => setError(null)} />
            )}

            {/* Loading state */}
            {isGenerating && <GeneratingLoader phase={generationPhase} />}

            {/* Step 1 */}
            {!isGenerating && step === 1 && (
              <>
                <TemplateSelector
                  selectedTemplate={selectedTemplate}
                  onSelectTemplate={setSelectedTemplate}
                />
                <SocialLinksForm
                  socialLinks={socialLinks}
                  onChange={setSocialLinks}
                />
                <div className="generate-btn-wrap">
                  <button
                    id="generate-pack-btn"
                    className="generate-btn"
                    onClick={handleGenerate}
                    disabled={isGenerating}
                  >
                    Generate the application
                  </button>
                </div>
              </>
            )}

            {/* Step 2 */}
            {!isGenerating && step === 2 && generatedPack && (
              <StepTwoResults
                pack={generatedPack}
                onDownloadAll={handleDownloadAll}
              />
            )}
          </>
        )}

      </main>
    </div>
  );
};

export default Apply;
