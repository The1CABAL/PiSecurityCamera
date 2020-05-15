
from flask import request
import Data.GlobalVars as cfg
import sqlite3
import os

class SQLITE():
    def create_dbo(home):

        data_path = (home+'/database')
        cfg.data_path = data_path
        filename = 'PiCamData.sqlite3'

        os.makedirs(data_path, exist_ok=True)

        conn = sqlite3.connect(data_path + filename)
        cfg.conn = conn
        c = conn.cursor()

        c.execute('CREATE TABLE IF NOT EXISTS Cameras (Name TEXT NOT NULL, IP TEXT NOT NULL, PRIMARY KEY (Name) ON CONFLICT REPLACE)')

        c.execute('CREATE TABLE IF NOT EXISTS Config (KeyName TEXT NOT NULL, KeyValue TEXT NOT NULL, Description TEXT NOT NULL, PRIMARY KEY (KeyName) ON CONFLICT REPLACE)')

        ##Insert Baseline "Out of Box" data

        c.execute('INSERT OR IGNORE INTO Cameras VALUES ("Main", "localhost")')

        baseline_config = [
            ('ApplicationId', '0', '0 is the default setting where camera is by itself. 1 means the solution is running solely as a server'),
            ('StreamToSelf', '0', 'If the server is being hosted on a camera (not recommended) then '),
            ('SendToIp', '0.0.0.0', 'Server IP Address'),
            ('SendToPort', '5555', 'Server Port')
            ]

        c.executemany('INSERT OR IGNORE INTO Config VALUES (?,?,?)', baseline_config)

        conn.commit()
        c.close()

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
        returned = []
        names = []
        ips = []
        if request.method == 'POST':

            form = request.form
            for v in form:
                returned.append(v)
            name_ids = (returned[::2])
            ip_ids = (returned[1::2])

            for n in name_ids:
                names.append(request.values[n])

            for i in ip_ids:
                ips.append(request.values[i])

            data_path = cfg.dataPath
            filename = 'PiCamData.sqlite3'
            conn = sqlite3.connect(data_path + filename)
            c = conn.cursor()

            for s in range(len(names)):
                c.execute("INSERT INTO Cameras (Name, IP) VALUES ('" + names[s] + "','"+ips[s]+"')")

            conn.commit()
            c.close()
            conn.close()

    def get_cams():
        cam_dict = {}
        conn = sqlite3.connect(cfg.data_path + 'PiCamData.sqlite3')
        c = conn.cursor()

        c.execute('SELECT Name, IP FROM Cameras')
        result = c.fetchall()

        for row in result:
            cam = {row[0]:row[1]}
            cam_dict.update(cam)

        return cam_dict