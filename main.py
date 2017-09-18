import os.path
from shapefile import Reader
import sqlite3

PATH = os.path.abspath(os.path.dirname(__file__))
SHAPE_FILE = "/data/nigeria/hotosm_nigeria_points_of_interest_points"
CREATE_TABLE_SQL = """CREATE TABLE
IF NOT EXISTS poi (
 id integer PRIMARY KEY,
 name text NOT NULL,
 latitude real NOT NULL,
 longitude real NOT NULL,
 address text NOT NULL,
 tags text
);"""


def create_connection():
    """ create a database connection to the SQLite database
        created in memory
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(PATH + '/test.sqlite3')
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def add_place_to_quadtree(place):
    pass


def insert_data_into_table(conn, places):
    """
    Create a new database entry into the poi table
    :param conn:
    :param shapes:
    :return:
    """
    sql = ''' INSERT INTO poi(id, name,latitude,longitude,address,tags)
                      VALUES(?,?,?,?,?,?) '''

    for place in places:
        coordinates = place.shape.points
        meta = place.record

        params = (int(meta[0]), meta[1], coordinates[0][1], coordinates[0][0], meta[11] + ' ' + meta[12], meta[2])
        cur = conn.cursor()
        cur.execute(sql, params)
        add_place_to_quadtree(place)


def seed_database_from_shape_file(conn, file_path):

    sf = Reader(file_path)
    shapes = sf.shapeRecords()

    with conn:
        print("1. Create Schema:")
        create_table(conn, CREATE_TABLE_SQL)

        print("2. Insert Data into the DataStore:")
        insert_data_into_table(conn, shapes)


def main():

    # create a database connection
    conn = create_connection()
    file_path = PATH + SHAPE_FILE
    seed_database_from_shape_file(conn, file_path)


if __name__ == '__main__':
    main()
