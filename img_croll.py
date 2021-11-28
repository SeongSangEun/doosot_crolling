import folium
import pandas as pd

sido = ["서울특별시", "경기도", "부산광역시"]
seoul = ["강남구", "강동구", "강북구", "강서구", "광진구"]
gyeonggi = ["광명시", "수원시", "평택시", "안양시", "하남시"];
busan = ["강서구", "금정구", "해운대구", "동구", "북구"];

gugun_dict = {"서울특별시":seoul, "경기도":gyeonggi,  "부산광역시":busan}

for a in sido :
    for s in range(5) :
        #print(gugun_dict[a][s])

        df = pd.read_excel(a+ '_' + gugun_dict[a][s] + '.xlsx')
        #print(df)
        
        #지도 객체 생성
        for i in range(len(df)) :
            map_osm = folium.Map(location=[df['위도'][i], df['경도'][i]],
                                 zoom_start=14)
            # 지도에 마커 추가
            marker = folium.Marker(location=[df['위도'][i], df['경도'][i]], popup='한솥도시락 평택소사벌점',
                                  icon=folium.Icon(color='red', icon='info-sign'))
            
            # 지도에 추가
            marker.add_to(map_osm)
            
            # 원형 구역 보여주기
            marker = folium.Circle([df['위도'][i], df['경도'][i]], popup='한솥도시락 평택소사벌점', 
                                   color='red', radius=2000, fill_color='blue')
            
            marker.add_to(map_osm)
            map_osm.save(df['매장명'][i] +'.html')
            
            print(a+ '_' + gugun_dict[a][s] + '저장완료')

