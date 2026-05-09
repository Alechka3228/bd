CREATE TABLE IF NOT EXISTS graph (
    from_node INT,
    to_node INT
);


CREATE OR REPLACE FUNCTION dfs(start_node INT)
RETURNS TABLE(node INT) AS $$
DECLARE
    stack INT[] := ARRAY[start_node];
    visited INT[] := ARRAY[]::INT[];
    current INT;
BEGIN
    WHILE array_length(stack, 1) > 0 LOOP

        current := stack[array_length(stack, 1)];
        stack := stack[1:array_length(stack, 1) - 1];

        IF current = ANY(visited) THEN
            CONTINUE;
        END IF;

        visited := visited || current;
        node := current;
        RETURN NEXT;

        stack := stack || ARRAY(
            SELECT to_node
            FROM graph
            WHERE from_node = current
            ORDER BY to_node DESC
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
    SELECT * FROM dfs(1)
)
SELECT 
    CASE 
        WHEN COUNT(*) = 5
         AND BOOL_AND(node IN (1,2,3,4,5))
        THEN 'DFS OK'
        ELSE 'DFS FAIL'
    END AS test_result
FROM result;

ROLLBACK;