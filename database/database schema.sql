CREATE SCHEMA IF NOT EXISTS webengineering;

CREATE TABLE IF NOT EXISTS artist (
	id VARCHAR(45),
	familiarity DOUBLE,
	hotttnesss DOUBLE,
	latitude DOUBLE,
	location INT,
	longitude DOUBLE,
	name TEXT,
	similar DOUBLE,
	terms TEXT,
	terms_freq DOUBLE,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS release_album (
	id INT,
	name INT,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS song (
	id VARCHAR(45),
	artist_id VARCHAR(45),
	release_id INT,
	artist_mbtags DOUBLE,
	artist_mbtags_count DOUBLE,
	bars_confidence DOUBLE,
	bars_start DOUBLE,
	beats_confidence DOUBLE,
	beats_start DOUBLE,
	duration DOUBLE,
	end_of_fade_in DOUBLE,
	hotttnesss DOUBLE,
	key_in DOUBLE,
	key_confidence DOUBLE,
	loudness DOUBLE,
	mode INT,
	mode_confidence DOUBLE,
	start_of_fade_out DOUBLE,
	tatums_confidence DOUBLE,
	tatums_start DOUBLE,
	tempo DOUBLE,
	time_signature DOUBLE,
	time_signature_confidence DOUBLE,
	title INT,
	year INT,
	PRIMARY KEY (id),
	FOREIGN KEY (artist_id) REFERENCES artist(id),
	FOREIGN KEY (release_id) REFERENCES release_album(id)	
);