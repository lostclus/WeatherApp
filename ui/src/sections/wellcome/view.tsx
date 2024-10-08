import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';

import { DashboardContent } from 'src/layouts/dashboard';

// ----------------------------------------------------------------------

export function WellcomeView() {
  return (
    <DashboardContent maxWidth="xl">
      <Typography variant="h4" sx={{ mb: { xs: 3, md: 5 } }}>
        <div>
        Hi, Welcome to WeatherApp 👋
	</div>
        <div>
	Please <Link href="/sign-in">sign-in</Link>
	</div>
      </Typography>
    </DashboardContent>
  );
}
