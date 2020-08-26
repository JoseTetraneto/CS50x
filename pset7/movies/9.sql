SELECT DISTINCT(name), birth FROM movies JOIN (people JOIN stars ON people.id = stars.person_id) ON movies.id = stars.movie_id WHERE year = 2004 ORDER BY birth DESC;