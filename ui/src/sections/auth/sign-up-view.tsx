import type { ServerErrors } from 'src/client/types';

import axios from "axios";
import { useState, useCallback } from 'react';

import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import LoadingButton from '@mui/lab/LoadingButton';
import InputAdornment from '@mui/material/InputAdornment';

import { useRouter } from 'src/routes/hooks';

import { CONFIG } from 'src/config-global';
import { FormErrors } from 'src/client/forms';

import { Iconify } from 'src/components/iconify';

// ----------------------------------------------------------------------

export function SignUpView() {
  const router = useRouter();

  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [errors, setErrors] = useState<FormErrors>(new FormErrors());

  const handleSignUp = useCallback(() => {
    const newErrors = new FormErrors();

    if (!email) {
      newErrors.addError('email', 'Email is required!');
    }
    if (!password) {
      newErrors.addError('password', 'Password is required!');
    }
    if (password !== password2) {
      newErrors.addError('password2', "Passwords does'nt match!");
    }
    if (newErrors.hasErrors()) {
      setErrors(newErrors);
    } else {
      axios(
	{
	  method: 'post',
	  url: `${CONFIG.api.coreURL}/v1/users/`,
	  data: { email, password },
	}
      )
      .then(
	() => router.push('/')
      )
      .catch(
	(error) => {
	  const serverErrors: ServerErrors = error.response.data;
	  newErrors.addFromServer(serverErrors);
	  setErrors(newErrors);
	}
      );
    }
  }, [router, email, password, password2, setErrors]);

  const renderForm = (
    <Box display="flex" flexDirection="column" alignItems="flex-end">
      <TextField
        fullWidth
        name="email"
        label="Email address"
	required
        InputLabelProps={{ shrink: true }}
        sx={{ mb: 3 }}
	value={email}
	onChange={(ev) => setEmail(ev.target.value)}
	error={errors.hasErrorsIn('email')}
	helperText={errors.getErrorsIn('email')}
      />

      <TextField
        fullWidth
        name="password"
        label="Password"
        InputLabelProps={{ shrink: true }}
        type={showPassword ? 'text' : 'password'}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                <Iconify icon={showPassword ? 'solar:eye-bold' : 'solar:eye-closed-bold'} />
              </IconButton>
            </InputAdornment>
          ),
        }}
        sx={{ mb: 3 }}
	value={password}
	onChange={(ev) => setPassword(ev.target.value)}
	error={errors.hasErrorsIn('password')}
	helperText={errors.getErrorsIn('password')}
      />

      <TextField
        fullWidth
        name="password2"
        label="Repeat password"
        InputLabelProps={{ shrink: true }}
	type="password"
        sx={{ mb: 3 }}
	value={password2}
	onChange={(ev) => setPassword2(ev.target.value)}
	error={errors.hasErrorsIn('password2')}
	helperText={errors.getErrorsIn('password2')}
      />

      <LoadingButton
        fullWidth
        size="large"
        type="submit"
        color="inherit"
        variant="contained"
        onClick={handleSignUp}
      >
        Sign up
      </LoadingButton>
    </Box>
  );

  return (
    <>
      <Box gap={1.5} display="flex" flexDirection="column" alignItems="center" sx={{ mb: 5 }}>
        <Typography variant="h5">Sign up</Typography>
      </Box>

      {renderForm}
    </>
  );
}
