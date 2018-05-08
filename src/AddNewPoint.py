from Request import Request


class AddNewPoint(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("insert into point(x, y) OUTPUT INSERTED.id values({}, {})".format(params['newX'],
                                                                                          params['newY']))
        id_new = cursor.fetchone()[0]

        cursor.execute("select id from Street where name='{}'".format(params['streetName']))
        id_street = cursor.fetchone()
        if id_street is None:
            cursor.execute("insert into Street(name, pointId) OUTPUT INSERTED.id values('{}', {})"
                           .format(params['streetName'], id_new))
            id_street = cursor.fetchone()[0]

        cursor.execute("insert into segmentStreet(idFirstPoint, idSecondPoint, idStreet) values({}, {}, {})"
                       .format(params['oldId'], id_new, id_street))
        dataTransferObject.status = "OK"


