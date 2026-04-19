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
