import type { User } from 'src/client/users';
import type { Location_ } from 'src/client/locations'
import type { ServerChoicesList } from 'src/client/types'
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
  aggGroup: string,
  aggGroupChoices: ServerChoicesList,
  onAggGroupChange: (event: SelectChangeEvent) => void,
  weatherFields: string[],
  weatherFieldsChoices: ServerChoicesList,
  onWeatherFieldsChange: (event: SelectChangeEvent<string[]>) => void,
  aggFunctions: string[],
  aggFunctionsChoices: ServerChoicesList,
  onAggFunctionsChange: (event: SelectChangeEvent<string[]>) => void,
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
    aggGroup,
    aggGroupChoices,
    onAggGroupChange,
    weatherFields,
    weatherFieldsChoices,
    onWeatherFieldsChange,
    aggFunctions,
    aggFunctionsChoices,
    onAggFunctionsChange,
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
	<FormControl sx={{ minWidth: 200 }}>
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
	<FormControl sx={{ minWidth: 100 }}>
	  <InputLabel id="agg-group-label">Group</InputLabel>
	  <Select
	    labelId="agg-group-label"
	    label="Group"
	    value={aggGroup}
	    onChange={onAggGroupChange}
	  >
	    <MenuItem value="">None</MenuItem>
	    {Object.entries(aggGroupChoices).map(([value, label]) => (
	      <MenuItem key={value} value={value}>{label}</MenuItem>
	    ))}
	  </Select>
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
	<FormControl sx={{ display: (aggGroup) ? '' : 'none' }}>
	  <InputLabel id="agg-functions-label">Aggregate</InputLabel>
	  <Select
	    labelId="agg-functions-label"
	    id="agg-functions"
	    multiple
	    value={aggFunctions}
	    onChange={onAggFunctionsChange}
	    input={<OutlinedInput label="Aggregate" />}
	    renderValue={(selected) => selected.join(', ')}
	  >
	    {
	      Object.entries(aggFunctionsChoices).map(
		([value, label]) => (
		  <MenuItem key={value} value={value}>
		    <Checkbox checked={aggFunctions.includes(value)} />
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
