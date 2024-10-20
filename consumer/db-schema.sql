create table readings (
    sensor_id bigint not null,
    ts timestamp with time zone not null,
    temperature decimal(4,2),
    humidity decimal(4,2)
);

create unique index on readings (sensor_id, ts);

SELECT create_hypertable('readings', by_range('ts', INTERVAL '1 week'));