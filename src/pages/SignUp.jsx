import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import AuthLayout from '../components/AuthLayout';

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // The user_profile triggered by Supabase Auth doesn't take fullName directly via standard auth email,
    // but the trigger handles user_account creation. Update happen later in /verify.
    const { error } = await signUp(fullName, email, password);

    if (error) {
      setError(error.message);
      setLoading(false);
    } else {
      const destination = location.state?.from?.pathname || '/upload';
      navigate(destination, { replace: true });
    }
  };

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
          {loading ? 'Creating account…' : 'Create account'}
        </button>
      </form>
    </AuthLayout>
  );
};

export default SignUp;
