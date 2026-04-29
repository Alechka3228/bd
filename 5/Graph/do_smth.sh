#!/bin/bash
createdb a2
psql -f schema.sql a2
psql -f inserts.sql a2
dropdb a2