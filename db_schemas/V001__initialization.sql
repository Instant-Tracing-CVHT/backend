
CREATE schema if not exists contact_tracer;
drop extension postgis cascade;
CREATE SCHEMA postgis;
CREATE EXTENSION postgis WITH SCHEMA postgis;
ALTER DATABASE contact_tracer SET search_path TO public, contact_tracer, postgis;


create table if not exists contact_tracer.device (
	device_id varchar not null unique primary key,
	first_sample timestamp,
	latest_sample timestamp,
	infected bool not null default false,
	notification_sent bool not null default false,
	infected_date timestamp null
);

drop table contact_tracer.device_location;
create table if not exists contact_tracer.device_location (
		device_id varchar not null references contact_tracer.device(device_id),
		sample_date timestamp,
		location postgis.geometry,
		accuracy float
);

create index location_device_time on contact_tracer.device_location(device_id,sample_date);
create index location_location on contact_tracer.device_location using gist(location);



create table if not exists contact_tracer.device_risk (
 device_id varchar not null references contact_tracer.device(device_id),
 last_calculated timestamp,
 score float,
 unique(device_id)
);
