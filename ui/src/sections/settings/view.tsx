import type { ServerErrors } from 'src/client/types';
import type { ChangeEvent, SyntheticEvent } from 'react';

import axios from "axios";
import { useState, useEffect } from 'react';

import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import Typography from '@mui/material/Typography';
import LoadingButton from '@mui/lab/LoadingButton';
import FormControl from '@mui/material/FormControl';
import CircularProgress from '@mui/material/CircularProgress';

import { CONFIG } from 'src/config-global';
import { FormErrors } from 'src/client/forms';
import { useAuth } from "src/client/auth-provider";
import { DashboardContent } from 'src/layouts/dashboard';
import { useServerConstants } from 'src/client/server-constants-provider';

// ----------------------------------------------------------------------

type FormData = {
  timezone: string,
  temperature_unit: string,
  wind_speed_unit: string,
  precipitation_unit: string,
  date_format: string,
  time_format: string
};

type SelectControlProps = {
  name: string,
  label: string,
  value: string,
  onChange: (element: any) => void,
  choices: { [index: string]: string},
};

function SelectControl(
  {
    name,
    label,
    value,
    onChange,
    choices,
  }: SelectControlProps
) {
  const labelId = `${name}-label`;
  return (
    <FormControl>
      <InputLabel id={labelId}>{label}</InputLabel>
      <Select
	name={name}
	label={label}
	labelId={labelId}
	autoWidth
	value={value}
	onChange={onChange}
      >
	{
	  Object.entries(choices).map(
	    ([v, l]) => (
	      <MenuItem key={v} value={v}>{l}</MenuItem>
	    )
	  )
	}
      </Select>
    </FormControl>
  );
}

export function SettingsView() {
  const { user } = useAuth();
  const serverConstants = useServerConstants();
  const [formData, setFormData] = useState<FormData | null>(null);
  const [errors, setErrors] = useState<FormErrors>(new FormErrors());

  if (!user)
    throw Error("Not authenticated");

  useEffect(() => {
    axios.get(`${CONFIG.api.coreURL}/v1/users/${user.id}`)
    .then(
      (response) => {
	const newData = response.data as FormData;
	setFormData(newData);
      }
    )
  }, [user]);

  const handleChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const { name, value } = event.target;
    const newData = { ...formData, [name]: value } as FormData;
    setFormData(newData);
  }

  const handleSubmit = (event: SyntheticEvent) => {
    event.preventDefault();
    const newErrors = new FormErrors();

    if (newErrors.hasErrors()) {
      setErrors(newErrors);
    } else {
      const data = formData;
      setFormData(null);
      axios(
	{
	  method: 'patch',
	  url: `${CONFIG.api.coreURL}/v1/users/${user.id}`,
	  data,
	}
      )
      .then(
	(response) => {
	  const newData = response.data as FormData;
	  setFormData(newData);
	}
      )
      .catch(
	(error) => {
	  const serverErrors: ServerErrors = error.response.data;
	  newErrors.addFromServer(serverErrors);
	  setErrors(newErrors);
	}
      );
    }
  }

  const renderForm = (
    <Box display="flex" flexDirection="column">
    {(!formData) ? <CircularProgress/> : (
      <form>
	<Stack spacing={2}>
	  {
	    (errors.hasErrors()) ? (
	      <Typography>errors.getErrors()</Typography>
	    ) : ""
	  }

	  <SelectControl
	    name="timezone"
	    label="Timezone"
	    value={formData.timezone}
	    onChange={handleChange}
	    choices={serverConstants.timezones}
	  />
	  <SelectControl
	    name="temperature_unit"
	    label="Temperature Unit"
	    value={formData.temperature_unit}
	    onChange={handleChange}
	    choices={serverConstants.temperatureUnits}
	  />
	  <SelectControl
	    name="wind_speed_unit"
	    label="Wind Speed Unit"
	    value={formData.wind_speed_unit}
	    onChange={handleChange}
	    choices={serverConstants.windSpeedUnits}
	  />
	  <SelectControl
	    name="precipitation_unit"
	    label="Precipitation Unit"
	    value={formData.precipitation_unit}
	    onChange={handleChange}
	    choices={serverConstants.precipitationUnits}
	  />
	  <SelectControl
	    name="date_format"
	    label="Date Format"
	    value={formData.date_format}
	    onChange={handleChange}
	    choices={serverConstants.dateFormats}
	  />
	  <SelectControl
	    name="time_format"
	    label="Time Format"
	    value={formData.time_format}
	    onChange={handleChange}
	    choices={serverConstants.timeFormats}
	  />

	  <LoadingButton
	    fullWidth
	    size="large"
	    type="submit"
	    color="inherit"
	    variant="contained"
	    onClick={handleSubmit}
	  >
	    Save
	  </LoadingButton>
	</Stack>
      </form>
    )}
    </Box>
  )

  return (
    <DashboardContent>
      <Box display="flex" alignItems="center" mb={5}>
        <Typography variant="h4" flexGrow={1}>
          User Settings
        </Typography>
      </Box>

      {renderForm}
    </DashboardContent>
  );
}
