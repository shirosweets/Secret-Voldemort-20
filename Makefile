
all:
	# rm -f data_base.sqlite
	rm -f test_data_base.sqlite
	pytest --disable-warnings

print:
	# rm -f data_base.sqlite
	rm -f test_data_base.sqlite
	pytest --disable-warnings --capture=no