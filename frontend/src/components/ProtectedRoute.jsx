import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

/**
 * Route guard component.
 * Renders children only if the user is authenticated.
 * Redirects to login page otherwise.
 */
export default function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return children;
}
