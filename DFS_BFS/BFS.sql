CREATE TABLE IF NOT EXISTS graph (
    from_node INT,
    to_node INT
);


CREATE OR REPLACE FUNCTION bfs(start_node INT)
RETURNS TABLE(node INT, level INT) AS $$
DECLARE
    queue INT[] := ARRAY[start_node];
    levels INT[] := ARRAY[0];
    current INT;
    current_level INT;
BEGIN
    WHILE array_length(queue, 1) > 0 LOOP

        current := queue[1];
        current_level := levels[1];

        queue := queue[2:array_length(queue, 1)];
        levels := levels[2:array_length(levels, 1)];

        node := current;
        level := current_level;
        RETURN NEXT;

        queue := queue || ARRAY(
            SELECT to_node
            FROM graph
            WHERE from_node = current
            ORDER BY to_node
        );

        levels := levels || ARRAY(
            SELECT current_level + 1
            FROM graph
            WHERE from_node = current
        );

    END LOOP;
END;
$$ LANGUAGE plpgsql;


BEGIN;

TRUNCATE graph;

INSERT INTO graph VALUES
(1,2),
(1,3),
(2,4),
(3,5);

WITH result AS (
    SELECT * FROM bfs(1)
)
SELECT
    CASE
        WHEN COUNT(*) = 5
         AND MAX(level) = 2
         AND BOOL_AND(node IN (1,2,3,4,5))
        THEN 'BFS OK'
        ELSE 'BFS FAIL'
    END AS test_result
FROM result;

ROLLBACK;
