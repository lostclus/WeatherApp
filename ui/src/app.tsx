import 'src/global.css';

import { Router } from 'src/routes/sections';

import { useScrollToTop } from 'src/hooks/use-scroll-to-top';

import { AuthProvider } from 'src/client/auth-provider';
import { ThemeProvider } from 'src/theme/theme-provider';


// ----------------------------------------------------------------------

export default function App() {
  useScrollToTop();

  return (
    <ThemeProvider>
	<AuthProvider>
	  <Router />
	</AuthProvider>
    </ThemeProvider>
  );
}
