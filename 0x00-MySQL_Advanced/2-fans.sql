-- SQL script that ranks country origins of bands, ordered by the number of (non-unique) fans

SELECT origin, SUM(fans) as fans_nb
FROM metal_bands
GROUP BY origin
ORDER BY fans_nb DESC
