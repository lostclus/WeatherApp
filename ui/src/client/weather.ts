import axios from "axios";

import { CONFIG } from 'src/config-global';

export type Weather = {
  location_id: string,
  timestamp: number,
  temperature_2m?: number,
  relative_humidity_2m?: number,
  dew_point_2m?: number,
  apparent_temperature?: number,
  pressure_msl?: number,
  precipitation?: number,
  rain?: number,
  snowfall?: number,
  cloud_cover?: number,
  cloud_cover_low?: number,
  cloud_cover_mid?: number,
  cloud_cover_high?: number,
  shortwave_radiation?: number,
  direct_radiation?: number,
  direct_normal_irradiance?: number,
  diffuse_radiation?: number,
  global_tilted_irradiance?: number,
  sunshine_duration?: number,
  wind_speed_10m?: number,
  wind_speed_100m?: number,
  wind_direction_10m?: number,
  wind_direction_100m?: number,
  wind_gusts_10m?: number,
  et0_fao_evapotranspiration?: number,
  weather_code?: number,
  snow_depth?: number,
  vapour_pressure_deficit?: number,
};

export type WeatherServerProps = {
  location_id: string,
  timestamp: string,
  temperature_2m?: number,
  relative_humidity_2m?: number,
  dew_point_2m?: number,
  apparent_temperature?: number,
  pressure_msl?: number,
  precipitation?: number,
  rain?: number,
  snowfall?: number,
  cloud_cover?: number,
  cloud_cover_low?: number,
  cloud_cover_mid?: number,
  cloud_cover_high?: number,
  shortwave_radiation?: number,
  direct_radiation?: number,
  direct_normal_irradiance?: number,
  diffuse_radiation?: number,
  global_tilted_irradiance?: number,
  sunshine_duration?: number,
  wind_speed_10m?: number,
  wind_speed_100m?: number,
  wind_direction_10m?: number,
  wind_direction_100m?: number,
  wind_gusts_10m?: number,
  et0_fao_evapotranspiration?: number,
  weather_code?: number,
  snow_depth?: number,
  vapour_pressure_deficit?: number,
};

export type BaseWeatherReqest = {
  locationIds: string[],
  fields: string[],
  timezone: string,
  temperatureUnit: string,
  windSpeedUnit: string,
  precipitationUnit: string,
};

export type WeatherReqest = BaseWeatherReqest & {
  startDate: string,
  endDate: string,
};

export type CurrentWeatherRequest = BaseWeatherReqest;

type BaseWeatherReqestServerProps = {
  location_ids: string[],
  fields: string[],
  timezone: string,
  temperature_unit: string,
  wind_speed_unit: string,
  precipitation_unit: string,
};

type WeatherReqestServerProps = BaseWeatherReqestServerProps & {
  start_date: string,
  end_date: string,
};

type CurrentWeatherReqestServerProps = BaseWeatherReqestServerProps;

function decodeWeather(serverWeather: WeatherServerProps): Weather {
  return {...serverWeather, timestamp: Date.parse(serverWeather.timestamp)};
}

function encodeWeatherReqest(req: WeatherReqest): WeatherReqestServerProps {
  const {
    locationIds,
    startDate,
    endDate,
    fields,
    timezone,
    temperatureUnit,
    windSpeedUnit,
    precipitationUnit,
  } = req;
  const serverReq: WeatherReqestServerProps = {
    location_ids: locationIds,
    start_date: startDate, 
    end_date: endDate,
    fields,
    timezone,
    temperature_unit: temperatureUnit,
    wind_speed_unit: windSpeedUnit,
    precipitation_unit: precipitationUnit,
  };
  return serverReq;
}

function encodeCurrentWeatherRequest(
  req: CurrentWeatherRequest
): CurrentWeatherReqestServerProps {
  const {
    locationIds,
    fields,
    timezone,
    temperatureUnit,
    windSpeedUnit,
    precipitationUnit,
  } = req;
  const serverReq: CurrentWeatherReqestServerProps = {
    location_ids: locationIds,
    fields,
    timezone,
    temperature_unit: temperatureUnit,
    wind_speed_unit: windSpeedUnit,
    precipitation_unit: precipitationUnit,
  };
  return serverReq;
}

export function getWeather(
  req: WeatherReqest,
  onSuccess: (newWeather: Weather[]) => void,
): void {
  axios.post(
    `${CONFIG.api.queryURL}/v1/weather`,
    encodeWeatherReqest(req),
  )
  .then(
    (response) => {
      const newWeather = response.data.map(decodeWeather);
      onSuccess(newWeather);
    }
  );
}

export function getCurrentWeather(
  req: CurrentWeatherRequest,
  onSuccess: (newWeather: Weather[]) => void,
): void {
  axios.post(
    `${CONFIG.api.queryURL}/v1/current-weather`,
    encodeCurrentWeatherRequest(req),
  )
  .then(
    (response) => {
      const newWeather = response.data.map(decodeWeather);
      onSuccess(newWeather);
    }
  );
}
