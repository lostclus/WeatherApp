import packageJson from '../package.json';

// ----------------------------------------------------------------------

export type ConfigValue = {
  appName: string;
  appVersion: string;
  api: {
      mainURL: string;
  };
};

// ----------------------------------------------------------------------

export const CONFIG: ConfigValue = {
  appName: 'WeatherApp',
  appVersion: packageJson.version,
  api: {
      mainURL: import.meta.env.VITE_MAIN_API_BASE_URL || 'http://localhost:8000/main/api',
  },
};
