import type { User } from 'src/client/users';
import type { Location_ } from 'src/client/locations'
import type { SelectChangeEvent } from '@mui/material/Select';

import Stack from '@mui/material/Stack';
import Select from '@mui/material/Select';
import Toolbar from '@mui/material/Toolbar';
import Checkbox from '@mui/material/Checkbox';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import ListItemText from '@mui/material/ListItemText';
import OutlinedInput from '@mui/material/OutlinedInput';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';


// ----------------------------------------------------------------------

type ExploreChartToolbarProps = {
  locations: Location_[],
  locationId: string,
  onLocationChange: (event: SelectChangeEvent) => void,
  startDate: any,
  onStartDateChange: (event: any) => void;
  endDate: any,
  onEndDateChange: (event: any) => void;
  weatherFields: string[],
  weatherFieldsChoices: { [key: string]: string },
  onWeatherFieldsChange: (event: SelectChangeEvent<string[]>) => void,
  settings: User,
};

export function ExploreChartToolbar(
  {
    locations,
    locationId,
    onLocationChange,
    startDate,
    onStartDateChange,
    endDate,
    onEndDateChange,
    weatherFields,
    weatherFieldsChoices,
    onWeatherFieldsChange,
    settings,
  }: ExploreChartToolbarProps
) {
  return (
    <Toolbar
      sx={{
        height: 96,
        display: 'flex',
        justifyContent: 'flex-start',
        p: (theme) => theme.spacing(0, 1, 0, 3),
      }}
    >
      <Stack direction="row" spacing={2}>
	<FormControl sx={{ minWidth: 250 }}>
	  <InputLabel id="location-label">Location</InputLabel>
	  <Select
	    labelId="location-label"
	    label="Location"
	    value={locationId}
	    onChange={onLocationChange}
	  >
	    {locations.map((loc) => (
	      <MenuItem key={loc.id} value={loc.id}>{loc.name}</MenuItem>
	    ))}
	  </Select>
	</FormControl>
	<FormControl>
	  <DatePicker
	    label="Start"
	    format={settings.dateFormat}
	    onChange={onStartDateChange}
	    value={startDate}
	  />
	</FormControl>
	<FormControl>
	  <DatePicker
	    label="End"
	    format={settings.dateFormat}
	    onChange={onEndDateChange}
	    value={endDate}
	  />
	</FormControl>
	<FormControl>
	  <InputLabel id="weather-fields-label">Parameters</InputLabel>
	  <Select
	    labelId="weather-fields-label"
	    id="weather-fields"
	    multiple
	    value={weatherFields}
	    onChange={onWeatherFieldsChange}
	    input={<OutlinedInput label="Parameters" />}
	    renderValue={(selected) => selected.join(', ')}
	  >
	    {
	      Object.entries(weatherFieldsChoices).map(
		([value, label]) => (
		  <MenuItem key={value} value={value}>
		    <Checkbox checked={weatherFields.includes(value)} />
		    <ListItemText primary={label} />
		  </MenuItem>
		)
	      )
	    }
	  </Select>
	</FormControl>
      </Stack>
    </Toolbar>
  );
}
