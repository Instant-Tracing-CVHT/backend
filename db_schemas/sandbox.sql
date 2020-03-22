
insert into contact_tracer.device (device_id ,first_sample ,latest_sample)
values ('device1', now(),now()),('device2', now(),now()),('device3', now(),now())
  

SELECT * FROM contact_tracer.device;


truncate contact_tracer.device_location ;
INSERT INTO contact_tracer.device_location (device_id,sample_date,location) VALUES 
('device1', now(), Point(29.733521,-95.388815)),
('device1', now() - interval '2 hours', Point(29.733730, -95.387850)),
('device1', now() - interval '3 hours', Point(29.734117, -95.387850)),
('device1', now() - interval '4 hours', Point(29.734410, -95.388113)),
('device2', now() - interval '2 hours', Point(29.7344752,-95.3882035)),
('device3', now() - interval '3 days', Point(29.7344752,-95.3882035));




--device1's user is infected, look at his history for the past 14 days (incubation period) 
-- for each reported location of device1, find the devices that were near him at that time

select dl.*,dl3.device_id, dl3.sample_date from contact_tracer.device_location dl
left join lateral (select * from contact_tracer.device_location dl2 where ST_DistanceSphere(dl.location,dl2.location) < 50) dl3
on true 
where device_id  = 'device1'
and sample_date > now() - interval '14 days';