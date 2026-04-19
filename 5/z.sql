-- 0
-- Вспомогательные функции для расчётов
CREATE OR REPLACE FUNCTION get_rack_id_by_storage(p_storage_id INTEGER)
RETURNS INTEGER AS $$
SELECT shelf_id FROM Storages WHERE id = p_storage_id;
$$ LANGUAGE sql STABLE;

CREATE OR REPLACE FUNCTION get_occupied_cells_count(p_rack_id INTEGER)
RETURNS INTEGER AS $$
SELECT COUNT(*) 
FROM Products p
JOIN Storages s ON p.storage_id = s.id
WHERE s.shelf_id = p_rack_id;
$$ LANGUAGE sql STABLE;

CREATE OR REPLACE FUNCTION get_total_weight_on_rack(p_rack_id INTEGER)
RETURNS NUMERIC AS $$
SELECT COALESCE(SUM(p.weight), 0)
FROM Products p
JOIN Storages s ON p.storage_id = s.id
WHERE s.shelf_id = p_rack_id;
$$ LANGUAGE sql STABLE;

-- Триггерная функция для Products (вставка, обновление)
CREATE OR REPLACE FUNCTION trg_products_check_rack()
RETURNS TRIGGER AS $$
DECLARE
v_rack_id INTEGER;
v_capacity INTEGER;
v_max_weight NUMERIC;
v_occupied INTEGER;
v_total_weight NUMERIC;
BEGIN
  -- При удалении ограничения не нужны
  IF TG_OP = 'DELETE' THEN
    RETURN OLD;
  END IF;

  -- Определяем ID стеллажа, на который ссылается товар
  SELECT shelf_id INTO v_rack_id
  FROM Storages WHERE id = NEW.storage_id;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'Ячейка с id=% не существует', NEW.storage_id;
  END IF;

  -- Получаем параметры стеллажа
  SELECT capacity, max_weight INTO v_capacity, v_max_weight
  FROM Racks WHERE id = v_rack_id;

  -- Проверка количества мест (только для INSERT и изменения storage_id)
  IF TG_OP = 'INSERT' OR (TG_OP = 'UPDATE' AND OLD.storage_id IS DISTINCT FROM NEW.storage_id) THEN
    v_occupied := get_occupied_cells_count(v_rack_id);
    -- При UPDATE нужно учесть, что старый товар уйдёт с прежнего стеллажа,
    -- но для нового стеллажа считаем занятые места включая текущую вставку/изменение
    IF v_occupied + 1 > v_capacity THEN
      RAISE EXCEPTION 'Стеллаж % переполнен: мест %, занято %', v_rack_id, v_capacity, v_occupied;
    END IF;
  END IF;

  -- Проверка веса при INSERT, UPDATE веса или смене стеллажа
  IF TG_OP = 'INSERT' OR 
      (TG_OP = 'UPDATE' AND (NEW.weight IS DISTINCT FROM OLD.weight OR 
                            NEW.storage_id IS DISTINCT FROM OLD.storage_id)) THEN
      v_total_weight := get_total_weight_on_rack(v_rack_id);
      -- При смене стеллажа или вставке добавляем текущий вес
      IF TG_OP = 'INSERT' OR (TG_OP = 'UPDATE' AND NEW.storage_id IS DISTINCT FROM OLD.storage_id) THEN
          IF v_total_weight + NEW.weight > v_max_weight THEN
              RAISE EXCEPTION 'Стеллаж % превышает максимальную нагрузку: лимит %, текущий вес с новым товаром %',
                              v_rack_id, v_max_weight, v_total_weight + NEW.weight;
          END IF;
      ELSE -- обновление веса на том же стеллаже
          IF v_total_weight - OLD.weight + NEW.weight > v_max_weight THEN
              RAISE EXCEPTION 'Стеллаж % превышает максимальную нагрузку: лимит %, новый общий вес %',
                              v_rack_id, v_max_weight, v_total_weight - OLD.weight + NEW.weight;
          END IF;
      END IF;
  END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для Products
