
all:
	rm -f test_data_base.sqlite 
	pytest test_users.py --disable-warnings || true 
	rm -f test_data_base.sqlite
	pytest test_1logIn.py test_2lobby.py test3_game_5-6_players.py  --disable-warnings || true
	pytest test4_game_7-8_players.py --disable-warnings || true
	pytest test5_game_9-10_players.py --disable-warnings || true

test_users:
	rm -f test_data_base.sqlite 
	pytest test_users.py --disable-warnings || true

logIn_test:
	rm -f test_data_base.sqlite 
	pytest test_1logIn.py --disable-warnings || true

lobby_test:
	rm -f test_data_base.sqlite
	pytest test_1logIn.py test_2lobby.py --disable-warnings || true

game_5-6_players:
	rm -f test_data_base.sqlite
	pytest test_1logIn.py test_2lobby.py test3_game_5-6_players.py  --disable-warnings || true

game_7-8_players:
	rm -f test_data_base.sqlite
	pytest test_1logIn.py test_2lobby.py test4_game_7-8_players.py  --disable-warnings || true

game_9-10_players:
	rm -f test_data_base.sqlite
	pytest test_1logIn.py test_2lobby.py test5_game_9-10_players.py  --disable-warnings || true