from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy, ConsistencyLevel
from cassandra.query import tuple_factory

class Cassandra:
    def __init__(self):
        self.profile = ExecutionProfile(
            load_balancing_policy=WhiteListRoundRobinPolicy(['127.0.0.1']),
            retry_policy=DowngradingConsistencyRetryPolicy(),
            consistency_level=ConsistencyLevel.LOCAL_QUORUM,
            serial_consistency_level=ConsistencyLevel.LOCAL_SERIAL,
            request_timeout=15,
            row_factory=tuple_factory)
        self.cluster = Cluster(execution_profiles={
                               EXEC_PROFILE_DEFAULT: self.profile})
        self.session = self.cluster.connect()
        self.key_space = None
        self.table_name = None

    def test_connection(self):
        print('Test Connection ')
        print(self.session.execute(
            "SELECT release_version FROM system.local").one())
        print(self.session.execute(
            "SELECT cluster_name, listen_address FROM system.local").one())

    def connection_details(self):
        """ get the details of keyspace and table name"""
        print('KeySpace = ', self.key_space)
        print('Tablename = ', self.table_name)

    def create_keyspace(self, key_space='master_db'):
        """ create keyspace """
        if key_space and key_space.lower() != self.key_space:
            self.key_space = key_space.lower()

        query = """CREATE KEYSPACE IF NOT EXISTS %s WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };""" % self.key_space
        print(query)
        self.session.execute(query)
        self.use_space()

    def use_space(self):
        # self.session.set_keyspace('users') # or you can do this instead
        query = 'USE {};'.format(self.key_space)
        print(query)
        self.session.execute(query)

    def create_table(self, table_name='meta_data'):
        """ create table """
        if table_name and table_name.lower() != self.table_name:
            self.table_name = table_name.lower()
        query = """CREATE TABLE IF NOT EXISTS {} (SourceFile TEXT, artifact_id UUID, source_id TEXT, PRIMARY KEY (source_id, artifact_id));""".format(
            self.table_name)
        print(query)
        self.session.execute(query)

    def get_columns(self):
        """ get columns from the table """
        query = """SELECT column_name FROM system_schema.columns WHERE keyspace_name = '{}' AND table_name = '{}';""".format(
            self.key_space, self.table_name)
        print(query)
        cols = self.session.execute(query)
        cols = [col[0] for col in cols]
        print('Column names - ', cols)
        return cols

    def add_missing_column(self, column):
        """ add the missing column name to the table """

        if 'date' in column:
            data_type = 'TIMESTAMP'
        elif any(x in column for x in ['height', 'width', 'depth']):
            data_type = 'INT'
        else:
            data_type = 'TEXT'

        query = """ALTER TABLE {} ADD {} {};""".format(
            self.table_name, column, data_type)
        print(query)
        self.session.execute(query)

    @staticmethod
    def parse_key(key):
        """ remove special character in the key name """
        return key.strip().lower().replace(':', '_')

    @staticmethod
    def adjust_timestamp(timestamp):
        try:
            from time import gmtime, strftime
            time_zone = strftime("%z", gmtime())
            date = timestamp.split(' ')[0].replace(':', '-')
            time = timestamp.split(' ')[1].split('-')[0]

            if any(x in timestamp for x in ['+', 'Z']):
                return ' '.join([date, time])

            timestamp = ' '.join([date, time, time_zone])
            if "0000-00-00" in timestamp:
                return ""
            return timestamp
        except Exception as err:
            print('Error - timestamp parsing - ', err)
            print('>>>>>>>>>>>>> - ', timestamp)
            return ""

    def parse_json(self, value):
        """ convert JSON to string and convert ' to " """
        parsed = dict()
        for key in value.keys():
            key1 = '"{}"'.format(self.parse_key(key))
            if any(x in key1 for x in ['height', 'width', 'depth']):
                value1 = '{}'.format(value[key])
            elif 'date' in key1:
                value1 = '"{}"'.format(self.adjust_timestamp(value[key]))
            else:
                value1 = '"{}"'.format(value[key])

            parsed[key1] = value1
        parsed = str(parsed).replace("'", '').replace('\\', '')
        print(parsed)
        return parsed

    def insert_json(self, value):
        """ insert json data to the table """
        keys = value.keys()
        keys = [self.parse_key(key) for key in keys]

        cols = self.get_columns()
        missing_cols = list(set(keys) - set(cols))
        if missing_cols:
            [self.add_missing_column(column=col)
             for col in missing_cols if col]

        value = self.parse_json(value)
        query = """INSERT INTO {} JSON '{}';""".format(self.table_name, value)
        print(query)
        self.session.execute(query)

    def drop_keyspace(self):
        query = 'DROP KEYSPACE IF EXISTS {};'.format(self.key_space)
        print(query)
        self.session.execute(query)

    def drop_table(self):
        query = 'DROP TABLE IF EXISTS {};'.format(self.table_name)
        print(query)
        self.session.execute(query)

    def truncate_table(self):
        query = 'TRUNCATE TABLE {};'.format(self.table_name)
        print(query)
        self.session.execute(query)

#
# if __name__ == '__main__':
#     c = Cassandra()
#     c.test_connection()
#     c.create_keyspace()
#     c.create_table()
#     c.get_columns()
#     c.connection_details()
#
#     value = {
#         "Composite:ImageSize": "64x58",
#         "Composite:Megapixels": 0.004,
#         "ExifTool:ExifToolVersion": 10.8,
#         "File:Directory": "/home/vijay-works/Downloads/Template_Data/img",
#         "File:FileAccessDate": "2020:06:06 05:38:56-07:00",
#         "File:FileInodeChangeDate": "2020:03:29 09:55:03-07:00",
#         "File:FileModifyDate": "2019:03:18 04:22:24-07:00",
#         "File:FileName": "home.png",
#         "File:FilePermissions": "rw-rw-r--",
#         "File:FileSize": "5.8 kB",
#         "File:FileType": "PNG",
#         "File:FileTypeExtension": "png",
#         "File:MIMEType": "image/png",
#         "PNG:BackgroundColor": "255 255 255",
#         "PNG:BitDepth": 8,
#         "PNG:ColorType": "RGB with Alpha",
#         "PNG:Compression": "Deflate/Inflate",
#         "PNG:Filter": "Adaptive",
#         "PNG:ImageHeight": 58,
#         "PNG:ImageWidth": 64,
#         "PNG:Interlace": "Noninterlaced",
#         "SourceFile": "/home/vijay-works/Downloads/Template_Data/img/home.png",
#         "artifact_id": "ee863eef-304e-476b-93a9-808765d701b8",
#         "source_id": "3D1RYEF6"
#     }
#
#     c.insert_json(value)
#     c.truncate_table()
#     c.drop_table()
#     c.drop_keyspace()
