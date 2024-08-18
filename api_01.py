from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import json

driver = webdriver.Chrome() 

driver.get("https://various.foodsafetykorea.go.kr/nutrient/general/food/firstList.do")

search_box = driver.find_element(By.ID, "searchText")
search_box.send_keys("김밥")
search_button = driver.find_element(By.ID, "searchBtn")
search_button.click()

time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'html.parser')

rows = soup.select('table.bbsList tbody tr')

results = []

for i, row in enumerate(rows[:5]):
    cells = row.find_all('td')
    if len(cells) > 0:
        result = {
            "번호": i+1,
            "식품명": cells[2].text.strip(),
            "식품대분류명": cells[3].text.strip(),
            "에너지(㎉)": cells[4].text.strip()
        }
        results.append(result)

# JSON 파일로 저장
with open('search_results.json', 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)

# 브라우저 닫기
driver.quit()

print("검색 결과가 'search_results.json' 파일로 저장되었습니다.")

