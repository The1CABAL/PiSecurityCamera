
import os
import Data.GlobalVars as cfg
from Classes.SQLITE import SQLITE as SQL


def SetUp():
    home = os.getcwd()
    SQL.create_dbo(home)
    os.chdir(home)
    os.makedirs(home + '/recordings', exist_ok=True)
    cfg.recordings = os.getcwd()
    os.chdir(home)


def get_settings():
    config_dict = SQL.get_config()

    AppId = config_dict['ApplicationId']
    SelfStream = config_dict['StreamToSelf']
    config_ip = config_dict['SendToIp']
    config_port = config_dict['SendToPort']

    return AppId, SelfStream, config_ip, config_port