from Request import Request

class Organization:
    def __init__(self, nameIn, addressIn, pointIn):
        self.name = nameIn
        self.address = addressIn
        self.point = pointIn

def getPointForId(cursor, id):
    cursor.execute("SELECT x,y FROM point WHERE id = '{}'".format(id))
    return cursor.fetchone()

def getOrganization(cursor, idBuilding, nameOrg):

    cursor.execute("SELECT pointId,idStreet,num FROM building WHERE id = '{}'".format(idBuilding))

    nms = cursor.fetchone()

    if nms is None:
        return

    pt = getPointForId(cursor, nms[0])

    if pt is None:
        return

    cursor.execute("SELECT name FROM Street WHERE id = '{}'".format(nms[1]))

    name1 = cursor.fetchone()

    if name1 is None:
        return

    return Organization(nameOrg, name1[0] + " " + nms[2], (pt[0], pt[1]))

class GetResult(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.status = "Error"
        dataTransferObject.points = []
        dataTransferObject.organizations = []

        request = params["request"]

        if request is None:
            dataTransferObject.message = "Пустой запрос строки"
            raise AttributeError

        check = 1

        street = ""
        numstreet = 0

        for i, curChr in enumerate(request):
            if '0' <= curChr <= '9':
                check = 0
                street = request[:i-1]
                numstreet = request[i:]
                break

        if check:
            # Поиск точек по названию улицы
            cursor.execute("SELECT pointId FROM Street WHERE name = '{}'".format(request))
            ptId = cursor.fetchone()
            if ptId is not None:
                pt = getPointForId(cursor, ptId[0])
                if pt is not None:
                    dataTransferObject.points.append((pt[0], pt[1]))

            # Поиск точек по названию компаниии
            cursor.execute("SELECT idBuilding FROM Organization WHERE name = '{}'".format(request))
            idBuild = cursor.fetchone()
            if idBuild is not None:
                curObjectBuild = getOrganization(cursor, idBuild[0], request)
                if curObjectBuild is not None:
                    dataTransferObject.organizations.append(curObjectBuild)

            # Поиск точек по названию типа компании
            cursor.execute("SELECT id FROM typeOrganization WHERE name = '{}'".format(request))
            id = cursor.fetchone()
            if id is not None:
                cursor.execute("SELECT idBuilding, name FROM Organization WHERE idType = '{}'".format(id[0]))
                allBuild = cursor.fetchall()
                for curBuild in allBuild:
                    curObjectBuild = getOrganization(cursor, curBuild[0], curBuild[1])
                    if curObjectBuild is not None:
                        dataTransferObject.organizations.append(curObjectBuild)

        else:
            # Поиск точек по названию дома
            cursor.execute("SELECT idStreet,pointId,id FROM building WHERE num = '{}'".format(numstreet))
            allStreet = cursor.fetchall()
            for curStreet in allStreet:
                cursor.execute("SELECT pointId FROM Street WHERE id = '{}' AND name = '{}'".format(curStreet[0], street))
                curPoint = cursor.fetchone()
                if curPoint is not None:
                    pt = getPointForId(cursor, curStreet[1])
                    if pt is not None:
                        dataTransferObject.points.append((pt[0], pt[1]))
                    cursor.execute("SELECT name FROM Organization WHERE idBuilding = {}".format(curStreet[2]))
                    orgs = cursor.fetchall()
                    if orgs is not None:
                        dataTransferObject.organizations = list()
                        for o in orgs:
                            dataTransferObject.organizations.append(Organization(o[0], request, [pt[0], pt[1]]))

        dataTransferObject.status = "OK"

        return