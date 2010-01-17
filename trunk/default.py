import urllib,urllib2,re,xbmcplugin,xbmcgui
from pyamf.remoting.client import RemotingService

# IndaVideo Film - by gm74 2010.

def CATEGORIES():
        addDir('Mozifilmek','http://film.indavideo.hu/videos/latest/mozifilm/',1,'http://files.indavideo.hu/images/film/general/iv_logo_film.png')
        addDir( 'Dokumentumfilmek','http://film.indavideo.hu/videos/latest/dokfilm/',1,'http://files.indavideo.hu/images/film/general/iv_logo_film.png')
                       
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<div class="a1ItemImg">\n\t    \t<a href="(.+?)">\n\t\t\t\t<img src="(.+?)" alt="(.+?)"').findall(link)
        for url,thumbnail,name in match:
                addDir(name,url,2,thumbnail)

def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('"flashvars", "vID=(.+?)&amp;').findall(link)

        vid = match[0]
        gwurl='http://indavideo.hu/amfphp2/gateway.php'
        gwref='http://files.indavideo.hu/player/gup.swf'
        gwuagent='Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)'

        gw = RemotingService(   url=gwurl,
                                referer=gwref,
                                user_agent=gwuagent,
                            )

        getVideo_service = gw.getService('hash_2_video.GetVideoValues.getVideo')
        gwresponse = getVideo_service(vid,'s')
        flvurl = gwresponse['VALUES']['video_flv']
        flvurl = flvurl.replace('film-director.indavideo.hu','magex-rp2.film.indavideo.hu')
        addLink(name,flvurl,'')

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
