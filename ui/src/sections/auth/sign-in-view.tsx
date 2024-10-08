import type { ServerErrors } from 'src/utils/forms';

import axios from "axios";
import { useState, useCallback } from 'react';

import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import LoadingButton from '@mui/lab/LoadingButton';
import InputAdornment from '@mui/material/InputAdornment';

import { useRouter } from 'src/routes/hooks';

import { FormErrors } from 'src/utils/forms';

import { CONFIG } from 'src/config-global';

import { Iconify } from 'src/components/iconify';

import { useAuth } from "src/auth/auth-provider";

// ----------------------------------------------------------------------

export function SignInView() {
  const router = useRouter();
  const { setToken } = useAuth();

  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<FormErrors>(new FormErrors());

  const handleSignIn = useCallback(() => {
    const newErrors = new FormErrors();

    if (!email) {
      newErrors.addError('email', 'Email is required!');
    }
    if (!password) {
      newErrors.addError('password', 'Password is required!');
    }
    if (newErrors.hasErrors()) {
      setErrors(newErrors);
    } else {
      axios(
	{
	  method: 'post',
	  url: `${CONFIG.api.mainURL}/v1/token/pair`,
	  data: { email, password },
	}
      )
      .then(
	(response) => {
	  const token: string = response.data.access as string;
	  setToken(token);
	  router.push('/')
	}
      )
      .catch(
	(error) => {
	  if (typeof error.response.data.detail === "string") {
	    newErrors.addError('email', error.response.data.detail);
	  } else {
	    const serverErrors: ServerErrors = error.response.data;
	    newErrors.addFromServer(serverErrors);
	  }
	  setErrors(newErrors);
	}
      );
    }
  }, [router, email, password, setErrors, setToken]);

  const renderForm = (
    <Box display="flex" flexDirection="column" alignItems="flex-end">
      <TextField
        fullWidth
        name="email"
        label="Email address"
        defaultValue="hello@gmail.com"
        InputLabelProps={{ shrink: true }}
        sx={{ mb: 3 }}
	value={email}
	onChange={(ev) => setEmail(ev.target.value)}
	error={errors.hasErrorsIn('email')}
	helperText={errors.getErrorsIn('email')}
      />

      {/*
      <Link variant="body2" color="inherit" sx={{ mb: 1.5 }}>
        Forgot password?
      </Link>
      */}

      <TextField
        fullWidth
        name="password"
        label="Password"
        defaultValue="@demo1234"
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

      <LoadingButton
        fullWidth
        size="large"
        type="submit"
        color="inherit"
        variant="contained"
        onClick={handleSignIn}
      >
        Sign in
      </LoadingButton>
    </Box>
  );

  return (
    <>
      <Box gap={1.5} display="flex" flexDirection="column" alignItems="center" sx={{ mb: 5 }}>
        <Typography variant="h5">Sign in</Typography>
        <Typography variant="body2" color="text.secondary">
          Don’t have an account?
          <Link href="/sign-up" variant="subtitle2" sx={{ ml: 0.5 }}>
            Sign Up
          </Link>
        </Typography>
      </Box>

      {renderForm}
    </>
  );
}
