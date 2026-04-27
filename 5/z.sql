-- 0
CREATE OR REPLACE FUNCTION check_rack_capacity()
RETURNS TRIGGER AS $$
DECLARE
    rack_id_new INTEGER;
    rack_capacity INTEGER;
    current_items INTEGER;
BEGIN
    SELECT shelf_id INTO rack_id_new FROM Storages WHERE id = NEW.storage_id;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Ячейка хранения с id=% не существует', NEW.storage_id;
    END IF;
    
    SELECT capacity INTO rack_capacity FROM Racks WHERE id = rack_id_new;
    
    IF TG_OP = 'INSERT' THEN
        SELECT COUNT(*) INTO current_items
        FROM Products p
        JOIN Storages s ON p.storage_id = s.id
        WHERE s.shelf_id = rack_id_new;
    ELSE
        IF OLD.storage_id = NEW.storage_id THEN
            RETURN NEW;
        END IF;
        SELECT COUNT(*) INTO current_items
        FROM Products p
        JOIN Storages s ON p.storage_id = s.id
        WHERE s.shelf_id = rack_id_new AND p.id != NEW.id;
    END IF;
    
    IF current_items + 1 > rack_capacity THEN
        RAISE EXCEPTION 'Невозможно добавить товар: на стеллаже % уже занято % из % мест', 
                        rack_id_new, current_items, rack_capacity;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_products_check_capacity
    BEFORE INSERT OR UPDATE OF storage_id ON Products
    FOR EACH ROW
    EXECUTE FUNCTION check_rack_capacity();

CREATE OR REPLACE FUNCTION check_rack_max_weight()
RETURNS TRIGGER AS $$
DECLARE
    total_weight NUMERIC;
BEGIN
    SELECT COALESCE(SUM(p.weight), 0) INTO total_weight
    FROM Products p
    JOIN Storages s ON p.storage_id = s.id
    WHERE s.shelf_id = OLD.id;
    
    IF NEW.max_weight < total_weight THEN
        RAISE EXCEPTION 'Невозможно уменьшить максимальную нагрузку стеллажа % до %, так как суммарный вес товаров на нём составляет %', 
                        OLD.id, NEW.max_weight, total_weight;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_racks_check_max_weight
    BEFORE UPDATE OF max_weight ON Racks
    FOR EACH ROW
    EXECUTE FUNCTION check_rack_max_weight();

-- 1
CREATE OR REPLACE FUNCTION count_expiring_products(
    p_client_name VARCHAR,
    p_date DATE
) RETURNS INTEGER AS $$
DECLARE
    result_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO result_count
    FROM Products pr
    JOIN Contracts c ON pr.contract_id = c.id
    JOIN Clients cl ON c.client_id = cl.id
    WHERE cl.client_name = p_client_name
      AND c.expiry_date < p_date;
    
    RETURN result_count;
END;
$$ LANGUAGE plpgsql;

-- 2
CREATE TYPE max_dims_state AS (
    max_h NUMERIC,
    max_w NUMERIC,
    max_l NUMERIC
);

CREATE OR REPLACE FUNCTION max_dims_transition(
    state max_dims_state,
    height NUMERIC,
    width NUMERIC,
    length NUMERIC
) RETURNS max_dims_state AS $$
BEGIN
    IF state IS NULL THEN
        state := ROW(height, width, length);
    ELSE
        IF height > state.max_h THEN state.max_h := height; END IF;
        IF width  > state.max_w THEN state.max_w := width; END IF;
        IF length > state.max_l THEN state.max_l := length; END IF;
    END IF;
    RETURN state;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION max_dims_final(state max_dims_state)
RETURNS TEXT AS $$
BEGIN
    IF state IS NULL THEN
        RETURN NULL;
    END IF;
    RETURN format('%s X %s X %s', state.max_h, state.max_w, state.max_l);
END;
$$ LANGUAGE plpgsql;

CREATE AGGREGATE max_dimensions(NUMERIC, NUMERIC, NUMERIC) (
    SFUNC = max_dims_transition,
    STYPE = max_dims_state,
    FINALFUNC = max_dims_final
);

-- 3
CREATE OR REPLACE VIEW client_products AS
SELECT 
    c.id AS client_id,
    c.client_name,
    c.bak_requisites,
    p.id AS product_id,
    p.name AS product_name,
    p.weight,
    p.receipt_date,
    ct.expiry_date AS contract_expiry
FROM Clients c
LEFT JOIN Contracts ct ON c.id = ct.client_id
LEFT JOIN Products p ON p.contract_id = ct.id;

CREATE OR REPLACE FUNCTION update_client_through_view()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Clients
    SET
        client_name = COALESCE(NEW.client_name, OLD.client_name),
        bak_requisites = COALESCE(NEW.bak_requisites, OLD.bak_requisites)
    WHERE id = OLD.client_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_client_products_update
    INSTEAD OF UPDATE ON client_products
    FOR EACH ROW
    EXECUTE FUNCTION update_client_through_view();

-- 4
-- Инициализация: удаляет старую таблицу и создаёт новую
CREATE OR REPLACE FUNCTION init_queue()
RETURNS VOID AS $$
BEGIN
    DROP TABLE IF EXISTS queue_data;
    CREATE TABLE queue_data (
        id SERIAL PRIMARY KEY,
        data VARCHAR(64) NOT NULL
    );
END;
$$ LANGUAGE plpgsql;

-- Добавление элемента в конец очереди
CREATE OR REPLACE FUNCTION enqueue(str VARCHAR)
RETURNS VARCHAR AS $$
DECLARE
    trimmed VARCHAR(64);
BEGIN
    trimmed := LEFT(str, 64);
    INSERT INTO queue_data (data) VALUES (trimmed);
    RETURN trimmed;
END;
$$ LANGUAGE plpgsql;

-- Удаление элемента из начала очереди
CREATE OR REPLACE FUNCTION dequeue()
RETURNS VARCHAR AS $$
DECLARE
    first_id INT;
    result_data VARCHAR(64);
BEGIN
    SELECT id INTO first_id FROM queue_data ORDER BY id ASC LIMIT 1;
    IF NOT FOUND THEN
        RETURN NULL;
    END IF;
    
    SELECT data INTO result_data FROM queue_data WHERE id = first_id;
    DELETE FROM queue_data WHERE id = first_id;
    RETURN result_data;
END;
$$ LANGUAGE plpgsql;

-- Очистка очереди
CREATE OR REPLACE FUNCTION empty()
RETURNS INT AS $$
DECLARE
    deleted_count INT;
BEGIN
    WITH deleted AS (DELETE FROM queue_data RETURNING *)
    SELECT COUNT(*) INTO deleted_count FROM deleted;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Просмотр конца очереди 
CREATE OR REPLACE FUNCTION tail()
RETURNS VARCHAR AS $$
DECLARE
    last_data VARCHAR(64);
BEGIN
    SELECT data INTO last_data FROM queue_data ORDER BY id DESC LIMIT 1;
    RETURN last_data;
END;
$$ LANGUAGE plpgsql;

-- Использование
SELECT init_queue();

SELECT enqueue('Первый элемент');
SELECT enqueue('Второй очень длинный элемент, который будет обрезан до 64 символов');
SELECT enqueue('Третий');

SELECT tail();

SELECT dequeue();
SELECT dequeue();

SELECT empty();

SELECT dequeue();
SELECT tail();

SELECT init_queue();
SELECT enqueue('Новая очередь');
SELECT tail();