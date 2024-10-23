import axios from "axios";

import { CONFIG } from 'src/config-global';

export type WeatherAggregated = {
  [ key: string]: any
};

export type WeatherAggregatedServerProps = {
  [ key: string]: any
};

export type WeatherAggregatedRequest = {
  locationIds: string[],
  startDate: string,
  endDate: string,
  group: string,
  fields: string[],
  timezone: string,
  temperatureUnit: string,
  windSpeedUnit: string,
  precipitationUnit: string,
};

type WeatherAggregatedRequestServerProps = {
  location_ids: string[],
  start_date: string,
  end_date: string,
  group: string,
  fields: string[],
  timezone: string,
  temperature_unit: string,
  wind_speed_unit: string,
  precipitation_unit: string,
};

function decodeWeatherAggregated(
  serverWeather: WeatherAggregatedServerProps
): WeatherAggregated {
  return {...serverWeather, timestamp: Date.parse(serverWeather.timestamp)};
}

function encodeWeatherAggregatedReqest(
  req: WeatherAggregatedRequest
): WeatherAggregatedRequestServerProps {
  const {
    locationIds,
    startDate,
    endDate,
    group,
    fields,
    timezone,
    temperatureUnit,
    windSpeedUnit,
    precipitationUnit,
  } = req;
  const serverReq: WeatherAggregatedRequestServerProps = {
    location_ids: locationIds,
    start_date: startDate, 
    end_date: endDate,
    group,
    fields,
    timezone,
    temperature_unit: temperatureUnit,
    wind_speed_unit: windSpeedUnit,
    precipitation_unit: precipitationUnit,
  };
  return serverReq;
}

export function getWeatherAggregated(
  req: WeatherAggregatedRequest,
  onSuccess: (newWeather: WeatherAggregated[]) => void,
): void {
  axios.post(
    `${CONFIG.api.queryURL}/v1/weather-aggregated`,
    encodeWeatherAggregatedReqest(req),
  )
  .then(
    (response) => {
      const newWeather = response.data.map(decodeWeatherAggregated);
      onSuccess(newWeather);
    }
  );
}
