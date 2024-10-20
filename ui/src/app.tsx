import 'src/global.css';

import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

import { Router } from 'src/routes/sections';

import { useScrollToTop } from 'src/hooks/use-scroll-to-top';

import { AuthProvider } from 'src/client/auth-provider';
import { ThemeProvider } from 'src/theme/theme-provider';
import { ServerConstantsProvider } from 'src/client/server-constants-provider';


// ----------------------------------------------------------------------

export default function App() {
  useScrollToTop();

  return (
    <ThemeProvider>
      <LocalizationProvider dateAdapter={AdapterDayjs}>
	<AuthProvider>
	  <ServerConstantsProvider>
	    <Router />
	  </ServerConstantsProvider>
	</AuthProvider>
      </LocalizationProvider>
    </ThemeProvider>
  );
}
