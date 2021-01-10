import sqlite3
import json

def create_ruleDb(db_name,table_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        query = 'create table '+table_name+' (ruleId, ruleData)'
        cur.execute(query)
        con.commit()
    except:
        pass
    con.close()


def addNsiforEngine(db_name,table_name,ruleId,ruleData):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.execute('insert into '+ table_name +' (ruleId,ruleData) values (?, ?)',[ruleId,ruleData])
        con.commit()
    except:
        pass
    cur.close()    
    return 0


def updateNsiStatus(db_name,table_name,ruleId,ruleData):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.execute('update '+ table_name+' set ruleData = "'+ ruleData +'" where ruleId = "' + ruleId + '"')
        con.commit()
    except:
        pass
    cur.close() 
    return 0

def get_fromDB(db_name,table_name,ruleId):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.execute('select ruleData from '+table_name+' where ruleId = "' + ruleId + '"'  )
        result = cur.fetchone()[0]
    except:
        result = None
    cur.close()
    return result


