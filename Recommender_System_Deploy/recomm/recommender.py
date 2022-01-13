#import mysql.connector
import pymysql.cursors
from sklearn.metrics.pairwise import cosine_similarity
import numpy


class RCMD:
    def __init__(self):
        #pass
        
        # pip install mysql-connector-python
        # 偕同過濾 基於 item
        #connection = mysql.connector.connect(host='167.172.73.217',
        #                                     database='BukaCa_test',
        #                                     user='admin',
        #                                     password='BukaCa123!',
        #                                     )
        
        connection = pymysql.connect(host='167.172.73.217',
                                             database='BukaCa_test',
                                             user='admin',
                                             password='BukaCa123!',
                                             cursorclass=pymysql.cursors.DictCursor
                                             )

        self.original_list = []
        tmp_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mycursor = connection.cursor()

        sql3 = "select * from lunch_element"
        mycursor.execute(sql3)
        tmp_result = mycursor.fetchall()
        tmp_result = tuple(tuple(dic.values()) for dic in tmp_result)
        #print(tmp_result)

        sql_rec = "SELECT count(*) FROM BukaCa_test.lunch_rec"
        mycursor.execute(sql_rec)
        tmp_rec = mycursor.fetchall()
        #print(tmp_rec)
        total_rec = int(tmp_rec[0]['count(*)'])

        # 把原始紀錄變成 1*15的 list，原始便當只要有便當設為1，沒有設為0

        for t in range(total_rec):
            for i, x in enumerate(tmp_result):
                # print(i,x)
                if x[1] == t+1:
                    tmp_list[x[2]-1] = 1
            self.original_list.append(tmp_list)
            tmp_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            t = t+1
        mycursor.close()
        connection.close()
        
    def getRecomm(self, new_rec, ratelist):
        # 計算新的紀錄與所有歷史紀錄的內稽
        #self.original_list = original_list = [[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0], [1,1,1,0,0,1,0,1,1,0,0,0,1,1,1], [1,0,1,0,0,1,1,1,1,0,0,0,1,1,1]]
        similarity_list = []
        for a in self.original_list:
            #inner_product = 0
            # for b in range(len(new_rec)):
            #     if a[b] == new_rec[b]:
            #         inner_product = inner_product + 1
            X = numpy.array(a).reshape(1, -1)
            y = numpy.array(new_rec).reshape(1, -1)
            inner_product = cosine_similarity(X, y)

            similarity_list.append(inner_product[0][0])

        # print(similarity_list)
        # print(max(similarity_list))
        bendom = []
        for similarity_index in range(len(similarity_list)):
            if similarity_list[similarity_index] == max(similarity_list):
                bendom.append(self.original_list[similarity_index])
        # print(bendom)

        final_bendom = [sum([j[i] for j in bendom])/(len(bendom))
                        for i in range(len(bendom[0]))]
        # print(final_bendom)
        return(final_bendom, ratelist)


if __name__ == '__main__':
    rc = RCMD()
    res = rc.getRecomm([1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1], [])
    print(res)
