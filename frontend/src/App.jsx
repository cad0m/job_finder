import { BrowserRouter as Router, Routes, Route, Navigate, useParams } from 'react-router-dom';
import LandingPage from './jm/landing/LandingPage';
import SignIn from './jm/signin/SignInPage';
import SignUp from './jm/signup/SignUpPage';
import ForgotPassword from './jm/signin/ForgotPasswordPage';
import ResetPassword from './jm/signin/ResetPasswordPage';
import UploadResume from './jm/upload/UploadPage';

import ProfileReview from './jm/review/ReviewPage';
import DashboardPage from './jm/dashboard/DashboardPage';
import Apply from './jm/apply/ApplyPage';
import Profile from './jm/profile/ProfilePage';

import { AuthProvider } from './context/AuthProvider';
import ProtectedRoute from './components/layout/ProtectedRoute';
import PublicOnlyRoute from './components/layout/PublicOnlyRoute';

/** Old links (job details, legacy apply) open the new prepare-application page for that job. */
function RedirectToApply() {
  const { jobId } = useParams();
  return <Navigate to={`/apply/${jobId}`} replace />;
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/signin" element={<PublicOnlyRoute><SignIn /></PublicOnlyRoute>} />
          <Route path="/signup" element={<PublicOnlyRoute><SignUp /></PublicOnlyRoute>} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />

          {/* Protected Routes */}
          <Route path="/upload" element={<ProtectedRoute><UploadResume /></ProtectedRoute>} />

          <Route path="/review" element={<ProtectedRoute><ProfileReview /></ProtectedRoute>} />
          <Route path="/dashboard" element={<ProtectedRoute><DashboardPage view="matches" /></ProtectedRoute>} />
          <Route path="/job-details/:jobId" element={<ProtectedRoute><RedirectToApply /></ProtectedRoute>} />
          <Route path="/apply/:jobId" element={<ProtectedRoute><Apply /></ProtectedRoute>} />
          <Route path="/apply-legacy/:jobId" element={<ProtectedRoute><RedirectToApply /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />

          <Route path="/search" element={<Navigate to="/dashboard" replace />} />
          <Route path="/saved" element={<ProtectedRoute><DashboardPage view="saved" /></ProtectedRoute>} />
          <Route path="/applied" element={<ProtectedRoute><DashboardPage view="applied" /></ProtectedRoute>} />

          {/* Unknown links go to the home page */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
