import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import AuthLayout from '../components/AuthLayout';
import { authMessage } from '../lib/authErrors';

/** Opened from the "reset your password" email. Supabase signs the user in from the link. */
const ResetPassword = () => {
  const { user, updatePassword } = useAuth();
  const navigate = useNavigate();
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!user) {
    return (
      <AuthLayout
        title="This link has expired"
        intro="Reset links work once and only for a short time. Ask for a new one."
        footer={<Link to="/signin" className="link">Back to sign in</Link>}
      >
        <Link to="/forgot-password" className="btn btn-primary w-full">Send me a new link</Link>
      </AuthLayout>
    );
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (password.length < 8) { setError('Use at least 8 characters for your password.'); return; }
    if (password !== confirm) { setError('The two passwords are not the same.'); return; }
    setLoading(true);
    const { error } = await updatePassword(password);
    setLoading(false);
    if (error) { setError(authMessage(error)); return; }
    navigate('/dashboard', { replace: true });
  };

  return (
    <AuthLayout title="Choose a new password" intro={`For ${user.email}.`}>
      <form className="space-y-5" onSubmit={handleSubmit}>
        {error && (
          <div className="notice notice-bad" role="alert">
            <span className="material-symbols-outlined" aria-hidden="true">error</span>
            <span>{error}</span>
          </div>
        )}
        <div>
          <label htmlFor="reset-password" className="label">New password</label>
          <input id="reset-password" type="password" autoComplete="new-password" minLength={8} value={password} onChange={(e) => setPassword(e.target.value)} required className="field" />
        </div>
        <div>
          <label htmlFor="reset-confirm" className="label">Type it again</label>
          <input id="reset-confirm" type="password" autoComplete="new-password" minLength={8} value={confirm} onChange={(e) => setConfirm(e.target.value)} required className="field" />
        </div>
        <button type="submit" disabled={loading} className="btn btn-primary w-full">
          {loading ? 'Saving…' : 'Save the new password'}
        </button>
      </form>
    </AuthLayout>
  );
};

export default ResetPassword;
