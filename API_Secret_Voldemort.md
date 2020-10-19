# API REST Secret Voldemort

## First Sprint: 15/10 to 03/11

| ENDPOINT     | METHOD | URL         | PARAMS       | RESPONSE      | COMMENTS |
| ---------    | ------ | ----------- | ------------ | ------------- | -------- |
| register     | POST   |`/user/`      | `{ e-mail: str, username: str, password: str, photo?: image }`                                           | 200 - Ok \ 409 - Conflict if: * `e-mail` already registered * * `username` already registered * \ 400 - Bad Request if: * can't parse `e-mail` * * can't parse `password` *                                                                | For now not include e-mail validation. `password` will be a hash |
| login        | POST   |`/login/`     | `{ e-mail: str, password: str }`                                                    | 200 - Ok \ 400 - Bad request: can't parse `e-mail` \ 404 - Not found: `e-mail` doesn't exist \ 401 Unauthorized: invalid `password`                                                                                  | `password` is a hash |
| list lobbies | GET    |`/rooms/`    |              | 200 - `[{ lobby_name: str, missing_players: int, max_players: int, min_players: int }]`                                | Not implemented in this sprint |
| create lobby | POST   |`/rooms/`    | `{ userId: int, lobby_name: str }`                                                    | 200 - `LOBBY` | Later add in Params: `, max_players?: int, max_players?: int`. For now, min_players = max_players = 5. PRE: user is login |
| join lobby | PATCH    |`/rooms/`    | `{ nick: str, url: str }`                                                    | 200 - `PLAYER` \ 409 - Conflict if: `nick` already exists in this lobby \ 404 - Not found: `url` doesn't exist                                                                                       | Later url endpoint will be `/rooms/<id>`. PRE: user is login |
| start game | PATCH    |`/rooms/`    | `{ url: str }`                                                    |                                      | Later url endpoint will be `/rooms/<id>`. PRE: user is login |

-------------

`LOBBY = { lobby_id: int, lobby_name: str, creation_date: datetimestr, creator_username: str, min_players: int, max_players: int, started: bool }`

`PLAYER = { player_id: int, nick: str, number_player: int, role: str, its_alive: bool, director: bool, minister: bool, game_started: bool, chat_blocked: bool }`

-------------

## Descripción de los endpoints:
 
**login POST /login/** : éste endpoint toma como parámetros en primer lugar un `e-mail` que se supone registrado y único en el sistema, cuyo formato se debe validar (c/c se devuelve un staus code 400 con un mensaje informativo), y además validar que efectivamente exista registrado en el sistema (c/c se devuelve un 404 con un mensaje informativo); en segundo lugar una `password` la cual debe hashearse en la base de datos del sistema para validar que existe registrada (c/c se devuelve un status code de 401 con un mensaje informativo). 

**register POST /user**: este endpoint toma de parámetros `e-mail`, `username`, `password` y `photo`; éstos se encuentran en campos que el agente externo debe completar y el sistema validar. Los campos a llenar son: un `e-mail` que debe ser único, un `username` que también deber ser único, una `password` alfanumérica que debe ser entre 8 a 32 carácteres y una `photo` que es una imagen que se elige entre las predeterminadas en el sistema, con un valor por defecto. Como respuesta devuelve un status code 200 - Ok si no hubo errores de validación, un 409 si el e-mail o el `username` ya está registrado o un 400 como error en el formato del `e-mail` o `password` proporcionados.

**create lobby POST /rooms/new**: este endpoint toma los parámetros `userId`, `lobby_name`, `max_players?` y `min_players?`. El parámetro `userId` es el usuario que será creador de ese lobby lo que le permitirá iniciar la partida cuando desee, el parámetro `lobby_name` debe ser elegido por el usuario obligatatoriamente y es único. Los parámetros `min_players?` y `max_players?` en un futuro podrán asignarse opcionalmente por el usuario creador `userId`, que tendrán valores por default 5 y 10 respectivamente, de lo cual se encargará el front de garantizar que no va a ser menor a 5 ni mayor a 10; en éste sprint serán asignados ambos con valor 5 exclusivamente. En la respuesta de éste endpoint se incluirán además atributos tales como `started`, que será el cual pertenece a el estado de la partida, es decir, si la partida del lobby ha iniciado o no, por default inicia en false; luego `creation_date` que corresponderá a la fecha de creación del lobby.


Nota 1 (KND): para reflejar que un creador de la partida lo sea para poder iniciar una, cómo lo ponemos en la API? solo lo aclaramos documentandolo como restricción?  
 - (Agus): Creo que eso ser arreglará cuando definamos la cuestion de autenticacion. Para mi el pedido POST de iniciar partida tiene la autenticacion y el server checkea que esa autenticacion sea la del dueño
 - (Knd)): estoy de acuerdo, pensaba algo así, no sé el resto (de todas formas deberiamos preguntar si entra en (éste sprint eso)

Nota 2 (KND): Faltan elegir Ministro de magia, emitir proclamación y Finalizar partida (importantes las PRE) y DOCUMENTAR (acá podemos incluir cuáles respectan a users, lobbies, turns/games [public info, personal info, transactions], y especificar qué se hace en cada endpoint (criterios de aceptación))

Nota 3 (Agus): Creo que tenemos que definir toda la API, al menos todo lo que podamos, por lo que yo agregaria ya mismo `max_players` a los parametros de `create lobby`

- (Knd): lo puse en comments a max_players?: int, max_players?: int pq se pidió para éste sprint no incluir ese requerimiento aún, pero calculo que en los próximos los pondremos.


Nota 4 (Agus): Yo diria que el URI de `crear lobby` sea directamente `/rooms`, ya que postear en eso seria inambiguo

- (Knd): estoy de acuerdo, o /romms/, que de hecho así lo vi ahora en el ejemplo de los profes, a todas las URIs/URLs las terminan con /


Nota 5 (Agus) : 'Params' se refiere a los headers o al body del pedido?

- (Knd) se refiere a las inputs o body del pedido.

Nota 6 (Agus) : Cambie `/rooms/join` a `/rooms/<id>` ... diganme si les parece bien

- (Knd) si, de hecho lo puse como comments pq lo pedían poner más adelante, pero ahora quizá podemos ponerle directamente /romms/ y listo, la url la pasamos en Param y se diferencia con otros endpoints igualmente.

Nota 7 (Knd) : cambié number_player por missing_players que es el nro de jugadores faltantes para llegar al mínimo

----
diferencia entre PUT y PATCH: https://www.bbvanexttechnologies.com/como-utilizar-los-metodos-put-y-patch-en-el-diseno-de-tus-apis-restful/ y preguntar al profe cual conviene en join lobby y start game. Resumen: con put hay que especificarle el cuerpo completo en {este caso de un lobby, con path no hace falta, solo un id creo que basta (en éste caso una url)}

status codes: https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html