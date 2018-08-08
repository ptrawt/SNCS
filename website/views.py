from django.shortcuts import render

# Create your views here.
def index(request):
	header_str = 'Smart Network Controller System'
	context = {
		'var1' : header_str
	}
	return render(request, 'index.html', context)