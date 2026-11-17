import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import AuthLayout from '../components/AuthLayout';
import { authMessage } from '../lib/authErrors';

const SignIn = () => {
  const { signIn, resendConfirmation } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [email, setEmail] = useState(location.state?.email || '');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [needsConfirm, setNeedsConfirm] = useState(false);
  const [notice, setNotice] = useState(location.state?.notice || '');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setNotice('');
    setNeedsConfirm(false);

    const { error } = await signIn(email, password);

    if (error) {
      setError(authMessage(error));
      setNeedsConfirm((error.message || '').toLowerCase().includes('email not confirmed'));
      setLoading(false);
      return;
    }
    const destination = location.state?.from?.pathname || '/dashboard';
    navigate(destination, { replace: true });
  };

  const resend = async () => {
    setError('');
    const { error } = await resendConfirmation(email);
    if (error) setError(authMessage(error));
    else { setNeedsConfirm(false); setNotice(`We sent a new confirmation link to ${email.trim()}.`); }
  };

  return (
    <AuthLayout
      title="Sign in"
      intro="Pick up where you left off: your matches, saved offers and applications."
      footer={
        <>
          New here?{' '}
          <Link to="/signup" state={{ from: location.state?.from }} className="link">Create an account</Link>
        </>
      }
    >
      <form className="space-y-5" onSubmit={handleSubmit} noValidate={false}>
        {notice && (
          <div className="notice notice-info" role="status">
            <span className="material-symbols-outlined" aria-hidden="true">mark_email_read</span>
            <span>{notice}</span>
          </div>
        )}
        {error && (
          <div className="notice notice-bad" role="alert">
            <span className="material-symbols-outlined" aria-hidden="true">error</span>
            <span>
              {error}
              {needsConfirm && (
                <> <button type="button" className="link" onClick={resend}>Send the link again</button></>
              )}
            </span>
          </div>
        )}

        <div>
          <label htmlFor="signin-email" className="label">Email</label>
          <input
            id="signin-email"
            type="email"
            autoComplete="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="field"
          />
        </div>

        <div>
          <div className="flex items-baseline justify-between gap-3">
            <label htmlFor="signin-password" className="label">Password</label>
            <Link to="/forgot-password" state={{ email }} className="link text-[0.875rem]">Forgot password?</Link>
          </div>
          <div className="relative">
            <input
              id="signin-password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="field pr-12"
            />
            <button
              type="button"
              onClick={() => setShowPassword((v) => !v)}
              aria-label={showPassword ? 'Hide password' : 'Show password'}
              aria-pressed={showPassword}
              className="absolute right-1.5 top-1/2 grid h-9 w-9 -translate-y-1/2 place-items-center rounded-md text-graphite hover:bg-desk hover:text-ink"
            >
              <span className="material-symbols-outlined" aria-hidden="true">{showPassword ? 'visibility_off' : 'visibility'}</span>
            </button>
          </div>
        </div>

        <button type="submit" disabled={loading} className="btn btn-primary w-full">
          {loading ? 'Signing in…' : 'Sign in'}
        </button>
      </form>
    </AuthLayout>
  );
};

export default SignIn;
