from Request import Request


class GetAllWaySegments(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("select idFirstPoint, idSecondPoint from segmentStreet")
        points = cursor.fetchall()

        dataTransferObject.segments = []
        for p in points:
            cursor.execute("select * from point where id={}".format(p[1]))
            data1 = cursor.fetchone()
            cursor.execute("select * from point where id={}".format(p[2]))
            data2 = cursor.fetchone()
            dataTransferObject.segments.append({'p1': {'x': data1[1], 'y': data1[2]}, 'p2': {'x': data2[1],
                                                                                             'y': data2[2]}})
        dataTransferObject.status = "OK"
