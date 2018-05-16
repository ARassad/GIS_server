import sqlite3
import json
from abc import ABCMeta, abstractmethod, abstractproperty
import traceback
import pyodbc

def connect_database():
    server = 'MSI'
    database = 'GIS'
    driver = '{ODBC Driver 13 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER={};SERVER={};Trusted_Connection=Yes;DATABASE={}'.format(driver, server, database), autocommit=True)


    return cnxn.cursor(), cnxn


class DataTransferObject:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Request:
    __metaclass__ = ABCMeta

    def __call__(self, params):

        dto = DataTransferObject()
        dto.status = "Succesful"
        cursor, connect = connect_database()

        try:
            if self.verification_params(params):
                self.request(cursor, params, dto)
            else:
                raise BaseException
        except Exception as e:
            print("Исключение при обработке запроса : {}".format(type(self).__name__))
            traceback.print_exc()
            dto.status = "Error"
        finally:
            cursor.close()
            connect.close()

        return dto.toJSON()

    @staticmethod
    @abstractmethod
    def request(cursor, params, dto):
        raise NotImplementedError

    @staticmethod
    def verification_params(params):
        return True
