#!/bin/bash

psql -f z_scheme.sql postgres
psql -f inserts.sql postgres
psql -f z.sql postgres
