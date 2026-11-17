import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import OnboardingLayout from '../components/OnboardingLayout';
import EmptyState from '../components/EmptyState';
import { useAuth } from '../hooks/useAuth';
import { supabaseDB } from '../services/supabaseDB';
import { edgeFunctions } from '../services/edgeFunctions';

const Section = ({ title, children }) => (
  <section className="sheet p-6 sm:p-8">
    <h2 className="mb-6 text-xl font-semibold">{title}</h2>
    {children}
  </section>
);

/* A short value edited in place, with a remove button: skills, languages. */
const EditableChip = ({ value, onChange, onRemove, label }) => (
  <li className="flex items-center rounded-md border border-rule-strong bg-paper pl-2.5 focus-within:border-pen">
    <input
      value={value}
      onChange={(e) => onChange(e.target.value)}
      size={Math.max(String(value).length, 4)}
      aria-label={label}
      className="min-w-0 bg-transparent py-1.5 text-[0.9375rem] focus:outline-none"
    />
    <button type="button" onClick={onRemove} aria-label={`Remove ${value || label}`} className="grid h-9 w-8 place-items-center text-pencil hover:text-bad">
      <span className="material-symbols-outlined text-[1.125rem]" aria-hidden="true">close</span>
    </button>
  </li>
);

const AddButton = ({ onClick, children }) => (
  <button type="button" onClick={onClick} className="btn btn-secondary btn-sm">
    <span className="material-symbols-outlined" aria-hidden="true">add</span>
    {children}
  </button>
);

