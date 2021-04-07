import os, io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
import re
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'indigo-listener-828-d01ad2f2c179.json'
client = vision.ImageAnnotatorClient()
path = os.path.abspath('g.jpeg')
print(path)
data={}


with io.open(path, 'rb') as image_file:
	content = image_file.read()
image = vision.types.Image(content=content)
# print("image",image)

response = client.document_text_detection(image=image)

# print("responce", response)

doc = response.full_text_annotation
text=doc.text

print(text)

match = re.search(r'UHID: (\S+)', text)
if match:
	found = match.group(1)
	print('UHID: {}'.format(found))
	data['UHID']=found
else:
	print('UHID: {}'.format("not found"))
	data['UHID']="not found"

#print(text)
# pages = response.full_text_annotation.pages

# print(pages)


