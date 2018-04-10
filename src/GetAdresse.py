from Request import Request

def getDistance(x1,y1,x2,y2):
    return (x2-x1)**2+(y2-y1)**2

class GetAdresse(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.Status = "Error"

        x = params["coordinateX"]
        y = params["coordinateY"]

        if x is None or y is None:
            dataTransferObject.message = "Пустой запрос строки"
            raise AttributeError

        cursor.execute("SELECT x,y,id FROM point".format(id))

        allPoint = cursor.fetchall()

        mnDist = 1000000000
        mnId = 0


        for curPoint in allPoint:
            curDist = getDistance(curPoint[0], curPoint[1], x, y)
            if mnDist > curDist:
                mnDist = curDist
                mnId = curPoint[2]

        cursor.execute("SELECT name FROM Street WHERE id = '{}'".format(mnId))

        name = cursor.fetchone()

        if name is not None:
            dataTransferObject.address = name

        else:
            cursor.execute("SELECT name FROM Organization WHERE idBuilding = '{}'".format(mnId))
            allOrg = cursor.fetchall()

            for i,curOrg in enumerate(allOrg):
                dataTransferObject.organizations.name[i] = curOrg
            dataTransferObject.organizations.cnt = len(allOrg)