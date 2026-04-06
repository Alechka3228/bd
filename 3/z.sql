-- 0
SELECT sum(p.weight) FROM rooms r 
  JOIN racks ra ON ra.room_id = r.id
  JOIN storages s ON s.shelf_id = ra.id
  JOIN products p ON p.storage_id = s.id
