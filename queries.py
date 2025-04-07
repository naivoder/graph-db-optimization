templates = [
    "MATCH (a:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(d:Person) "
    "WHERE {actor_clause} AND m.released IS NOT NULL AND d.born IS NOT NULL AND m.released > {year} "
    "WITH a, d, m, m.released - a.born AS age_at_release "
    "WHERE age_at_release > 30 "
    "RETURN a.name, m.title, d.name, age_at_release ORDER BY age_at_release DESC",
    "MATCH (m:Movie)<-[:ACTED_IN]-(a:Person), (m)<-[:DIRECTED]-(d:Person) "
    "WHERE m.released IS NOT NULL AND {actor_clause} AND d.name CONTAINS 'e' AND m.released < {year2} "
    "RETURN m.title, collect(DISTINCT a.name) AS cast, d.name ORDER BY size(cast) DESC",
    "MATCH (a:Person)-[:ACTED_IN]->(m:Movie) "
    "WHERE {actor_clause} AND a.born IS NOT NULL AND m.released IS NOT NULL AND m.released >= {year} "
    "WITH a.name AS actor, count(m) AS total, avg(m.released - a.born) AS avg_gap "
    "WHERE total > 2 "
    "RETURN actor, total, avg_gap ORDER BY avg_gap DESC",
    "MATCH (d:Person)-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(a:Person) "
    "WHERE {title_clause} AND d.born IS NOT NULL AND a.born IS NOT NULL AND m.released < {year2} "
    "RETURN m.title, d.name, a.name, m.released - d.born AS d_gap, m.released - a.born AS a_gap",
    "MATCH (m:Movie)<-[:ACTED_IN]-(a:Person) "
    "WHERE m.released >= {year} AND m.released IS NOT NULL AND a.born IS NOT NULL AND {title_clause} "
    "WITH m.title AS movie, collect(a.name) AS cast, avg(m.released - a.born) AS avg_age "
    "RETURN movie, cast, avg_age ORDER BY avg_age DESC",
    "MATCH (a:Person)-[:ACTED_IN]->(m:Movie), (d:Person)-[:DIRECTED]->(m) "
    "WHERE m.released >= {year} AND m.released <= {year2} AND a.born IS NOT NULL AND d.born IS NOT NULL AND {title_clause} "
    "WITH a, d, m "
    "RETURN a.name, d.name, m.title ORDER BY m.released",
    "MATCH (m:Movie)<-[:ACTED_IN]-(a:Person) "
    "WHERE m.title STARTS WITH 'The' AND a.born IS NOT NULL AND {actor_clause} AND m.released >= {year} "
    "RETURN m.title, a.name, m.released ORDER BY m.released DESC",
    "MATCH (a:Person)-[:ACTED_IN]->(m:Movie) "
    "WHERE {actor_clause} AND m.tagline IS NOT NULL AND m.released IS NOT NULL AND m.released < {year2} "
    "RETURN a.name, m.title, m.tagline, m.released",
    "MATCH (a:Person)-[:ACTED_IN]->(m:Movie) "
    "WITH a.name AS actor, collect(m.title) AS films, count(*) AS num "
    "WHERE num > 2 AND actor = '{actor}' "
    "RETURN actor, films, num ORDER BY num DESC",
    "MATCH (a:Person)-[:ACTED_IN]->(m:Movie) "
    "WHERE m.released IS NOT NULL AND {actor_clause} AND m.released >= {year} AND m.released <= {year2} "
    "WITH m.title AS movie, count(DISTINCT a.name) AS cast_size "
    "RETURN movie, cast_size ORDER BY cast_size DESC",
    "MATCH (m:Movie)<-[:ACTED_IN]-(a:Person)-[:DIRECTED]->(m2:Movie) "
    "WHERE m.released IS NOT NULL AND m2.released IS NOT NULL AND {title_clause} "
    "RETURN a.name, m.title, m2.title, m.released, m2.released",
    "MATCH (a:Person)-[:ACTED_IN]->(m:Movie) "
    "WHERE {actor_clause} AND a.born IS NOT NULL AND m.released IS NOT NULL AND m.released >= {year} "
    "RETURN a.name, m.title, m.released - a.born AS age_at_release ORDER BY age_at_release",
    "MATCH (a:Person)-[:DIRECTED]->(m:Movie) "
    "WHERE {actor_clause} AND a.born IS NOT NULL AND m.released IS NOT NULL AND m.released < {year2} "
    "RETURN a.name, m.title, m.released - a.born AS dir_age ORDER BY dir_age DESC",
    "MATCH (a:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(d:Person) "
    "WHERE {actor_clause} AND d.name IS NOT NULL "
    "RETURN a.name, d.name, m.title ORDER BY m.title",
    "MATCH (m:Movie)<-[:ACTED_IN]-(a:Person) "
    "WHERE m.released IS NOT NULL AND {title_clause} "
    "WITH m, count(a) AS cast_size "
    "RETURN m.title, cast_size ORDER BY cast_size DESC",
    "MATCH (a:Person)-[:ACTED_IN]->(m:Movie), (a)-[:DIRECTED]->(m2:Movie) "
    "WHERE m.released >= {year} AND m2.released IS NOT NULL AND {actor_clause} "
    "RETURN a.name, m.title AS acted_in, m2.title AS directed",
    "MATCH (a:Person)-[:ACTED_IN]->(m:Movie) "
    "WHERE {actor_clause} AND {title_clause} AND m.released IS NOT NULL AND m.released > {year} "
    "RETURN a.name, m.title, m.released ORDER BY m.released",
    "MATCH (m:Movie) "
    "WHERE m.released IS NOT NULL AND {title_clause} AND m.released >= {year} AND m.tagline IS NOT NULL "
    "RETURN m.title, m.released, m.tagline ORDER BY m.released DESC",
    "MATCH (a:Person) "
    "WHERE {actor_clause} AND a.born IS NOT NULL "
    "RETURN a.name, a.born ORDER BY a.born DESC",
    "MATCH (a:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(d:Person) "
    "WHERE {actor_clause} AND d.born IS NOT NULL AND m.released IS NOT NULL AND m.released > {year} "
    "WITH a, d, m, m.released - a.born AS act_age, m.released - d.born AS dir_age "
    "RETURN a.name, d.name, m.title, act_age, dir_age",
]
