import urllib.request
import xml.etree.ElementTree
import re
import hexchat

__author__ = "INSVNX"
__module_name__ = "np3"
__module_version__ = "3.0"
__module_description__ = "Now Playing 3"

def on_np3(word, word_eol, userdata):
	vlcurl = 'http://localhost:8080/requests/status.xml'
	vlcrealm = 'VLC stream'
	location = 'http://localhost:8080/' 
	username = ''
	password = 'ob08FS7ZkRMiHNZU'
	auth = urllib.request.HTTPBasicAuthHandler()
	auth.add_password(vlcrealm, location, username, password)
	opener = urllib.request.build_opener(auth)
	urllib.request.install_opener(opener)
	status = urllib.request.urlopen(vlcurl)
	tree = xml.etree.ElementTree.parse(status)
	root = tree.getroot()

	for info in root.findall(".//*[@name='artist']"):
	  artist = info.text

	for info in root.findall(".//*[@name='title']"):
	  title = info.text

	for length in root.findall('length'):
	  t = int(length.text)
	  m = t // 60
	  s = t - m * 60
	  minutes = str(m)
	  seconds = str(s)

	for info in root.findall(".//*[@name='Bitrate']"):
	  bitrate = re.sub(r' kb/s', 'kb/s', info.text)

	hexchat.command("say np3("+artist+" - "+title+")("+minutes+"m"+seconds+"s/"+bitrate+")")
	return hexchat.EAT_ALL

hexchat.hook_command("np3", on_np3, userdata=hexchat.get_info('channel'))

hexchat.prnt(__module_name__ + ' by ' + __author__ + ' loaded.')
