from Request import Request


class AddNewPoint(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("select id from AdminInfo where login='{}' and password='{}'".format(params['login'],
                                                                                            params['password']))
        dataTransferObject.status = "Error"
        data = cursor.fetchall()
        if data is not None:
            cursor.execute("insert into point(x, y) values({}, {})".format(params['newX'], params['newY']))
            id_new = cursor.lastrowid

            cursor.execute("select id from Street where name='{}'".format(params['streetName']))
            id_street = cursor.fetchone()
            if id_street is None:
                cursor.execute("insert into Street(name, pointId) values('{}', {})"
                               .format(params['streetName'], id_new))
                id_street = cursor.lastrowid

            cursor.execute("insert into segmentStreet(idFirstPoint, idSecondPoint, idStreet) values({}, {}, {})"
                           .format(params['oldId'], id_new, id_street))
            dataTransferObject.status = "OK"
