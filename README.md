# Doosot 프로젝트 중 기존 한솥 도시락의 매장정보를 크롤링 / Oracle DB에 저장하는 코드입니다.
# 실행 순서
# 1. SQL_LOCA ) Oracle SQL 에서 loca Table 및 Sequence 생성
# 2. hansot_croll ) 네이버지도에서 한솥 + 대단위 + 중단위 검색 후 정보(매장명, 전화번호, 주소, 위도, 경도) 크롤링하여 엑셀파일로 저장
# 3. img_croll ) python folium과 위 크롤링에서 받아온 위도, 경도를 이용하여 초기 지도위치, 마크, 범위 설정 후 html파일로 저장
# 4. loca_insert ) 2번에서 저장한 엑셀파일을 불러온 후 Oracle SQL에 저장
# 순입니다.

# data 폴더에 있는 크롬드라이버는 크롬 96버전을 기준으로 만들어진 파일입니다. 만약 버전이 다르다고 에러가 발생시 https://chromedriver.chromium.org/downloads 
# 방문하여서 현재 사용하시는 크롬버전에 맞는 크롬드라이버 버전을 다운받으시면 됩니다.
