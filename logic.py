import pandas as pd
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='parfum_db'
        )
        return conn
    except Error as e:
        raise ConnectionError(f"Koneksi ke database gagal: {e}")

def save_to_database(data: dict, cluster: int):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO parfum_predictions (
            year, followers, price_per_ml, size, concentration, cluster
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        int(data['year']),
        int(data['followers']),
        float(data['price_per_ml']),
        float(data['size']),
        str(data['concentration']),
        int(cluster)
    ))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_all_predictions():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM parfum_predictions ORDER BY id ASC")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    cursor.close()
    conn.close()
    return df
