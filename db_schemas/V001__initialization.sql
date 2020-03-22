
CREATE schema if not exists contact_tracer;
CREATE extension if not exists postgis;


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
		location geometry,
		accuracy float
);

create index location_device_time on contact_tracer.device_location(device_id,sample_date);
create index location_location on contact_tracer.device_location using gist(location);
