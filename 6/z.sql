-- 0
SELECT DISTINCT
    r.id AS rack_number,
    rm.room_name,
    COALESCE(SUM(p.weight) OVER (PARTITION BY r.id), 0) AS total_weight_on_rack,
    ROUND(AVG(p.weight) OVER (PARTITION BY rm.id),2) AS avg_weight_in_room
FROM Racks r
JOIN Rooms rm ON r.room_id = rm.id
LEFT JOIN Storages s ON s.shelf_id = r.id
LEFT JOIN Products p ON p.storage_id = s.id;

-- 1
SELECT
    rm.room_name,
    STRING_AGG(DISTINCT c.bak_requisites, ', ' ORDER BY c.bak_requisites) AS client_legal_addresses
FROM Rooms rm
JOIN Racks r ON r.room_id = rm.id
JOIN Storages s ON s.shelf_id = r.id
JOIN Products p ON p.storage_id = s.id
JOIN Contracts ct ON ct.id = p.contract_id
JOIN Clients c ON c.id = ct.client_id
GROUP BY rm.id, rm.room_name;