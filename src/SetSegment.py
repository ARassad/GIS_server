from Request import Request

class SetSegment(Request):

    @staticmethod
    def request(cursor, params, dataTransferObject):
        dataTransferObject.status = "Error"

        cursor.execute("DELETE FROM TRACK")
        cursor.execute("DELETE FROM VertexTrack")


        f = open('tracks.txt', 'r')
        cnt = 0
        for i, line in enumerate(f):
            arr = line.split(" ")
            cursor.execute(
                "insert into Track(idVertex1, idVertex2) OUTPUT INSERTED.id values('{}','{}')".format(arr[0], arr[1]))
            id_track = cursor.fetchone()[0]

            for j in range(3, (int)(arr[2])+3):

                cursor.execute(
                    "insert into VertexTrack(idVertex,idTrack) values('{}','{}')".format(arr[j], id_track))
                cnt += 1

        dataTransferObject.status = "OK"
