export type ServerErrorDetail = {
  msg: string,
  loc: string[],
}

export type ServerErrors = {
  detail: ServerErrorDetail[] | string,
};

export type ServerChoicesList = { [index: string]: string };

export type ServerConstants = {
  timezones: ServerChoicesList,
  temperatureUnits: ServerChoicesList,
  windSpeedUnits: ServerChoicesList,
  precipitationUnits: ServerChoicesList,
  dateFormats: ServerChoicesList,
  timeFormats: ServerChoicesList,
  weatherFields: ServerChoicesList,
  aggregateGroups: ServerChoicesList,
  aggregateFunctions: ServerChoicesList,
};
