from Request import Request
from GetAdresse import getDistance


def pointStreet(x, y):
    cursor.execute("SELECT x,y,id FROM point".format(id))

    allPoint = cursor.fetchall()

    mnDist = 1000000000
    mnId = 0

    for curPoint in allPoint:
        curDist = getDistance(curPoint[0], curPoint[1], x, y)
        cursor.execute(
            "SELECT street FROM segmentAddress WHERE firstPoint = '{}' OR secondPoint = '{}'".format(curPoint[2],
                                                                                                     curPoint[2]))

        if cursor.fetchone() is not None and mnDist > curDist:
            mnDist = curDist
            mnId = curPoint[2]
    return mnId


class GetRoute(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.Status = "Error"

        x1 = params["coordinateX1"]
        y1 = params["coordinateY1"]

        x2 = params["coordinateX2"]
        y2 = params["coordinateY2"]

        if x1 is None or y1 is None or x2 is None or y2 is None:
            dataTransferObject.message = "Пустой запрос строки"
            raise AttributeError

        dataTransferObject.points[0].x = x1
        dataTransferObject.points[0].y = y1

        cursor.execute("SELECT id FROM Track WHERE idVertex1 = '{}' AND idVertex2 = '{}'".format(pointStreet(x1, y1),
                                                                                             pointStreet(x2, y2)))

        cursor.execute("SELECT idVertex FROM VertexTrack WHERE idTrack = '{}'".format(cursor.fetchone()))

        allPoint = cursor.fetchall()

        for i, curPoint in enumerate(allPoint):
            cursor.execute("SELECT x,y FROM point WHERE id = '{}'".format(curPoint))

            pt = cursor.fetchone()

            if pt is not None:
                dataTransferObject.points[i + 1].x = pt[0]
                dataTransferObject.points[i + 1].y = pt[1]

        cnt = len(allPoint)

        dataTransferObject.points[cnt + 1].x = x2
        dataTransferObject.points[cnt + 1].y = y2
        dataTransferObject.cnt = cnt + 2