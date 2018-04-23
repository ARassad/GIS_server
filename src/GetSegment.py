from Request import Request
from GetAddresse import getDistance

def getCoordPoint(cursor, idPoint):
    cursor.execute("select x,y from point where id = '{}'".format(idPoint))
    pt = cursor.fetchone()
    return pt[0], pt[1]

class GetSegment(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.status = "Error"
        cursor.execute("select idFirstPoint,idSecondPoint from segmentStreet".format())
        f = open('segment.txt', 'w+')
        allSegment = cursor.fetchall()

        f.write(str(len(allSegment)) + '\n')

        for segment in allSegment:
            x1, y1 = getCoordPoint(cursor, segment[0])
            x2, y2 = getCoordPoint(cursor, segment[1])
            dist = getDistance(x1, y1, x2, y2)
            f.write(str(segment[0]) + ' ' + str(segment[1]) + ' ' + str(dist) + '\n')

        dataTransferObject.status = "OK"
