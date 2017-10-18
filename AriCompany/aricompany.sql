--
-- Ari company database structure, test data and queries
--

--
-- Create db, select db, create tables
--
CREATE DATABASE aridb;
\c aridb;

CREATE TABLE crew(ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, AGE INT NOT NULL);
CREATE TABLE aircraft(ID INT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL);
CREATE TABLE flight(ID INT PRIMARY KEY NOT NULL, AIRCRAFT_ID INT NOT NULL, CREW_MEMBERS_IDS INT[] NOT NULL);
\d crew
\d aircraft
\d flight

--
-- Add data to tables
--
INSERT INTO crew(id, name, age) VALUES (1, 'Ljudmila', 45);
INSERT INTO crew(id, name, age) VALUES (2, 'Olja', 23);
INSERT INTO crew(id, name, age) VALUES (3, 'Jovana', 18);
INSERT INTO crew(id, name, age) VALUES (4, 'Cecilija', 35);
INSERT INTO crew(id, name, age) VALUES (5, 'Aleksandra', 33);

INSERT INTO aircraft(id, name) VALUES (777, 'Americana');
INSERT INTO aircraft(id, name) VALUES (123, 'Tango');
INSERT INTO aircraft(id, name) VALUES (23, 'Juno');

INSERT INTO flight(id, aircraft_id, crew_members_ids) VALUES(1, 777, '{1, 2, 4, 5}');
INSERT INTO flight(id, aircraft_id, crew_members_ids) VALUES(2, 123, '{1, 2}');
INSERT INTO flight(id, aircraft_id, crew_members_ids) VALUES(3, 123, '{1}');
INSERT INTO flight(id, aircraft_id, crew_members_ids) VALUES(4, 23, '{1, 5}');
INSERT INTO flight(id, aircraft_id, crew_members_ids) VALUES(5, 777, '{4, 5}');

SELECT * FROM crew;
SELECT * FROM aircraft;
SELECT * FROM flight;

--
-- helper functions
--

-- for given name find nth crew member by age
CREATE FUNCTION nth_crew_by_age (integer)
RETURNS text AS $crew_name$
   DECLARE
      crew_name text;
   BEGIN
      SELECT name into crew_name FROM crew ORDER BY age DESC LIMIT 1 OFFSET ($1 - 1);
      RETURN crew_name;
   END;
   $crew_name$ LANGUAGE plpgsql;

-- for given crew id, find out in how many aircrafts he has been
CREATE FUNCTION get_num_of_aircraft (cid integer)
RETURNS integer AS $aircraft_num$
  DECLARE
     aircraft_num integer;
  BEGIN
     SELECT COUNT (*) INTO aircraft_num
     FROM(
       SELECT aircraft_id FROM flight WHERE crew_members_ids @> ARRAY[cid::int] GROUP BY aircraft_id
     ) AS aircraft_count;
     RETURN aircraft_num;
  END;
  $aircraft_num$ LANGUAGE plpgsql;

--
-- queries
--

--
-- Get name of oldest crew member
--
SELECT name FROM crew ORDER BY age DESC LIMIT 1;

--
-- Get name of n-th oldest crew member
--
SELECT nth_crew_by_age(5);
SELECT nth_crew_by_age(2);

--
-- Get name of most experienced crew member
--
SELECT crew.name, get_num_of_aircraft(crew.id) AS aircraft_num
FROM crew ORDER BY aircraft_num DESC LIMIT 1;

--
-- Get name of least experienced crew member
--
SELECT crew.name, get_num_of_aircraft(crew.id) AS aircraft_num
FROM crew ORDER BY aircraft_num LIMIT 1;

--
-- Delete db
--
\c postgres
DROP DATABASE aridb;

--
-- End
--
