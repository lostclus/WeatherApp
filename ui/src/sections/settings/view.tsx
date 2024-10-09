import type { ServerErrors } from 'src/client/types';

import axios from "axios";
import { useState, useCallback } from 'react';

import Box from '@mui/material/Box';
import Radio from '@mui/material/Radio';
import FormLabel from '@mui/material/FormLabel';
import RadioGroup from '@mui/material/RadioGroup';
import Typography from '@mui/material/Typography';
import LoadingButton from '@mui/lab/LoadingButton';
import FormControl from '@mui/material/FormControl';
import FormControlLabel from '@mui/material/FormControlLabel';

import { CONFIG } from 'src/config-global';
import { FormErrors } from 'src/client/forms';
import { useAuth } from "src/client/auth-provider";
import { DashboardContent } from 'src/layouts/dashboard';


// ----------------------------------------------------------------------

export function SettingsView() {
  const { user } = useAuth();
  const [temperatureUnit, setTemperatureUnit] = useState("");
  const [errors, setErrors] = useState<FormErrors>(new FormErrors());

  if (!user)
    throw Error("Not authenticated");

  const handleSubmit = useCallback(() => {
    const newErrors = new FormErrors();

    if (newErrors.hasErrors()) {
      setErrors(newErrors);
    } else {
      axios(
	{
	  method: 'patch',
	  url: `${CONFIG.api.coreURL}/v1/users/${user.id}/`,
	  data: {
	    temperature_unit: temperatureUnit,
	  },
	}
      )
      .then(
	() => {
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

  }, [temperatureUnit, setErrors, user]);

  const renderForm = (
    <Box display="flex" flexDirection="column">
      { (errors) ? "" : "" }
      <FormControl>
	<FormLabel htmlFor="temperatureUnit">
	    Temperature Unit
	</FormLabel>

	<RadioGroup
	  name="temperatureUnit"
	  value={temperatureUnit}
	  onChange={(ev) => setTemperatureUnit(ev.target.value)}
	>
	  <FormControlLabel value="a" control={<Radio />} label="A" />
	  <FormControlLabel value="b" control={<Radio />} label="B" />
	  <FormControlLabel value="c" control={<Radio />} label="C" />
	</RadioGroup>

      </FormControl>
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
