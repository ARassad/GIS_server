from Request import Request
from GetAddresse import getDistance


def pointStreet(cursor, x, y):
    cursor.execute("SELECT x,y,id FROM point")

    allPoint = cursor.fetchall()

    mnDist = 1000000000
    mnId = 0

    for curPoint in allPoint:
        curDist = getDistance(curPoint[0], curPoint[1], x, y)
        cursor.execute("SELECT idStreet FROM segmentStreet WHERE idFirstPoint = '{}' OR idSecondPoint = '{}'".format(curPoint[2], curPoint[2]))
        if cursor.fetchone() is not None and mnDist > curDist:
            mnDist = curDist
            mnId = curPoint[2]
    return mnId


class GetRoute(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.status = "Error"
        dataTransferObject.points = []
        x1 = params["coordinateX1"]
        y1 = params["coordinateY1"]

        x2 = params["coordinateX2"]
        y2 = params["coordinateY2"]

        if x1 is None or y1 is None or x2 is None or y2 is None:
            dataTransferObject.message = "Пустой запрос строки"
            raise AttributeError

        dataTransferObject.points.append((x1, y1))

        f = pointStreet(cursor, x1, y1)
        t = pointStreet(cursor, x2, y2)
        cursor.execute("SELECT id FROM Track WHERE idVertex1={} AND idVertex2={}".format(f, t))
        curEdge = cursor.fetchone()

        if curEdge is None:
            dataTransferObject.message = "Данный путь не построен, обратитесь к системному администратору"
            return AttributeError

        cursor.execute("SELECT idVertex FROM VertexTrack WHERE idTrack = '{}'".format(curEdge[0]))

        allPoint = cursor.fetchall()

        for i, curPoint in enumerate(allPoint):
            cursor.execute("SELECT x,y FROM point WHERE id = '{}'".format(curPoint[0]))

            pt = cursor.fetchone()

            if pt is None:
                dataTransferObject.message = \
                    "При построении пути не была найдена точка с идентификатором: {}".format(id)
                return AttributeError

            dataTransferObject.points.append((pt[0], pt[1]))

        dataTransferObject.points.append((x2, y2))
        dataTransferObject.status = "OK"