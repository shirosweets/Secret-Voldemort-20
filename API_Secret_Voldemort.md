# API REST Secret Voldemort

## First Sprint: 15/10 to 03/11

| ENDPOINT     | METHOD | URI         | PARAMS       | RESPONSE      | COMMENTS |
| ---------    | ------ | ----------- | ------------ | ------------- | -------- |
| register     | POST   | `/user/` | `{ e-mail: str, username: str, password: str, photo?: image }` | 200 - Ok \ 409 - Conflict if: * `e-mail` already registered * * `username` already registered * \ 400 - Bad Request if: * can't parse `e-mail` * * can't parse `password` * * can't parse `username` * | For now not include e-mail validation.  |
| login        | POST   | `/login/`   | `{ e-mail: str, password: str }`   | 200 - Ok \ 400 - Bad request: can't parse `e-mail` \ 404 - Not found: `e-mail` doesn't exist \ 401 Unauthorized: invalid `password` | |
| list lobbies | GET    | `/rooms/`    | `{ min_players?: int, max_players?: int }` | 200 - `[{ lobby_name: str, missing_players: int, max_players: int, min_players: int }]` | Not implemented in this sprint |                                                      | create lobby | POST   |`/rooms/`    | `{ userId: int, lobby_name: str }` | 200 - `LOBBY` | Later add in Params: `, max_players?: int, max_players?: int`. For now, min_players = max_players = 5. PRE: user is login | 
| join lobby | PUT    | `/rooms/<id>` | `{ nick: str, url: str }`  | 200 - `PLAYER` \ 409 - Conflict: `nick` already exists in this lobby \ 404 - Not found: `<id>` doesn't exist | PRE: user is login 
| start game | PATCH    | `/rooms/<id>`  |  | PRE: user is login |
| player available actions | GET	| `/games/<id>/actions/` | `[ { action_type: enum } ]` | PRE: player is login | 
| avaliable candidates | GET     | `/games/<id>/actions/` | | 200 - `[ { nick: str } ]` | PRE: There's a Minister Selected |
| select director | POST     | `/games/<id>/player/actions/`    | `{ nick: str }` | 200 - `{ nick: str }` \ 409 - Conflict: nick submitted is not valid  |  |
| post proclamation | POST   | `/games/<id>/player/actions/` | `{ is_fenix_procl: bool }` | 200 - `{ is_fenix_procl: bool }` | PRE : Minister and Director are selected |
| end game | PUT   |`/games/<id>/`  | 200 - `[ROL]` | |

-------------

`LOBBY = { lobby_id: int, lobby_name: str, creation_date: datetimestr, creator_username: str, min_players: int, max_players: int, started: bool }`

`PLAYER = { player_id: int, nick: str, number_player: int, role: str, its_alive: bool, director: bool, minister: bool, game_started: bool, chat_blocked: bool }`  

`ROL = { nick : str, rol : enum }`

-------------

## Descripción de los endpoints:
 
**register POST /user**: este endpoint toma de parámetros `e-mail`, `username`, `password` y `photo`; éstos se encuentran en campos que el agente externo debe completar y el sistema validar. Los campos a llenar son: un `e-mail` que debe ser único, un `username` que también deber ser único, una `password` alfanumérica que debe ser entre 8 a 32 carácteres y una `photo` que es una imagen que se elige entre las predeterminadas en el sistema, con un valor por defecto. Como respuesta devuelve un status code 200 - Ok si no hubo errores de validación, un 409 si el e-mail o el `username` ya está registrado o un 400 como error en el formato del `e-mail` o `password` proporcionados.

**login POST /login/** : éste endpoint toma como parámetros en primer lugar un `e-mail` que se supone registrado y único en el sistema, cuyo formato se debe validar por el front (c/c se devuelve un status code 400 con un mensaje informativo), y además validar que efectivamente exista registrado en el sistema (c/c se devuelve un 404 con un mensaje informativo); en segundo lugar una `password` la cual debe hashearse en la base de datos del sistema para validar que se ecuentra registrada en él (c/c se devuelve un status code de 401 con un mensaje informativo). Éstos dos parámetros serán introducidos por un agente externo en los campos de un formulario provisto por el front.

**create lobby POST /rooms/new**: este endpoint toma los parámetros `userId`, `lobby_name`, `max_players?` y `min_players?`. El parámetro `userId` es el identificador de usuario que será creador de ese lobby lo que le permitirá iniciar la partida cuando desee, el parámetro `lobby_name` debe ser elegido por el usuario obligatatoriamente y es único. Los parámetros `min_players?` y `max_players?` en un futuro podrán asignarse opcionalmente por el usuario creador, que tendrán valores por default 5 y 10 respectivamente, de lo cual se encargará el front de garantizar que no va a ser menor a 5 ni mayor a 10; en éste sprint serán asignados ambos con valor 5 exclusivamente. En la respuesta de éste endpoint se incluirán, además de los mencionados, atributos tales como `started`, que será el cual pertenece al estado de la partida, es decir, si la partida del lobby ha iniciado o no, por default inicia en false; luego `creation_date` que corresponderá a la fecha de creación del lobby.

---


Nota 7 (Knd) PREGUNTAR : cambié number_player por missing_players que es el nro de jugadores faltantes para llegar al mínimo