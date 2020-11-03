APP = main

all: main.py
	rm -f data_base.sqlite
	uvicorn $(APP):app --reload

.PHONY: clean

clean:
	