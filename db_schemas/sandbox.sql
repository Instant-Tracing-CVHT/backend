
insert into contact_tracer.device (device_id ,first_sample ,latest_sample)
values 
('device1', now(),now()),
('device2', now(),now()),
('device3', now(),now())
 on conflict do nothing ; 

SELECT * FROM contact_tracer.device;


truncate contact_tracer.device_location ;
INSERT INTO contact_tracer.device_location (device_id,sample_date,location) VALUES 
('device1', now(), ST_MakePoint(29.733521,-95.388815)),
('device1', now() - interval '2 hours', ST_MakePoint(29.733730, -95.387850)),
('device1', now() - interval '3 hours', ST_MakePoint(29.734117, -95.387850)),
('device1', now() - interval '4 hours', ST_MakePoint(29.734410, -95.388113)),
('device2', now() - interval '2 hours', ST_MakePoint(29.7344752,-95.3882035)),
('device3', now() - interval '3 days', ST_MakePoint(29.7344752,-95.3882035));



CREATE FUNCTION abs(interval) RETURNS interval AS
  $$ select case when ($1<interval '0') then -$1 else $1 end; $$
LANGUAGE sql immutable;

--device1's user is infected, look at his history for the past 14 days (incubation period) 
-- for each reported location of device1, find the devices that were near him at that time


select ST_DistanceSphere(ST_MakePoint(37.842245, -122.261125),ST_MakePoint(37.842012, -122.261388))



select device_id from contact_tracer.device order by latest_sample desc;
select score from contact_tracer.device_risk where device_id = 'device1';

insert into contact_tracer.device_risk(device_id ,score ,last_calculated ) values
('device1',2,now()) on conflict(device_id) do update set score =EXCLUDED.score, last_calculated = EXCLUDED.last_calculated;


select distinct dl3.device_id as notifyDeviceId
from 
contact_tracer.device_location dl join lateral 
(select * from contact_tracer.device_location where device_id != dl.device_id and ST_DistanceSphere(location,dl.location) < 500
and abs(dl.sample_date - sample_date) <= interval '1 hour'
) dl3
on true 
where dl.device_id  = 'device1'
and dl.sample_date > now() - interval '14 days';