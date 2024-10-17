-- +goose Up
-- +goose StatementBegin
CREATE TABLE weather (
    `timestamp` DateTime,
    `location_id` Int64,
    `_time` DateTime,
    `temperature_2m` Nullable(Float32),
    `relative_humidity_2m` Nullable(Float32),
    `dew_point_2m` Nullable(Float32),
    `apparent_temperature` Nullable(Float32),
    `pressure_msl` Nullable(Float32),
    `precipitation` Nullable(Float32),
    `rain` Nullable(Float32),
    `snowfall` Nullable(Float32),
    `cloud_cover` Nullable(Float32),
    `cloud_cover_low` Nullable(Float32),
    `cloud_cover_mid` Nullable(Float32),
    `cloud_cover_high` Nullable(Float32),
    `shortwave_radiation` Nullable(Float32),
    `direct_radiation` Nullable(Float32),
    `direct_normal_irradiance` Nullable(Float32),
    `diffuse_radiation` Nullable(Float32),
    `global_tilted_irradiance` Nullable(Float32),
    `sunshine_duration` Nullable(Float32),
    `wind_speed_10m` Nullable(Float32),
    `wind_speed_100m` Nullable(Float32),
    `wind_direction_10m` Nullable(Float32),
    `wind_direction_100m` Nullable(Float32),
    `wind_gusts_10m` Nullable(Float32),
    `et0_fao_evapotranspiration` Nullable(Float32),
    `weather_code` Nullable(Int),
    `snow_depth` Nullable(Float32),
    `vapour_pressure_deficit` Nullable(Float32)
)
ENGINE ReplacingMergeTree(_time)
ORDER BY (timestamp, location_id)
PARTITION BY (toYYYYMM(`timestamp`));
-- +goose StatementEnd
-- +goose StatementBegin
CREATE TABLE weather_queue (
    `timestamp` DateTime,
    `location_id` Int64,
    `_time` DateTime,
    `temperature_2m` Nullable(Float32),
    `relative_humidity_2m` Nullable(Float32),
    `dew_point_2m` Nullable(Float32),
    `apparent_temperature` Nullable(Float32),
    `pressure_msl` Nullable(Float32),
    `precipitation` Nullable(Float32),
    `rain` Nullable(Float32),
    `snowfall` Nullable(Float32),
    `cloud_cover` Nullable(Float32),
    `cloud_cover_low` Nullable(Float32),
    `cloud_cover_mid` Nullable(Float32),
    `cloud_cover_high` Nullable(Float32),
    `shortwave_radiation` Nullable(Float32),
    `direct_radiation` Nullable(Float32),
    `direct_normal_irradiance` Nullable(Float32),
    `diffuse_radiation` Nullable(Float32),
    `global_tilted_irradiance` Nullable(Float32),
    `sunshine_duration` Nullable(Float32),
    `wind_speed_10m` Nullable(Float32),
    `wind_speed_100m` Nullable(Float32),
    `wind_direction_10m` Nullable(Float32),
    `wind_direction_100m` Nullable(Float32),
    `wind_gusts_10m` Nullable(Float32),
    `et0_fao_evapotranspiration` Nullable(Float32),
    `weather_code` Nullable(Int),
    `snow_depth` Nullable(Float32),
    `vapour_pressure_deficit` Nullable(Float32)
)
ENGINE Kafka(kafka_cluster)
-- +goose StatementEnd
-- +goose StatementBegin
CREATE MATERIALIZED VIEW weather_view TO weather AS
SELECT *
FROM weather_queue;
-- +goose StatementEnd
-- +goose Down
-- +goose StatementBegin
DROP TABLE IF EXISTS weather_view;
-- +goose StatementEnd
-- +goose StatementBegin
DROP TABLE IF EXISTS weather_queue;
-- +goose StatementEnd
-- +goose StatementBegin
DROP TABLE IF EXISTS weather;
-- +goose StatementEnd
