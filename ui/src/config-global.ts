import packageJson from '../package.json';

// ----------------------------------------------------------------------

export type ConfigValue = {
  appName: string;
  appVersion: string;
  api: {
      coreURL: string;
  };
};

// ----------------------------------------------------------------------

export const CONFIG: ConfigValue = {
  appName: 'WeatherApp',
  appVersion: packageJson.version,
  api: {
      coreURL: import.meta.env.VITE_CORE_API_BASE_URL || 'http://localhost:8000/core/api',
  },
};
