import psycopg2
import logging
from lib.kafkaconnect_api import KafkaConnectApi
from config import *
from lib.commons import set_logger, get_tabulate_fmt
from lib.slack_api import SlackApi


log = logging.getLogger(__name__)
set_logger(log)


class StateManager(object):
    states_tbl_insert = """ 
    INSERT INTO kafkaconnect.states
        (environment, site, connector, task,  
        start_time, end_time, modified_time, 
        restart_count, alert, pause, active)
    VALUES 
        (%(environment)s, %(site)s, %(connector)s, %(task)s,  
        %(start_time)s, %(end_time)s, %(modified_time)s, 
        %(restart_count)s, %(alert)s, %(pause)s, %(active)s)
    """

    restart_log_tbl_insert = """ 
    INSERT INTO kafkaconnect.restart_log
        (state_id, modified_time)
    VALUES 
       (%s, %s)
    """

    alert_log_tbl_insert = """ 
    INSERT INTO kafkaconnect.alert_log
        (state_id, modified_time)
    VALUES 
       ( %(state_id)s, %(modified_time)s)
    """

    pause_log_tbl_insert = """ 
    INSERT INTO kafkaconnect.pause_log
        (state_id, modified_time)
    VALUES 
       (%s, %s)
    """

    query_states_tbl = """
    SELECT state_id, restart_count, start_time, end_time  
    FROM 
        kafkaconnect.states 
    WHERE  
        environment = '{environment}'
        AND site = '{site}' 
        AND connector = '{connector}' 
        AND task = '{task}' 
        AND alert = false 
        AND pause = false 
        AND active = true 
        AND end_time > {event_time};
    """

    update_states_tbl_restrat_count = """
    UPDATE 
        kafkaconnect.states 
    SET 
        restart_count = %s,
        modified_time = %s
    WHERE 
        state_id = %s
    """

    update_states_tbl_flags = """
    UPDATE kafkaconnect.states 
    SET 
        alert = %s,
        pause = %s,
        active = %s,
        modified_time = %s
    WHERE 
        state_id = %s
    """

    query_state_id_to_alerted = """
    SELECT s.*
    FROM 
        kafkaconnect.states s 
    LEFT JOIN 
        kafkaconnect.alert_log a
    ON 
        a.state_id = s.state_id  
    WHERE 
        s.alert = true 
        AND a.alert_id is null
    """

    def __init__(self):
        self.conn = psycopg2.connect(
            database=DB, host=HOST, user=USER, password=PASSWORD, port=PORT
        )
        self.cursor = self.conn.cursor()

    def insert(self, records):
        """insert records to the table"""

        if not records:
            return

        data = [
            {
                "environment": event["environment"],
                "site": event["site"],
                "connector": event["connector"],
                "task": event["task"],
                "start_time": event["event_time"],
                "end_time": event["event_time"] + EVENT_END_TIME,
                "modified_time": event["event_time"],
                "restart_count": 0,
                "alert": False,
                "pause": False,
                "active": True,
            }
            for event in records
        ]
        self.cursor.executemany(self.states_tbl_insert, data)
        self.conn.commit()

    def upsert(self, events):
        """update records to the table and manages the incident, restart timing, alerting and pause jobs"""

        if not events:
            return

        insert_records = []

        for event in events:
            environment = event["environment"]
            env = ENVIRONMENT_V1[environment]
            site = event["site"]
            connector = event["connector"]
            task = event["task"]
            event_time = event["event_time"]

            query = self.query_states_tbl.format(
                environment=environment,
                site=site,
                connector=connector,
                task=task,
                event_time=event_time,
            )
            self.cursor.execute(query)
            records = self.cursor.fetchall()

            if not records:
                insert_records.append(event)
                continue

            columns = [desc[0] for desc in self.cursor.description]
            result = [dict(zip(columns, row)) for row in records][0]

            state_id = result["state_id"]
            new_restart_count = result["restart_count"] + 1
            start_time = result["start_time"]
            end_time = result["end_time"]
            exponential_time_gap = 2 ** (new_restart_count - 1) * 60

            if end_time > event_time >= (start_time + exponential_time_gap):
                cluster = KafkaConnectApi(env=env, site=site)
                cluster.restart_task(connector, task)  # RESTART JOB
                self.cursor.execute(
                    self.update_states_tbl_restrat_count,
                    (new_restart_count, event_time, state_id),
                )
                self.cursor.execute(self.restart_log_tbl_insert, (state_id, event_time))
            elif event_time + 1 > end_time:
                cluster = KafkaConnectApi(env=env, site=site)
                cluster.pause_connector(connector)  # PAUSE JOB
                self.cursor.execute(
                    self.update_states_tbl_flags,
                    (True, True, False, event_time, state_id),
                )
                self.cursor.execute(self.pause_log_tbl_insert, (state_id, event_time))
            self.conn.commit()
        self.insert(insert_records)

    def alert(self):
        """sends the alerts to the slack channel"""

        self.cursor.execute(self.query_state_id_to_alerted)
        records = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        result = [dict(zip(columns, row)) for row in records]

        if not result:
            log.debug("No Alerts found.")
            return

        with open(SLACK_TMP_FILE, "w") as fp:
            fp.write(get_tabulate_fmt(result))

        slack = SlackApi()
        slack.upload_file(file_name=SLACK_TMP_FILE, text=SLACK_SUBJECT)

        data = [
            {"state_id": event["state_id"], "modified_time": event["modified_time"]}
            for event in result
        ]
        self.cursor.executemany(self.alert_log_tbl_insert, data)
        self.conn.commit()
