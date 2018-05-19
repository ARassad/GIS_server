from Request import Request


class Registration(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("select id from AdminInfo where login='{}' and password='{}'".format(params['login'],
                                                                                            params['password']))
        dataTransferObject.success = False
        data = cursor.fetchall()
        if data is None:
            dataTransferObject.success = True
            cursor.execute("insert into AdminInfo(login, password) values('{}', '{}')".format(params['login'],
                                                                                              params['password']))
