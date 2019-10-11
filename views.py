from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib import messages
import os
from datetime import datetime

# Create your views here.
def upload_data_sheet(request):
    template="ocr/upload_doc.html"
    if request.method=="POST":
        uploaded_file = request.FILES['file']
        if is_document_file_pdf(uploaded_file.name.split('.')[1]):
            fs=FileSystemStorage()
            name=fs.save(uploaded_file.name.strip().replace(" ", "_"),uploaded_file)
            uploaded_file_url=fs.url(name)
            uploadedFilePath=getAbsolutePath(uploaded_file_url)
            print(uploadedFilePath)
            Imagespath = getImageOfPdf(uploadedFilePath)
            print(Imagespath)
            return render(request, template)
        messages.error(request, ' * Please upload pdf format')
        return render(request, "home/download.html")

def getImageOfPdf(inputpath):
    from pdf2jpg import pdf2jpg
    outputpath,_ = os.path.split(inputpath)
    outputimagePath = makedirectory(outputpath)
    # print(outputpath)
    # prepare task for it
    result = pdf2jpg.convert_pdf2jpg(inputpath, outputimagePath, pages="ALL")
    print(result)
    return outputimagePath 

def makedirectory(path,):
    try:
        dirname = getFileNameInDateTime()
        # print(dirname)
        os.mkdir(os.path.join( path+'/', dirname))
    except OSError as e:
        if e.errno == 17:
            # Dir already exists. No biggie.
            print("error")
            return None
    return  path+'/' + dirname

def getFileNameInDateTime():
    return datetime.now().strftime('%Y.%m.%d.%H.%M.%S') #2010.08.09.12.08.45 

def getAbsolutePath(url):
    basePath=settings.BASE_DIR + url
    return basePath

def is_document_file_pdf(ext):
    pdf_ext_list = ['pdf']
    return ext.lower() in pdf_ext_list