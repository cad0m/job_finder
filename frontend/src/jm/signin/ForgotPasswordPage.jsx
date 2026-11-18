import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { authMessage } from '../../lib/authErrors';
import AuthShell from './AuthShell';
import { GoButton, MailIc } from './authBits';

export default function ForgotPasswordPage() {
  const { sendPasswordReset } = useAuth();
  const location = useLocation();
  const [email, setEmail] = useState(location.state?.email || '');
  const [state, setState] = useState('idle');
  const [error, setError] = useState('');

  const onSubmit = async (e) => {
    e.preventDefault();
    if (state === 'wait') return;
    setError(''); setState('wait');
    const { error: err } = await sendPasswordReset(email);
    if (err) { setState('idle'); setError(authMessage(err)); return; }
    setState('ok');
  };

  return (
    <AuthShell title={['Reset', 'your', 'password.']} sub="Type your email and we send you a link to choose a new password." done={state === 'ok'}
      foot={<>Remembered it? <Link to="/signin" state={{ email }}>Sign in</Link></>}>
      <form id="authform" onSubmit={onSubmit}>
        <div className="fld rise" style={{ '--d': '1' }}>
          <label className="lbl" htmlFor="email">Email</label>
          <span className="ctl"><MailIc /><input id="email" name="email" type="email" autoComplete="email" placeholder="you@example.com" required value={email} onChange={(e) => { setEmail(e.target.value); if (state === 'ok') setState('idle'); }} /></span>
        </div>
        <GoButton state={state} label="Send the link" wait="Sending…" ok="Link sent" d={2} />
        {state === 'ok' && <p className="note jm-msg" role="status">If an account exists for {email.trim()}, a link to choose a new password is on its way. It works once.</p>}
        {error && <p className="note jm-msg bad" role="alert">{error}</p>}
      </form>
    </AuthShell>
  );
}
