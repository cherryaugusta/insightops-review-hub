import { Navigate, useLocation } from "react-router-dom";
import { isAuthenticated } from "../../lib/auth";

type Props = {
  children: React.ReactNode;
};

export function ProtectedRoute({ children }: Props) {
  const location = useLocation();

  if (!isAuthenticated()) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return <>{children}</>;
}
