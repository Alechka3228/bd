-- 0
SELECT DISTINCT
    r.id AS rack_number,
    ro.room_name,
    ROUND(SUM(p.weight) OVER (PARTITION BY r.id), 2) AS total_weight_on_rack,
    ROUND(AVG(p.weight) OVER (PARTITION BY r.room_id), 2) AS avg_weight_in_room
FROM Racks r
JOIN Rooms ro ON r.room_id = ro.id
JOIN Storages s ON s.shelf_id = r.id
JOIN Products p ON p.storage_id = s.id
ORDER BY r.id;


-- 1
SELECT 
    ro.room_name,
    STRING_AGG(DISTINCT c.bak_requisites, ', ') AS client_addresses
FROM Rooms ro
JOIN Racks r ON r.room_id = ro.id
JOIN Storages s ON s.shelf_id = r.id
JOIN Products p ON p.storage_id = s.id
JOIN Contracts ct ON p.contract_id = ct.id
JOIN Clients c ON ct.client_id = c.id
GROUP BY ro.id, ro.room_name
ORDER BY ro.room_name;
