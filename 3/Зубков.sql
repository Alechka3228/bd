DROP TABLE IF EXISTS Products CASCADE;
DROP TABLE IF EXISTS Contracts CASCADE;
DROP TABLE IF EXISTS Storages CASCADE;
DROP TABLE IF EXISTS Storages_types CASCADE;
DROP TABLE IF EXISTS Racks CASCADE;
DROP TABLE IF EXISTS Clients CASCADE;
DROP TABLE IF EXISTS Rooms CASCADE;

-- ============================================================
-- Таблица помещений
-- ============================================================
CREATE TABLE Rooms
(
  id serial,
  room_name character varying(128) NOT NULL,
  volume numeric NOT NULL DEFAULT 1,
  min_temp numeric NOT NULL DEFAULT -30,
  max_temp numeric NOT NULL DEFAULT 30,
  min_humid numeric NOT NULL DEFAULT 0,
  max_humid numeric NOT NULL DEFAULT 100,
  PRIMARY KEY (id),
  CONSTRAINT chk_room_volume_positive CHECK (volume > 0),
  CONSTRAINT chk_room_temp_range CHECK (min_temp <= max_temp),
  CONSTRAINT chk_room_humid_range CHECK (min_humid <= max_humid),
  CONSTRAINT chk_room_temp_bounds CHECK (min_temp >= -50 AND max_temp <= 60),
  CONSTRAINT chk_room_humid_bounds CHECK (min_humid >= 0 AND max_humid <= 100)
);

-- ============================================================
-- Таблица стеллажей
-- ============================================================
CREATE TABLE Racks
(
  id serial,
  room_id integer NOT NULL,
  capacity integer NOT NULL,
  max_weight numeric NOT NULL,
  client_id integer,
  PRIMARY KEY (id),
  CONSTRAINT chk_rack_capacity_positive CHECK (capacity > 0),
  CONSTRAINT chk_rack_max_weight_positive CHECK (max_weight > 0)
);

-- ============================================================
-- Таблица типов ячеек
-- ============================================================
CREATE TABLE Storages_types
(
  id serial,
  height numeric NOT NULL,
  width numeric NOT NULL,
  lenght numeric NOT NULL,
  max_weight numeric NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT chk_storage_type_dimensions_positive CHECK (height > 0 AND width > 0 AND lenght > 0),
  CONSTRAINT chk_storage_type_max_weight_positive CHECK (max_weight > 0)
);

-- ============================================================
-- Таблица ячеек хранения
-- ============================================================
CREATE TABLE Storages
(
  id serial,
  shelf_id integer NOT NULL,
  type integer NOT NULL,
  PRIMARY KEY (id)
);

-- ============================================================
-- Таблица клиентов
-- ============================================================
CREATE TABLE Clients
(
  id serial,
  client_name character varying NOT NULL,
  bak_requisites character varying NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT chk_client_name_not_empty CHECK (client_name <> ''),
  CONSTRAINT chk_client_requisites_not_empty CHECK (bak_requisites <> '')
);

-- ============================================================
-- Таблица контрактов (исправлен тип expiry_date)
-- ============================================================
CREATE TABLE Contracts
(
  id serial,
  client_id integer NOT NULL,
  expiry_date date NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT chk_contract_expiry_future CHECK (expiry_date > CURRENT_DATE)
);

-- ============================================================
-- Таблица товаров (исправлен тип receipt_date)
-- ============================================================
CREATE TABLE Products
(
  id serial,
  name character varying NOT NULL,
  height numeric NOT NULL,
  width numeric NOT NULL,
  length numeric NOT NULL,
  contract_id integer NOT NULL,
  storage_id integer NOT NULL,
  max_temp numeric,
  min_temp numeric,
  max_humid numeric,
  min_humid numeric,
  weight numeric NOT NULL,
  receipt_date date NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT chk_product_dimensions_positive CHECK (height > 0 AND width > 0 AND length > 0),
  CONSTRAINT chk_product_weight_positive CHECK (weight > 0),
  CONSTRAINT chk_product_temp_range CHECK (min_temp IS NULL OR max_temp IS NULL OR min_temp <= max_temp),
  CONSTRAINT chk_product_humid_range CHECK (min_humid IS NULL OR max_humid IS NULL OR min_humid <= max_humid),
  CONSTRAINT chk_product_temp_bounds CHECK (
    (min_temp IS NULL OR min_temp >= -50) AND 
    (max_temp IS NULL OR max_temp <= 60)
  ),
  CONSTRAINT chk_product_humid_bounds CHECK (
    (min_humid IS NULL OR min_humid >= 0) AND 
    (max_humid IS NULL OR max_humid <= 100)
  ),
  CONSTRAINT chk_product_receipt_date_valid CHECK (receipt_date <= CURRENT_DATE)
);

