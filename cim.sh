#!/bin/bash
createdb a1
psql -f ../z_scheme.sql a1
psql -f ../inserts.sql a1
psql -f z.sql a1
dropdb a1
