from Request import Request


class GetAllWayPoints(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        cursor.execute("select idFirstPoint, idSecondPoint from segmentStreet")
        points = cursor.fetchall()
        st = set()
        for i in points:
            st.add(i[0])
            st.add(i[1])

        dataTransferObject.points = []
        for i in st:
            cursor.execute("select * from point where id={}".format(i))
            data = cursor.fetchone()
            dataTransferObject.points.append({'xy': [data[1], data[2]], 'id': [data[0]]})
        dataTransferObject.status = "OK"
