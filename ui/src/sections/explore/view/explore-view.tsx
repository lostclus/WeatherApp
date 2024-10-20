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
import { getLocations } from 'src/client/locations';
import { DashboardContent } from 'src/layouts/dashboard';

import { ExploreChart } from '../explore-chart';
import { ExploreChartToolbar } from '../explore-chart-toolbar';

// ----------------------------------------------------------------------

export function ExploreView() {
  const [locations, setLocations] = useState<Location_[]>([]);
  const [locationId, setLocationId] = useState<string | null>(null);
  const [startDate, setStartDate] = useState(dayjs('2024-10-01'));
  const [endDate, setEndDate] = useState(dayjs('2024-11-01'));
  const [dataset, setDataset] = useState<Weather[]>([]);

  useEffect(() => {
    getLocations(
      (newLocations: Location_[]) => {
	setLocations(newLocations);
      }
    );
  }, []);


  if (!locationId && locations && locations.length > 0) {
    let defaultLoc = locations.find((loc: Location_) => loc.isDefault);
    if (!defaultLoc) defaultLoc = locations[0];
    setLocationId(defaultLoc.id);
  }

  useEffect(() => {
    if (locationId) {
      getWeather(
	{
	  locationId,
	  startDate: startDate.format('YYYY-MM-DD'),
	  endDate: endDate.format('YYYY-MM-DD'),
	  fields: ["temperature_2m", "relative_humidity_2m"],
	  timezone: "UTC",
	},
	(newWeather: Weather[]) => setDataset(newWeather)
      );
    } else {
      setDataset([]);
    }
  }, [locationId, startDate, endDate]);

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
	  />

	  <ExploreChart dataset={dataset} />
      </Card>

    </DashboardContent>
  );
}
