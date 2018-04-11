from Request import Request

def getPointForId(cursor, id):
    cursor.execute("SELECT x,y FROM point WHERE id = '{}'".format(id))
    return cursor.fetchone()

def getOrganization(cursor, id, nameOrg, curOutputData):
    cursor.execute("SELECT pointId,idStreet FROM building WHERE id = '{}'".format(id))

    nms = cursor.fetchone()

    pt = getPointForId(cursor, nms[0])

    if pt is not None:
        cursor.execute("SELECT name FROM Street WHERE id = '{}'".format(nms[1]))
        curOutputData.append((nameOrg, cursor.fetchone()[0], pt))

class Organization:
    name = ""
    address = ""
    point = 0

class GetResult(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.status = "Error"

        request = params["request"]

        if request is None:
            dataTransferObject.message = "Пустой запрос строки"
            raise AttributeError

        check = 1

        street = ""
        numstreet = 0

        for i, curChr in enumerate(request):
            if curChr >= '0' and curChr <='9':
                check = 0
                street = request[:i-1]
                numstreet = request[i:]
                break

        if check:
            # Поиск точек по названию улицы
            cursor.execute("SELECT pointId FROM Street WHERE name = '{}'".format(request))

            pt = getPointForId(cursor, cursor.fetchone()[0])

            dataTransferObject.points = []

            if pt is not None:
                dataTransferObject.points.append(pt)

            # Поиск точек по названию компаниии
            cursor.execute("SELECT idBuilding FROM Organization WHERE name = '{}'".format(request))

            if cursor.fetchone() is not None:
                dataTransferObject.Organization = Organization()
                dataTransferObject.Organization = []
                getOrganization(cursor, cursor.fetchone(), request, dataTransferObject.Organization)

            # Поиск домов по названию типа компании
            cursor.execute("SELECT id FROM typeOrganization WHERE name = '{}'".format(request))

            id = cursor.fetchone()[0]

            cursor.execute("SELECT idBuilding, name FROM Organization WHERE idType = '{}'".format(id))

            allBuild = cursor.fetchall()

            for curBuild in allBuild:
                getOrganization(cursor, curBuild[0], curBuild[1], dataTransferObject.Organization)

        else:
            cursor.execute("SELECT idStreet FROM building WHERE num = '{}'".format(numstreet))

            allStreet = cursor.fetchall()
            dataTransferObject.points = []

            for idStreet in allStreet:
                cursor.execute("SELECT pointId FROM Street WHERE id = '{}' AND name = '{}'".format(idStreet[0], street))

                curPoint = cursor.fetchone()

                pt = getPointForId(cursor, curPoint[0])

                if pt is not None:
                    dataTransferObject.points.append((pt[0], pt[1]))

        dataTransferObject.status = "Ok"

        return


