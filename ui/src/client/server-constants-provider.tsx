import axios from "axios";
import { useState, useEffect, useContext, createContext } from "react";

import { CONFIG } from 'src/config-global';

import { useAuth } from './auth-provider';

import type { ServerConstants } from './types';

const nullServerConstants: ServerConstants = {
  timezones: {},
  temperatureUnits: {},
  windSpeedUnits: {},
  precipitationUnits: {},
  dateFormats: {},
  timeFormats: {},
  weatherFields: {},
  aggregateGroups: {},
  aggregateFunctions: {},
};

const ServerConstantsContext = createContext<ServerConstants>(nullServerConstants);

type Props = {
  children: React.ReactNode;
};

export function ServerConstantsProvider({ children }: Props) {
  const { user } = useAuth();
  const [serverConstants, setServerConstants] = useState<ServerConstants | null>(null);

  if (user && !serverConstants) {
    const serverConstantsRaw = sessionStorage.getItem("serverConstants");
    if (serverConstantsRaw) {
      setServerConstants(JSON.parse(serverConstantsRaw) as ServerConstants);
    } else {
      axios.get(`${CONFIG.api.coreURL}/v1/constants`)
      .then(
	(response) => {
	  const {
	    timezones, 
	    temperature_units: temperatureUnits,
	    wind_speed_units: windSpeedUnits,
	    precipitation_units: precipitationUnits,
	    date_formats: dateFormats,
	    time_formats: timeFormats,
	    weather_fields: weatherFields,
	    aggregate_groups: aggregateGroups,
	    aggregate_functions: aggregateFunctions,
	  } = response.data;
	  const newServerConstants = {
	    timezones,
	    temperatureUnits,
	    windSpeedUnits,
	    precipitationUnits,
	    dateFormats,
	    timeFormats,
	    weatherFields,
	    aggregateGroups,
	    aggregateFunctions,
	  };
	  setServerConstants(newServerConstants);
	}
      )
    }
  }

  useEffect(() => {
    if (user && serverConstants) {
      sessionStorage.setItem("serverConstants", JSON.stringify(serverConstants));
    } else {
      sessionStorage.removeItem("serverConstants");
    }
  }, [user, serverConstants]);

  const contextValue = serverConstants || nullServerConstants;

  return (
    <ServerConstantsContext.Provider value={contextValue}>{children}</ServerConstantsContext.Provider>
  );
}

export function useServerConstants(): ServerConstants {
  return useContext(ServerConstantsContext);
}
