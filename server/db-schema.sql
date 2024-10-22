create table readings (
    sensor_id bigint not null,
    ts timestamp with time zone not null,
    temperature decimal(5,2),
    humidity decimal(5,2)
);

create unique index on readings (sensor_id, ts);

select create_hypertable('readings', by_range('ts', interval '1 week'));