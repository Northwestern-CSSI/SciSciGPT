#!/bin/bash

# uvicorn app:app --host 0.0.0.0 --port 8080 --workers 4
uvicorn app:app --host 0.0.0.0 --port 8080 --reload