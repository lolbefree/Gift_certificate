import pyodbc


def m1(f1):
    var = f1
    server = '10.10.10.25'
    database = 'amprod'
    username = 'sa'
    password = 'pw'
    driver = '{SQL Server}'  # Driver you need to connect to the database
    port = '1433'
    cnn = pyodbc.connect(
        'DRIVER=' + driver + ';PORT=port;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username +
        ';PWD=' + password)
    gsalid = 2077107
    cursor = cnn.cursor()

    cursor.execute("""
select c.LNAME,c.WTEL,c.email,g.WRKORDNO from GSALS01 g
join cust c on c.CUSTNO=g.CUSTNO
where g.GSALID=(select gsalid from GSALS01 where WRKORDNO={})""".format(f1))
    for row in cursor:
        print(row[0])
        print(row[2])


m1(2077107)