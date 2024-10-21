import type { User } from 'src/client/users';
import type { Location_ } from 'src/client/locations'
import type { SelectChangeEvent } from '@mui/material/Select';

import Stack from '@mui/material/Stack';
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
  settings: User,
};

export function ExploreChartToolbar(
  {
    locations,
    locationId,
    startDate,
    endDate,
    onLocationChange,
    onStartDateChange,
    onEndDateChange,
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
      </Stack>
    </Toolbar>
  );
}
