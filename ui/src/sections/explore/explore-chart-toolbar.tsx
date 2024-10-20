import type { Location_ } from 'src/client/locations'
import type { SelectChangeEvent } from '@mui/material/Select';

import Select from '@mui/material/Select';
import Toolbar from '@mui/material/Toolbar';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

// ----------------------------------------------------------------------

type ExploreChartToolbarProps = {
  locations: Location_[],
  locationId: string,
  startDate: any,
  endDate: any,
  onLocationChange: (event: SelectChangeEvent) => void,
  onStartDateChange: (event: any) => void;
  onEndDateChange: (event: any) => void;
};

export function ExploreChartToolbar(
  {
    locations,
    locationId,
    startDate,
    endDate,
    onLocationChange,
    onStartDateChange,
    onEndDateChange
  }: ExploreChartToolbarProps
) {
  return (
    <Toolbar
      sx={{
        height: 96,
        display: 'flex',
        justifyContent: 'flex-start',
        p: (theme) => theme.spacing(0, 1, 0, 3),
        bgcolor: 'primary.lighter',
      }}
    >
      <FormControl>
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
      <DatePicker
	label="Start"
       	onChange={onStartDateChange}
	value={startDate}
      />
      <DatePicker
	label="End"
       	onChange={onEndDateChange}
	value={endDate}
      />
    </Toolbar>
  );
}
