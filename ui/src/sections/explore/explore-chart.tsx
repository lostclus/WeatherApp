import type { Weather } from 'src/client/weather';

import dayjs from 'dayjs';

import { LineChart } from '@mui/x-charts/LineChart';

// ----------------------------------------------------------------------

const keyToLabel: { [key: string]: string } = {
  temperature_2m: "Temperature (2m)",
  relative_humidity_2m: "Relative humidity (2m)",
};

type Props =  {
  dataset: Weather[],
};

export function ExploreChart({ dataset }: Props) {
  return (
    <LineChart
      xAxis={[
	{
	  dataKey: 'timestamp',
	  scaleType: 'time',
	  valueFormatter: (value) => dayjs.unix(value / 1000).format(),
	}
      ]}
      series={Object.keys(keyToLabel).map((key) => ({
        dataKey: key,
        label: keyToLabel[key],
      }))}
      dataset={dataset}
      height={400}
    />
  );
}
