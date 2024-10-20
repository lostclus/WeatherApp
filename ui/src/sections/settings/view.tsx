import type { User } from 'src/client/users'
import type { ServerErrors } from 'src/client/types';
import type { Location_ } from 'src/client/locations';
import type { ChangeEvent, SyntheticEvent } from 'react';

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

import { FormErrors } from 'src/client/forms';
import { useAuth } from "src/client/auth-provider";
import { getLocations } from 'src/client/locations';
import { getUser, updateUser } from 'src/client/users';
import { DashboardContent } from 'src/layouts/dashboard';
import { useServerConstants } from 'src/client/server-constants-provider';

// ----------------------------------------------------------------------

type Choices = { [key: string]: string };

type SelectControlProps = {
  name: string,
  label: string,
  value: string,
  onChange: (element: any) => void,
  choices: Choices,
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
  const labelId = `${name}-label-id`;
  const elemId = `${name}-id`;
  return (
    <FormControl>
      <InputLabel id={labelId}>{label}</InputLabel>
      <Select
	labelId={labelId}
        id={elemId}
	name={name}
	label={label}
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
  const [locationChoices, setLocationChoices] = useState<Choices>({});
  const [formUser, setFormUser] = useState<User | null>(null);
  const [errors, setErrors] = useState<FormErrors>(new FormErrors());

  if (!user)
    throw Error("Not authenticated");

  useEffect(() => {
    getLocations(
      (newLocations: Location_[]) => {
	const choices = Object.fromEntries(newLocations.map((loc) => [loc.id, loc.name]));
	setLocationChoices(choices);
      }
    );
  }, []);

  useEffect(() => {
    getUser(user.id, (newUser: User) => setFormUser(newUser));
  }, [user]);

  const handleChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const { name, value } = event.target;
    const newUser = { ...formUser, [name]: value } as User;
    setFormUser(newUser);
  }

  const handleSubmit = (event: SyntheticEvent) => {
    event.preventDefault();
    if (!formUser) return;
    const newErrors = new FormErrors();

    if (newErrors.hasErrors()) {
      setErrors(newErrors);
    } else {
      updateUser(
	formUser, 
	(newUser: User) => {
	  setFormUser(newUser);
	},
	(serverErrors: ServerErrors) => {
	  newErrors.addFromServer(serverErrors);
	  setErrors(newErrors);
	},
      )
    }
  }

  const renderForm = (
    <Box display="flex" flexDirection="column">
    {(!formUser) ? <CircularProgress/> : (
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
	    value={formUser.timezone}
	    onChange={handleChange}
	    choices={serverConstants.timezones}
	  />
	  <SelectControl
	    name="temperatureUnit"
	    label="Temperature Unit"
	    value={formUser.temperatureUnit}
	    onChange={handleChange}
	    choices={serverConstants.temperatureUnits}
	  />
	  <SelectControl
	    name="windSpeedUnit"
	    label="Wind Speed Unit"
	    value={formUser.windSpeedUnit}
	    onChange={handleChange}
	    choices={serverConstants.windSpeedUnits}
	  />
	  <SelectControl
	    name="precipitationUnit"
	    label="Precipitation Unit"
	    value={formUser.precipitationUnit}
	    onChange={handleChange}
	    choices={serverConstants.precipitationUnits}
	  />
	  <SelectControl
	    name="dateFormat"
	    label="Date Format"
	    value={formUser.dateFormat}
	    onChange={handleChange}
	    choices={serverConstants.dateFormats}
	  />
	  <SelectControl
	    name="timeFormat"
	    label="Time Format"
	    value={formUser.timeFormat}
	    onChange={handleChange}
	    choices={serverConstants.timeFormats}
	  />
	  <SelectControl
	    name="defaultLocationId"
	    label="Default Location"
	    value={(formUser.defaultLocationId in locationChoices) ? formUser.defaultLocationId : ""}
	    onChange={handleChange}
	    choices={locationChoices}
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
