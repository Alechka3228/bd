from random import randrange

# menus
main_menu = [["1", "Убить поднять заполнить"],
             ["2", "Работа с помещениями"],
             ["3", "Работа с стелажами"],
             ["q", "На выход"]]
room_manipulation_menu = [["1", "Добить"],
             ["2", "Изменить"],
             ["3", "Удалить"]]

def print_that_user_is_disabled(message: str) -> None:
    consolations = [
        "Глупость? Нет, это такой секретный шифр?.. Если нет, просто введи, пожалуйста, правильно.",
        "Ваше сообщение выглядит как загадка. Я не разгадал(а), но ставлю лайк за креативность! Попробуйте написать прозой.",
        "Похоже, по клавиатуре прошёлся кот. Выжившим после такого положена вторая попытка!",
        "Человек, который ничего не вводит неправильно, ничего не делает. Ошибка — это просто черновик правильного ответа.",
        "В мире, где полно настоящих проблем, случайно нажать не ту клавишу — почти подвиг беззаботности. А теперь исправьтесь и поехали дальше."
    ]

    print()
    print(consolations[randrange(len(consolations))])
    print("Note " + message)
    print()

def is_malicious(string: str) -> bool:
    postgresql_keywords = [
        # Основные DML команды
        "SELECT", "INSERT", "UPDATE", "DELETE", "MERGE",
        "FROM", "WHERE", "GROUP BY", "HAVING", "ORDER BY",
        "LIMIT", "OFFSET", "FETCH", "FIRST", "NEXT", "ROW", "ROWS", "ONLY",
        
        # JOIN операции
        "JOIN", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN",
        "CROSS JOIN", "NATURAL JOIN", "LATERAL", "ON", "USING",
        
        # Условия и операторы
        "AND", "OR", "NOT", "IN", "EXISTS", "ANY", "SOME", "ALL",
        "BETWEEN", "LIKE", "ILIKE", "SIMILAR TO", "IS NULL", "IS NOT NULL",
        "IS TRUE", "IS FALSE", "IS UNKNOWN", "DISTINCT", "UNIQUE",
        
        # Функции агрегации
        "COUNT", "SUM", "AVG", "MIN", "MAX", "ARRAY_AGG", "STRING_AGG",
        "JSON_AGG", "JSONB_AGG", "XMLAGG", "GROUP_CONCAT",
        
        # Оконные функции
        "OVER", "PARTITION BY", "ROW_NUMBER", "RANK", "DENSE_RANK",
        "LEAD", "LAG", "FIRST_VALUE", "LAST_VALUE", "NTH_VALUE",
        
        # DDL команды
        "CREATE", "ALTER", "DROP", "TRUNCATE", "RENAME",
        "TABLE", "INDEX", "VIEW", "MATERIALIZED VIEW", "SEQUENCE",
        "SCHEMA", "DATABASE", "FUNCTION", "PROCEDURE", "TRIGGER",
        "TYPE", "DOMAIN", "RULE", "CAST", "CONVERSION",
        
        # Ограничения (Constraints)
        "PRIMARY KEY", "FOREIGN KEY", "REFERENCES", "UNIQUE", "CHECK",
        "DEFAULT", "NOT NULL", "CONSTRAINT", "DEFERRABLE", "INITIALLY",
        
        # DCL команды
        "GRANT", "REVOKE", "PRIVILEGES", "ROLE", "USER", "GROUP",
        
        # Транзакции
        "BEGIN", "COMMIT", "ROLLBACK", "SAVEPOINT", "RELEASE SAVEPOINT",
        "START TRANSACTION", "ABORT", "PREPARE TRANSACTION",
        
        # Управление соединениями
        "LOCK TABLE", "SHARE", "EXCLUSIVE", "ACCESS SHARE", "ROW SHARE",
        
        # WITH (CTE)
        "WITH", "RECURSIVE", "AS", "MATERIALIZED", "NOT MATERIALIZED",
        
        # Значения и литералы
        "NULL", "TRUE", "FALSE", "DEFAULT", "CURRENT_DATE", "CURRENT_TIME",
        "CURRENT_TIMESTAMP", "LOCALTIME", "LOCALTIMESTAMP", "NOW()",
        "CURRENT_USER", "SESSION_USER", "USER",
        
        # Приведение типов
        "::", "CAST", "::text", "::integer", "::bigint", "::boolean",
        "::date", "::timestamp", "::json", "::jsonb", "::uuid",
        
        # JSON операции
        "->", "->>", "#>", "#>>", "@>", "<@", "?", "?|", "?&",
        "JSON_BUILD_OBJECT", "JSON_BUILD_ARRAY", "TO_JSON", "JSON_STRIP_NULLS",
        
        # Массивы
        "ARRAY", "[]", "UNNEST", "array_agg", "array_cat", "array_append",
        "array_prepend", "array_replace", "array_to_string",
        
        # Строковые функции
        "CONCAT", "CONCAT_WS", "FORMAT", "LOWER", "UPPER", "INITCAP",
        "LENGTH", "CHAR_LENGTH", "POSITION", "STRPOS", "SUBSTRING",
        "LEFT", "RIGHT", "TRIM", "LTRIM", "RTRIM", "REPLACE", "REVERSE",
        "SPLIT_PART", "REGEXP_MATCH", "REGEXP_REPLACE", "REGEXP_SPLIT_TO_ARRAY",
        
        # Числовые функции
        "ABS", "CEIL", "CEILING", "FLOOR", "ROUND", "TRUNC", "MOD",
        "POWER", "SQRT", "EXP", "LN", "LOG", "RANDOM", "SETSEED",
        "SIN", "COS", "TAN", "PI", "DEGREES", "RADIANS",
        
        # Date/Time функции
        "AGE", "EXTRACT", "DATE_PART", "DATE_TRUNC", "MAKE_DATE",
        "MAKE_TIME", "MAKE_TIMESTAMP", "JUSTIFY_DAYS", "JUSTIFY_HOURS",
        
        # Условные выражения
        "CASE", "WHEN", "THEN", "ELSE", "END", "COALESCE", "NULLIF",
        "GREATEST", "LEAST",
        
        # Операторы сравнения
        "=", "<>", "!=", "<", ">", "<=", ">=", "<=>",
        
        # Специальные операторы PostgreSQL
        "~~", "~~*", "!~~", "!~~*",  # LIKE/ILIKE операторы
        "@@",  # текстовый поиск
        "##",  # сходство
        "@",   # абсолютное значение
        "&",   # битовое AND
        "|",   # битовое OR
        "#",   # битовое XOR
        "~",   # битовое NOT
        
        # Полнотекстовый поиск
        "TO_TSVECTOR", "TO_TSQUERY", "PLAINTO_TSQUERY", "PHRASETO_TSQUERY",
        "TS_RANK", "TS_RANK_CD", "TS_HEADLINE", "TS_DEBUG",
        
        # Администрирование
        "VACUUM", "ANALYZE", "REINDEX", "CLUSTER", "CHECKPOINT",
        "EXPLAIN", "ANALYZE", "VERBOSE", "COSTS", "BUFFERS", "TIMING",
        
        # Бэкапирование
        "pg_dump", "pg_restore", "COPY", "PROGRAM", "STDIN", "STDOUT",
        
        # Системные схемы и таблицы
        "pg_catalog", "information_schema", "pg_class", "pg_database",
        "pg_tables", "pg_indexes", "pg_views", "pg_stat_activity",
        "pg_locks", "pg_settings", "pg_stat_statements",
        
        # Расширения
        "CREATE EXTENSION", "DROP EXTENSION", "hstore", "ltree", "pgcrypto",
        "uuid-ossp", "postgis", "pg_trgm", "btree_gin", "btree_gist",
        
        # Настройки
        "SET", "RESET", "SHOW", "SESSION", "LOCAL", "CONSTRAINTS",
        
        # Комментарии
        "--", "/*", "*/", "COMMENT ON", "COMMENT",
        
        # Импорт/Экспорт
        "EXPORT", "IMPORT", "FOREIGN DATA WRAPPER", "SERVER",
        
        # Секционирование
        "PARTITION BY RANGE", "PARTITION BY LIST", "PARTITION BY HASH",
        "PARTITION OF", "FOR VALUES FROM", "TO", "WITH", "WITHOUT",
    ]

    for i in postgresql_keywords:
        if i in string:
            return True
        
    return False

def safety_input(before_prompt: str) -> str:
    string = input(before_prompt)
    if is_malicious(string):
        return ""
    else:
        return string
    
def check_done(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            print("\nDone\n")
        except Exception as e:
            print()
            print("Not done or done with error")
            print(f"Error: {e}")
            print()
    return wrapper