import cv2
import pytesseract
from pytesseract import Output
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv2.imread('h.jpg')

d = pytesseract.image_to_data(img, output_type=Output.DICT)
#d = pytesseract.image_to_data(img, pandas_config=Output.DATAFRAME)

data=pd.DataFrame.from_dict(d)
txt=data.dropna()
print(txt['text'])

n_boxes = len(d['text'])
for i in range(n_boxes):
    if int(d['conf'][i]) > 60:
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)

#df = pd.DataFrame(d)
#print(df)