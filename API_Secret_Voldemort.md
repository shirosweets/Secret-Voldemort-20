# API REST Secret Voldemort

## First Sprint: 15/10 to 03/11

| ENDPOINT     | METHOD | URI         | PARAMS       | RESPONSE      | COMMENTS |
| ---------    | ------ | ----------- | ------------ | ------------- | -------- |
| register     | POST   | `/user/` | `{ e-mail: str, username: str, password: str, photo?: image }` | 200 - Ok \ 409 - Conflict if: * `e-mail` already registered * * `username` already registered * \ 400 - Bad Request if: * can't parse `e-mail` * * can't parse `password` * * can't parse `username` * | For now not include e-mail validation  |
| login        | POST | `/login/` | `{ e-mail: str, password: str }`   | 200 - Ok \ 400 - Bad request: can't parse `e-mail` \ 404 - Not found: `e-mail` doesn't exist \ 401 Unauthorized: invalid `password` | |
| create lobby | POST | `/rooms/` | `{ userId: int, lobby_name: str }` | 200 - `LOBBY` | Later add in Params: `, max_players?: int, max_players?: int`. For now, min_players = max_players = 5. PRE: user is login | 
| join lobby | PUT | `/rooms/<lobby_id>` | `{ nick: str, url: str }`  | 200 - `PLAYER` \ 409 - Conflict: `nick` already exists in this lobby \ 404 - Not found: `<lobby_id>` doesn't exist | |
| leave lobby | DELETE | `/rooms/<lobby_id>` | `{ user_id : int }` | | If player is owner, lobby dies |
| start game | PUT | `/rooms/<lobby_id>` | `{ started = true }` | 200 - Ok | PRE: Player is owner|
| player available actions | GET | `/games/<game_id>/actions/` | | 200 - `[ { action_type: enum } ]` | | 
| avaliable candidates | GET | `/games/<game_id>/candidate` | | 200 - `[ { nick: str } ]` | PRE: There's a Minister Selected |
| select director | POST | `/games/<game_id>/actions/`    | `{ nick: str }` | 200 - `{ nick: str }` \ 409 - Conflict: nick submitted is not valid  |  |
| post proclamation | POST | `/games/<game_id>/actions/` | `{ is_fenix_procl: bool }` | 200 - `{ is_fenix_procl: bool }` | PRE : Minister and Director are selected |

-------------

`LOBBY = { lobby_id: int, lobby_name: str, creation_date: datetimestr, creator_username: str, min_players: int, max_players: int, started: bool }`

`PLAYER = { user_id: int, nick: str, number_player: int, role: str, its_alive: bool, director: bool, minister: bool, game_started: bool, chat_blocked: bool }`

`ROL = { nick : str, rol : enum }`

-------------

## Descripción de los endpoints:
 
**register POST /user**: este endpoint toma de parámetros `e-mail`, `username`, `password` y `photo`; éstos se encuentran en campos que el agente externo debe completar y el sistema validar. Los campos a llenar son: un `e-mail` que debe ser único, un `username` que también deber ser único, una `password` alfanumérica que debe ser entre 8 a 32 carácteres y una `photo` que es una imagen que se elige entre las predeterminadas en el sistema, con un valor por defecto. Como respuesta devuelve un status code 200 - Ok si no hubo errores de validación, un 409 si el e-mail o el `username` ya está registrado o un 400 como error en el formato del `e-mail` o `password` proporcionados.

**login POST /login/** : éste endpoint toma como parámetros en primer lugar un `e-mail` que se supone registrado y único en el sistema, cuyo formato se debe validar por el front (c/c se devuelve un status code 400 con un mensaje informativo), y además validar que efectivamente exista registrado en el sistema (c/c se devuelve un 404 con un mensaje informativo); en segundo lugar una `password` la cual debe hashearse en la base de datos del sistema para validar que se ecuentra registrada en él (c/c se devuelve un status code de 401 con un mensaje informativo). Éstos dos parámetros serán introducidos por un agente externo en los campos de un formulario provisto por el front.

**create lobby POST /rooms/new**: este endpoint toma los parámetros `userId`, `lobby_name`, `max_players?` y `min_players?`. El parámetro `userId` es el identificador de usuario que será creador de ese lobby lo que le permitirá iniciar la partida cuando desee, el parámetro `lobby_name` debe ser elegido por el usuario obligatatoriamente y es único. Los parámetros `min_players?` y `max_players?` en un futuro podrán asignarse opcionalmente por el usuario creador, que tendrán valores por default 5 y 10 respectivamente, de lo cual se encargará el front de garantizar que no va a ser menor a 5 ni mayor a 10; en éste sprint serán asignados ambos con valor 5 exclusivamente. En la respuesta de éste endpoint se incluirán, además de los mencionados, atributos tales como `started`, que será el cual pertenece al estado de la partida, es decir, si la partida del lobby ha iniciado o no, por default inicia en false; luego `creation_date` que corresponderá a la fecha de creación del lobby.

---


Nota 1 (Knd) PREGUNTAR : cambié number_player por missing_players que es el nro de jugadores faltantes para llegar al mínimo

Nota 2 (Agus) Segun como interpretó Cande la clase Jugador se crea cuando se crea el lobby. Yo interpreté que el objeto Jugador se crea cuando entra un usuario al lobby. Decidamos como es porque eso hace la diferencia de como funciona la API (y si es PUT o POST)