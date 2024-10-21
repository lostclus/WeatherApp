import type { User } from 'src/client/users'
import type { ServerErrors } from 'src/client/types';
import type { Location_ } from 'src/client/locations';
import type { ChangeEvent, SyntheticEvent } from 'react';

import { useState, useEffect } from 'react';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import Alert from '@mui/material/Alert';
import Select from '@mui/material/Select';
import Button from '@mui/material/Button';
import Snackbar from '@mui/material/Snackbar';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import Typography from '@mui/material/Typography';
import FormControl from '@mui/material/FormControl';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
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
  const [isSuccess, setIsSuccess] = useState(false);

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
    setIsSuccess(false);
  }

  const handleSubmit = (event: SyntheticEvent) => {
    event.preventDefault();
    const newErrors = new FormErrors();
    setIsSuccess(false);
    if (!formUser) return;

    if (newErrors.hasErrors()) {
      setErrors(newErrors);
    } else {
      updateUser(
	formUser, 
	(newUser: User) => {
	  setFormUser(newUser);
	  setIsSuccess(true);
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
	<Stack spacing={2} sx={{ mt: 1 }}>
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
	</Stack>
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

      <Snackbar
	open={isSuccess}
	anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
	autoHideDuration={3000}
	onClose={() => setIsSuccess(false)}
      >
	<Alert severity="success" variant="filled">Settings was updated.</Alert>
      </Snackbar>
      <Snackbar
	open={errors.hasErrors()}
	anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
	<Alert severity="error" variant="filled">{ errors.getErrors() }</Alert>
      </Snackbar>

      <Grid
	container
	spacing={0}
	direction="column"
	alignItems="center"
      >
	<Grid item xs={3}>
	  <Card sx={{ minWidth: 500 }}>
	    <form>
	      <CardContent>
		{renderForm}
	      </CardContent>
	      <CardActions
		sx={{
		  alignSelf: "stretch",
		  display: "flex",
		  justifyContent: "flex-end",
		  alignItems: "flex-start",
		  m: 1,
		}}
	      >
		<Button
		  type="submit"
		  variant="contained"
		  onClick={handleSubmit}
		>
		  Save
		</Button>
	      </CardActions>
	    </form>
	  </Card>
	</Grid>
      </Grid>
    </DashboardContent>
  );
}
