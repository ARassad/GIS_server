from Request import Request


class GetAllWayPoints(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("select * from point")
        dataTransferObject.points = []
        data = cursor.fetchall()
        for i in data:
            dataTransferObject.points.append({'xy': [i[1], i[2]], 'id': [i[0]]})
        dataTransferObject.status = "OK"
