import type { User } from 'src/client/users';
import type { Weather } from 'src/client/weather';
import type { Location_ } from 'src/client/locations';
import type { SelectChangeEvent } from '@mui/material/Select';

import dayjs from 'dayjs';
import { useState, useEffect } from 'react';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import Typography from '@mui/material/Typography';

import { getWeather } from 'src/client/weather';
import { useAuth } from 'src/client/auth-provider';
import { getLocations } from 'src/client/locations';
import { getUser, nullUser } from 'src/client/users';
import { DashboardContent } from 'src/layouts/dashboard';
import { useServerConstants } from 'src/client/server-constants-provider';

import { ExploreChart } from '../explore-chart';
import { ExploreChartToolbar } from '../explore-chart-toolbar';

// ----------------------------------------------------------------------

export function ExploreView() {
  const { user } = useAuth();
  const serverConstants = useServerConstants();
  const [settings, setSettings] = useState(nullUser);
  const [locations, setLocations] = useState<Location_[]>([]);
  const [locationId, setLocationId] = useState<string | null>(null);
  const [startDate, setStartDate] = useState(dayjs().subtract(7, 'day'));
  const [endDate, setEndDate] = useState(dayjs());
  const [weatherFields, setWeatherFields] = useState(["temperature_2m"]);
  const [dataset, setDataset] = useState<Weather[]>([]);

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


  if (!locationId && locations && locations.length > 0) {
    let defaultLoc = locations.find((loc: Location_) => loc.isDefault);
    if (!defaultLoc) defaultLoc = locations[0];
    setLocationId(defaultLoc.id);
  }

  useEffect(() => {
    if (locationId) {
      getWeather(
	{
	  locationIds: [locationId],
	  startDate: startDate.format('YYYY-MM-DD'),
	  endDate: endDate.format('YYYY-MM-DD'),
	  fields: weatherFields,
	  timezone: settings.timezone,
	  temperatureUnit: settings.temperatureUnit,
	  windSpeedUnit: settings.windSpeedUnit,
	  precipitationUnit: settings.precipitationUnit,
	},
	(newWeather: Weather[]) => setDataset(newWeather)
      );
    } else {
      setDataset([]);
    }
  }, [locationId, startDate, endDate, weatherFields, settings]);

  const handleWeatherFieldsChange = (event: SelectChangeEvent<string[]>) => {
    const {
      target: { value },
    } = event;
    setWeatherFields(
      typeof value === 'string' ? value.split(',') : value,
    );
  };

  return (
    <DashboardContent>
      <Box display="flex" alignItems="center" mb={5}>
        <Typography variant="h4" flexGrow={1}>
          Explore
        </Typography>
      </Box>

      <Card>
	<CardHeader title="Explore weather data" />
	  <ExploreChartToolbar
	    locations={locations}
	    locationId={locationId || ""}
	    startDate={startDate}
	    endDate={endDate}
	    onLocationChange={(event: SelectChangeEvent) => setLocationId(event.target.value)}
	    onStartDateChange={(value: any) => setStartDate(value)}
	    onEndDateChange={(value: any) => setEndDate(value)}
	    weatherFields={weatherFields}
	    weatherFieldsChoices={serverConstants.weatherFields}
	    onWeatherFieldsChange={handleWeatherFieldsChange}
	    settings={settings}
	  />

	  <ExploreChart
	    dataset={dataset}
	    weatherFields={weatherFields}
	    weatherFieldsChoices={serverConstants.weatherFields}
	    settings={settings}
	  />
      </Card>

    </DashboardContent>
  );
}
