import requests
from bs4 import BeautifulSoup

# 웹페이지에 요청을 보내고 응답을 가져옴
url = "https://www.tjmedia.com/tjsong/song_monthPopular.asp"
response = requests.get(url)

# 응답 내용을 UTF-8로 디코딩하고, 깨진 문자가 있을 경우에는 'replace'를 사용하여 교체
html = response.content.decode('utf-8', 'replace')

# BeautifulSoup을 사용하여 파싱
soup = BeautifulSoup(html, 'html.parser')

# <ul class="left"> 요소를 찾아서 저장
left_ul = soup.find("ul", class_="left")
date_range = left_ul.text.strip()  # 날짜 범위 추출

# <div id="BoardType1"> 요소를 찾아서 저장
board_div = soup.find("div", id="BoardType1")
table_rows = board_div.find_all("tr")  # 표의 모든 행 추출

# 결과를 가공하여 저장할 문자열 초기화
formatted_data = f"{date_range}\n순위\t곡번호\t곡제목\t가수\n"

# 표의 각 행을 반복하면서 데이터 추출
for row in table_rows[1:]:  # 첫 번째 행은 헤더이므로 제외
    columns = row.find_all("td")
    rank = columns[0].text.strip()
    song_number = columns[1].text.strip()
    song_title = columns[2].text.strip()
    singer = columns[3].text.strip()
    formatted_data += f"{rank}\t{song_number}\t{song_title}\t{singer}\n"

# 결과를 파일에 저장
with open("인기차트 순위-곡번호-곡제목-가수.txt", "w", encoding="utf-8") as file:
    file.write(formatted_data)