-- ============================================================
-- Внешние ключи
-- ============================================================
ALTER TABLE Racks
ADD CONSTRAINT fk_racks_room FOREIGN KEY (room_id)
REFERENCES Rooms (id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE Racks
ADD CONSTRAINT fk_racks_client FOREIGN KEY (client_id)
REFERENCES Clients (id) ON UPDATE CASCADE ON DELETE SET NULL;

ALTER TABLE Storages
ADD CONSTRAINT fk_storages_shelf FOREIGN KEY (shelf_id)
REFERENCES Racks (id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE Storages
ADD CONSTRAINT fk_storages_type FOREIGN KEY (type)
REFERENCES Storages_types (id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE Contracts
ADD CONSTRAINT fk_contracts_client FOREIGN KEY (client_id)
REFERENCES Clients (id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE Products
ADD CONSTRAINT fk_products_storage FOREIGN KEY (storage_id)
REFERENCES Storages (id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE Products
ADD CONSTRAINT fk_products_contract FOREIGN KEY (contract_id)
REFERENCES Contracts (id) ON UPDATE CASCADE ON DELETE RESTRICT;

ALTER TABLE Products
ADD CONSTRAINT uk_products_storage UNIQUE (storage_id);

-- ============================================================
-- 1. Заполнение помещений (Rooms)
-- ============================================================
INSERT INTO Rooms (room_name, volume, min_temp, max_temp, min_humid, max_humid) VALUES
('Сухой склад А', 1500.0, 15, 25, 30, 60),
('Холодильная камера B', 800.0, -20, 0, 70, 90),
('Морозильный отсек C', 600.0, -30, -18, 80, 95),
('Винный погреб D', 400.0, 10, 14, 50, 70),
('Овощехранилище E', 1200.0, 0, 8, 85, 95);

-- ============================================================
-- 2. Заполнение типов ячеек (Storages_types)
-- ============================================================
INSERT INTO Storages_types (height, width, lenght, max_weight) VALUES
(2.0, 1.2, 1.5, 500.0),
(1.8, 0.8, 1.2, 300.0),
(2.2, 1.5, 2.0, 1000.0),
(1.5, 0.6, 0.8, 150.0),
(2.5, 1.8, 2.2, 1200.0);

-- ============================================================
-- 3. Заполнение клиентов (Clients)
-- ============================================================
INSERT INTO Clients (client_name, bak_requisites) VALUES
('ООО "Северный ветер"', 'ИНН 1234567890, КПП 123456001, р/с 40702810123456789012'),
('АО "Фрукт-Трейд"', 'ИНН 9876543210, КПП 987654002, р/с 40702810987654321098'),
('ИП Петров И.И.', 'ИНН 4561237890, р/с 40802810456789123456'),
('ЗАО "Мясопродукт"', 'ИНН 1122334455, КПП 112233001, р/с 40702810765432109876'),
('ООО "Рыбный мир"', 'ИНН 5566778899, КПП 556677001, р/с 40702810234567890123');

-- ============================================================
-- 4. Заполнение стеллажей (Racks)
-- ============================================================
INSERT INTO Racks (room_id, capacity, max_weight, client_id) VALUES
(1, 20, 8000.0, NULL),
(1, 15, 6000.0, 1),
(2, 25, 5000.0, NULL),
(3, 30, 7000.0, 3),
(4, 10, 2000.0, 2);

-- ============================================================
-- 5. Заполнение контрактов (Contracts)
-- ============================================================
INSERT INTO Contracts (client_id, expiry_date) VALUES
(1, '2026-05-15'),
(2, '2026-06-01'),
(3, '2026-07-20'),
(4, '2026-08-01'),
(5, '2026-09-10');

-- ============================================================
-- 6. Заполнение ячеек хранения (Storages)
-- ============================================================
INSERT INTO Storages (shelf_id, type) VALUES
(1, 1),
(1, 2),
(1, 3),
(2, 1),
(2, 4),
(3, 2),
(3, 5),
(4, 1),
(4, 3),
(5, 4);

-- ============================================================
-- 7. Заполнение товаров (Products)
-- ============================================================
INSERT INTO Products (
  name, height, width, length, contract_id, storage_id,
  max_temp, min_temp, max_humid, min_humid, weight, receipt_date
) VALUES
('Филе трески замороженное', 0.3, 0.4, 0.5, 1, 1,
  -18, -25, 90, 80, 15.0, '2026-04-01'),

('Яблоки Голден', 0.5, 0.4, 0.6, 2, 4,
  4, 0, 85, 75, 20.0, '2026-04-05'),

('Говядина охлаждённая', 0.4, 0.5, 0.5, 3, 6,
  2, -2, 85, 75, 25.0, '2026-04-06'),

('Макароны твёрдых сортов', 0.2, 0.3, 0.4, 4, 2,
  25, 15, 60, 30, 10.0, '2026-03-28'),

('Каберне Совиньон', 0.35, 0.25, 0.25, 2, 9,
  14, 10, 70, 50, 1.5, '2026-04-03'),

('Креветки королевские', 0.2, 0.3, 0.4, 5, 7,
  -18, -20, 85, 80, 12.0, '2026-04-06');
