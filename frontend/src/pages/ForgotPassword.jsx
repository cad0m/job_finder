import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import AuthLayout from '../components/AuthLayout';
import { authMessage } from '../lib/authErrors';

const ForgotPassword = () => {
  const { sendPasswordReset } = useAuth();
  const location = useLocation();
  const [email, setEmail] = useState(location.state?.email || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [sent, setSent] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    const { error } = await sendPasswordReset(email);
    setLoading(false);
    if (error) setError(authMessage(error));
    else setSent(true);
  };

  if (sent) {
    return (
      <AuthLayout
        title="Check your inbox"
        intro={`If an account exists for ${email.trim()}, we sent it a link to choose a new password. The link works once.`}
        footer={<Link to="/signin" className="link">Back to sign in</Link>}
      >
        <button type="button" className="btn btn-secondary w-full" onClick={() => setSent(false)}>Send it again</button>
      </AuthLayout>
    );
  }

  return (
    <AuthLayout
      title="Reset your password"
      intro="Enter your email and we will send you a link to choose a new password."
      footer={<Link to="/signin" className="link">Back to sign in</Link>}
    >
      <form className="space-y-5" onSubmit={handleSubmit}>
        {error && (
          <div className="notice notice-bad" role="alert">
            <span className="material-symbols-outlined" aria-hidden="true">error</span>
            <span>{error}</span>
          </div>
        )}
        <div>
          <label htmlFor="forgot-email" className="label">Email</label>
          <input
            id="forgot-email"
            type="email"
            autoComplete="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="field"
          />
        </div>
        <button type="submit" disabled={loading} className="btn btn-primary w-full">
          {loading ? 'Sending…' : 'Send the link'}
        </button>
      </form>
    </AuthLayout>
  );
};

export default ForgotPassword;
