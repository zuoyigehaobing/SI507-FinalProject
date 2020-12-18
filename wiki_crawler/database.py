import sqlite3

DB_PATH = "../var/movies_check.db"


def create_tables():
    """ initialize the database

    Parameters
    ----------

    Returns
    -------
    None
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # read the schema file
    sql_file = open("schema.sql", "r")
    sql_as_string = sql_file.read()
    sql_file.close()

    # execute the script
    cur.executescript(sql_as_string)

    # close the database
    conn.close()


if __name__ == "__main__":
    create_tables()
