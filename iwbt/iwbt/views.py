from django.template import Template, Context
from django.http import HttpResponse, Http404
from django.template.loader import get_template
import datetime

def hello(request):
	return HttpResponse("Hello world")

def home(request):
	wd = '/home/exley/Django/iwbt/iwbt/web/'
	#t = _fetch_html_template(wd + 'index.html')
	now = datetime.datetime.now().strftime('%m/%d/%Y')
	t = get_template('index.html')
	html = t.render(Context({'img_wd': wd}))
	return HttpResponse(html)

def select_river(request):
	wd = '/home/exley/Django/iwbt/iwbt/web/'
	t = get_template('select_river.html')
	html = t.render(Context({'': ''}))
	return HttpResponse(html)

def about_us(request):
	wd = '/home/exley/Django/iwbt/iwbt/web/'
	t = _fetch_html_template(wd + 'about_us.html')
	html = t.render(Context({'temp_title': 'wololo'}))
	return HttpResponse(html)


def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body>It is now %s</body></html>" % now
	return HttpResponse(html)


def _fetch_html_template(file_dir):
	f_open = open(file_dir)
	t = Template(f_open.read())
	f_open.close()
	return t
