from database.DB_connect import DBConnect
from model.airport import Airport
from model.tratta import Tratta


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM airports a order by a.AIRPORT ASC """

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(n, idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t.ID, t.IATA_CODE, count(*) as N
                    FROM (select a.ID , a.IATA_CODE , f.AIRLINE_ID 
                    from airports a , flights f 
                    where a.ID  = f.ORIGIN_AIRPORT_ID 
                    or a.ID = f.DESTINATION_AIRPORT_ID
                    group BY a.ID , a.IATA_CODE , f.AIRLINE_ID) t 
                    GROUP BY t.ID, t.IATA_CODE
                    HAVING N>= %s
                    order by N ASC """

        cursor.execute(query, (n,))

        for row in cursor:
            result.append(idMapAirports[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1(idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as peso
                    from flights f 
                    group BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID """

        cursor.execute(query)

        for row in cursor:
            # result.append((idMapAirports[row["ID"]],
                           # idMapAirports[row["DESTINATION_AIRPORT_ID"]],
                           # row["peso"]))
            # Posso crearmi un oggetto di tipo tratta, così lo richiamo con la notazione puntata
            result.append(Tratta(
                idMapAirports[row["ORIGIN_AIRPORT_ID"]],
                idMapAirports[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, coalesce(t1.n, 0) + COALESCE(t2.n,0) as peso
                    from (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f 
                    group BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) t1
                    left join (select f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, count(*) as n
                    from flights f 
                    group BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID) t2
                    on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID
                    and t1.DESTINATION_AIRPORT_ID = t2.ORIGIN_AIRPORT_ID
                    where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is Null"""

        cursor.execute(query)

        for row in cursor:
            # result.append((idMapAirports[row["ID"]],
            # idMapAirports[row["DESTINATION_AIRPORT_ID"]],
            # row["peso"]))
            # Posso crearmi un oggetto di tipo tratta, così lo richiamo con la notazione puntata
            result.append(Tratta(
                idMapAirports[row["ORIGIN_AIRPORT_ID"]],
                idMapAirports[row["DESTINATION_AIRPORT_ID"]],
                row["peso"]))

        cursor.close()
        conn.close()
        return result