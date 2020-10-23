# API REST Secret Voldemort

## First Sprint: 15/10 to 03/11

| ENDPOINT     | METHOD | URI         | PARAMS       | RESPONSE      | COMMENTS |
| ---------    | ------ | ----------- | ------------ | ------------- | -------- |
| register     | POST   | `/user/` | `{ e-mail: str, username: str, password: str, photo?: image }` | 200 - Ok \ 409 - Conflict if: `e-mail` already registered `username` already registered \ 400 - Bad Request if: can't parse `e-mail` can't parse `password` can't parse `username` | For now not include e-mail validation  |
| login        | POST | `/login/` | `{ e-mail: str, password: str }`   | 200 - Ok \ 400 - Bad request: can't parse `e-mail` \ 404 - Not found: `e-mail` doesn't exist \ 401 Unauthorized: invalid `password` | |
| create lobby | POST | `/rooms/` | `{ lobby_name: str }` | 200 - `LOBBY` | Later add in Params: `, max_players?: int, max_players?: int`. For now, min_players = max_players = 5. PRE: user is login | 
| join lobby | POST | `/rooms/<lobby_id>` | `{ nick: str }` | 200 - `{ nick: str }` \ 409 - Conflict: `nick` already exists in this lobby \ 404 - Not found: `<lobby_id>` doesn't exist | PRE: User is login. `nick` is `username` of user that call. Player is created when user join in a lobby. Set `number_of_players` to `number_of_players + 1` |
| leave lobby | DELETE | `/rooms/<lobby_id>` | | 200 - Ok  | PRE: there is at least one player in the lobby that not is creater. The player that call is deleted, LOBBY's `number_of_players` is decremented in one. |
| start game | DELETE | `/rooms/<lobby_id>/start_game` | | 200 - Ok | PRE: Player is the creator. A new game is created with players that joined in the lobby, and the lobby is deleted |
| select director | POST | `/games/<game_id>/actions/`    | `{ nick: str }` | 200 - `{ nick: str }` \ 409 - Conflict: nick submitted is not valid  | PRE: Player is the Minister |
| post proclamation | POST | `/games/<game_id>/actions/` | `{ is_fenix_procl: bool }` | 200 - `{ is_fenix_procl: bool }` | PRE : Minister and Director are selected |

-------------
**Types:**
---

`LOBBY = { lobby_id: int, lobby_name: str, creation_date: datetimestr, creator_username: str, min_players: int, max_players: int, number_of_players: int }`

`PLAYER = { player_id: int, nick: str, number_player: int, role: str, its_alive: bool, director: bool, minister: bool, game_started: bool, chat_blocked: bool }`

`ROLE = { nick : str, rol : enum }`

---  

`STAGE_TURN = -1: Lobby | 0 : presentacion_mortifaga | 1 : elección_ministro | 2 : elección_director | 3 : votación_director | 4 : legislativa_ministro | 5 : legislativa_director | 6 : acción ejecutiva | 7 : finalizó`

`GAME = { game_id: int, election_marker: enum[0..3] = 0, next_minister: enum[0..9] = random(0..9), turn_stage: enum, last_director: enum[-1, 0..9] = -1, last_minister[-1, 0..9] = -1 }` 

-------------

## Descripción de los endpoints:
 
**register POST /user**: este endpoint toma de parámetros `e-mail`, `username`, `password` y `photo`; éstos se encuentran en campos que el agente externo debe completar y el sistema validar. Los campos a llenar son: un `e-mail` que debe ser único, un `username` que también deber ser único, una `password` alfanumérica que debe ser entre 8 a 32 carácteres y una `photo` que es una imagen que se elige entre las predeterminadas en el sistema, con un valor por defecto. Como respuesta devuelve un status code 200 - Ok si no hubo errores de validación, un 409 si el e-mail o el `username` ya está registrado o un 400 como error en el formato del `e-mail` o `password` proporcionados.

**login POST /login/** : éste endpoint toma como parámetros en primer lugar un `e-mail` que se supone registrado y único en el sistema, cuyo formato se debe validar por el front (c/c se devuelve un status code 400 con un mensaje informativo), y además validar que efectivamente exista registrado en el sistema (c/c se devuelve un 404 con un mensaje informativo); en segundo lugar una `password` la cual debe hashearse en la base de datos del sistema para validar que se ecuentra registrada en él (c/c se devuelve un status code de 401 con un mensaje informativo). Éstos dos parámetros serán introducidos por un agente externo en los campos de un formulario provisto por el front.

**create lobby POST /rooms/new**: este endpoint toma los parámetros `userId`, `lobby_name`, `max_players?` y `min_players?`. El parámetro `userId` es el identificador de usuario que será creador de ese lobby lo que le permitirá iniciar la partida cuando desee, el parámetro `lobby_name` debe ser elegido por el usuario obligatatoriamente y es único. Los parámetros `min_players?` y `max_players?` en un futuro podrán asignarse opcionalmente por el usuario creador, que tendrán valores por default 5 y 10 respectivamente, de lo cual se encargará el front de garantizar que no va a ser menor a 5 ni mayor a 10; en éste sprint serán asignados ambos con valor 5 exclusivamente. En la respuesta de éste endpoint se incluirán, además de los mencionados, atributos tales como `started`, que será el cual pertenece al estado de la partida, es decir, si la partida del lobby ha iniciado o no, por default inicia en false; luego `creation_date` que corresponderá a la fecha de creación del lobby.

---
## Notas de decisiones implicitas:  
 - Como decidimos hacer sockets, eliminamos varios endpoints que pedian informacion al server ya que el server proveera la informacion necesaria a un jugador cuando se necesite que realice una acción (ie: pasarle el candidato para votar, los jugadores posibles a ser nominados, etc)  
 
 - Al finalizar el último turno de un game se pasa esa info a las otras clases para llegar a historial de partidas y se elimina ese objeto de game  

 - Cuando el creador inicia la partida se crea un game con los players unidos al lobby y se borra el lobby, ésto explica el DELETE en 'start game'. 

- El objeto Jugador se crea cuando entra un usuario al lobby y cuando éste se va se require eliminar ese Jugador, ésto explica el DELETE en `leave lobby`.

- El atributo de lobby, is_started, se eliminó pq no hace falta, ya que una partida iniciada se representa como game, sino genera ambiguedad e inconsistencia.

- Las caracteristicas de agregación, tales como cambiar el `nick` dentro del lobby, restricciones en `photo` y 3 valores por defecto de  `photo`, para éste sprint en principio se omite, solamente se define:
 1)  el `nick` es el `username`
 2)  la foto tiene ya un solo valor por defecto.          
  Al finalizar todo veremos si llegamos con el tiempo para agregarlo, sino será en los próximos sprints.

- Vamos a modelar foreign keys para varias clases: por ejemplo en player (a user), en historyGame (a user), Game (a player), etc.

- Como vamos a trabajar con web socket, para start game debemos preparar toda la estructura tanto en back como en front del ésta forma, luego el endpoint de start game devolverá minimamente el orden del player en la mesa a **todos** los players.


Nota 1 (PREGUNTAR) : ponemos el atributo  number_players que es la cantidad de jugadores en el lobby o missing_players que es el nro de jugadores faltantes para llegar al mínimo en el lobby
