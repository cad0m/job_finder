import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { authMessage } from '../../lib/authErrors';
import AuthShell from './AuthShell';
import { GoButton, LockIc } from './authBits';

/** Opened from the reset email: Supabase signs the user in from the link. */
export default function ResetPasswordPage() {
  const { user, updatePassword } = useAuth();
  const navigate = useNavigate();
  const [a, setA] = useState('');
  const [b, setB] = useState('');
  const [state, setState] = useState('idle');
  const [error, setError] = useState('');

  if (!user) {
    return (
      <AuthShell title={['This', 'link', 'has', 'expired.']} sub="Reset links work once and only for a short time. Ask for a new one."
        foot={<Link to="/signin">Back to sign in</Link>}>
        <form id="authform" onSubmit={(e) => { e.preventDefault(); navigate('/forgot-password'); }}>
          <GoButton state="idle" label="Send me a new link" wait="" ok="" d={1} />
        </form>
      </AuthShell>
    );
  }

  const onSubmit = async (e) => {
    e.preventDefault();
    if (state !== 'idle') return;
    setError('');
    if (a.length < 8) { setError('Use at least 8 characters for your password.'); return; }
    if (a !== b) { setError('The two passwords are not the same.'); return; }
    setState('wait');
    const { error: err } = await updatePassword(a);
    if (err) { setState('idle'); setError(authMessage(err)); return; }
    setState('ok');
    setTimeout(() => navigate('/dashboard', { replace: true }), 900);
  };

  return (
    <AuthShell title={['Choose', 'a', 'new', 'password.']} sub={`For ${user.email}.`} done={state === 'ok'}>
      <form id="authform" onSubmit={onSubmit}>
        <div className="fld rise" style={{ '--d': '1' }}>
          <label className="lbl" htmlFor="password">New password</label>
          <span className="ctl"><LockIc /><input id="password" name="password" type="password" autoComplete="new-password" placeholder="8 or more characters" minLength={8} required value={a} onChange={(e) => setA(e.target.value)} /></span>
        </div>
        <div className="fld rise" style={{ '--d': '2' }}>
          <label className="lbl" htmlFor="password2">Type it again</label>
          <span className="ctl"><LockIc /><input id="password2" name="password2" type="password" autoComplete="new-password" placeholder="Same password" minLength={8} required value={b} onChange={(e) => setB(e.target.value)} /></span>
        </div>
        <GoButton state={state} label="Save the new password" wait="Saving…" ok="Password saved" d={3} />
        {error && <p className="note jm-msg bad" role="alert">{error}</p>}
      </form>
    </AuthShell>
  );
}
