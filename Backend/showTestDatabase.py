# run with $ python3 showTestDatabase.py
import config 
config.database = "test_data_base.sqlite"
import db_functions as dbf

dbf.showDatabase()