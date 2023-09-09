from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from scripts.trans_pt import exec_text
from scripts.trans_file import exec_file
from scripts.trans_wc import exec_wc
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# create a function
@csrf_exempt
def trans(request):
	template = loader.get_template('translate.html')
	return HttpResponse(template.render()) 

@csrf_exempt
def op(request):
	if 'cap' in request.POST:
		translated_text = exec_wc()
		return render(request,'op.html', {'translated_text': translated_text})
	if 'pt' in request.POST:
		translated_text = exec_text(request.POST['pt'])
		return render(request,'op.html', {'translated_text': translated_text})
	if 'myfile' in request.FILES:
		myfile = request.FILES['myfile']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		fileurl = fs.url(filename)
		translated_text = exec_file("H:\lst\LST"+fileurl)
		return render(request,'op.html', {'translated_text': translated_text})