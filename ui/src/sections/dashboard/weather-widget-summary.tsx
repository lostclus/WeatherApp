import type { User } from 'src/client/users';
import type { Weather } from 'src/client/weather';
import type { Location_ } from 'src/client/locations';
import type { ColorType } from 'src/theme/core/palette';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import { useTheme } from '@mui/material/styles';

import { fShortenNumber } from 'src/utils/format-number';
import { weatherCodeInfoMap } from 'src/utils/weather-code';

import { varAlpha, bgGradient } from 'src/theme/styles';
import { useServerConstants } from 'src/client/server-constants-provider';

import { SvgColor } from 'src/components/svg-color';

// ----------------------------------------------------------------------

type Props = {
  loc: Location_;
  weather: Weather;
  settings: User;
  color?: ColorType;
};

export function WeatherWidgetSummary({
  loc,
  weather,
  settings,
  color = 'primary',
}: Props) {
  const theme = useTheme();
  const serverConstants = useServerConstants();

  const temperature = fShortenNumber(weather.temperature_2m);
  const tempUnit = serverConstants.temperatureUnits[settings.temperatureUnit];
  const tempUnitShort = (tempUnit.indexOf(" ") > 0) ? tempUnit.split(" ").at(-1) : tempUnit;
  const weatherCode = weather.weather_code || 0;
  const weatherCodeInfo = weatherCodeInfoMap[weatherCode.toString()];

  return (
    <Card
      sx={{
        ...bgGradient({
          color: `135deg, ${varAlpha(theme.vars.palette[color].lighterChannel, 0.48)}, ${varAlpha(theme.vars.palette[color].lightChannel, 0.48)}`,
        }),
        p: 3,
        boxShadow: 'none',
        position: 'relative',
        color: `${color}.darker`,
        backgroundColor: 'common.white',
      }}
    >
      <Box sx={{ width: 48, height: 48, mb: 3 }}>
	<img
	  src={ weatherCodeInfo.day.image }
	  alt={ weatherCodeInfo.day.description }
	/>
      </Box>

      <Box
        sx={{
          display: 'flex',
          flexWrap: 'wrap',
          alignItems: 'flex-end',
          justifyContent: 'flex-end',
        }}
      >
        <Box sx={{ flexGrow: 1, minWidth: 112 }}>
          <Box sx={{ mb: 1, typography: 'subtitle2' }}>{loc.name}</Box>
          <Box sx={{ typography: 'h4' }}>
	    {`${temperature} ${tempUnitShort}`}
	  </Box>
        </Box>

      </Box>

      <SvgColor
        src="/assets/background/shape-square.svg"
        sx={{
          top: 0,
          left: -20,
          width: 240,
          zIndex: -1,
          height: 240,
          opacity: 0.24,
          position: 'absolute',
          color: `${color}.main`,
        }}
      />
    </Card>
  );
}
