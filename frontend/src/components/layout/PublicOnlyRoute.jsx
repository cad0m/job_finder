import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

/** Sign-in and sign-up pages: a signed-in user goes straight to the app. */
const PublicOnlyRoute = ({ children }) => {
  const { user } = useAuth();
  const location = useLocation();
  if (user) return <Navigate to={location.state?.from?.pathname || '/dashboard'} replace />;
  return children;
};

export default PublicOnlyRoute;
