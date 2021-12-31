import psycopg2
from datetime import datetime, timedelta


class DBCrud(object):
    postgresConnection = psycopg2.connect("dbname=postgres user=postgres password=password host=0.0.0.0, port=3000")
    postgresCursor = postgresConnection.cursor()
    current_date = datetime.now().date() - timedelta(3)
    postgresCursor.execute("SELECT * FROM public.historicalstates where date_start_incidence < (%s)",[str(current_date)])
    rows = postgresCursor.fetchall()
    print(current_date, len(rows))
    if len(rows) is not 0:
        postgresCursor.execute("DELETE FROM public.historicalstates where date_start_incidence < (%s)",[str(current_date)])
        postgresConnection.commit()

    postgresCursor.close()
    postgresConnection.close()
