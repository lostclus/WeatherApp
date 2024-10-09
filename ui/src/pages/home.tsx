import { Helmet } from 'react-helmet-async';

import { CONFIG } from 'src/config-global';
import { useAuth } from 'src/client/auth-provider';

import { WellcomeView } from 'src/sections/wellcome';
import { OverviewAnalyticsView } from 'src/sections/overview/view';


// ----------------------------------------------------------------------

export default function Page() {
  const { user } = useAuth();

  return (user) ? (
      <>
	<Helmet>
	  <title> {`Dashboard - ${CONFIG.appName}`}</title>
	</Helmet>

	<OverviewAnalyticsView />
      </>
    ) : (
      <>
	<Helmet>
	  <title> {`Wellcome - ${CONFIG.appName}`}</title>
	</Helmet>

	<WellcomeView />
      </>
    );
}
