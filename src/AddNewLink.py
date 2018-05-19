from Request import Request


class AddNewLink(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("select id from AdminInfo where login='{}' and password='{}'".format(params['login'],
                                                                                            params['password']))
        dataTransferObject.status = "Error"
        data = cursor.fetchall()
        if data is not None:
            cursor.execute("select id from Street where name='{}'".format(params['streetName']))
            id_street = cursor.fetchone()
            if id_street is None:
                cursor.execute("insert into Street(name, pointId) OUTPUT INSERTED.id values('{}', {})"
                               .format(params['streetName'], params['point1']))
                id_street = cursor.fetchone()[0]
            else:
                id_street = id_street[0]

            cursor.execute("insert into segmentStreet(idFirstPoint, idSecondPoint, idStreet) values({}, {}, {})"
                           .format(params['point1'], params['point2'], id_street))
            dataTransferObject.status = "OK"
