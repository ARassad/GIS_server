from Request import Request


class Authorization(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("select id from AdminInfo where login='{}' and password='{}'".format(params['login'],
                                                                                            params['password']))
        dataTransferObject.isAuth = False
        data = cursor.fetchall()
        if data is not None:
            dataTransferObject.isAuth = True
