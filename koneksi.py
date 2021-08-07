import mysql.connector


conn = mysql.connector.connect(
    user='root', 
    password='', 
    host='localhost', 
    database='db_handwashing'
    )
cursor = conn.cursor()


def savelog():
    memulai = "INSERT INTO t_log(log)VALUES ('Menghubungkan server')"
    cursor.execute(memulai)
    conn.commit()


def saveHistory(poseCount, totalFrames):
    
    summary = "INSERT INTO t_summary(poseCount, totalFrames)VALUES ('"+str(
            poseCount)+"','" + str(totalFrames)+"' )"
    cursor.execute(summary)
    conn.commit()


def getLastHistory():
        sql = 'SELECT poseCount, totalFrames FROM `t_summary` ORDER BY id DESC LIMIT 1'
        cursor.execute(sql)
        result = cursor.fetchall()
        if cursor.rowcount > 0:
            for data in result:
                pose = data[0]
                total = data[1]

        poseCount   = pose 
        totalFrames = int(total)
        kata = poseCount
        remove_characters = ["[", "]"]
        for item in remove_characters:
                kata = kata.replace(item, "") 
        x = kata.split()

        return x, totalFrames


# print(getLastHistory())
