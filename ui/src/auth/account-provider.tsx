import { useMemo, useState, useEffect, useContext, createContext } from "react";

export type Account = { user_id: number, email: string };
type AccountData = {
  account: Account | null,
  rawAccount: string | null,
  setAccount: (newAccount: Account | null) => void,
};

const noAccount: AccountData = {
  account: null,
  rawAccount: null,
  setAccount: (newAccount: Account | null): void => {},
};

const AccountContext = createContext<AccountData>(noAccount);

type Props = {
  children: React.ReactNode;
};

export function AccountProvider({ children }: Props) {
  const storageAccount = localStorage.getItem("account");
  const [rawAccount, setRawAccount] = useState<string | null>(storageAccount);

  const setAccount = (newAccount: Account | null): void => {
    setRawAccount((newAccount) ? JSON.stringify(newAccount) : null);
  };

  useEffect(() => {
    if (rawAccount) {
      localStorage.setItem("account", rawAccount);
    } else {
      localStorage.removeItem("account");
    }
  }, [rawAccount]);

  const contextValue: AccountData = useMemo(
    () => ({
      account: (rawAccount) ? JSON.parse(rawAccount) as Account : null,
      rawAccount,
      setAccount,
    }),
    [rawAccount]
  );

  return (
    <AccountContext.Provider value={contextValue}>{children}</AccountContext.Provider>
  );
};

export function useAccount(): AccountData {
  return useContext(AccountContext);
}
