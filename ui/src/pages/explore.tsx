import { Helmet } from 'react-helmet-async';

import { CONFIG } from 'src/config-global';

import { ExploreView } from 'src/sections/explore/view';

// ----------------------------------------------------------------------

export default function Page() {
  return (
    <>
      <Helmet>
        <title> {`Explore - ${CONFIG.appName}`}</title>
      </Helmet>

      <ExploreView />
    </>
  );
}
