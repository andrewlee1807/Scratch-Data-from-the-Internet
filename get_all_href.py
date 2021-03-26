import requests
from bs4 import BeautifulSoup
from scratch_data import ScratchData
import os

main_src = "http://www.dapsa.kr/blog/?page_id=20129"
sub_folder = "history.go"
# sub_folder = "err"

# Get the fake request
html = requests.get(main_src, verify=False).text  # pull html as text
soup = BeautifulSoup(html, "html.parser")  # parse into BeautifulSoup object

class_name = None
src = "http://contents.history.go.kr/eh_kk/teach/notebook/hacsoob/03/03.htm"
src = "https://thewiki.kr/w/%EC%9E%A5%ED%98%95"
src = "http://contents.history.go.kr/eh_kk/teach/notebook/hacsoob/v/49/49.html"
tag_name = "body"
file_name = os.path.join(sub_folder, "thewiki" )
scratch_data = ScratchData(class_name, tag_name, file_name, src)
scratch_data.start_scratch()


# try:
#     tag_name = "div"
#     class_name = "entry-content"
#     # class_name = "article"
#     # filter to get list hrefs
#     div_area = soup.find("div", {"class": "entry-content"})
#     list_a_tags = div_area.find_all("a")
#     # Get all text from list of links
#     for i, a_tag in enumerate(list_a_tags):
#         src = a_tag.get("href")
#         print(src)
#         file_name = os.path.join(sub_folder, "dapsa." + class_name + str(i))
#         scratch_data = ScratchData(class_name, tag_name, file_name, src)
#         scratch_data.start_scratch()
#
# except:
#     print("Can not find correctly tag_name")
