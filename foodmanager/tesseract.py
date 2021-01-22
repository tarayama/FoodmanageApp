import pyocr
from PIL import Image
import pyocr.builders
import pytesseract
import re

def pyocr_tesseract(img):
    img = Image.open(img)
    result = None
    tools = pyocr.get_available_tools()
    print(tools[0].get_name())
    tool = tools[0]
    print(tool)
    langs = tool.get_available_languages()
    print("support languages: %s" % ", ".join(langs))
    lang = 'eng'  #言語設定で、「英語」を選択
    text = tool.image_to_string(
      img,
      lang=lang,
      builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    if text == "":
         text = None
    list = []
    str = ""
    for i in text:
        str += i
        if (i == "\n"):
            list.append(str)
            str = ""
    return list

def pytesseract_jpn(img):
    img = Image.open(img)
    #windows path
    #pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
        
    #heroku path
    pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract' 
    print("コマンドを取得しました")
        
        
    text = pytesseract.image_to_string(img, lang='jpn')
    print(text)
    if text == "":
         text = None
    list = []
    str = ""
    for i in text:
        str += i
        if (i == "\n"):
            list.append(str)
            str = ""
    return list


def drop_limit(string_list):
    res_list = []
    pattern = r'(明治|大正|昭和|平成|令和)?[12]?\d{1}?\d{1,2}[./\-年](0?[1-9]|1[0-2])[./\-月]?(0?[1-9]?|[12]?[0-9]?|3?[01]?)日?$'
    prog = re.compile(pattern)
    for string in string_list:
        result = prog.search(string)
        if result:
            #print("期限：",result.group())
            res_list.append(result.group())
    #print("うまく読み取れませんでした。もう一度お試しください")
    if not res_list:
        res_list.append("うまく読み取れませんでした。もう一度お試しください")
    return res_list
