INSERT INTO Nodes (value) VALUES
(10.50),
(25.75),
(32.00),
(15.25),
(42.30),
(18.90),
(55.60),
(12.40),
(28.15),
(35.80);

INSERT INTO Relations (parent, child, weight) VALUES
(1, 2, 1.50),
(1, 3, 2.00),
(1, 4, 1.25),
(2, 5, 3.00),
(2, 6, 2.50),
(4, 7, 1.75),
(6, 8, 2.20),
(7, 9, 1.90),
(7, 10, 2.10),
(3, 6, 1.80),
(5, 9, 3.50);

SELECT * FROM Nodes;
SELECT * FROM Relations;