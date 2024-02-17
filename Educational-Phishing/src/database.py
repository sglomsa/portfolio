from hashlib import md5
import random
import mysql.connector


def db_connect():
    """
    Establishes a connection to the MySQL database.

    Returns:
    mysql.connector.connection.MySQLConnection: A MySQL database connection object.
    """
    try:
        connection = mysql.connector.connect(
            host="172.16.100.46",
            database="phishing",
            user="phishing_project_usr",
            password="EtVeldigBraPassord",
        )
        return connection
    except:
        print("Error connecting to the DB")


def add_cookie(cookie_id: str, url: str):
    """
    Adds a cookie entry to the database.

    Args:
    cookie_id (str): The ID of the cookie.
    url (str): The URL associated with the cookie.

    Returns:
    None
    """
    con = db_connect()
    cur = con.cursor()
    sql = """INSERT INTO `cookie` 
        (`ID`, `gruppe`) 
        VALUES (%s, %s);
        """
    values = [cookie_id, url]
    cur.execute(sql, values)
    cur.close()
    con.commit()


def create_new_cookie():
    """
    Creates a new cookie ID using MD5 hashing.

    Returns:
    str: The newly generated cookie ID.
    """
    return md5(random.randbytes(100)).hexdigest()


def click_cookie_update(cookie_id: str):
    """
    Updates the 'clicked' status of a specific cookie in the database.

    Args:
    cookie_id (str): The ID of the cookie to be updated.

    Returns:
    None
    """
    connection = db_connect()
    cursor = connection.cursor()

    sql = """UPDATE `cookie` SET
        `clicked` = '1' 
        WHERE `cookie`.`ID` = %s;"""
    value = [cookie_id]
    cursor.execute(sql, value)
    cursor.close()
    connection.commit()


def delete_cookie(cookie_id: str):
    """
    Deletes a cookie from the database and updates the count of deleted cookies.

    Args:
    cookie_id (str): The ID of the cookie to be deleted.

    Returns:
    None
    """
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cookie = get_cookie(cookie_id, cursor)
        if cookie:
            sql_update = """UPDATE `deleted_cookies` 
            SET `number_deleted` = `number_deleted` + '1', 
            `clicked_and_deleted` = `clicked_and_deleted` + %s
            WHERE `deleted_cookies`.`ID` = 1;"""
            cursor.execute(sql_update, [cookie[2]])

            sql_del = """DELETE FROM `cookie` WHERE `cookie`.`ID` = %s"""
            cursor.execute(sql_del, [cookie[0]])

            cursor.close()
            connection.commit()
    except:
        print("Something went wrong in the deletion of a cookie.")


def get_cookie(cookie_id: str, cursor):
    """
    Retrieves information about a specific cookie from the database.

    Args:
    cookie_id (str): The ID of the cookie to retrieve.
    cursor: Cursor object for executing MySQL queries.

    Returns:
    tuple: Information about the cookie if found, otherwise None.
    """
    sql_select = """SELECT * FROM `cookie` WHERE `ID`=%s;"""
    cursor.execute(sql_select, [cookie_id])
    return cursor.fetchone()


def get_number_of_people():
    """
    Retrieves the total count of visitors and clicked cookies from the database.

    Returns:
    tuple: A tuple containing the total number of visitors and total number of clicked cookies.
    """
    connection = db_connect()
    cursor = connection.cursor()

    sql_cookie_count = """SELECT COUNT(ID) Amount, SUM(`clicked`) clicks 
    FROM `cookie` WHERE `gruppe` = "http://mcdonalds.tanvgs.no/";"""
    cursor.execute(sql_cookie_count)
    cookies = cursor.fetchone()
    sql_deleted_count = """SELECT * FROM `deleted_cookies`"""
    cursor.execute(sql_deleted_count)
    deleted = cursor.fetchone()
    total_visitors = int(cookies[0]) + int(deleted[1])
    total_clicked = int(cookies[1]) + int(deleted[2])
    return total_visitors, total_clicked


def get_number_of_people_mcdonalds():
    connection = db_connect()
    cursor = connection.cursor()

    sql_cookie_count = """SELECT COUNT(ID) Amount, SUM(`clicked`) clicks 
    FROM `cookie` WHERE `gruppe` = "http://mcdonalds.tanvgs.no/";"""
    cursor.execute(sql_cookie_count)
    cookies = cursor.fetchone()
    total_visitors = int(cookies[0]) + int(cookies[1])
    return total_visitors


print(db_connect())
