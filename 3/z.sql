BEGIN;
-- 0
SELECT sum(p.weight) FROM rooms r 
  JOIN racks ra ON ra.room_id = r.id
  JOIN storages s ON s.shelf_id = ra.id
  JOIN products p ON p.storage_id = s.id;

-- 1
WITH cl_sh AS (
  SELECT sum(p.height * p.width * p.length) AS total_volume, c.client_id 
  FROM rooms r 
    JOIN racks ra ON ra.room_id = r.id
    JOIN storages s ON s.shelf_id = ra.id
    JOIN products p ON p.storage_id = s.id
    JOIN contracts c ON c.client_id = p.contract_id
  GROUP BY c.client_id
)
SELECT * FROM cl_sh
LIMIT 3;

-- 2
WITH zagr AS (
  SELECT ROUND(COUNT(p.id)::NUMERIC / ra.capacity, 2) AS "Загруженность",
    ra.id 
  FROM rooms r 
    JOIN racks ra ON ra.room_id = r.id
    JOIN storages s ON s.shelf_id = ra.id
    JOIN products p ON p.storage_id = s.id
  GROUP BY ra.id, ra.capacity
)
SELECT * FROM zagr;

-- 3
WITH racks_to_delete AS (
  SELECT ra.id FROM racks ra
  WHERE ra.max_weight < 100
),
products_to_delete AS (
  SELECT p.id FROM products p
  JOIN storages s ON p.storage_id = s.id
  JOIN racks_to_delete rtd ON s.shelf_id = rtd.id
)
DELETE FROM products
WHERE id IN (SELECT id FROM products_to_delete);

-- 4
WITH to_change AS (
  SELECT c.id FROM contracts c
    JOIN clients cl ON cl.id = c.client_id
    WHERE cl.client_name = 'ООО "Рога и копыта"'
)
UPDATE contracts
SET expiry_date = expiry_date + INTERVAL '1 month'
FROM to_change AS tc
WHERE contracts.id = tc.id
RETURNING *;

-- 5
ALTER TABLE products
  ADD COLUMN IF NOT EXISTS
  fragility BOOLEAN DEFAULT FALSE;

-- 6
ALTER TABLE products
  ADD CONSTRAINT
  chk_product_weight_max CHECK (weight <= 500);
