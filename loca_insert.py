from pandas import read_excel
import cx_Oracle


sido = ["서울특별시", "경기도", "부산광역시"]
seoul = ["강남구", "강동구", "강북구", "강서구", "광진구"]
gyeonggi = ["광명시", "수원시", "평택시", "안양시", "하남시"];
busan = ["강서구", "금정구", "해운대구", "동구", "북구"];

gugun_dict = {"서울특별시":seoul, "경기도":gyeonggi,  "부산광역시":busan}

for a in sido :
    for s in range(5) :
        #print(gugun_dict[a][s])
        df = read_excel(a+'_'+gugun_dict[a][s]+'.xlsx', sheet_name='Sheet1')
        
        #print(df['매장명'])
        
        df['매장명_수정'] = df['매장명'].str.slice_replace(start=0, stop=1, repl='두')
        print(df)
        
        #print('Row count is:',len(df.index))
        
        #print(df.iloc[0]['매장명'])
        
        list1 = ['매장명_수정', '주소', '전화번호', '매장명']
       
        
        for i in range(len(df.index)) :
            
            list2 = []
            
            for y in list1 :
                list2.append(df.iloc[i][y])
            
            cursor = None
            
            try :
                conn = cx_Oracle.connect('C##doosot', 'm1234', 'localhost:1521/xe')
                sql = "insert into loca values (loca_num.nextval, '{}', '{}', '{}', '{}.html', sysdate, 'true')".format(
                    list2[0], list2[1], list2[2], list2[3])
                
                cursor = conn.cursor()
                
                ## 데이터를 db에 추가
                cursor.execute(sql)
                
                #commint
                conn.commit()
                
                # 처리결과
                result = cursor.rowcount
                print(result)
                print('-'*30)    
                
                if result > 0 : print('저장성공')
                else : print('저장 실패')
                
            except Exception as e :
                print('저장실패', e)
            finally :
                if cursor != None :
                    cursor.close()
                    cursor = None
                if conn != None :
                    conn.close()
                    conn = None
            