import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';

import { DashboardContent } from 'src/layouts/dashboard';

// ----------------------------------------------------------------------

export function WellcomeView() {
  return (
    <DashboardContent maxWidth="xl">
      <Typography variant="h4" sx={{ mb: { xs: 3, md: 5 } }}>
        Hi, Welcome to WeatherApp 👋
      </Typography>
      <Typography>
	Please <Link href="/sign-in">sign-in</Link>
      </Typography>
    </DashboardContent>
  );
}
