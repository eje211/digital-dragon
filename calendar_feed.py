from django.http import HttpResponse
import urllib2

def feed(request, args):
  addr = 'https://www.google.com/calendar/feeds/vc712v7s84edkgbea3l41eskn8%40group.calendar.google.com/public/basic' + args
  return HttpResponse(urllib2.urlopen(addr).read(), mimetype="application/xml")
  
