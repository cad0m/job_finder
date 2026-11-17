// Supabase auth errors, in words a user understands
export const authMessage = (error) => {
  const m = (error?.message || '').toLowerCase();
  if (m.includes('invalid login credentials')) return 'That email and password do not match. Check them, or reset your password.';
  if (m.includes('email not confirmed')) return 'Confirm your email first: open the link we sent you.';
  if (m.includes('user already registered') || m.includes('already been registered')) return 'An account already exists with this email. Sign in instead.';
  if (m.includes('password should be') || m.includes('weak')) return 'Choose a stronger password: at least 8 characters, with a number or a symbol.';
  if (m.includes('rate limit') || m.includes('too many') || m.includes('security purposes')) return 'Too many tries. Wait a minute, then try again.';
  if (m.includes('network') || m.includes('failed to fetch')) return 'No connection. Check your internet and try again.';
  return error?.message || 'Something went wrong. Try again.';
};
