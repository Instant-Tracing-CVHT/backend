
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

create table if not exists contact_tracer.device_location (
		device_id varchar not null references contact_tracer.device(device_id),
		sample_date timestamp,
		location Point,
		accuracy float
);