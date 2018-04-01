import pyodbc
import json
from abc import ABCMeta, abstractmethod, abstractproperty

pyodbc.pooling = False


def connect_database():
    server = 'poaskbs.database.windows.net'
    database = 'kbs'
    username = 'poas_root'
    password = 'P0asgovno'
    driver = '{ODBC Driver 13 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER={};PORT=1433;SERVER={};PORT=1443;DATABASE={};UID={};PWD={}'.format
                          (driver, server, database, username, password), autocommit=True)
    cursor = cnxn.cursor()
    return cursor, cnxn


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
        except:
            print("Исключение при обработке запроса : {}".format(type(self).__name__))
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
