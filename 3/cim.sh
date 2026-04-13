#!/bin/bash

psql -f Зубков.sql postgres
psql -f inserts.sql postgres
psql -f z.sql postgres
