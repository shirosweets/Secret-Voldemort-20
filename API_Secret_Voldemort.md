# API REST Secret Voldemort

## First Sprint: 15/10 to 03/11

| ENDPOINT  | METHOD | URL | PARAMS       | RESPONSE | COMMENTS |
| ------------------ | ------- | ------- | -------------------------------------- | ------------------------- | ----------- |
| register as user | POST   | `/user`       | `{e-mail: str, username: str, password: str, photo?: image}`                      | 200 - Ok \ 409 - Conflict if: * `e-mail` already registered * * `username` already registered * \ 400 - Bad Request if: * can't parse `e-mail` * * can't parse `password` * * can't parse `photo` * | For now not include e-mail validation |
| login as user | POST   | `/login`  | `{e-mail: str, password: str}` | 200 - Ok \ 400 - Bad request: can't parse `e-mail` \ 404 - Not found: `e-mail` doesn't exist \ 401 Unauthorized: invalid `password` |
| create lobby | POST   | `/rooms/new`      | `{userId: int, name: str}` | 200 - `{id: int, name: str, creation_date: datetimestr, usernameCreator: str, min_players: int, max_players: int, started: bool}` | Later add in Params: `, max_players?: int, max_players?: int`. For now, min_players = max_players = 5 |
| join lobby | PATCH    | `/rooms/join` | `{nick: str, url: str}` | 200 - `{nick: str, number_player: int, role: str, its_alive: bool, director: bool, minister: bool, game_started: bool, chat_blocked: bool}` \ 409 - Conflict if: `nick` already exists in this lobby \ 404 - Not found: `url` doesn't exist | Later url endpoint will be `/rooms/<id>` PRE: user is login |
| start game | PATCH   | `/rooms/start` | `{url: str}` | 


Nota 1: para reflejar que un creador de la partida lo sea para poder iniciar una, cómo lo ponemos en la API? solo lo aclaramos documentandolo como restricción? 

Nota 3: Faltan elegir Ministro de magia, emitir proclamación y Finalizar partida (importantes las PRE) y DOCUMENTAR (acá podemos incluir cuáles respectan a users, lobbies, turns/games [public info, personal info, transactions], y especificar qué se hace en cada endpoint (criterios de aceptación))

diferencia entre PUT y PATCH: https://www.bbvanexttechnologies.com/como-utilizar-los-metodos-put-y-patch-en-el-diseno-de-tus-apis-restful/ y preguntar al profe cual conviene en join lobby y start game. Resumen: con put hay que especificarle el cuerpo completo en {este caso de un lobby, con path no hace falta, solo un id creo que basta (en éste caso una url)}

status codes: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html