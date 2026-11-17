import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import OnboardingLayout from '../components/OnboardingLayout';
import { edgeFunctions } from '../services/edgeFunctions';

const formatSize = (bytes) =>
  bytes >= 1024 * 1024 ? `${(bytes / (1024 * 1024)).toFixed(1)} MB` : `${Math.max(1, Math.round(bytes / 1024))} KB`;

const UploadResume = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFile = (selectedFile) => {
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (selectedFile && allowedTypes.includes(selectedFile.type)) {
      setFile(selectedFile);
      setError('');
    } else {
      setError('That file type isn’t supported. Use a PDF, JPEG, PNG or WEBP.');
      setFile(null);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    handleFile(droppedFile);
  };

  const processResume = () => {
    if (!file) return;
    setLoading(true);
    setError('');

    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = async () => {
      // Remove 'data:application/pdf;base64,' prefix which often causes 422 errors!
      const base64Raw = reader.result.split(',')[1];

      try {
        const data = await edgeFunctions.invokeCvOcr({
          fileBase64: base64Raw,
          filename: file.name,
          mimeType: file.type,
        });

        // Non-blocking fire and forget
        edgeFunctions.invokeEmbedCv().catch((err) => console.warn('Embedding delayed', err));

        setLoading(false);

        // Safety check: ensure we have candidate data
        const extractedCandidate = data?.candidate || { fullName: 'Unknown Candidate', skills: [], experience: [] };

        // Since the user must be authenticated to upload, skip straight to review
        navigate('/review', { state: { candidate: extractedCandidate } });
      } catch (err) {
        console.error('OCR Error Logic:', err);
        setError(err.message || 'Your CV could not be read. Upload it again, or use a different file.');
        setLoading(false);
      }
    };
    reader.onerror = () => {
      setError('The file could not be opened. Choose it again.');
      setLoading(false);
    };
  };

  return (
    <OnboardingLayout
      step={1}
      title="Upload your CV"
      intro="JobMatcher reads it to fill in your profile: experience, skills, education and languages. You check the result on the next step."
    >
      <input
        type="file"
        ref={fileInputRef}
        className="sr-only"
        tabIndex={-1}
        accept=".pdf,.jpg,.jpeg,.png,.webp"
        onChange={(e) => handleFile(e.target.files[0])}
      />

      {error && (
        <div className="notice notice-bad mb-5" role="alert">
          <span className="material-symbols-outlined" aria-hidden="true">error</span>
          <span>{error}</span>
        </div>
      )}

      {!file ? (
        <button
          type="button"
          onClick={() => fileInputRef.current.click()}
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={onDrop}
          className={`flex w-full flex-col items-center gap-2 rounded-[0.875rem] border-2 border-dashed px-6 py-14 text-center transition-colors sm:py-20 ${
            isDragging ? 'border-pen bg-pen-wash' : 'border-rule-strong bg-paper hover:border-pen'
          }`}
        >
          <span className="material-symbols-outlined text-[2rem] text-pen" aria-hidden="true">upload_file</span>
          <span className="mt-2 text-xl font-semibold">Drop your CV here, or choose a file</span>
          <span className="text-graphite">PDF, JPEG, PNG or WEBP, up to 10 MB</span>
        </button>
      ) : (
        <div className="sheet flex flex-col gap-5 p-6 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex min-w-0 items-center gap-4">
            <span className="material-symbols-outlined text-[2rem] text-pen" aria-hidden="true">description</span>
            <div className="min-w-0">
              <p className="truncate font-semibold">{file.name}</p>
              <p className="text-sm text-graphite">{formatSize(file.size)}</p>
            </div>
          </div>
          <div className="flex shrink-0 gap-3">
            <button onClick={() => { setFile(null); setError(''); }} disabled={loading} className="btn btn-secondary">
              Remove
            </button>
            <button onClick={processResume} disabled={loading} className="btn btn-primary">
              {loading ? (
                <>
                  <span className="spinner h-4 w-4 border-white/40 border-t-white" aria-hidden="true" />
                  Reading your CV…
                </>
              ) : (
                'Read my CV'
              )}
            </button>
          </div>
        </div>
      )}

      {loading && <p className="mt-4 text-[0.9375rem] text-graphite" role="status">Reading can take a moment. Keep this page open.</p>}
    </OnboardingLayout>
  );
};

export default UploadResume;
