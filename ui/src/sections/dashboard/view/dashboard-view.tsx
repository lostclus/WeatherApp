import type { User } from 'src/client/users';
import type { Weather } from 'src/client/weather';
import type { Location_ } from 'src/client/locations';

import { useState, useEffect } from 'react';

import Grid from '@mui/material/Unstable_Grid2';
import Typography from '@mui/material/Typography';

import { useAuth } from 'src/client/auth-provider';
import { getLocations } from 'src/client/locations';
import { getUser, nullUser } from 'src/client/users';
import { getCurrentWeather } from 'src/client/weather';
import { DashboardContent } from 'src/layouts/dashboard';

import { WeatherWidgetSummary } from '../weather-widget-summary';

// ----------------------------------------------------------------------

export function DashboardView() {
  const { user } = useAuth();
  const [settings, setSettings] = useState(nullUser);
  const [locations, setLocations] = useState<Location_[]>([]);
  const [currentWeather, setCurrentWeather] = useState<Weather[]>([]);

  if (!user) throw Error("No authenticated");

  useEffect(() => {
    getLocations(
      (newLocations: Location_[]) => {
	setLocations(newLocations);
      }
    );
  }, []);

  useEffect(() => {
    getUser(
      user.id,
      (newUser: User) => setSettings(newUser)
    );
  }, [user]);

  useEffect(() => {
    if (settings !== nullUser) {
      getCurrentWeather(
	{
	  locationIds: locations.map((loc) => loc.id),
	  fields: ["temperature_2m", "weather_code"],
	  timezone: settings.timezone,
	  temperatureUnit: settings.temperatureUnit,
	  windSpeedUnit: settings.windSpeedUnit,
	  precipitationUnit: settings.precipitationUnit,
	},
	(newWeather: Weather[]) => setCurrentWeather(newWeather)
      );
    }
  }, [locations, settings]);

  const locationsMap = Object.fromEntries(locations.map((loc) => [loc.id, loc]));

  return (
    <DashboardContent maxWidth="xl">
      <Typography variant="h4" sx={{ mb: { xs: 3, md: 5 } }}>
        Hi, Welcome back 👋
      </Typography>

      <Grid container spacing={3}>
	{currentWeather.map((weather: Weather) => (
	  <Grid key={weather.location_id} xs={12} sm={6} md={3}>
	    <WeatherWidgetSummary
	      loc={locationsMap[weather.location_id]}
	      weather={weather}
	      settings={settings}
	    />
	  </Grid>
	))}
      </Grid>

    </DashboardContent>
  );
}
