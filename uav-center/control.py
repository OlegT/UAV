# -*- coding: utf-8


try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import os, time, math, string
import cgi
import wsgiref.handlers
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.api import memcache

import urllib2



class settingsbd(db.Model):
  keyS = db.StringProperty()
  valueS = db.TextProperty()

def GetST_Store(key):
    value=None
    STdb = db.GqlQuery("SELECT * FROM settingsbd WHERE keyS = :1", key)
    for item in STdb:
        value=item.valueS
    #default settings
    if value==None:
        if key=="B_str":            value=""
        if key=="TimeZone":         value="3"
    return value

def PutST_Store(key, value):
    STdb = db.GqlQuery("SELECT * FROM settingsbd WHERE keyS = :1", key)
    existItem=False
    for item in STdb:
       item.valueS=value
       db.put(item)
       existItem=True
    if existItem:
        #settingsbd.put(STdb)
        pass
    else:
        item = settingsbd()
        item.keyS=key
        item.valueS=value
        item.put()

def GetST(key):
  value = memcache.get(key)
  if value is not None:
    return value
  else:
    value = GetST_Store(key)
    memcache.add(key, value)
    return value

def PutST(key, value):
  PutST_Store(key, value)
  data = memcache.get(key)
  if data is not None:
    if data<>value:
        memcache.set(key, value)
  else:
    memcache.add(key, value)





def int2str(i):
    return str(i)

def str2int(s):
    try:
        i = int(s)
    except ValueError:
        i = 0
    return i



def UnitButtons(Bts,s):
    Bts2=Bts
    for si in s.split(","):
        if si[-1:]=="p":
            sv=si[:-1]+"m"
        else:
            sv=si[:-1]+"p"

        Bts1=[]
        Cont1=True

        for d in Bts2.split(","):
            if d==sv and Cont1:
                Cont1=False
            else: Bts1.append(d)
        if Cont1: Bts1.append(si)
        Bts2=Bts1
    res = ",".join(Bts2)
    if res[:1]=="," :  res=res[1:]
    return res

class logbd(db.Model):
  time1 = db.StringProperty()
  time2 = db.StringProperty()
  logstr = db.StringProperty()

def SendLog(s):
        logItem = logbd()
        logItem.time1=time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(time.time() + str2int(GetST('TimeZone'))*60*60))
        logItem.time2=time.strftime('%d-%m-%Y  %H:%M', time.gmtime(time.time() +  str2int(GetST('TimeZone'))*60*60))
        logItem.logstr=s
        logItem.put()

class LogHTML(webapp.RequestHandler):
    def get(self):
        Logs=logbd()
        Logss = Logs.all().order('-time1')
        Logss = Logss.fetch(900)
        template_values = {
          'Logs': Logss,
          }

        path = os.path.join(os.path.dirname(__file__), 'templates')
        path = os.path.join(path, 'logs.html')
        self.response.out.write(template.render(path, template_values))


class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {'a':""}
        path = os.path.join(os.path.dirname(__file__), 'templates')
        path = os.path.join(path, 'index.html')
        return self.response.out.write(template.render(path, template_values))

def InsertFormData():
    template_values = {

    'submit1': GetST('submit1'),
    }

    path = os.path.join(os.path.dirname(__file__), 'templates')
    path = os.path.join(path, 'settings.html')
    return template.render(path, template_values)



class Settings(webapp.RequestHandler):
  def get(self):
    SendLog("Init Control")
    self.response.out.write(InsertFormData())

#  def post(self):
    # сохранение настроек в базу

#    SendLog(self.request.get('data'))
    #self.response.out.write(InsertFormData())


class Button(webapp.RequestHandler):
  def post(self):
    #PutST('CP1', int2str(str2int(GetST('CP1'))+1))
    #SendLog("Button1: " + GetST('CP1'))

    PutST('B_str', UnitButtons(GetST('B_str'),self.request.get('data')))
    SendLog("Button:" + GetST('B_str'))
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Ok')


class Result(webapp.RequestHandler):
  def get(self):
    SendLog("Result: " + GetST('B_str'))
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write("Buttons:"+GetST('B_str'))
    PutST('B_str', "")


  def post(self):
    #SendLog("Result: (Post) " + self.request.get('Model'))
    res="Buttons:"+GetST('B_str')
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(res)
    PutST('B_str', "")



def main():
  application = webapp.WSGIApplication(
                                       [('/', MainPage),
                                        ('/settings', Settings),
                                        ('/logs', LogHTML),
                                        ('/button', Button),
                                        ('/result', Result),
                                        ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()



