VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: setup deps generate clean db run test

setup:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

deps:
	$(PIP) install -r requirements.txt

generate:
	$(PY) data/generate_data.py --rows 100000

clean:
	rm -f data/sales_data.csv data/sales_data_clean.csv sql/sales_data.db

db: generate
	$(PY) data/clean_data.py

run:
	$(PY) -m streamlit run dashboard/app.py

test:
	$(VENV)/bin/pytest -q
