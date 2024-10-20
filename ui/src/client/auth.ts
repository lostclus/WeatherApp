import axios from "axios";

import { CONFIG } from 'src/config-global';

import type { ServerErrors } from './types';

export type AuthResponse = {
  email: string,
  user_id: string,
  token_access: string,
  token_refresh: string,
  token_access_life_time: number,
};

export type UserInfo = {
  id: string,
  email: string,
}

export type AuthStore = {
  token: {
    access: string,
    refresh: string,
    refreshDelay: number,
  } | null,
  user: UserInfo | null,
}

export type AuthCallbackInfo = {
  setAuthenticated: (response: AuthResponse) => void,
  dropAuthenticated: () => void,
};

export type AuthInfo = AuthStore & AuthCallbackInfo;

export function createJwtToken(
  email: string,
  password: string,
  onSuccess: (authResponse: AuthResponse) => void,
  onError: (error: ServerErrors) => void,
): void {
  axios(
    {
      method: 'post',
      url: `${CONFIG.api.coreURL}/v1/token/`,
      data: { email, password },
    }
  )
  .then(
    (response) => onSuccess(response.data as AuthResponse)
  )
  .catch(
    (error) => onError(error.response.data as ServerErrors)
  );
}

export function refreshJwtToken(
  tokenRefresh: string,
  onSuccess: (authResponse: AuthResponse) => void,
  onError: (error: ServerErrors) => void,
): void {
  axios(
    {
      method: 'post',
      url: `${CONFIG.api.coreURL}/v1/token/refresh`,
      data: { token_refresh: tokenRefresh },
    }
  )
  .then(
    (response) => onSuccess(response.data as AuthResponse)
  )
  .catch(
    (error) => onError(error.response.data as ServerErrors)
  );
}
