
all:
	# rm -f data_base.sqlite
	rm -f test_data_base.sqlite
	pytest test_1logIn.py test_2lobby.py test3_game_5-6_players.py test4_game_7-8_players.py test5_game_9-10_players.py --disable-warnings 

print:
	# rm -f data_base.sqlite
	rm -f test_data_base.sqlite
	pytest --disable-warnings --capture=no