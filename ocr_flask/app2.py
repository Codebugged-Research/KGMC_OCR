import os
from flask import Flask, render_template, request
import re

# import our OCR function
from ocr_core import ocr_core

data={}
report=['UHID','Reg Date','Patient Name ','Sex','Age','Department','Unit Name',
		'Sample Collection Date','Sample Received Time','Lab Ref No','SPECIMEN',
		'LAB NUMBER','GROSS','MIcROscoPIc','DIAGNOSIS','ADVICE','Report entered by','Report Checked by'
		,'Report Validated by','']

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@app.route('/')
def home_page():
    return render_template('index.html')

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])

def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        print(request.files)
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):

            # call the OCR function on it
            extracted_text = str(ocr_core(file))
            print(extracted_text)
            for key in report:
            	match = re.search(r''+str(key)+': (\S+)', extracted_text)
            	if match:
            		found = match.group(1)
            		print(''+key+': {}'.format(found))
            		data[key]=found
            	else:
            		print(''+key+': {}'.format("not found"))
            		data[key]="not found"

         

            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=data,
                                   img_src=UPLOAD_FOLDER + file.filename,
                                   uhid=data['UHID'],
                                   reg_date=data['Reg Date'],
                                   paitent_name=data['Patient Name '],
                                   sex=data['Sex'],
                                   age=data['Age'])
                                   #Department=,
                                   #unit_name=data[6],
                                   #Sample_coll=data[7],
                                   #sample_recived=data[8])
                                   
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug="True")