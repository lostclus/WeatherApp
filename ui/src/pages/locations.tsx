import { Helmet } from 'react-helmet-async';

import { CONFIG } from 'src/config-global';

import { LocationsView } from 'src/sections/location/view';

// ----------------------------------------------------------------------

export default function Page() {
  return (
    <>
      <Helmet>
        <title> {`Location - ${CONFIG.appName}`}</title>
      </Helmet>

      <LocationsView />
    </>
  );
}
