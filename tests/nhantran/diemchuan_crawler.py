import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class University:
    def __init__(self, code, name, link = ''):
        self.code = code
        self.name = name
        self.link = link

    def __str__(self):
        return f"{self.code}: {self.name} - {self.link}"

    def __repr__(self):
        return f"{self.code}: {self.name} - {self.link}"
    
    def printInTerminal(self):
        print(f"""CODE: {self.code}""")
        print(f"""NAME: {self.name}""")
        print(f"""LINK: {self.link}""")

class Major:
    def __init__(self, id, major, score, block, tuition):
        self.id = id
        # self.major_name, self.major_code = major.split('\n')
        self.score = score
        self.block = block
        self.tuition = tuition
        try:
            self.major_name, self.major_code = major.split('\n')
        except ValueError:
            # Xử lý nếu không có đủ hai phần tử sau khi split
            self.major_name = major
            self.major_code = None

    def __str__(self):  
        return f"""{self.id}, {self.major_name}, {self.major_code}, {self.score}, {self.block}, {self.tuition}"""
    
    def __repr__(self):
        return f"""{self.id}, {self.major_name}, {self.major_code}, {self.score}, {self.block}, {self.tuition}"""
    
    def writeToCSV(self):
        return [self.id, self.major_name, self.major_code, self.score, self.block, self.tuition]

# Khởi tạo trình duyệt Chrome
driver = webdriver.Chrome()

# Truy cập trang web
driver.get("https://diemthi.vnexpress.net/tra-cuu-dai-hoc")

# Load hết tất cả dữ liệu lên màn hình bằng cách dùng selenium để click vào nút "Xem thêm"
while True:
    try:
        load_more_button = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-outline.btn_loadmore")
        load_more_button.click()

        # Đợi một khoảng thời gian để dữ liệu tải xong
        time.sleep(5)
        
    except:
        break

# Tìm thẻ chứa các kết quả tra cứu
university = driver.find_element(By.CLASS_NAME, "lookup__results")
list_university = university.text.split('\n')

# Tạo danh sách chứa mã trường và tên trường
university_code = [University(list_university[i], list_university[i+1]) for i in range(0, len(list_university), 2)]

# Tạo danh sách chứa link của các trường đại học
for i in range(len(university_code)):
    # Sử dụng đúng cú pháp cho XPATH
    link_element = driver.find_element(By.XPATH, f"/html/body/main/div/div[1]/section[2]/ul/li[{i+1}]/div[1]/a")
    university_code[i].link = link_element.get_attribute("href")

# Vào link các trường đại học để crawl dữ liệu về 
# for i in university_code:
driver.get(university_code[0].link)

# Đợi phần tử <li> bên trong <span> có chứa văn bản 'Năm 2022' xuất hiện và có thể click
try:
    li_element = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='select2-dropdown select2-dropdown--below']//li[text()='Năm 2022']"))
    )
    
    # Cuộn phần tử vào vùng nhìn thấy và click
    driver.execute_script("arguments[0].scrollIntoView();", li_element)
    li_element.click()
    
except Exception as e:
    print(f"Không tìm thấy phần tử trong thời gian chờ: {e}")


# Tìm thẻ chứa điểm chuẩn

tables = driver.find_elements(By.XPATH, "/html/body/main/div/div[1]/section[2]/div/div[2]/div/div/div/table/tbody")
# Lặp qua từng hàng và in ra dữ liệu từ các thẻ <td>
rows = tables[0].find_elements(By.CSS_SELECTOR, "tr.university__benchmark")
cell_data = []
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    cell_data += [[cell.text for cell in cells]]  # Lấy văn bản trong mỗi thẻ <td>

major_list = []

for i in cell_data:
    if i[0] == '': continue
    else:
        major_list.append(Major(i[0], i[1], i[2], i[3], i[4]))

# for i in major_list:
#     print(i)

with open(f"{university_code[0].code}.csv", "w", newline='', encoding='utf-8') as csvfile:
    fieldnames = ["id", "major_name", "major_code", "score", "block", "tuition"]
    
    # Tạo writer object từ DictWriter
    writer = csv.writer(csvfile)
    
    # Ghi dòng tiêu đề
    writer.writerow(fieldnames)
    
    # Lặp qua major_list và ghi từng dòng dữ liệu
    for i in major_list:
        writer.writerow(i.writeToCSV())

# Đóng trình duyệt sau khi hoàn tất
driver.quit()
