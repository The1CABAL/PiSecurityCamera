
import os
from Classes.SQLITE import SQLITE as SQL


def SetUp():
    home = os.getcwd()
    SQL.create_dbo(home)


def get_settings():
    config_dict = SQL.get_config()

    AppId = config_dict['ApplicationId']
    SelfStream = config_dict['StreamToSelf']
    config_ip = config_dict['SendToIp']
    config_port = config_dict['SendToPort']

    return AppId, SelfStream, config_ip, config_port