from Request import Request

def getPointForId(cursor, id):
    cursor.execute("SELECT x,y FROM point WHERE id = '{}'".format(id))
    return cursor.fetchone()

def getOrganization(cursor, id, nameOrg, curOutputData):
    cursor.execute("SELECT pointId,idStreet FROM building WHERE id = '{}'".format(id))

    nms = cursor.fetchone()

    pt = getPointForId(cursor, nms[0])

    if pt is not None:
        curOutputData.point.x = pt[0]
        curOutputData.point.y = pt[1]
        curOutputData.name = nameOrg
        cursor.execute("SELECT name FROM Street WHERE id = '{}'".format(nms[1]))
        curOutputData.street = cursor.fetchone()

class GetResult(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.Status = "Error"

        request = params["request"]

        if request is None:
            dataTransferObject.message = "Пустой запрос строки"
            raise AttributeError

        check = 1

        street = ""
        numstreet = 0

        for i, curChr in enumerate(request):
            if curChr >= '0'  and curChr <='9':
                check = 0
                street = request[:i-2]
                numstreet = request[i:]

        if check:
            # Поиск точек по названию улицы
            cursor.execute("SELECT pointId FROM Street WHERE login = '{}'".format(request))

            pt = getPointForId(cursor, cursor.fetchone())

            if pt is not None:
                dataTransferObject.Street.point.x = pt[0]
                dataTransferObject.Street.point.y = pt[1]

            # Поиск точек по названию компаниии
            cursor.execute("SELECT idBuilding FROM Organization WHERE name = '{}'".format(request))

            id = cursor.fetchone()

            getOrganization(cursor, id, request, dataTransferObject.organization)

            # Поиск домов по названию типа компании
            cursor.execute("SELECT id FROM typeOrganization WHERE name = '{}'".format(request))

            id = cursor.fetchone()

            cursor.execute("SELECT idBuilding, name FROM Organization WHERE idType = '{}'".format(id))

            allBuild = cursor.fetchall()

            cntBuild = 0

            for curBuild in allBuild:
                cursor.execute("SELECT pointId,idStreet FROM building WHERE id = '{}'".format(curBuild[0]))

                nms = cursor.fetchone()

                pt = getPointForId(cursor, nms[0])


                if pt is not None:
                    dataTransferObject.typeOrganization.point[cntBuild].x = pt[0]
                    dataTransferObject.typeOrganization.point[cntBuild].y = pt[1]
                    dataTransferObject.typeOrganization.name[cntBuild] = curBuild[1]
                    cursor.execute("SELECT name FROM Street WHERE id = '{}'".format(nms[1]))
                    curOutputData.street = cursor.fetchone()
                    cntBuild += 1

            dataTransferObject.typeOrganization.cntBuild = cntBuild

        else:
            cursor.execute("SELECT idStreet FROM building WHERE num = '{}'".format(numstreet))

            allStreet = cursor.fetchall()

            for idStreet in allStreet:
                cursor.execute("SELECT pointId FROM Street WHERE id = '{}' AND name = '{}'".format(idStreet, street))

                pt = getPointForId(cursor, cursor.fetchone())

                if pt is not None:
                    dataTransferObject.building.point.x = pt[0]
                    dataTransferObject.building.point.y = pt[1]

        dataTransferObject.Status = "Ok"

        return


