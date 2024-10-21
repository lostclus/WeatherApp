import type { User } from 'src/client/users';
import type { Weather } from 'src/client/weather';

import dayjs from 'dayjs';

import { LineChart } from '@mui/x-charts/LineChart';

// ----------------------------------------------------------------------

type Props =  {
  dataset: Weather[],
  weatherFields: string[],
  weatherFieldsChoices: { [key: string]: string},
  settings: User,
};

export function ExploreChart(
  {
    dataset,
    weatherFields,
    weatherFieldsChoices,
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
      series={weatherFields.map((key) => ({
        dataKey: key,
        label: weatherFieldsChoices[key],
	showMark: false,
      }))}
      dataset={dataset}
      height={400}
    />
  );
}
