# run with $ python3 showDatabase.py
import config 
config.database = "data_base.sqlite"
#config.database = "test_data_base.sqlite"
import db_functions as dbf

dbf.showDatabase()