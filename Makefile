
all: test_lobby.py
	rm -f data_base.sqlite
	pytest --disable-warnings

print: test_lobby.py
	rm -f data_base.sqlite
	pytest --disable-warnings --capture=no