import pymysql as pm

# MySQL database config:
dbCfg = {
    'dbHost': "127.0.0.1",
    'dbUser': "root",
    'dbPassword': "",
    'dbName': "shop",
    'charSet': "utf8mb4",
    'cursorType': pm.cursors.DictCursor
}

# Creating database file:
db = pm.connect(host=dbCfg['dbHost'], user=dbCfg['dbUser'], password=dbCfg['dbPassword'], charset=dbCfg['charSet'],
                cursorclass=dbCfg['cursorType'])

try:
    cursor = db.cursor()
    sqlStatement = "CREATE DATABASE IF NOT EXISTS " + dbCfg['dbName']
    cursor.execute(sqlStatement)

except Exception as e:
    print("Exception occurred:{}".format(e))

finally:
    db.close()

# Creating database tables:
db = pm.connect(host=dbCfg['dbHost'], user=dbCfg['dbUser'], password=dbCfg['dbPassword'], charset=dbCfg['charSet'],
                cursorclass=dbCfg['cursorType'], database=dbCfg['dbName'])

try:
    cursor = db.cursor()
    sqlQuery = ["CREATE TABLE IF NOT EXISTS items (id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id), title VARCHAR("
                "100) NOT NULL, description VARCHAR(500), price FLOAT(10, 2) NOT NULL, quantity INT NOT NULL, "
                "category INT(11) NOT NULL, img_name TEXT)",
                "CREATE TABLE IF NOT EXISTS item_category (id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id), "
                "title VARCHAR(30) NOT NULL, description VARCHAR(500))",
                "CREATE TABLE IF NOT EXISTS qty_changelog (id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id), "
                "change_time DATETIME NOT NULL, item_id INT(11) NOT NULL, qty_old INT NOT NULL, qty_new INT NOT NULL"
                ")",
                "CREATE TABLE IF NOT EXISTS users (id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id), "
                "name VARCHAR(100), email VARCHAR(100) NOT NULL UNIQUE, "
                "password VARCHAR(255) NOT NULL)"
                ]
    for sql in sqlQuery:
        cursor.execute(sql)

except Exception as e:
    print("Exception occurred:{}".format(e))

# Filling tables with values:
try:
    cursor = db.cursor()
    reset = "TRUNCATE TABLE item_category"
    cursor.execute(reset)
    reset = "TRUNCATE TABLE items"
    cursor.execute(reset)

    with open('sql.txt', 'r') as file:
        val = file.readline()
        sql = '''INSERT INTO item_category (title, description) VALUES {}'''.format(val)
        cursor.execute(sql)
        val = file.readline()
        sql = '''INSERT INTO items (title, description, price, quantity, category) VALUES {}'''.format(val)
        cursor.execute(sql)
        file.close()

    db.commit()

except Exception as e:
    print("Exception occurred:{}".format(e))

finally:
    db.close()
