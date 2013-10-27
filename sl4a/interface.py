import android, os, sys, urllib, urllib2

url = 'http://uav-center.appspot.com/result'

#defaults
Tiles=[0,0,0,0,0,0]


def int2str(i):
    return str(i)

def str2int(s):
    try:
        i = int(s)
    except ValueError:
        i = 0
    return i

def ColorI(i):
    if i>=4: CI="FFFFFF"
    if i==3: CI="C0C0C0"
    if i==2: CI="808080"
    if i==1: CI="404040"
    if i<=0: CI="000000"
    return CI


def Interface1(T):
    s='<TABLE border=0 bgcolor=#000000>'
    s=s+'<TR><TD></TD> <TD bgcolor=#000000><p style="color:#000000">______________________</p></TD> <TD bgcolor=#000000> <p style="color:#000000">______________________</p></TD> <TD bgcolor=#000000><p style="color:#000000">______________________</p></TD> </TR>'
    s=s+'<TR><TD>1<p>1<p>1<p>1</TD> <TD bgcolor=#'+ColorI(T[1])+'></TD> <TD bgcolor=#'+ColorI(T[3])+'></TD><TD bgcolor=#'+ColorI(T[5])+'></TD></TR>'
    s=s+'<TR><TD>1<p>1<p>1<p>1</TD> <TD bgcolor=#'+ColorI(T[0])+'></TD> <TD bgcolor=#'+ColorI(T[2])+'></TD><TD bgcolor=#'+ColorI(T[4])+'></TD></TR>'
    s=s+'</TABLE>'
    return s


def Analys(s):
    for line in s.split("\n"):
        if line[:8]=='Buttons:':
            line=line[8:]
            for b in line.split(","):
                i=str2int(b[:-1])-1
                if i>=0 and i<=5:
                    if b[-1:]=="p":
                        if Tiles[i]<4: Tiles[i]=Tiles[i]+1
                    else:
                        if Tiles[i]>0: Tiles[i]=Tiles[i]-1

def LinkToServer(gps_data):

    values = {
            'Model' : 'FlyM1',
            'location' : 'Northampton',
            'language' : 'Python',
            }




    try:
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        #i=str2int(the_page)
        Analys(the_page)
    except:
        i = 0
        feed="Error"









droid = android.Android()
#print os.path.dirname(sys.argv[0]) + '/interface.html'
droid.webViewShow(os.path.dirname(sys.argv[0]) + '/interface.html')

droid.startLocating(0, 0)
event = droid.eventWait(1000).result
gps_data=''

while True:
    #if event['name'] == "location": gps_data=event['data']['gps']
    LinkToServer(gps_data)

    droid.eventPost('html_code', Interface1(Tiles))






