import { lazy, Suspense } from 'react';
import { Outlet, Navigate, useRoutes } from 'react-router-dom';

import Box from '@mui/material/Box';
import LinearProgress, { linearProgressClasses } from '@mui/material/LinearProgress';

import { varAlpha } from 'src/theme/styles';
import { AuthLayout } from 'src/layouts/auth';
import { SimpleLayout } from 'src/layouts/simple';
import { DashboardLayout } from 'src/layouts/dashboard';

import { useAuth } from "src/auth/auth-provider";
import { ProtectedRoute } from 'src/auth/protected-route';

// ----------------------------------------------------------------------

export const HomePage = lazy(() => import('src/pages/home'));
export const BlogPage = lazy(() => import('src/pages/blog'));
export const UserPage = lazy(() => import('src/pages/user'));
export const SignInPage = lazy(() => import('src/pages/sign-in'));
export const SignUpPage = lazy(() => import('src/pages/sign-up'));
export const SettingsPage = lazy(() => import('src/pages/settings'));
export const ProductsPage = lazy(() => import('src/pages/products'));
export const Page404 = lazy(() => import('src/pages/page-not-found'));

// ----------------------------------------------------------------------

const renderFallback = (
  <Box display="flex" alignItems="center" justifyContent="center" flex="1 1 auto">
    <LinearProgress
      sx={{
        width: 1,
        maxWidth: 320,
        bgcolor: (theme) => varAlpha(theme.vars.palette.text.primaryChannel, 0.16),
        [`& .${linearProgressClasses.bar}`]: { bgcolor: 'text.primary' },
      }}
    />
  </Box>
);

export function Router() {
  const { user } = useAuth();

  const homePageElement = (user) ? (
    <DashboardLayout>
      <Suspense fallback={renderFallback}>
      <Outlet />
      </Suspense>
    </DashboardLayout>
  ) : (
    <SimpleLayout>
      <Suspense fallback={renderFallback}>
      <Outlet />
      </Suspense>
    </SimpleLayout>
  )

  return useRoutes([
    {
      element: homePageElement,
      children: [
        { element: <HomePage />, index: true },
      ],
    },
    {
      element: (
        <DashboardLayout>
          <Suspense fallback={renderFallback}>
	  <ProtectedRoute />
          </Suspense>
        </DashboardLayout>
      ),
      children: [
        { path: 'user', element: <UserPage /> },
        { path: 'products', element: <ProductsPage /> },
        { path: 'blog', element: <BlogPage /> },
        { path: 'settings', element: <SettingsPage /> },
      ],
    },
    {
      path: 'sign-in',
      element: (
        <AuthLayout>
          <SignInPage />
        </AuthLayout>
      ),
    },
    {
      path: 'sign-up',
      element: (
        <AuthLayout>
          <SignUpPage />
        </AuthLayout>
      ),
    },
    {
      path: '404',
      element: <Page404 />,
    },
    {
      path: '*',
      element: <Navigate to="/404" replace />,
    },
  ]);
}
