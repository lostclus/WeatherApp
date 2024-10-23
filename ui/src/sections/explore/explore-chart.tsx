import type { User } from 'src/client/users';
import type { Weather } from 'src/client/weather';
import type { WeatherAggregated } from 'src/client/weather-aggregated';

import dayjs from 'dayjs';

import { LineChart } from '@mui/x-charts/LineChart';

// ----------------------------------------------------------------------

type Props =  {
  dataset: Weather[] | WeatherAggregated[],
  fields: string[],
  fieldsChoices: { [key: string]: string},
  settings: User,
};

export function ExploreChart(
  {
    dataset,
    fields,
    fieldsChoices,
    settings
  }: Props
) {
  return (
    <LineChart
      xAxis={[
	{
	  dataKey: 'timestamp',
	  scaleType: 'time',
	  valueFormatter: (value) => {
	    const fmt = `${settings.dateFormat} ${settings.timeFormat}`;
	    return dayjs.unix(value / 1000).format(fmt);
	  },
	}
      ]}
      series={fields.map((key) => ({
        dataKey: key,
        label: fieldsChoices[key],
	showMark: false,
      }))}
      dataset={dataset}
      height={400}
    />
  );
}
