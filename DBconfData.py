__author__ = 'Valery'
import configparser

class DBconfData(object):
    def __init__(self):
        self.__IniFile=configparser.ConfigParser()
        self.__IniFile.read(['dbconfig.ini'])

    @property
    def db_params(self):
        R={}
        R.update(self.__IniFile['DATABASE'])
        return R

DBconf=DBconfData()