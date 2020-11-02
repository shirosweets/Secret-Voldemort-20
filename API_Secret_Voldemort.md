# API REST Secret Voldemort

## First Sprint: 15/10 to 03/11

| ENDPOINT     | METHOD | URI         | PARAMS       | RESPONSE      | COMMENTS |
| ---------    | ------ | ----------- | ------------ | ------------- | -------- |
| register     | POST   | `/user/` | `{ userIn_email: EmailStr, userIn_username: str, userIn_password: str, userIn_photo: Optional[str] }` | 201 - `{ userOut_email: str, userOut_username: str, userOut_operation_result: str = "Succefully created" }` \ 409 - Conflict if: `email` already registered `username` already registered \ 400 - Bad Request if:  can't parse `password` can't parse `username` \ 422 - Unprocessable Entity if `email`'s format is invalid | For now not include email validation  |
| login        | POST | `/login/` | `{logIn_email: str, logIn_password: str}` | 200 - Ok  `{token: Byte}` \ 400 - Bad request: can't parse `email` \ 404 - Not found: `email` doesn't exist \ 401 Unauthorized: invalid `password` | |
| create new lobby | POST | `/lobby/` | `{PRIVATE} {lobbyIn_name: str,  lobbyIn_max_players: Optional[int], lobbyIn_min_players: Optional[int]}` | 201 - Created `{ lobbyOut_name : str, lobbyOut_Id : int, lobbyOut_result : str = "Succefully created" }` | |
 | join lobby | POST | `/lobby/<lobby_id>` | `{PRIVATE}` | 202 - Accepted `{ joinLobby_name : str, joinLobby_result = (f"welcome to {lobby_name}")}` \ 409 - Conflict: `user_id` already exists in this lobby \ 404 - Not found: `<lobby_id>` doesn't exist | Next Sprint: Change `nick`. Error `nick` is the exact same `username`|
| leave lobby | DELETE | `/lobby/<lobby_id>` | `{PRIVATE}`| 202-ACCEPTED | |
| start game | DELETE | `/lobby/<lobby_id>/start_game` | `{PRIVATE}`| 200 - Ok | PRE: Player is the creator|
| select director | POST | `/games/<game_id>/actions/` | `{PRIVATE} {player_number: int }` | 200 - `{player_nick: str }` | PRE: Player is the Minister |
| post proclamation | PUT | `/games/<game_id>/actions/` | `{PRIVATE} { is_fenix_procl: bool }` | 200 - `{ is_fenix_procl: bool, fenix_proclamations: Optional[int], death_eaters_proclamations: Optional[int] }` | PRE : Minister and Director are selected |

-------------

## Descripción de los endpoints

**register POST /user**: este endpoint toma de parámetros `email`, `username`, `password` y `photo`; éstos se encuentran en campos que el agente externo debe completar y el sistema validar. Los campos a llenar son: un `email` que debe ser único, un `username` que también deber ser único, una `password` alfanumérica que debe ser entre 8 a 32 carácteres y una `photo` que es una imagen que se elige entre las predeterminadas en el sistema, con un valor por defecto. Como respuesta devuelve un status code 200 - Ok si no hubo errores de validación, un 409 si el email o el `username` ya está registrado o un 400 como error en el formato del `email` o `password` proporcionados.

**login POST /login/** : éste endpoint toma como parámetros en primer lugar un `email` que se supone registrado y único en el sistema, cuyo formato se debe validar por el front (c/c se devuelve un status code 400 con un mensaje informativo), y además validar que efectivamente exista registrado en el sistema (c/c se devuelve un 404 con un mensaje informativo); en segundo lugar una `password` la cual debe hashearse en la base de datos del sistema para validar que se ecuentra registrada en él (c/c se devuelve un status code de 401 con un mensaje informativo). Éstos dos parámetros serán introducidos por un agente externo en los campos de un formulario provisto por el front.

**create_new_lobby POST /lobby/new**: este endpoint toma los parámetros `userId`, `lobby_name`, `max_players?` y `min_players?`. El parámetro `userId` es el identificador de usuario que será creador de ese lobby lo que le permitirá iniciar la partida cuando desee, el parámetro `lobby_name` debe ser elegido por el usuario obligatatoriamente y es único. Los parámetros `min_players?` y `max_players?` en un futuro podrán asignarse opcionalmente por el usuario creador, que tendrán valores por default 5 y 10 respectivamente, de lo cual se encargará el front de garantizar que no va a ser menor a 5 ni mayor a 10; en éste sprint serán asignados ambos con valor 5 exclusivamente. En la respuesta de éste endpoint se incluirán, además de los mencionados, atributos tales como `started`, que será el cual pertenece al estado de la partida, es decir, si la partida del lobby ha iniciado o no, por default inicia en false; luego `creation_date` que corresponderá a la fecha de creación del lobby.

-------------

## Notas de decisiones implicitas

- Como decidimos hacer sockets, eliminamos varios endpoints que pedian informacion al server ya que el server proveera la informacion necesaria a un jugador cuando se necesite que realice una acción (ie: pasarle el candidato para votar, los jugadores posibles a ser nominados, etc)

- Al finalizar el último turno de un game se pasa esa info a las otras clases para llegar a historial de partidas y se elimina ese objeto de game  

- Cuando el creador inicia la partida se crea un game con los players unidos al lobby y se borra el lobby, ésto explica el DELETE en 'start game'.

- El objeto Jugador se crea cuando entra un usuario al lobby y cuando éste se va se require eliminar ese Jugador, ésto explica el DELETE en `leave lobby`.

- El atributo de lobby, is_started, se eliminó pq no hace falta, ya que una partida iniciada se representa como game, sino genera ambiguedad e inconsistencia.

- Las caracteristicas de agregación, tales como cambiar el `nick` dentro del lobby, restricciones en `photo` y 3 valores por defecto de  `photo`, para éste sprint en principio se omite, solamente se define:

  1) El `nick` es el `username`.

  2) La foto tiene ya un solo valor por defecto.

Al finalizar todo veremos si llegamos con el tiempo para agregarlo, sino será en los próximos sprints.

- Vamos a modelar foreign keys para varias clases: por ejemplo en player (a user), en historyGame (a user), Game (a player), etc.

- Como vamos a trabajar con web socket, para start game debemos preparar toda la estructura tanto en back como en front del ésta forma, luego el endpoint de start game devolverá minimamente el orden del player en la mesa a **todos** los players.

Nota (para Agus): los endpoints `start game`, `select director` y `post problamation` no están definidos del todo qué modelos responden. Falta implementarlos al 100%.
