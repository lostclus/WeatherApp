import 'src/global.css';

import { Router } from 'src/routes/sections';

import { useScrollToTop } from 'src/hooks/use-scroll-to-top';

import { ThemeProvider } from 'src/theme/theme-provider';

import { AuthProvider } from 'src/auth/auth-provider'
import { AccountProvider } from 'src/auth/account-provider'

// ----------------------------------------------------------------------

export default function App() {
  useScrollToTop();

  return (
    <ThemeProvider>
	<AuthProvider>
	  <AccountProvider>
	    <Router />
	  </AccountProvider>
	</AuthProvider>
    </ThemeProvider>
  );
}
