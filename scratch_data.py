"""
Author: Andrew
Copyright (C) : 2021
"""

import requests
from bs4 import BeautifulSoup
import re

import pandas as pd


class ScratchData:
    # Constant
    KOREAN = "ko"
    SPECIAL_CHARACTERS = "~!@#$%^&*()-+?_=<>”\n"
    EXTENSION = ".txt"

    def __init__(self, class_name, tag_name, file_name, src):
        self.file_name = file_name
        self.class_name = class_name
        self.tag_name = tag_name
        self.src = src

    def store2txt(self, file_name, data):
        # text_file = open("data_raw.txt", "a", encoding="utf-8")
        text_file = open(file_name, "w", encoding="utf-8")
        # Write a list String to txt
        for i in data:
            text_file.writelines(i + "\n")

        # text_file.write("\n".join(data))
        text_file.close()

    def break2sentence(self, st):
        """
        # Break the to list sentence
        :param st: String
        :return:
        """
        # Remove all the special characters
        for character in self.SPECIAL_CHARACTERS:
            st = st.replace(character, "")
        # re.sub("[" + SPECIAL_CHARACTERS + "]", "", st)

        return re.split("[.!;?:\xa0ㅇ]", st)

    def break_line_by_tag(self, soup, tag_name, class_name=None):
        """
        In case : filter_raw_data is not worked and get only a string without "/n"
        :param soup: BeautifulSoup
        :param tag_name: string
        :param class_name: string
        :return: the list of sentences by tag_name (and class_name) (string)
        """
        list_sentence_by_tag = []
        # Conditionally filter
        if class_name is None:
            tag_list = soup.find_all(tag_name)
        else:
            tag_list = soup.find_all(tag_name, {"class": class_name})

        for tag_sentence in tag_list:
            sub_sentence = self.break2sentence(tag_sentence.get_text().strip())
            list_sentence_by_tag.extend(sub_sentence)
        return list_sentence_by_tag

    def filter_raw_data(self, soup, tag_name, class_name=None):
        """
        Get correctly raw data from html by a Tag_name
        :param soup: BeautifulSoup
        :param tag_name: String
        :param class_name: String
        :return: String
        """
        # Conditionally filter
        if class_name is None:
            soup_found = soup.find_all(tag_name)
        else:
            soup_found = soup.find_all(tag_name, {"class": class_name})
            # soup_found = soup.find(tag_name, {"id": class_name})

        if len(soup_found) == 0:
            print("Cannot found this tag_name")
            return

        # Comment this code after found the correct position to save
        if len(soup_found) > 1:
            print("Found more than one tag")
            return

        data_raw = soup_found[0].get_text().strip()
        # data_raw = soup_found.get_text().strip()
        return data_raw

    def ck_detect(self, texts):
        """
        Detect a sentence was written in Chinese or Korean
        :param texts: String
        :return:
        """
        # chinese
        if re.search("[\u4e00-\u9FFF]", texts):
            return "zh"
        # korean
        if re.search("[\uac00-\ud7a3]", texts):
            return "ko"
        return None

    def format_data(self, data_raw):
        """
        try to break to separate sentences
        :param data_raw: String
        :return: list of string
        """
        list_sentence_by_tag = []
        pre_list_sentence = self.break2sentence(data_raw)
        for sentence in pre_list_sentence:
            if len(sentence) > 2 and self.ck_detect(sentence) == self.KOREAN:
                list_sentence_by_tag.append(sentence.lstrip())

        return list_sentence_by_tag

    def start_scratch(self):
        html = requests.get(self.src, verify=False).text  # pull html as text
        soup = BeautifulSoup(html, "html.parser")  # parse into BeautifulSoup object

        #  Filter data
        try:
            data_tag = self.filter_raw_data(soup, self.tag_name, self.class_name)
            # data_tag = self.break_line_by_tag(soup, self.tag_name, self.class_name)
            data_clearly = self.format_data(data_tag)
            self.store2txt(self.file_name + self.EXTENSION, data_clearly)
            print("Successfully")
        except Exception:
            print("Failed to save the data")

# # get web address
# tag_name = "div"
# class_name = "view-info-cont"
# src = "https://www.museum.go.kr/site/main/exhiSpecialTheme/view/specialGallery?exhiSpThemId=542310&listType=gallery"
# src = "https://www.museum.go.kr/site/main/exhiSpecialTheme/view/specialGallery?exhiSpThemId=562558&listType=gallery"
# src = "https://www.museum.go.kr/site/main/exhiSpecialTheme/view/specialGallery?exhiSpThemId=514869&listType=list&current=present"
# src = "https://www.museum.go.kr/site/main/exhiSpecialTheme/view/specialGallery?exhiSpThemId=565928&listType=list&current=present"
#
# # class_name = "con_txt"
# # src = "https://jinju.museum.go.kr/kor/html/sub02/0202.html?mode=V&mng_no=91"
# # src = "https://gimhae.museum.go.kr/kr/html/sub02/020201.html?mode=V&mng_no=130"
#
# class_name = "showCont"
# src = "https://chuncheon.museum.go.kr/html/kr/display/display_02_01_t01.html?mod=view&linkid=030302&dis_gubun=01&idx=15142"
#
# file_name = "dapsa.kr"
# class_name = "entry-content"
# src = "http://www.dapsa.kr/blog/?page_id=19242"
#
# html = requests.get(src, verify=False).text  # pull html as text
# soup = BeautifulSoup(html, "html.parser")  # parse into BeautifulSoup object
#
# #  Filter data
# try:
#     data_tag = filter_raw_data(soup, tag_name, class_name)
#     data_clearly = format_data(data_tag)
#     store2txt(file_name + EXTENSION, data_clearly)
#     print("Successfully")
# except Exception:
#     print("Failed to save the data")
