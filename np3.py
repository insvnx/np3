#
# np3 by INSVNX
#
# requires hexchat / python3 / vlc
#   add http iface in vlc
#   modify 'password' field below
#
# /np3 - spams chan with current song
# 
import urllib.request
import xml.etree.ElementTree
import re
import hexchat

__author__ = "INSVNX"
__module_name__ = "np3"
__module_version__ = "3.0"
__module_description__ = "Now Playing 3"

def on_np3(word, word_eol, userdata):
	vlcurl = 'http://[::1]:8080/requests/status.xml'
	vlcrealm = 'VLC stream'
	location = 'http://[::1]:8080/' 
	username = ''
	password = 'teaminsane'
	auth = urllib.request.HTTPBasicAuthHandler()
	auth.add_password(vlcrealm, location, username, password)
	opener = urllib.request.build_opener(auth)
	urllib.request.install_opener(opener)
	status = urllib.request.urlopen(vlcurl)
	tree = xml.etree.ElementTree.parse(status)
	root = tree.getroot()

	for artist in root.findall(".//*[@name='artist']"):
	  artist = artist.text

	for title in root.findall(".//*[@name='title']"):
	  title = title.text

	for length in root.findall('length'):
	  t = int(length.text)
	  m = t // 60
	  s = t - m * 60
	  minutes = str(m)
	  seconds = str(s)

	for bitrate in root.findall(".//*[@name='Bitrate']"):
	  bits = re.sub(r' kb/s', 'kb/s', bitrate.text)

	hexchat.command("say np3("+artist+" - "+title+")("+minutes+"m"+seconds+"s/"+bits+")")
	return hexchat.EAT_ALL

hexchat.hook_command("np3", on_np3, userdata=hexchat.get_info('channel'))

hexchat.prnt(__module_name__ + ' by ' + __author__ + ' loaded.')