DROP TRIGGER IF EXISTS trg_products_check_rack ON Products;
CREATE TRIGGER trg_products_check_rack
    BEFORE INSERT OR UPDATE OF storage_id, weight ON Products
    FOR EACH ROW EXECUTE FUNCTION trg_products_check_rack();

-- Триггерная функция для Racks (обновление capacity и max_weight)
CREATE OR REPLACE FUNCTION trg_racks_check_update()
RETURNS TRIGGER AS $$
DECLARE
    v_occupied INTEGER;
    v_total_weight NUMERIC;
BEGIN
    IF NEW.capacity IS DISTINCT FROM OLD.capacity THEN
        v_occupied := get_occupied_cells_count(NEW.id);
        IF NEW.capacity < v_occupied THEN
            RAISE EXCEPTION 'Нельзя уменьшить количество мест стеллажа % до % (занято %)',
                            NEW.id, NEW.capacity, v_occupied;
        END IF;
    END IF;

    IF NEW.max_weight IS DISTINCT FROM OLD.max_weight THEN
        v_total_weight := get_total_weight_on_rack(NEW.id);
        IF NEW.max_weight < v_total_weight THEN
            RAISE EXCEPTION 'Нельзя уменьшить максимальную нагрузку стеллажа % до % (текущий вес %)',
                            NEW.id, NEW.max_weight, v_total_weight;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для Racks
DROP TRIGGER IF EXISTS trg_racks_check_update ON Racks;
CREATE TRIGGER trg_racks_check_update
    BEFORE UPDATE OF capacity, max_weight ON Racks
    FOR EACH ROW EXECUTE FUNCTION trg_racks_check_update();

-- 1
CREATE OR REPLACE FUNCTION count_expiring_products(
    p_client_name VARCHAR,
    p_date DATE
)
RETURNS INTEGER AS $$
DECLARE
    v_client_id INTEGER;
    v_count INTEGER;
BEGIN
    -- Находим клиента по имени (берём первого, если несколько)
    SELECT id INTO v_client_id FROM Clients WHERE client_name = p_client_name LIMIT 1;
    IF NOT FOUND THEN
        RETURN 0;
    END IF;

    SELECT COUNT(*) INTO v_count
    FROM Products p
    JOIN Contracts c ON p.contract_id = c.id
    WHERE c.client_id = v_client_id
      AND c.expiry_date < p_date;

    RETURN v_count;
END;
$$ LANGUAGE plpgsql;

-- 2
-- Тип состояния для агрегата
DROP TYPE IF EXISTS max_dimensions_state CASCADE;
CREATE TYPE max_dimensions_state AS (
    max_h NUMERIC,
    max_w NUMERIC,
    max_l NUMERIC
);

-- Функция перехода
CREATE OR REPLACE FUNCTION max_dimensions_transition(
    state max_dimensions_state,
    height NUMERIC,
    width NUMERIC,
    length NUMERIC
)
RETURNS max_dimensions_state AS $$
BEGIN
    IF state IS NULL THEN
        RETURN ROW(height, width, length)::max_dimensions_state;
    END IF;
    RETURN ROW(
        GREATEST(state.max_h, height),
        GREATEST(state.max_w, width),
        GREATEST(state.max_l, length)
    )::max_dimensions_state;
END;
$$ LANGUAGE plpgsql;

-- Функция завершения
CREATE OR REPLACE FUNCTION max_dimensions_final(state max_dimensions_state)
RETURNS TEXT AS $$
BEGIN
    IF state IS NULL THEN
        RETURN NULL;
    END IF;
    RETURN state.max_h || ' X ' || state.max_w || ' X ' || state.max_l;
END;
$$ LANGUAGE plpgsql;

