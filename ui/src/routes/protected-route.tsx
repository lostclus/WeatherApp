import { Outlet, Navigate } from "react-router-dom";

import { useAuth } from "src/client/auth-provider";

export const ProtectedRoute = () => {
  const { user } = useAuth();

  // Check if the user is authenticated
  if (!user) {
    // If not authenticated, redirect to the login page
    return <Navigate to="/sign-in" />;
  }

  // If authenticated, render the child routes
  return <Outlet />;
};
