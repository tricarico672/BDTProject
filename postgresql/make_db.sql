CREATE TABLE  trips (
	id BIGSERIAL,
	trip_id VARCHAR(50),
	route_id VARCHAR(50),
	direction_id BOOLEAN,
	total_travel_time_scheduled TIMESTAMP,
	shape_id  VARCHAR(50)
	);
