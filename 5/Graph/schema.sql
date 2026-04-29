DROP TABLE IF EXISTS Nodes;
DROP TABLE IF EXISTS Relations;

CREATE TABLE Nodes (
    id SERIAL PRIMARY KEY,
    value NUMERIC(5,2)
);

CREATE TABLE Relations (
    parent INTEGER,
    child INTEGER,
    weight NUMERIC(5,2)
);