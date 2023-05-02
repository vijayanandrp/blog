import psycopg2
from datetime import datetime
from config import *


class StateManager(object):
    insert_query = """ INSERT INTO kafkaconnect.states
    (environment, site, connector, task,  
    event_start_time, event_end_time, event_modified_time, 
    restart_count, last_restart_time, is_alerted, is_paused, is_active)
    VALUES (%(environment)s, %(site)s, %(connector)s, %(task)s,  
    %(event_start_time)s, %(event_end_time)s, %(event_modified_time)s, 
    %(restart_count)s, %(last_restart_time)s, %(is_alerted)s, %(is_paused)s, %(is_active)s)
    """
    select_id_query = """
    SELECT id FROM kafkaconnect.states 
    WHERE  environment = '{environment}' AND site = '{site}' AND
    connector = '{connector}' AND task = '{task}' AND is_paused = false AND
    is_active = true AND event_end_time >= '{event_time}';
    """
    
    update_event_time_query = """
    UPDATE kafkaconnect.states 
    SET event_modified_time = %s
    WHERE id = %s
    """
    
    def __init__(self):
        self.conn = psycopg2.connect(database=DB,
                                     host=HOST,
                                     user=USER,
                                     password=PASSWORD,
                                     port=PORT)
        self.cursor = self.conn.cursor()
    
    def insert(self, records):
        if not records:
            return
        
        data = []
        for r in records:
            data.append(
                {
                    "environment": r["environment"],
                    "site": r["site"],
                    "connector": r["connector"],
                    "task": r["task"],
                    "event_start_time": datetime.utcfromtimestamp(r["event_time"]),
                    "event_end_time": datetime.utcfromtimestamp(r["event_time"] + EVENT_END_TIME),
                    "event_modified_time": datetime.utcfromtimestamp(r["event_time"]),
                    "restart_count": 1,
                    "last_restart_time": datetime.now(),
                    "is_alerted": False,
                    "is_paused": False,
                    "is_active": True,
                }
            )
        self.cursor.executemany(self.insert_query, data)
        self.conn.commit()
        

    
    def upsert(self, events):
        insert_records = []
        
        for event in events:
            query  = self.select_id_query.format(environment=event['environment'],   
                                                 site = event["site"],
                                                 connector = event["connector"],
                                                 task = event["task"],
                                                 event_time = datetime.utcfromtimestamp(event["event_time"])
                                                )
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            id_key = [r[0] for r in records]
            id_key = id_key[0] if id_key else insert_records.append(event)
            if not id_key:
                continue
            self.cursor.execute(self.update_event_time_query, (datetime.utcfromtimestamp(event["event_time"]), id_key))
            self.conn.commit()
             
        self.insert(insert_records)
            
            
        
    def check_active_status(self):
        pass
