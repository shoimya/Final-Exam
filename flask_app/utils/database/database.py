import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

import string
import random

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['users','nfts','transaction','institutions','positions','experiences','skills','feedback','wallet']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        ''' FILL ME IN WITH CODE THAT CREATES YOUR DATABASE TABLES.'''

        #should be in order or creation - this matters if you are using forign keys.
         
        if purge:
            for table in self.tables[::-1]:
                self.query(f"""DROP TABLE IF EXISTS {table}""")
            
        # Execute all SQL queries in the /database/create_tables directory.
        for table in self.tables:
            
            #Create each table using the .sql file in /database/create_tables directory.
            with open(data_path + f"create_tables/{table}.sql") as read_file:
                create_statement = read_file.read()
            self.query(create_statement)

            # Import the initial data
            try:
                params = []
                with open(data_path + f"initial_data/{table}.csv") as read_file:
                    scsv = read_file.read()            
                for row in csv.reader(StringIO(scsv), delimiter=','):
                    params.append(row)
            
                # Insert the data
                cols = params[0]; params = params[1:] 
                self.insertRows(table = table,  columns = cols, parameters = params)
            except:
                print('no initial data')

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        
        # Check if there are multiple rows present in the parameters
        has_multiple_rows = any(isinstance(el, list) for el in parameters)
        keys, values      = ','.join(columns), ','.join(['%s' for x in columns])
        
        # Construct the query we will execute to insert the row(s)
        query = f"""INSERT IGNORE INTO {table} ({keys}) VALUES """
        if has_multiple_rows:
            for p in parameters:
                query += f"""({values}),"""
            query     = query[:-1] 
            parameters = list(itertools.chain(*parameters))
        else:
            query += f"""({values}) """                      
        
        insert_id = self.query(query,parameters)[0]['LAST_INSERT_ID()']         
        return insert_id

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user',entry=0, key=""):
        tab = "users"
        params = ["role","email","password","entry","user_key"]
        vals = []
        enc_pass = self.onewayEncrypt(password) #encrypt the password
        vals.append(role)
        vals.append(email)
        vals.append(enc_pass)
        vals.append(entry)
        vals.append(key)
        self.insertRows(table=tab,columns=params,parameters=vals) #new user inserted to db
        self.insertRows(table="wallet",columns = ["user_key"],parameters=[key])
        return {'success': 1}


    def authenticate(self, email='me@email.com', password='password'):
        users = self.query()
        print(users)
        for item in users:
            if item['email'] == email: 
                if self.onewayEncrypt(password) == item['password']:     
                    return {'success': 1}
        return {'success': 0}


    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message
    

    def getResumeData(self):
        result = {}
        inst = self.query("SELECT * FROM institutions;")
        pos = self.query("SELECT * FROM positions;")
        exp = self.query("SELECT * FROM experiences;")
        skills = self.query("SELECT * FROM skills;")
	
        for inst_row in inst:
            # extract the institution ID and create a dictionary for it in the result
            inst_id = inst_row['inst_id']
            result[inst_id] = {
                'name': inst_row['name'],
                'type': inst_row['type'],
                'department': inst_row['department'],
                'address': inst_row['address'],
                'city': inst_row['city'],
                'state': inst_row['state'],
                'zip': inst_row['zip'],
                'positions': {}
            }
            
            # iterate over the positions data for this institution
            for pos_row in pos:
                if pos_row['inst_id'] == inst_id:
                    # extract the position ID and create a dictionary for it in the institution's positions
                    pos_id = pos_row['position_id']
                    result[inst_id]['positions'][pos_id] = {
                        'title': pos_row['title'],
                        'start_date': pos_row['start_date'],
                        'end_date': pos_row['end_date'],
                        'responsibilities': pos_row['responsibilities'],
                        'experiences': {}
                    }
                    
                    # iterate over the experiences data for this position
                    for exp_row in exp:
                        if exp_row['position_id'] == pos_id:
                            # extract the experience ID and create a dictionary for it in the position's experiences
                            exp_id = exp_row['experience_id']
                            result[inst_id]['positions'][pos_id]['experiences'][exp_id] = {
                                'name': exp_row['name'],
                                'start_date': exp_row['start_date'],
                                'end_date': exp_row['end_date'],
                                'description': exp_row['description'],
                                'hyperlink': exp_row['hyperlink'],
                                'skills': {}
                            }
                            
                            # iterate over the skills data for this experience
                            for skill_row in skills:
                                if skill_row['experience_id'] == exp_id:
                                    # extract the skill ID and create a dictionary for it in the experience's skills
                                    skill_id = skill_row['skill_id']
                                    result[inst_id]['positions'][pos_id]['experiences'][exp_id]['skills'][skill_id] = {
                                        'name': skill_row['name'],
                                        'skill_level': skill_row['skill_level']
                                    }
        # Pulls data from the database to genereate data like this:
        return result
    
    def generate_key(self,length=12):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        key_ = ''.join(random.choices(chars, k=length))
        return key_