const ProfileReview = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();

  // Use data from upload flow if available, else fallback to JSON
  const initialData = location.state?.candidate;
  const [candidate, setCandidate] = useState(initialData);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState('');

  if (!candidate) {
    return (
      <OnboardingLayout step={2} title="Check what was read">
        <EmptyState
          icon="upload_file"
          title="There is no CV to review yet"
          action={<Link to="/upload" className="btn btn-primary">Upload your CV</Link>}
        >
          Upload your CV first. What JobMatcher reads from it will appear here for you to check.
        </EmptyState>
      </OnboardingLayout>
    );
  }

  const handleSave = async () => {
    if (!user) {
      setError('Sign in to save your profile.');
      return;
    }

    setIsSaving(true);
    setError('');

    try {
      await supabaseDB.saveProfile(candidate, user.id);
      // Trigger embedding generation in the background
      try {
        await edgeFunctions.invokeEmbedCv();
      } catch (embedErr) {
        console.warn('Embedding generation failed, but profile was saved:', embedErr);
      }
      navigate('/dashboard');
    } catch (err) {
      console.error('Failed to save profile', err);
      setError(`Your profile was not saved: ${err.message || 'the database did not respond'}. Check your connection and save again.`);
      setIsSaving(false);
    }
  };

  const updateField = (field, value) => {
    setCandidate((prev) => ({ ...prev, [field]: value }));
  };

  const list = (name) => candidate[name] || [];

  const updateItemInList = (listName, index, field, value) => {
    const newList = [...list(listName)];
    if (field === null) {
      newList[index] = value;
    } else {
      newList[index] = { ...newList[index], [field]: value };
    }
    updateField(listName, newList);
  };

  const addItemToList = (listName, defaultValue) => {
    updateField(listName, [...list(listName), defaultValue]);
  };

  const removeItemFromList = (listName, index) => {
    updateField(listName, list(listName).filter((_, i) => i !== index));
  };

  return (
    <OnboardingLayout
      step={2}
      title="Check what was read"
      intro="This is what JobMatcher found in your CV. Fix anything that is wrong or missing: your matches are ranked from this."
    >
      <div className="space-y-6">
        <Section title="About you">
          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <label htmlFor="pr-name" className="label">Full name</label>
              <input id="pr-name" type="text" autoComplete="name" value={candidate.full_name ?? ''} onChange={(e) => updateField('full_name', e.target.value)} className="field" />
            </div>
            <div>
              <label htmlFor="pr-email" className="label">Email</label>
              <input id="pr-email" type="email" autoComplete="email" value={candidate.email ?? ''} onChange={(e) => updateField('email', e.target.value)} className="field" />
            </div>
            <div>
              <label htmlFor="pr-location" className="label">City</label>
              <input id="pr-location" type="text" value={candidate.location ?? ''} onChange={(e) => updateField('location', e.target.value)} className="field" />
            </div>
            <div>
              <label htmlFor="pr-phone" className="label">Phone</label>
              <input id="pr-phone" type="tel" autoComplete="tel" value={candidate.phone ?? ''} onChange={(e) => updateField('phone', e.target.value)} className="field" />
            </div>
            <div>
              <label htmlFor="pr-level" className="label">Level</label>
              <select id="pr-level" value={candidate.seniority_level ?? ''} onChange={(e) => updateField('seniority_level', e.target.value)} className="field">
                <option value="junior">Junior</option>
                <option value="mid">Mid-level</option>
                <option value="senior">Senior</option>
                <option value="lead">Lead</option>
              </select>
            </div>
            <div>
              <label htmlFor="pr-years" className="label">Years of experience</label>
              <input id="pr-years" type="number" min="0" value={candidate.years_experience ?? 0} onChange={(e) => updateField('years_experience', parseInt(e.target.value) || 0)} className="field" />
            </div>
          </div>

          <div className="mt-5">
            <label htmlFor="pr-summary" className="label">Summary</label>
            <textarea id="pr-summary" rows={4} value={candidate.professional_summary ?? ''} onChange={(e) => updateField('professional_summary', e.target.value)} className="field resize-y leading-relaxed" />
          </div>
        </Section>

        <Section title="Experience">
          <ul className="space-y-4">
            {list('experience').map((exp, index) => (
              <li key={index} className="rounded-lg border border-rule p-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label htmlFor={`exp-title-${index}`} className="label">Job title</label>
                    <input id={`exp-title-${index}`} type="text" value={exp.job_title ?? ''} onChange={(e) => updateItemInList('experience', index, 'job_title', e.target.value)} className="field" />
                  </div>
                  <div>
                    <label htmlFor={`exp-company-${index}`} className="label">Company</label>
                    <input id={`exp-company-${index}`} type="text" value={exp.company ?? ''} onChange={(e) => updateItemInList('experience', index, 'company', e.target.value)} className="field" />
                  </div>
                  <div>
                    <label htmlFor={`exp-start-${index}`} className="label">From</label>
                    <input id={`exp-start-${index}`} type="text" placeholder="e.g. 2023-02" value={exp.start_date ?? ''} onChange={(e) => updateItemInList('experience', index, 'start_date', e.target.value)} className="field" />
                  </div>
                  <div>
                    <label htmlFor={`exp-end-${index}`} className="label">To</label>
                    <input id={`exp-end-${index}`} type="text" placeholder="e.g. Present" value={exp.end_date ?? ''} onChange={(e) => updateItemInList('experience', index, 'end_date', e.target.value)} className="field" />
                  </div>
                </div>
                <button type="button" onClick={() => removeItemFromList('experience', index)} className="btn btn-danger btn-sm mt-4">
                  <span className="material-symbols-outlined" aria-hidden="true">delete</span>
                  Remove this job
                </button>
              </li>
            ))}
          </ul>
          <div className="mt-4">
            <AddButton onClick={() => addItemToList('experience', { company: '', job_title: '', start_date: '', end_date: '', responsibilities: [] })}>
              Add a job
            </AddButton>
          </div>
        </Section>

        <Section title="Skills">
          <ul className="flex flex-wrap gap-2">
            {list('skills').map((skill, index) => (
              <EditableChip key={index} value={skill} label="Skill" onChange={(v) => updateItemInList('skills', index, null, v)} onRemove={() => removeItemFromList('skills', index)} />
            ))}
            <li><AddButton onClick={() => addItemToList('skills', '')}>Add a skill</AddButton></li>
          </ul>
        </Section>

        <Section title="Education">
          <ul className="space-y-4">
            {list('education').map((edu, index) => (
              <li key={index} className="rounded-lg border border-rule p-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <label htmlFor={`edu-school-${index}`} className="label">School</label>
                    <input id={`edu-school-${index}`} value={edu.institution ?? ''} onChange={(e) => updateItemInList('education', index, 'institution', e.target.value)} className="field" />
                  </div>
                  <div>
                    <label htmlFor={`edu-degree-${index}`} className="label">Degree</label>
                    <input id={`edu-degree-${index}`} value={edu.degree ?? ''} onChange={(e) => updateItemInList('education', index, 'degree', e.target.value)} className="field" />
                  </div>
                </div>
                <button type="button" onClick={() => removeItemFromList('education', index)} className="btn btn-danger btn-sm mt-4">
                  <span className="material-symbols-outlined" aria-hidden="true">delete</span>
                  Remove this degree
                </button>
              </li>
            ))}
          </ul>
          <div className="mt-4">
            <AddButton onClick={() => addItemToList('education', { institution: '', degree: '' })}>Add a degree</AddButton>
          </div>
        </Section>

        <Section title="Languages">
          <ul className="flex flex-wrap gap-2">
            {list('languages').map((lang, index) => (
              <EditableChip key={index} value={lang} label="Language" onChange={(v) => updateItemInList('languages', index, null, v)} onRemove={() => removeItemFromList('languages', index)} />
            ))}
            <li><AddButton onClick={() => addItemToList('languages', '')}>Add a language</AddButton></li>
          </ul>
        </Section>

        {error && (
          <div className="notice notice-bad" role="alert">
            <span className="material-symbols-outlined" aria-hidden="true">error</span>
            <span>{error}</span>
          </div>
        )}

        <div className="flex flex-wrap items-center gap-x-6 gap-y-4 pt-2">
          <button onClick={handleSave} disabled={isSaving} className="btn btn-primary btn-lg">
            {isSaving ? 'Saving…' : 'Save and see my matches'}
          </button>
          <Link to="/upload" className="link">Upload a different CV</Link>
        </div>
        <p className="text-sm text-graphite">Saving stores this profile in your account and uses it to rank offers for you.</p>
      </div>
    </OnboardingLayout>
  );
};

export default ProfileReview;
