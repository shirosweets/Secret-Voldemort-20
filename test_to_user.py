#test for user db functions
#from db_entities_relations import *
#from db_functions import *

#insert_user("s@gmail.com", "s", "12345p", None)
#insert_user("h@gmail.com", "h", "12345p", "hola")

# in terminal
#venv activated
#python
#from db_entities_relations import *
#from db_functions import * 
# User.select().show()

import hashlib 
print ("The available algorithms are : ", end ="") 
for h in hashlib.algorithms_guaranteed:
    print(h)

st = "contraseñaalgorara"
hashedResult = hashlib.sha256(st.encode()).hexdigest()
print(hashedResult)
#print (for h in (hashlib.algorithms_guaranteed) 