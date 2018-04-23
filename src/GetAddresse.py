from Request import Request
from GetResult import getOrganization

def getDistance(x1, y1, x2, y2):
    return ((int)(x2)-(int)(x1))**2+((int)(y2)-(int)(y1))**2

class GetAddresse(Request):
    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.status = "Error"
        dataTransferObject.organizations = []
        dataTransferObject.address = ""
        x = int(params["coordinateX"])
        y = int(params["coordinateY"])

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

        cursor.execute("SELECT idStreet FROM segmentStreet WHERE idFirstPoint = '{}' OR idSecondPoint= '{}'"
                       .format(mnId, mnId))

        idStreet = cursor.fetchone()

        cursor.execute("SELECT id FROM Street WHERE pointId = '{}'"
                       .format(mnId))

        idStreet2 = cursor.fetchone()

        if idStreet is None:
            idStreet = idStreet2
        if idStreet is not None:
            cursor.execute("SELECT name FROM Street WHERE id = '{}'".format(idStreet[0]))
            curStreet = cursor.fetchone()
            if curStreet is not None:
                dataTransferObject.address = curStreet[0]

        else:

            cursor.execute(
                "SELECT id,num,idStreet FROM building WHERE pointId = '{}'".format(mnId, mnId))

            idBuilding = cursor.fetchone()
            if idBuilding is not None:
                cursor.execute("SELECT name FROM Street WHERE id = '{}'".format(idBuilding[2]))

                nameStreet = cursor.fetchone()

                if nameStreet is None:
                    dataTransferObject.message = "Не найдена улица дома"
                    raise AttributeError

                dataTransferObject.address = nameStreet[0] + " " + idBuilding[1]

                cursor.execute("SELECT name FROM Organization WHERE idBuilding = '{}'".format(idBuilding[0]))

                allOrg = cursor.fetchall()

                for curNameOrg in allOrg:
                    curOrg = getOrganization(cursor, idBuilding[0], curNameOrg[0])
                    if curOrg is not None:
                        dataTransferObject.organizations.append(curOrg)

        dataTransferObject.status = "OK"
