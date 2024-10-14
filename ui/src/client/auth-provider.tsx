import axios from "axios";
import { useMemo, useState, useEffect, useContext, createContext } from "react";

import type { AuthInfo, AuthStore, AuthResponse} from "./types";


const nullAuth: AuthInfo = {
  token: null,
  user: null,
  setAuthenticated: (response: AuthResponse): void => {},
  dropAuthenticated: (): void => {},
};

const AuthContext = createContext<AuthInfo>(nullAuth);

type Props = {
  children: React.ReactNode;
};

export function AuthProvider({ children }: Props) {
  const [rawAuth, setRawAuth] = useState(localStorage.getItem("auth"));
  const store = (rawAuth) ? JSON.parse(rawAuth) : null;

  const setAuthenticated = (response: AuthResponse): void => {
    const newStore: AuthStore = {
      token: {
	access: response.token_access,
	refresh: response.token_refresh,
      },
      user: {
	id: response.user_id,
	email: response.email,
      }
    };
    setRawAuth(JSON.stringify(newStore));
  };

  const dropAuthenticated = (): void => {
    setRawAuth(null);
  }

  useEffect(() => {
    if (rawAuth) {
      localStorage.setItem("auth", rawAuth);
    } else {
      localStorage.removeItem("auth");
    }
  }, [rawAuth]);

  if (store && rawAuth) {
    axios.defaults.headers.common.Authorization = `Bearer ${store.token.access}`;
  } else {
    delete axios.defaults.headers.common.Authorization;
  }

  const contextValue: AuthInfo = useMemo(
    () => ({
      ...store,
      setAuthenticated,
      dropAuthenticated,
    }),
    [store]
  );

  // Provide the authentication context to the children components
  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};

export function useAuth() : AuthInfo {
  return useContext(AuthContext);
}
