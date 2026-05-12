from database.DB_connect import DBConnect
from model.airport import Airport


class DAO():

    @staticmethod
    def getAllNodes():
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
                    HAVING N>=5
                    order by N ASC """

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result