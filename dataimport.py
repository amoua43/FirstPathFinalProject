import pandas as pd
import sqlite3


#connect to the databaswe 
conn = sqlite3.connect("db.sqlite3")

#read data from a csv files
df = pd.read_csv("job_postings_data.csv")

#write the dataframe to a new table
df.to_sql('base_job',conn, if_exists='append', index=False)

#close the connection
conn.close()
