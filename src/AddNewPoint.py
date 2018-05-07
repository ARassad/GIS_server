from Request import Request


class AddNewPoint(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("insert into point(x, y) values({}, {})".format(params['newX'], params['newY']))
        cursor.execute("select id from point where x={} and y={}".format(params['newX'], params['newY']))
        id_new = cursor.fetchone()[0]
        cursor.execute("insert into segmentStreet(firstPoint, secondPoint, street) values({}, {}, '{}')"
                       .format(params['oldId'], id_new, params['streetName']))
        dataTransferObject.status = "OK"
