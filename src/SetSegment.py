from Request import Request

class SetSegment(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.status = "Error"

        f = open('tracks.txt', 'r')
        cnt = 0
        for i, line in enumerate(f):
            arr = line.split(" ")
            cursor.execute(
                "insert into Track(id, idVertex1, idVertex2) values('{}','{}','{}')".format(i, arr[0], arr[1]))

            for j in range(3, (int)(arr[2])+3):

                cursor.execute(
                    "insert into VertexTrack(id,idVertex,idTrack) values('{}','{}','{}')".format(cnt, arr[j], i))
                cnt += 1

        dataTransferObject.status = "OK"
