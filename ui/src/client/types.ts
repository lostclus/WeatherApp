export type AuthResponse = {
  access: string,
  refresh: string,
  email: string,
};

export type UserInfo = {
  id: string,
  email: string,
}

export type AuthStore = {
  token: {
    access: string,
    refresh: string,
  } | null,
  user: UserInfo | null,
}

export type AuthCallbackInfo = {
  setAuthenticated: (response: AuthResponse) => void,
  dropAuthenticated: () => void,
};

export type AuthInfo = AuthStore & AuthCallbackInfo;

export type ServerErrorDetail = {
    msg: string,
    loc: string[],
}

export type ServerErrors = {
    detail: ServerErrorDetail[] | string,
};
