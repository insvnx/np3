# np3 by INSVNX
# requires hexchat / python3 / vlc
#   add http iface and set password in vlc
#   modify 'password' field below
# /np3 - spams chan with current song
import urllib.request
import xml.etree.ElementTree
import html
from html import unescape
import re
import hexchat

__author__ = "INSVNX"
__module_name__ = "np3"
__module_version__ = "4.2.0"
__module_description__ = "Now Playing 3"

def format_case(a):
    return a.group(1) + a.group(2).upper()

def on_np3(word, word_eol, userdata):
	vlcurl = 'http://localhost:8080/requests/status.xml'
	vlcrealm = 'VLC stream'
	location = 'http://localhost:8080/'
	username = ''
	password = 'CHANGETHISPASSWORD'
	auth = urllib.request.HTTPBasicAuthHandler()
	auth.add_password(vlcrealm, location, username, password)
	opener = urllib.request.build_opener(auth)
	urllib.request.install_opener(opener)
	status = urllib.request.urlopen(vlcurl)
	tree = xml.etree.ElementTree.parse(status)
	root = tree.getroot()

	for artist in root.findall(".//*[@name='artist']"):
	  scrubbed = html.unescape(artist.text)
	  clean = re.sub(r'_', ' ', scrubbed)
	  format = re.sub("(^|\s)(\S)", format_case, clean)
	  artist = format

	for album in root.findall(".//*[@name='album']"):
	  scrubbed = html.unescape(album.text)
	  clean = re.sub(r'_', ' ', scrubbed)
	  format = re.sub("(^|\s)(\S)", format_case, clean)
	  album = format

	for title in root.findall(".//*[@name='title']"):
	  scrubbed = html.unescape(title.text)
	  clean = re.sub(r'_', ' ', scrubbed)
	  format = re.sub("(^|\s)(\S)", format_case, clean)
	  title = format

	for genre in root.findall(".//*[@name='genre']"):
	  scrubbed = html.unescape(genre.text)
	  clean = re.sub(r'_', ' ', scrubbed)
	  format = re.sub("(^|\s)(\S)", format_case, clean)
	  genre = format

	for date in root.findall(".//*[@name='date']"):
	  date = int(date.text)
	  year = str(date)

	for length in root.findall('length'):
	  time = int(length.text)
	  division = time // 60
	  subtraction = time - division * 60
	  minutes = str(division)
	  seconds = str(subtraction)

	for bitrate in root.findall(".//*[@name='Bitrate']"):
	  format = re.sub(r' kb/s', '', bitrate.text)
	  vbr_check = int(format)
	  if vbr_check < 128:
	    bitrate = str(256)
	  else:
	    bitrate = str(vbr_check) 

	hexchat.command("say mp3("+artist+"-"+album+"-"+title+"-"+year+")("+minutes+"m"+seconds+"s/"+bitrate+"kb/s)")
	return hexchat.EAT_ALL

hexchat.hook_command("np3", on_np3, userdata=hexchat.get_info('channel'))

hexchat.prnt(__module_name__ + ' ' + __module_version__ + ' by ' + __author__ + ' loaded.')
