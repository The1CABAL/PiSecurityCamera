
import Data.GlobalVars as cfg
import sqlite3
import os

class SQLITE():
    def create_dbo(home):

        data_path = (home+'/database')
        filename = 'PiCamData.sqlite3'

        os.makedirs(data_path, exist_ok=True)

        conn = sqlite3.connect(data_path + filename)
        cfg.conn = conn
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS Cameras (Name TEXT NOT NULL, IP TEXT NOT NULL, PRIMARY KEY (Name) ON CONFLICT REPLACE)')

        c.execute('CREATE TABLE IF NOT EXISTS Config (KeyName TEXT NOT NULL, KeyValue TEXT NOT NULL, Description TEXT NOT NULL, PRIMARY KEY (KeyName) ON CONFLICT REPLACE)')

        baseline_config = [
            ('ApplicationId', '0', '0 is the default setting where camera is by itself. 1 means the camera is streaming to a server. 2 means the current machine IS the server'),
            ('StreamToSelf', '0', 'If the server is being hosted on a camera (not recommended) then '),
            ('SendToIp', '0.0.0.0', 'Server IP Address'),
            ('SendToPort', '5555', 'Server Port')
            ]


        c.executemany('INSERT OR IGNORE INTO Config VALUES (?,?,?)', baseline_config)

    def get_config():
        config_dict = {}
        conn = cfg.conn
        c = conn.cursor()

        c.execute('SELECT KeyName, KeyValue FROM Config')
        result = c.fetchall()

        for row in result:
            add = {row[0]:row[1]}
            config_dict.update(add)

        return config_dict

    def insert_camera_ips():
        new_cams = []
        if request.method == 'POST':
            Cameras = {
                'CameraNameOne':'CameraIpOne'
                }

            for v in Cameras:
                if not request.form[v]:
                    pass
                else:
                    new_cams.append(str(request.form[v]), str(request.form[v]))

            conn = cfg.conn
            c = conn.cursor()

            c.executemany('INSERT INTO Cameras (Name, IP) VALUES (?,?);', new_cams)

            conn.commit()
            c.close()