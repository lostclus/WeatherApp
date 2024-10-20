import axios from "axios";

import { CONFIG } from 'src/config-global';

import type { ServerErrors} from './types';

export type Location_ = {
  id: string,
  name: string,
  latitude: string,
  longitude: string,
  isDefault: boolean,
  isActive: boolean,
};

type LocationServerProps = {
  id: string;
  name: string;
  latitude: string;
  longitude: string;
  is_default: boolean;
  is_active: boolean;
};

function encodeLocation(loc: Location_): LocationServerProps {
  const { id, name, latitude, longitude, isDefault, isActive } = loc;
  const serverLoc: LocationServerProps = {
    id, name, latitude, longitude, is_default: isDefault, is_active: isActive,
  };
  return serverLoc;
}

function decodeLocation(serverLoc: LocationServerProps): Location_ {
  const { id, name, latitude, longitude, is_default, is_active } = serverLoc;
  const loc: Location_ = {
    id, name, latitude, longitude, isDefault: is_default, isActive: is_active
  };
  return loc;
}

export function getLocations(onSuccess: (newLocations: Location_[]) => void):void {
  axios.get(`${CONFIG.api.coreURL}/v1/locations/`)
  .then(
    (response) => {
      const newLocations = response.data.map(decodeLocation);
      onSuccess(newLocations);
    }
  );
}

export function getMyLocations(onSuccess: (newLocations: Location_[]) => void):void {
  axios.get(`${CONFIG.api.coreURL}/v1/locations/my`)
  .then(
    (response) => {
      const newLocations = response.data.map(decodeLocation);
      onSuccess(newLocations);
    }
  );
}

export function createLocation(
  location_: Location_,
  onSuccess: (loc: Location_) => void,
  onError: (errors: ServerErrors) => void
): void {
  const serverLoc = encodeLocation(location_);
  axios.post(
    `${CONFIG.api.coreURL}/v1/locations/`, serverLoc
  )
  .then((response) => {
    const newLoc = decodeLocation(response.data as LocationServerProps);
    onSuccess(newLoc);
  })
  .catch(
    (error) => {
	const serverErrors: ServerErrors = error.response.data;
	onError(serverErrors);
    }
  );
}

export function updateLocation(
  location_: Location_,
  onSuccess: (location_: Location_) => void,
  onError: (errors: ServerErrors) => void
): void {
  const serverLoc = encodeLocation(location_);
  axios.put(
    `${CONFIG.api.coreURL}/v1/locations/${location_.id}`, serverLoc
  )
  .then((response) => {
    const newLoc = decodeLocation(response.data as LocationServerProps);
    onSuccess(newLoc);
  })
  .catch(
    (error) => {
	const serverErrors: ServerErrors = error.response.data;
	onError(serverErrors);
    }
  );
}

export function deleteLocation(
  locationId: string,
  onSuccess: () => void,
): void {
  axios.delete(
    `${CONFIG.api.coreURL}/v1/locations/${locationId}`,
  )
  .then(() => onSuccess());
}
