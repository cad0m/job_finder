import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import AuthLayout from '../components/AuthLayout';
import { authMessage } from '../lib/authErrors';

const SignUp = () => {
  const { signUp } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [sentTo, setSentTo] = useState(''); // set when Supabase asks the user to confirm their email

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (password.length < 8) {
      setError('Use at least 8 characters for your password.');
      setLoading(false);
      return;
    }

    // The sign-up trigger creates user_account and user_profile (with this full name).
    const { data, error } = await signUp(fullName, email, password);

    if (error) {
      setError(authMessage(error));
      setLoading(false);
      return;
    }
    // Supabase returns an existing, unconfirmed user with no identities: the email is taken
    if (data?.user && Array.isArray(data.user.identities) && data.user.identities.length === 0) {
      setError(authMessage({ message: 'User already registered' }));
      setLoading(false);
      return;
    }
    if (!data?.session) {
      // Email confirmation is on: no session until the user clicks the link
      setSentTo(email.trim());
      setLoading(false);
      return;
    }
    const destination = location.state?.from?.pathname || '/upload';
    navigate(destination, { replace: true });
  };

  if (sentTo) {
    return (
      <AuthLayout
        title="Check your inbox"
        intro={`We sent a confirmation link to ${sentTo}. Open it to activate your account, then add your CV.`}
        footer={<>Wrong email? <button type="button" className="link" onClick={() => setSentTo('')}>Go back</button></>}
      >
        <Link to="/signin" state={{ email: sentTo }} className="btn btn-primary w-full">I confirmed it, sign me in</Link>
      </AuthLayout>
    );
  }

  return (
    <AuthLayout
      title="Create your account"
      intro="Next you upload your CV, and your first ranked offers follow."
      footer={
        <>
          Already have an account?{' '}
          <Link to="/signin" state={{ from: location.state?.from }} className="link">Sign in</Link>
        </>
      }
    >
      <form className="space-y-5" onSubmit={handleSubmit}>
        {error && (
          <div className="notice notice-bad" role="alert">
            <span className="material-symbols-outlined" aria-hidden="true">error</span>
            <span>{error}</span>
          </div>
        )}

        <div>
          <label htmlFor="signup-name" className="label">Full name</label>
          <input
            id="signup-name"
            type="text"
            autoComplete="name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
            className="field"
          />
        </div>

        <div>
          <label htmlFor="signup-email" className="label">Email</label>
          <input
            id="signup-email"
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
          <label htmlFor="signup-password" className="label">Password</label>
          <div className="relative">
            <input
              id="signup-password"
              type={showPassword ? 'text' : 'password'}
              autoComplete="new-password"
              minLength={8}
              aria-describedby="signup-password-hint"
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

        <p id="signup-password-hint" className="-mt-3 text-[0.875rem] text-graphite">At least 8 characters.</p>

        <button type="submit" disabled={loading} className="btn btn-primary w-full">
          {loading ? 'Creating account…' : 'Create account'}
        </button>
      </form>
    </AuthLayout>
  );
};

export default SignUp;
