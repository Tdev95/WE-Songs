---------------- Artists ----------------
-- GET /artists
SELECT *
FROM artist;

-- GET /artists/{artistId}
SELECt *
FROM artist
WHERE id = artistId;

-- GET /artists?name=
SELECT *
FROM artist
WHERE name = _name;

-- GET /artists?genre=
SELECT *
FROM artists
WHERE terms = _genre;

-- GET /artists?name=&genre=
SELECT *
FROM artist
WHERE name = _name AND terms = _genre;

-- GET /artists?sort=hotttnesss
SELECT *
FROM artist
WHERE hotttnesss >= 0
ORDER BY hotttnesss;

-- GET /artists?sort=hotttnesss&subset=
SELECT *
FROM artist
ORDER BY hotttnesss
WHERE hotttnesss >= 0
LIMIT _subset;

---------------- Songs ----------------
-- GET /songs
SELECT *
FROM song;

-- GET /songs/{songId}
SELECT *
FROM song
WHERE id = songId

-- POST /songs
INSERT INTO song
VALUES (value1, value2, ...);

-- PUT /songs/{songId}
UPDATE song
SET col1 = value, col2 = value2, ...
WHERE id = songId;

-- DELETE /songs/{songId}
DELETE FROM song
WHERE id = songId;

-- GET /songs?sort=hotttnesss
SELECT *
FROM song
WHERE hotttnesss >= 0
ORDER BY hotttnesss;

-- GET /songs?sort=hotttnesss&subset=
SELECT *
FROM song
WHERE hotttnesss >= 0
ORDER BY hotttnesss
LIMIT _subset;

---------------- Statistics ----------------
-- NOTE: no actual calculations are done. It just returns the hotttnesss
-- GET /statistics/artistId=
SELECT hotttnesss
FROM song
WHERE artistId = _artistId

-- GET /statistics/artistId=&year=
SELECT hotttnesss
FROM song
WHERE artistId = _artistId AND year = _year

---------------- Genres ----------------
-- GET /genres
SELECT terms, COUNT(*)
FROM artist
GROUP BY terms;

-- GET /genres?threshold=
SELECT terms, COUNT(*)
FROM artist
GROUP BY terms
HAVING COUNT(*) >= _threshold;

---------------- Keys ----------------
-- GET /keys
SELECT key_in, COUNT(*)
FROM song
GROUP BY key_in
ORDER BY key_in;

-- GET /keys?genre=
SELECT key_in, COUNT(*)
FROM song JOIN artist ON song.artist_id = artist.id
WHERE terms = _terms
GROUP BY key_in
ORDER BY key_in;

-- GET /keys?threshold=
SELECT key_in, COUNT(*)
FROM song
WHERE hotttnesss > _threshold
GROUP BY key_in
ORDER BY key_in;

-- GET /keys?genre=&threshold=
SELECT key_in, COUNT(*)
FROM song JOIN artist ON song.artist_id = artist.id
WHERE terms = _terms & song.hotttnesss > _threshold
GROUP BY key_in
ORDER BY key_in;