import type { User } from 'src/client/users';
import type { Weather } from 'src/client/weather';
import type { Location_ } from 'src/client/locations';
import type { ServerChoicesList } from 'src/client/types'
import type { SelectChangeEvent } from '@mui/material/Select';
import type { WeatherAggregated } from 'src/client/weather-aggregated';

import dayjs from 'dayjs';
import { useMemo, useState, useEffect } from 'react';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import Typography from '@mui/material/Typography';

import { cartesianProduct } from 'src/utils/cartesian-product';

import { getWeather } from 'src/client/weather';
import { useAuth } from 'src/client/auth-provider';
import { getLocations } from 'src/client/locations';
import { getUser, nullUser } from 'src/client/users';
import { DashboardContent } from 'src/layouts/dashboard';
import { getWeatherAggregated } from 'src/client/weather-aggregated';
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
  const [aggGroup, setAggGroup] = useState("");
  const [aggFunctions, setAggFunctions] = useState(["avg"]);
  const [dataset, setDataset] = useState<WeatherAggregated[] | Weather[]>([]);

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

  const aggFields: string[] = useMemo(
    () => (
      (aggGroup) ? (
	cartesianProduct(weatherFields, aggFunctions).map(
	  ([field, func]) => `${field}_${func}`
	)
      ) : []
    ),
    [aggGroup, weatherFields, aggFunctions]
  );

  const aggFieldsChoices: ServerChoicesList = useMemo(
    () => (
      (aggGroup) ? (
	Object.fromEntries(
	  cartesianProduct(weatherFields, aggFunctions).map(
	    ([field, func]) => [
	      `${field}_${func}`,
	      `${serverConstants.weatherFields[field]} ${serverConstants.aggregateFunctions[func]}`
	    ]
	  )
	)
      ) : {}
    ),
    [aggGroup, weatherFields, aggFunctions, serverConstants]
  );

  useEffect(() => {
    if (locationId) {
      if (aggGroup) {
	if (aggFields.length > 0) {
	  getWeatherAggregated(
	    {
	      locationIds: [locationId],
	      startDate: startDate.format('YYYY-MM-DD'),
	      endDate: endDate.format('YYYY-MM-DD'),
	      group: aggGroup,
	      fields: aggFields,
	      timezone: settings.timezone,
	      temperatureUnit: settings.temperatureUnit,
	      windSpeedUnit: settings.windSpeedUnit,
	      precipitationUnit: settings.precipitationUnit,
	    },
	    (newWeather: WeatherAggregated[]) => setDataset(newWeather)
	  );
	  return;
	}
      } else if (weatherFields.length > 0) {
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
	return;
      }
    }
    setDataset([]);
  }, [
    locationId,
    startDate,
    endDate,
    aggGroup,
    aggFunctions,
    weatherFields,
    aggFields,
    settings,
  ]);

  const handleWeatherFieldsChange = (event: SelectChangeEvent<string[]>) => {
    const {
      target: { value },
    } = event;
    setWeatherFields(
      typeof value === 'string' ? value.split(',') : value,
    );
  };

  const handleAggFunctionsChange = (event: SelectChangeEvent<string[]>) => {
    const {
      target: { value },
    } = event;
    setAggFunctions(
      typeof value === 'string' ? value.split(',') : value,
    );
  };

  const chartFields = (aggGroup) ? aggFields : weatherFields;
  const chartFieldsChoices = (
    (aggGroup) ? aggFieldsChoices : serverConstants.weatherFields
  );

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
	    onLocationChange={(event: SelectChangeEvent) => setLocationId(event.target.value)}
	    startDate={startDate}
	    onStartDateChange={(value: any) => setStartDate(value)}
	    endDate={endDate}
	    onEndDateChange={(value: any) => setEndDate(value)}
	    aggGroup={aggGroup}
	    aggGroupChoices={serverConstants.aggregateGroups}
	    onAggGroupChange={(event: SelectChangeEvent) => setAggGroup(event.target.value)}
	    weatherFields={weatherFields}
	    weatherFieldsChoices={serverConstants.weatherFields}
	    onWeatherFieldsChange={handleWeatherFieldsChange}
	    aggFunctions={aggFunctions}
	    aggFunctionsChoices={serverConstants.aggregateFunctions}
	    onAggFunctionsChange={handleAggFunctionsChange}
	    settings={settings}
	  />

	  <ExploreChart
	    dataset={dataset}
	    fields={chartFields}
	    fieldsChoices={chartFieldsChoices}
	    settings={settings}
	  />
      </Card>

    </DashboardContent>
  );
}
