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

-- 2
WITH zagr as (
    SELECT ROUND(COUNT(p.id)::NUMERIC / ra.capacity, 2) AS "Загруженность",
    ra.id FROM rooms r 
    JOIN racks ra ON ra.room_id = r.id
    JOIN storages s ON s.shelf_id = ra.id
    JOIN products p ON p.storage_id = s.id
  GROUP BY ra.id
)

SELECT * FROM zagr;

-- 4
WITH to_change as (
  SELECT c.id FROM contracts c
  JOIN clients cl ON cl.id = c.client_id
  WHERE cl.client_name = 'ООО "Рога и копыта"'
)

UPDATE contracts
  SET expiry_date = expiry_date + INTERVAL '1 month'
  FROM to_change as tc
  WHERE contracts.id = tc.id
RETURNING *;
