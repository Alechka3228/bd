-- 0
SELECT sum(p.weight) FROM rooms r 
  JOIN racks ra ON ra.room_id = r.id
  JOIN storages s ON s.shelf_id = ra.id
  JOIN products p ON p.storage_id = s.id;

-- 1
WITH cl_sh as (
  SELECT sum(p.height * p.width * p.length), c.client_id FROM rooms r 
    JOIN racks ra ON ra.room_id = r.id
    JOIN storages s ON s.shelf_id = ra.id
    JOIN products p ON p.storage_id = s.id
    JOIN contracts c ON c.client_id = p.contract_id
    GROUP BY c.client_id
)

SELECT * FROM cl_sh
LIMIT 3;
