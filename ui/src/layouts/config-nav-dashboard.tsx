import { Iconify } from 'src/components/iconify';
import { SvgColor } from 'src/components/svg-color';

// ----------------------------------------------------------------------

const icon = (name: string) => (
  <SvgColor width="100%" height="100%" src={`/assets/icons/navbar/${name}.svg`} />
);

export const navData = [
  {
    title: 'Dashboard',
    path: '/',
    icon: icon('dashboard'),
  },
  {
    title: 'Explore',
    path: '/explore',
    icon: icon('ic-analytics'),
  },
  {
    title: 'My Locations',
    path: '/locations',
    icon: icon('my-location'),
  },
  {
    title: 'Settings',
    path: '/settings',
    icon: (
      <Iconify width={22} icon="solar:settings-bold-duotone" />
    ),
  },
];
