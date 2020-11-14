# Socket Communication Specification  
The websocket communication allows to send Python *dictionaries*, in such a way that on the Front end we can transform them into **JSON (JavaScript Object Notation)**.  
We **cannot** send *Models*. We can only send plain strings, or python dictionaries.  
This file specifies what the Front end expects from the websocket.  
## **General structure:**  
Sending pure strings are depreciated. Even basic chat will be sent by dictionary. The structure of all messages will be of the form:  

`{ "TYPE": ..., "PAYLOAD": ... }`

The *keys* `TYPE` and `PAYLOAD` should always be present
The value of `TYPE` signals the type of **action** we're sending the player, the value in `PAYLOAD` is relevant information (read: *arguments*) necesary to perform the action.

## Register (POST) /users/
No socket communication
## Login (POST) /login/
No socket communication
## User Information (GET) /users/  
No socket communication
## Update Profile (PATCH) /users/change_profile/
No socket communication
## Change Password (PATCH) /users/change_profile/change_password/
No socket communication
## Create New Lobby (POST) /lobby/
No socket communication
## List Lobbies (GET) /lobby/list_lobbies/
No socket communication  

---  

## Join Lobby (POST) /lobby/{lobby_id}/
`{ "TYPE": "NEW_PLAYER_JOINED", "PAYLOAD": nick }`  
`nick` **:** *string*  

**Send to:** All players in lobby  

---  

## Change Nick (POST) /lobby/{lobby_id}/change_nick
`{ "TYPE": "CHANGED_NICK", "PAYLOAD": payload }`  
`payload` **:** *dictionary*  -- `{ "OLD_NICK": nick, "NEW_NICK": nick }`  
`nick` **:** *string*  

**Send to:** All players in lobby  

---  

## Leave Lobby (DELETE) /lobby/{lobby_id}/
`{ "TYPE": "PLAYER_LEFT", "PAYLOAD": nick }`  
`nick` **:** *string*  

**Send to:** All players in lobby  

---  

## Start Game (DELETE) /lobby/{lobby_id}/start_game/
`{ "TYPE": "START_GAME", "PAYLOAD": game_id }`  
`game_id` **:** *int*  

**Send to:** All players in lobby  

---  

## List Games  
No socket communication  

---  

## Start of Turn *(Various endpoints)*
When we need to choose a new Minister:  
`{ "TYPE": "NEW_MINISTER", "PAYLOAD": minister_nick }`  
`minister_nick` **:** *str*

**Send to:** All players in game  
**Also** send the available candidates for Director to the Minister  

`{ "TYPE": "REQUEST_CANDIDATE", "PAYLOAD": available_candiates }`  
`available_candiates` **:** *list of nicks*  
Example: `{ "TYPE": "REQUEST_CANDIDATE", "PAYLOAD": ["lao", "shiro", "kndlita"] }`  

**Send to:** Current Minister  

---  

## Select Director (POST) /games/{game_id}/select_director/
We need to ask everyone to vote for the candidate the Minister selected:  

`{ "TYPE": "REQUEST_VOTE", "PAYLOAD": candidate_nick}`  
`candidate_nick` **:** *string*

**Send to:** All players in game  

---  
## Vote (PUT) /games/{game_id}/select_director/vote
### If not all votes are entered:  
No socket communication  
### If **ALL VOTES ARE IN**:
`{ "TYPE": "ELECTION_RESULT", "PAYLOAD": votes }`  
`votes` **:** *dictionary with nicks as keys* -- `{ player_nick : vote, ... }`  
Example: `{ "kndlita" : True, "agus" : False, "shiro" : True }`  
`player_nick` **:** *string*  
`vote` **:** *bool* 

**Send to:** All players in game  

### If candidate was **ACCEPTED**:  
`{ "TYPE": "MINISTER_DISCARD", "PAYLOAD": cards }`  
`cards` **:** *list of 3 ints*  -- `[ card1, card2, card3 ]`  
`cardx` **:** *int* *(like on deck)*

**Send to:** Current Minister  

