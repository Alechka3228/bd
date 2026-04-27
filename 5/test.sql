-- ============================================================
-- ТЕСТ 1: Триггер check_rack_capacity (BEFORE INSERT)
-- ============================================================

-- Создаем стеллаж с capacity=1
INSERT INTO Racks (room_id, capacity, max_weight, client_id) VALUES (1, 1, 1000, NULL);
-- Добавляем ячейку 1
INSERT INTO Storages (shelf_id, type) VALUES ((SELECT max(id) FROM Racks), 1);
-- Добавляем ячейку 2 на тот же стеллаж
INSERT INTO Storages (shelf_id, type) VALUES ((SELECT max(id) FROM Racks), 1);
-- Добавляем товар в ячейку 1 - должен пройти
INSERT INTO Products (name, height, width, length, contract_id, storage_id, weight, receipt_date) 
VALUES ('Товар1', 0.5, 0.5, 0.5, 1, (SELECT id FROM Storages WHERE shelf_id = (SELECT max(id) FROM Racks) ORDER BY id LIMIT 1), 10, CURRENT_DATE);
-- Добавляем товар в ячейку 2 - должен заблокироваться (steллаж capacity=1)
INSERT INTO Products (name, height, width, length, contract_id, storage_id, weight, receipt_date) 
VALUES ('Товар2', 0.5, 0.5, 0.5, 1, (SELECT id FROM Storages WHERE shelf_id = (SELECT max(id) FROM Racks) ORDER BY id DESC LIMIT 1), 10, CURRENT_DATE);

-- Очистка теста 1
DELETE FROM Products WHERE name = 'Товар1';
DELETE FROM Storages WHERE shelf_id = (SELECT id FROM Racks WHERE capacity = 1 ORDER BY id DESC LIMIT 1);
DELETE FROM Racks WHERE capacity = 1;

-- ============================================================
-- ТЕСТ 2: Триггер check_rack_capacity (BEFORE UPDATE OF storage_id)
-- ============================================================

-- Создаем стеллаж A с capacity=1
INSERT INTO Racks (room_id, capacity, max_weight, client_id) VALUES (1, 1, 1000, NULL);
-- Создаем стеллаж B с capacity=1
INSERT INTO Racks (room_id, capacity, max_weight, client_id) VALUES (1, 1, 1000, NULL);
-- Добавляем ячейку на стеллаж A
INSERT INTO Storages (shelf_id, type) VALUES ((SELECT id FROM Racks ORDER BY id DESC LIMIT 1 OFFSET 1), 1);
-- Добавляем ячейку на стеллаж B
INSERT INTO Storages (shelf_id, type) VALUES ((SELECT id FROM Racks ORDER BY id DESC LIMIT 1), 1);
-- Добавляем товар в ячейку на стеллаже A
INSERT INTO Products (name, height, width, length, contract_id, storage_id, weight, receipt_date) 
VALUES ('Товар3', 0.5, 0.5, 0.5, 1, (SELECT id FROM Storages WHERE shelf_id IN (SELECT id FROM Racks ORDER BY id DESC LIMIT 1 OFFSET 1) LIMIT 1), 10, CURRENT_DATE);
-- Обновляем: перемещаем товар на стеллаж B (свободен, capacity=1) - должно пройти
UPDATE Products SET storage_id = (SELECT id FROM Storages WHERE shelf_id = (SELECT id FROM Racks ORDER BY id DESC LIMIT 1) LIMIT 1) 
WHERE name = 'Товар3';
-- Обновляем: пытаемся переместить обратно на стеллаж A (уже занят, capacity=1) - должно заблокироваться
UPDATE Products SET storage_id = (SELECT id FROM Storages WHERE shelf_id IN (SELECT id FROM Racks ORDER BY id DESC LIMIT 1 OFFSET 1) LIMIT 1) 
WHERE name = 'Товар3';

-- Очистка теста 2
DELETE FROM Products WHERE name = 'Товар3';
DELETE FROM Storages WHERE shelf_id IN (SELECT id FROM Racks WHERE capacity = 1 ORDER BY id DESC LIMIT 2);
DELETE FROM Racks WHERE capacity = 1я;

-- ============================================================
-- ТЕСТ 3: Триггер check_rack_max_weight (BEFORE UPDATE OF max_weight)
-- ============================================================

-- Уменьшаем max_weight ниже текущего веса товаров (на rack 2 вес = 30) - должно заблокироваться
UPDATE Racks SET max_weight = 25 WHERE id = 2;
-- Уменьшаем max_weight ровно до текущего веса - должно пройти
UPDATE Racks SET max_weight = 30 WHERE id = 2;
-- Увеличиваем max_weight - должно пройти
UPDATE Racks SET max_weight = 6000 WHERE id = 2;

-- ============================================================
-- ТЕСТ 4: Функция count_expiring_products
-- ============================================================

SELECT count_expiring_products('ООО "Рога и копыта"', '2026-05-01');
SELECT count_expiring_products('АО "Фрукт-Трейд"', '2026-06-15');
SELECT count_expiring_products('Несуществующий клиент', '2026-12-31');

-- ============================================================
-- ТЕСТ 5: Агрегат max_dimensions
-- ============================================================

SELECT max_dimensions(height, width, length) AS global_max FROM Products;
SELECT contract_id, max_dimensions(height, width, length) AS per_contract_max FROM Products GROUP BY contract_id ORDER BY contract_id;

-- ============================================================
-- ТЕСТ 6: Триггер update_client_through_view (INSTEAD OF UPDATE)
-- ============================================================

-- Обновляем клиента с существующими товарами
UPDATE client_products SET client_name = 'Новое имя1', bak_requisites = 'Новые реквизиты1' WHERE client_id = 1;
SELECT * FROM Clients WHERE id = 1;
UPDATE Clients SET client_name = 'ООО "Рога и копыта"', bak_requisites = 'ИНН 1234567890, КПП 123456001, р/с 40702810123456789012' WHERE id = 1;

-- Обновляем только имя
UPDATE client_products SET client_name = 'Новое имя2' WHERE client_id = 2;
SELECT * FROM Clients WHERE id = 2;
UPDATE Clients SET client_name = 'АО "Фрукт-Трейд"' WHERE id = 2;

-- Обновляем только реквизиты
UPDATE client_products SET bak_requisites = 'Новые реквизиты3' WHERE client_id = 3;
SELECT * FROM Clients WHERE id = 3;
UPDATE Clients SET bak_requisites = 'ИНН 4561237890, р/с 40802810456789123456' WHERE id = 3;

-- Обновляем клиента без товаров (product_id IS NULL)
UPDATE client_products SET client_name = 'Новое имя5' WHERE client_id = 5 AND product_id IS NULL;
SELECT * FROM Clients WHERE id = 5;
UPDATE Clients SET client_name = 'ООО "Рыбный мир"' WHERE id = 5;

-- ============================================================
-- ТЕСТ 7: Функции очереди
-- ============================================================

SELECT init_queue();
SELECT enqueue('Первый');
SELECT enqueue('Второй');
SELECT enqueue('Третий');
SELECT tail();
SELECT dequeue();
SELECT dequeue();
SELECT tail();
SELECT empty();
SELECT dequeue();
SELECT init_queue();
SELECT enqueue('Новая очередь');
SELECT tail();
SELECT empty();