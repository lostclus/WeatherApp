import axios from "axios";

import { CONFIG } from 'src/config-global';

import type { ServerErrors} from './types';

type UserServerProps = {
  id: string,
  timezone: string,
  temperature_unit: string,
  wind_speed_unit: string,
  precipitation_unit: string,
  date_format: string,
  time_format: string,
  default_location_id: string,
};

export type User = {
  id: string,
  timezone: string,
  temperatureUnit: string,
  windSpeedUnit: string,
  precipitationUnit: string,
  dateFormat: string,
  timeFormat: string,
  defaultLocationId: string,
}

function decodeUser(userServer: UserServerProps): User {
  const {
    id,
    timezone,
    temperature_unit,
    wind_speed_unit,
    precipitation_unit,
    date_format,
    time_format,
    default_location_id,
  } = userServer;

  return {
    id,
    timezone,
    temperatureUnit: temperature_unit,
    windSpeedUnit: wind_speed_unit,
    precipitationUnit: precipitation_unit,
    dateFormat: date_format,
    timeFormat: time_format,
    defaultLocationId: default_location_id,
  };
}

function encodeUser(user: User): UserServerProps {
  const {
    id,
    timezone,
    temperatureUnit,
    windSpeedUnit,
    precipitationUnit,
    dateFormat,
    timeFormat,
    defaultLocationId,
  } = user;
  return {
    id,
    timezone,
    temperature_unit: temperatureUnit,
    wind_speed_unit: windSpeedUnit,
    precipitation_unit: precipitationUnit,
    date_format: dateFormat,
    time_format: timeFormat,
    default_location_id: defaultLocationId,
  };
}

export function createUser(
  email: string,
  password: string,
  onSuccess: (user: User) => void,
  onError: (errors: ServerErrors) => void,
): void {
  axios(
    {
      method: 'post',
      url: `${CONFIG.api.coreURL}/v1/users/`,
      data: { email, password },
    }
  )
  .then(
    (response) => onSuccess(decodeUser(response.data as UserServerProps))
  )
  .catch(
    (error) => onError(error.response.data as ServerErrors)
  );
}

export function getUser(userId: string, onSuccess: (user: User) => void): void {
  axios.get(`${CONFIG.api.coreURL}/v1/users/${userId}`)
  .then(
    (response) => {
      const user = decodeUser(response.data);
      onSuccess(user);
    }
  );
}

export function updateUser(
  user: User,
  onSuccess: (user: User) => void,
  onError: (errors: ServerErrors) => void
): void {
  const serverUser = encodeUser(user);
  axios.patch(
    `${CONFIG.api.coreURL}/v1/users/${user.id}`, serverUser
  )
  .then((response) => {
    const newUser = decodeUser(response.data as UserServerProps);
    onSuccess(newUser);
  })
  .catch(
    (error) => {
	const serverErrors: ServerErrors = error.response.data;
	onError(serverErrors);
    }
  );
}
