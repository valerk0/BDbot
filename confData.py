__author__ = 'Valery'
import configparser

class confData(object):
    def __init__(self,file,section):
        self.__IniFile=configparser.ConfigParser()
        self.__IniFile.read([file])
        self.__section=section

    @property
    def params(self):
        R={}
        R.update(self.__IniFile[self.__section])
        return R

