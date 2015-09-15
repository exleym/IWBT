from django.template import Template, Context
from django.http import HttpResponse, Http404
from django.template.loader import get_template
import paddlelog.models as plmods
import datetime


def home(request):
	t = get_template('index.html')
	html = t.render(Context({}))
	return HttpResponse(html)

def select_river(request):
	wd = '/home/exley/Projects/IWBT/iwbt/iwbt/web/'
	t = get_template('select_river.html')
	river_list = plmods.River.objects.all().order_by('river_name', 'section_name')
	r_dict = {'river_list': river_list,}
	html = t.render(Context(r_dict))
	return HttpResponse(html)

def about_us(request):
	wd = '/home/exley/Projects/IWBT/iwbt/iwbt/web/'
	t = _fetch_html_template(wd + 'about_us.html')
	html = t.render(Context({'temp_title': 'wololo'}))
	return HttpResponse(html)


def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body>It is now %s</body></html>" % now
	return HttpResponse(html)

def show_river(request, river_name, section_name):
	t = get_template('river_main.html')
	section_name = section_name.replace('_', ' ')
	river = plmods.River.objects.get(river_name=river_name, section_name=section_name)
	river_info = {'river': river}
	html = t.render(Context(river_info))
	return HttpResponse(html)


def _fetch_html_template(file_dir):
	f_open = open(file_dir)
	t = Template(f_open.read())
	f_open.close()
	return t