-- Создание агрегата
CREATE OR REPLACE AGGREGATE max_dimensions(NUMERIC, NUMERIC, NUMERIC) (
    SFUNC = max_dimensions_transition,
    STYPE = max_dimensions_state,
    FINALFUNC = max_dimensions_final
);

-- 3
-- Представление: клиент + список его товаров
CREATE OR REPLACE VIEW client_products_info AS
SELECT 
    c.id,
    c.client_name,
    c.bak_requisites,
    COALESCE(array_agg(p.name ORDER BY p.id), '{}'::TEXT[]) AS products_list
FROM Clients c
LEFT JOIN Contracts ct ON c.id = ct.client_id
LEFT JOIN Products p ON ct.id = p.contract_id
GROUP BY c.id, c.client_name, c.bak_requisites;

-- Триггерная функция для обновления описания клиента через представление
CREATE OR REPLACE FUNCTION trg_client_products_info_update()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Clients
    SET client_name = NEW.client_name,
        bak_requisites = NEW.bak_requisites
    WHERE id = OLD.id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- INSTEAD OF триггер на представление
DROP TRIGGER IF EXISTS trg_client_products_info_update ON client_products_info;
CREATE TRIGGER trg_client_products_info_update
    INSTEAD OF UPDATE ON client_products_info
    FOR EACH ROW
    EXECUTE FUNCTION trg_client_products_info_update();

-- 4
-- Инициализация очереди: удаляет старую таблицу и создаёт новую
CREATE OR REPLACE FUNCTION init()
RETURNS VOID AS $$
BEGIN
    DROP TABLE IF EXISTS queue CASCADE;
    CREATE TABLE queue (
        id SERIAL PRIMARY KEY,
        value VARCHAR(64) NOT NULL
    );
END;
$$ LANGUAGE plpgsql;

-- Добавление элемента в конец очереди
CREATE OR REPLACE FUNCTION enqueue(str VARCHAR(64))
RETURNS VARCHAR(64) AS $$
DECLARE
    v_len INTEGER;
BEGIN
    v_len := LENGTH(str);
    IF v_len > 64 THEN
        -- Обрезаем до 64 символов, чтобы не было ошибки
        str := LEFT(str, 64);
    END IF;
    INSERT INTO queue (value) VALUES (str);
    RETURN str;
END;
$$ LANGUAGE plpgsql;

-- Удаление элемента из начала очереди
CREATE OR REPLACE FUNCTION dequeue()
RETURNS VARCHAR(64) AS $$
DECLARE
    v_value VARCHAR(64);
BEGIN
    SELECT value INTO v_value FROM queue ORDER BY id DESC LIMIT 1;
    IF NOT FOUND THEN
        RETURN NULL;
    END IF;
    DELETE FROM queue WHERE id = (SELECT id FROM queue ORDER BY id DESC LIMIT 1);
    RETURN v_value;
END;
$$ LANGUAGE plpgsql;

-- Очистка очереди (возвращает количество удалённых элементов)
CREATE OR REPLACE FUNCTION empty()
RETURNS INTEGER AS $$
DECLARE
    v_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM queue;
    DELETE FROM queue;
    RETURN v_count;
END;
$$ LANGUAGE plpgsql;

-- Просмотр последнего элемента очереди
CREATE OR REPLACE FUNCTION tail()
RETURNS VARCHAR(64) AS $$
DECLARE
    v_value VARCHAR(64);
BEGIN
    SELECT value INTO v_value FROM queue ORDER BY id DESC LIMIT 1;
    RETURN v_value;
END;
$$ LANGUAGE plpgsql;

-- Пример работы с очередью

SELECT init();
SELECT enqueue('Первый элемент');
SELECT enqueue('Второй элемент');
SELECT enqueue('Очень длинная строка, которая превышает 64 символа, но будет обрезана');
SELECT tail();
SELECT dequeue();
SELECT dequeue();
SELECT dequeue();
SELECT dequeue();
SELECT enqueue('Новый после очистки');
SELECT empty();
SELECT empty();