### If candidate was **REJECTED** and **NO** CAOS:  
No socket communication

### If candidate was **REJECTED** and **CAOS**:  
`{ "TYPE": "CAOS_PROCLAMATION", "PAYLOAD": proclamation }`  
`proclamation` **:** *int* *(like on deck)*

**Send to:** All players in game  

---  
## Discard Card (PUT) /games/{game_id}/discard_card/
### If **minister** is discarding  
`{ "TYPE": "DIRECTOR_DISCARD", "PAYLOAD": cards }`  
`cards` **:** *list of 2 ints*  -- `[ card1, card2 ]`  

**Send to:** Current Director  

### If **director** is discarding  
No socket communication  

---
## Post Proclamation (PUT) /games/{game_id}/proclamation/
`{ "TYPE": "PROCLAMATION", "PAYLOAD": proclamation }`  
`proclamation` **:** *int* *(like on deck)*

**Send to:** All players in game  

---
## End Game *(Various Endpoints)*  
`{ "TYPE": "ENDGAME", "PAYLOAD": result }`  
`result` **:** *dictionary*  -- `{ "WINNER" : w, "ROLES" : roles }`  
`w` **:** *int*  (0 == PHOENIX WINS || 1  == VOLDEMORT WINS)  
`roles` **:** *dictionary with nicks as key* -- `{ player_nick: secret_role, ... }`  
Example: `{ "agus": 2, "shiro": 0, "diego": 1 }`  
`secret_role` **:** *int*  (0 == PHOENIX || 1  == DEATH EATER || 2 == VOLDEMORT)  


---
## Trigger Spell *(End of Post Proclamation)*  
### Adivination:
`{ "TYPE": "REQUEST_SPELL", "PAYLOAD": "ADIVINATION" }`  
**Send to:** Current Minister
### Avada Kedavra:
`{ "TYPE": "REQUEST_SPELL", "PAYLOAD": "AVADA_KEDRAVA" }`  
**Send to:** Current Minister

---
## Adivination (GET) /games/{game_id}/spell/prophecy/  
So we can show that the minister is doing this  
`{ "TYPE": "ADIVINATION_NOTICE", "PAYLOAD": minister_nick }`  
`minister_nick` **:** *player_nick*

**Send to:** All players in game  

--- 
## Avada Kedavra
`{ "TYPE": "AVADA_KEDAVRA", "PAYLOAD": victim_nick }`  
`victim_nick` **:** *player_nick*

**Send to:** All players in game  


--- 
## Chat
`{ "TYPE": "CHAT", "PAYLOAD": message }`  
`message` **:** *string*
  
---  
# Python Dictionaries:  
## Initialization  
There are two common ways to create a dictionary. One is already with some keys we're going to use:  

`myDict = { "KEY_1" : 1, "KEY_2" : 2 }`  

The other is creating a empty one and then adding the vales 1 by 1:  

`myDict = {}`  
`myDict["KEY_1"] = 1`  
`myDict["KEY_2"] = 2`  

This can be done with loops:  
    
    myDict = {}
    for (i in range(1, 11)):
        key = f"KEY_{i}"
        myDict[key] = i

## Subdictionaries (dictionaries as value)  
Pretty much anything (except classes) can be put as value and key of a dictionary. keys must be immutable (string, ints, ...)  
But values can be that and also **Lists** or other **dictionaries**  

`subdict = { "KEY_A" : "SOMETHING", "KEY_B" : 4 }`  
`myDict = { "KEY_1" : "SOME NAME", "KEY_2" : subdict }` 

## Lists of values:  
If we need to send a list of entries with information about the players for example, we simply can construct the subdictionary and then put it as value:  

    players = dbe.get_players_by...(...) # get players
    subdict = {}
    for player in players:
        player_vote = player...vote # get vote
        subdict[player.player_nick] = player_vote
    finalDict = { "TYPE": "ELECTION_RESULT", "VOTES": subdict }
    await ... broadcast ... (..., message=finalDict) # Send socket  

