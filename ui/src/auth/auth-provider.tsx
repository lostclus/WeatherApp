import axios from "axios";
import { useMemo, useState, useEffect, useContext, createContext } from "react";

type Token = string | null;
type AuthData = { token: Token, setToken: (newToken: Token) => void };

const noAuth : AuthData = {
  token: null,
  setToken: (newToken: Token) => {},
};

const AuthContext = createContext<AuthData>(noAuth);

type Props = {
  children: React.ReactNode;
};

export function AuthProvider({ children }: Props) {
  // State to hold the authentication token
  const [token, setToken_] = useState(localStorage.getItem("token"));

  // Function to set the authentication token
  const setToken = (newToken: string | null) => {
    setToken_(newToken);
  };

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common.Authorization = `Bearer ${token}`;
      localStorage.setItem("token", token);
    } else {
      delete axios.defaults.headers.common.Authorization;
      localStorage.removeItem("token");
    }
  }, [token]);

  // Memoized value of the authentication context
  const contextValue: AuthData = useMemo(
    () => ({
      token,
      setToken,
    }),
    [token]
  );

  // Provide the authentication context to the children components
  return (
    <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>
  );
};

export function useAuth() : AuthData {
  return useContext(AuthContext);
}
