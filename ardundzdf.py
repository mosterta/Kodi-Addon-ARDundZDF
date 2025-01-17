# -*- coding: utf-8 -*-

# Python3-Kompatibilität:
from __future__ import absolute_import		# sucht erst top-level statt im akt. Verz. 
from __future__ import division				# // -> int, / -> float
from __future__ import print_function		# PYTHON2-Statement -> Funktion
from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui, xbmcvfs

# o. Auswirkung auf die unicode-Strings in PYTHON3:
from kodi_six.utils import py2_encode, py2_decode

import os, sys, subprocess 
PYTHON2 = sys.version_info.major == 2
PYTHON3 = sys.version_info.major == 3
if PYTHON2:
	from urllib import quote, unquote, quote_plus, unquote_plus, urlencode, urlretrieve
	from urllib2 import Request, urlopen, URLError 
	from urlparse import urljoin, urlparse, urlunparse, urlsplit, parse_qs
elif PYTHON3:
	from urllib.parse import quote, unquote, quote_plus, unquote_plus, urlencode, urljoin, urlparse, urlunparse, urlsplit, parse_qs
	from urllib.request import Request, urlopen, urlretrieve
	from urllib.error import URLError
	try:									
		xbmc.translatePath = xbmcvfs.translatePath
	except:
		pass

# Kodi-API-Änderungen:
#	18.08.2021 xbmc.translatePath -> xbmc.translatePath (nur PYTHON3)
#		https://github.com/xbmc/xbmc/pull/18345
#		https://forum.kodi.tv/showthread.php?tid=344263&pid=2975581#pid2975581
#	13.09.2020 	LOG_MSG = xbmc.LOGNOTICE (nur PYTHON2) 	Modul util
#				LOG_MSG = xbmc.LOGINFO (nur PYTHON3) 	Modul util
#		https://forum.kodi.tv/showthread.php?tid=344263&pid=2943703#pid2943703


# Python
import base64 			# url-Kodierung für Kontextmenüs
import sys				# Plattformerkennung
import shutil			# Dateioperationen
import re				# u.a. Reguläre Ausdrücke, z.B. in CalculateDuration
import datetime, time
import json				# json -> Textstrings
import string
import importlib		# dyn. Laden zur Laufzeit, s. router


# ständige Addonmodule - Rest dyn. in router
import resources.lib.updater as updater	
from resources.lib.util import *
import resources.lib.EPG as EPG
import resources.lib.epgRecord as epgRecord

																		
# +++++ ARDundZDF - Addon Kodi-Version, migriert von der Plexmediaserver-Version +++++

# VERSION -> addon.xml aktualisieren
# 	<nr>105</nr>										# Numerierung für Einzelupdate
VERSION = '4.7.2'
VDATE = '16.05.2023'


# (c) 2019 by Roland Scholz, rols1@gmx.de
# 
#     Functions -> README.md
# 
# 	Licensed under MIT License (MIT)
# 	(previously licensed under GPL 3.0)
# 	A copy of the License you find here:
#		https://github.com/rols1/Kodi-Addon-ARDundZDF/blob/master/LICENSE.txt

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.


####################################################################################################
NAME			= 'ARD und ZDF'
PREFIX 			= '/video/ardundzdf'		#	
												
PLAYLIST 		= 'livesenderTV.xml'		# TV-Sender-Logos erstellt von: Arauco (Plex-Forum). 											
FAVORITS_Pod 	= 'podcast-favorits.txt' 	# Lesezeichen für Podcast-Erweiterung 
FANART					= 'fanart.png'		# ARD + ZDF - breit
ART 					= 'art.png'			# ARD + ZDF
ICON 					= 'icon.png'		# ARD + ZDF
ICON_SEARCH 			= 'ard-suche.png'
ICON_ZDF_SEARCH 		= 'zdf-suche.png'				
ICON_FILTER				= 'icon-filter.png'	

ICON_MAIN_ARD 			= 'ard-mediathek.png'
ICON_MAIN_ZDF 			= 'zdf-mediathek.png'
ICON_MAIN_ZDFMOBILE		= 'zdf-mobile.png'
ICON_MAIN_TVLIVE 		= 'tv-livestreams.png'
ICON_MAIN_RADIOLIVE 	= 'radio-livestreams.png'
ICON_MAIN_UPDATER 		= 'plugin-update.png'
ICON_UPDATER_NEW 		= 'plugin-update-new.png'

ICON_ARD_AZ 			= 'ard-sendungen-az.png'
ICON_ARD_VERP 			= 'ard-sendung-verpasst.png'
ICON_ARD_RUBRIKEN 		= 'ard-rubriken.png'
ICON_ARD_BARRIEREARM 	= 'ard-barrierearm.png'
ICON_ARD_HOERFASSUNGEN	= 'ard-hoerfassungen.png'
ICON_ARD_BILDERSERIEN 	= 'ard-bilderserien.png'

ICON_ZDF_AZ 			= 'zdf-sendungen-az.png'
ICON_ZDF_VERP 			= 'zdf-sendung-verpasst.png'
ICON_ZDF_RUBRIKEN 		= 'zdf-rubriken.png'
ICON_ZDF_BARRIEREARM 	= 'zdf-barrierearm.png'
ICON_ZDF_BILDERSERIEN 	= 'zdf-bilderserien.png'

ICON_MAIN_POD			= 'radio-podcasts.png'
ICON_POD_AZ				= 'pod-az.png'
ICON_POD_FEATURE 		= 'pod-feature.png'
ICON_POD_TATORT 		= 'pod-tatort.png'
ICON_POD_RUBRIK	 		= 'pod-rubriken.png'
ICON_POD_NEU			= 'pod-neu.png'
ICON_POD_MEIST			= 'pod-meist.png'
ICON_POD_REFUGEE 		= 'pod-refugee.png'
ICON_POD_FAVORITEN		= 'pod-favoriten.png'

ICON_MAIN_AUDIO			= 'ard-audiothek.png'
ICON_AUDIO_LIVE			= 'ard-audio-live.png'
ICON_AUDIO_AZ			= 'ard-audio-az.png'

ICON_OK 				= "icon-ok.png"
ICON_INFO 				= "icon-info.png"
ICON_WARNING 			= "icon-warning.png"
ICON_NEXT 				= "icon-next.png"
ICON_CANCEL 			= "icon-error.png"
ICON_MEHR 				= "icon-mehr.png"
ICON_DOWNL 				= "icon-downl.png"
ICON_DOWNL_DIR			= "icon-downl-dir.png"
ICON_DELETE 			= "icon-delete.png"
ICON_STAR 				= "icon-star.png"
ICON_NOTE 				= "icon-note.png"
ICON_SPEAKER 			= "icon-speaker.png"
ICON_TOOLS 				= "icon-tools.png"
ICON_PREFS 				= "icon-preferences.png"

# Basis DIR-Icons: Tango/folder.png s. Wikipedia Tango_Desktop_Project
ICON_DIR_CURLWGET 		= "Dir-curl-wget.png"
ICON_DIR_FOLDER			= "Dir-folder.png"
ICON_DIR_PRG 			= "Dir-prg.png"
ICON_DIR_IMG 			= "Dir-img.png"
ICON_DIR_TXT 			= "Dir-text.png"
ICON_DIR_MOVE 			= "Dir-move.png"
ICON_DIR_MOVE_SINGLE	= "Dir-move-single.png"
ICON_DIR_MOVE_ALL 		= "Dir-move-all.png"
ICON_DIR_BACK	 		= "Dir-back.png"
ICON_DIR_SAVE 			= "Dir-save.png"
ICON_DIR_STRM			= "Dir-strm.png"

ICON_DIR_VIDEO 			= "Dir-video.png"
ICON_DIR_WORK 			= "Dir-work.png"
ICON_MOVEDIR_DIR 		= "Dir-moveDir.png"
ICON_DIR_FAVORITS		= "Dir-favorits.png"

ICON_DIR_WATCH			= "Dir-watch.png"
ICON_PHOENIX			= 'phoenix.png'			

# Github-Icons zum Nachladen aus Platzgründen
ICON_MAINXL 	= 'https://github.com/rols1/PluginPictures/blob/master/ARDundZDF/TagesschauXL/tagesschau.png?raw=true'
GIT_CAL			= "https://github.com/rols1/PluginPictures/blob/master/ARDundZDF/KIKA_tivi/icon-calendar.png?raw=true"
GIT_TIVIHOME	= "https://github.com/rols1/PluginPictures/blob/master/ARDundZDF/KIKA_tivi/zdftivi-home.png?raw=true"

# 01.12.2018 	Änderung der BASE_URL von www.ardmediathek.de zu classic.ardmediathek.de
# 06.12.2018 	Änderung der BETA_BASE_URL von  beta.ardmediathek.de zu www.ardmediathek.de
# 03.06.2021	Classic-Version im Web entfallen, Code bereinigt
ARD_BASE_URL	= 'https://www.ardmediathek.de'								# vorher beta.ardmediathek.de
ARD_VERPASST 	= '/tv/sendungVerpasst?tag='								# ergänzt mit 0, 1, 2 usw.
# ARD_AZ 			= 'https://www.ardmediathek.de/ard/shows'				# ARDneu, komplett (#, A-Z)
ARD_AZ 			= '/tv/sendungen-a-z?buchstabe='							# ARD-Classic ergänzt mit 0-9, A, B, usw.
ARD_Suche 		= '/tv/suche?searchText=%s&words=and&source=tv&sort=date'	# Vorgabe UND-Verknüpfung
ARD_Live 		= '/tv/live'


# ARD-Podcasts - 03.06.2021 alle Links der Classic-Version entfernt

# ARD Audiothek
ARD_AUDIO_BASE = 'https://api.ardaudiothek.de/'
HEADERS="{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', \
	'Referer': '%s', 'Accept-Encoding': 'gzip, deflate, br', 'Accept': 'application/json, text/plain, */*'}"

# Relaunch der Mediathek beim ZDF ab 28.10.2016: xml-Service abgeschaltet
ZDF_BASE				= 'https://www.zdf.de'
ZDF_CacheTime_Start = 300			# 5 Min.
ZDF_CacheTime_AZ 	= 1800			# 30 Min.

REPO_NAME		 	= 'Kodi-Addon-ARDundZDF'
GITHUB_REPOSITORY 	= 'rols1/' + REPO_NAME

PLog('Addon: lade Code')
PluginAbsPath = os.path.dirname(os.path.abspath(__file__))				# abs. Pfad für Dateioperationen
ADDON_ID      	= 'plugin.video.ardundzdf'
SETTINGS 		= xbmcaddon.Addon(id=ADDON_ID)
ADDON_NAME    	= SETTINGS.getAddonInfo('name')
SETTINGS_LOC  	= SETTINGS.getAddonInfo('profile')
ADDON_PATH    	= SETTINGS.getAddonInfo('path')
ADDON_VERSION 	= SETTINGS.getAddonInfo('version')
PLUGIN_URL 		= sys.argv[0]
HANDLE			= int(sys.argv[1])

ICON = R(ICON)
PLog("ICON: " + ICON)
TEMP_ADDON		= xbmc.translatePath("special://temp")
USERDATA		= xbmc.translatePath("special://userdata")
ADDON_DATA		= os.path.join("%sardundzdf_data") % USERDATA

# Anpassung Kodi 20 Nexus: "3.0.0" -> "3."
if 	check_AddonXml('"xbmc.python" version="3.'):						# ADDON_DATA-Verzeichnis anpasen
	PLog('python_3.x.x')
	ADDON_DATA	= os.path.join("%s", "%s", "%s") % (USERDATA, "addon_data", ADDON_ID)
PLog("ADDON_DATA: " + ADDON_DATA)


THUMBNAILS 		= os.path.join(USERDATA, "Thumbnails")
M3U8STORE 		= os.path.join(ADDON_DATA, "m3u8") 
DICTSTORE 		= os.path.join(ADDON_DATA, "Dict") 
SLIDESTORE 		= os.path.join(ADDON_DATA, "slides") 
SUBTITLESTORE 	= os.path.join(ADDON_DATA, "subtitles") 
TEXTSTORE 		= os.path.join(ADDON_DATA, "Inhaltstexte")
WATCHFILE		= os.path.join(ADDON_DATA, "merkliste.xml") 
JOBFILE			= os.path.join(ADDON_DATA, "jobliste.xml") 		# Jobliste für epgRecord
MONITOR_ALIVE 	= os.path.join(ADDON_DATA, "monitor_alive") 	# Lebendsignal für JobMonitor
DL_CHECK 		= os.path.join(ADDON_DATA, "dl_check_alive") 	# Anzeige Downloads (Lockdatei)
DL_CNT 			= os.path.join(ADDON_DATA, "dl_cnt") 			# Anzeige Downloads (Zähler)
STRM_SYNCLIST	= os.path.join(ADDON_DATA, "strmsynclist")		# strm-Liste für Synchronisierung	
STRM_CHECK 		= os.path.join(ADDON_DATA, "strm_check_alive") 	# strm-Synchronisierung (Lockdatei)
FLAG_OnlyUrl	= os.path.join(ADDON_DATA, "onlyurl")			# Flag PlayVideo_Direct	-> strm-Modul
PLog(SLIDESTORE); PLog(WATCHFILE); 
check 			= check_DataStores()					# Check /Initialisierung / Migration 
PLog('check: ' + str(check))


# die tvtoday-Seiten decken 12 Tage ab, trotzdem EPG-Lauf alle 12 Stunden
#	 (dto. Cachezeit für einz. EPG-Seite in EPG.EPG).
# 26.10.2020 Update der Datei livesenderTV.xml hinzugefügt - s. thread_getepg
if SETTINGS.getSetting('pref_epgpreload') == 'true':		# EPG im Hintergrund laden?
	EPGACTIVE = os.path.join(DICTSTORE, 'EPGActive') 		# Marker thread_getepg aktiv
	EPGCacheTime = 43200									# 12 STd.
	is_activ=False
	if os.path.exists(EPGACTIVE):							# gesetzt in thread_getepg 
		is_activ=True
		now = time.time()
		mtime = os.stat(EPGACTIVE).st_mtime
		diff = int(now) - mtime
		PLog(diff)
		if diff > EPGCacheTime:								# entf. wenn älter als 1 Tag	
			os.remove(EPGACTIVE)
			is_activ=False
	if is_activ == False:									# EPG-Daten veraltet, neu holen
		from threading import Thread
		bg_thread = Thread(target=EPG.thread_getepg, args=(EPGACTIVE, DICTSTORE, PLAYLIST))
		bg_thread.start()
													
if SETTINGS.getSetting('pref_dl_cnt') == 'true':			# laufende Downloads anzeigen
	if os.path.exists(DL_CHECK) == False:					# Lock beachten (Datei dl_check_alive)						
		PLog("Haupt_PRG: get_active_dls")
		from threading import Thread
		bg_thread = Thread(target=epgRecord.get_active_dls, args=())
		bg_thread.start()	
else:
		if os.path.exists(DL_CHECK):	
			os.remove(DL_CHECK)								# Setting Aus: Lock dl_check_alive entfernen
		if os.path.exists(DL_CNT):
			os.remove(DL_CNT)								# Zähler dl_cnt entfernen

if os.path.exists(FLAG_OnlyUrl):							# Lockdatei für Synchronisierung strm-Liste				
	now = time.time()
	mtime = os.stat(FLAG_OnlyUrl).st_mtime
	diff = int(now) - mtime
	if diff > 60:											# entf. wenn älter als 60 sec	
		os.remove(FLAG_OnlyUrl)
		PLog("onlyurl_removed, age: %d sec" % diff)
	
if os.path.exists(STRM_SYNCLIST):							# strm-Liste für Synchronisierung					
	if os.path.exists(STRM_CHECK):							# Leiche? 2-sec-Aktualisierung durch strm_sync
		now = time.time()
		mtime = os.stat(STRM_CHECK).st_mtime
		diff = int(now) - mtime
		if diff > 10:										# entf. wenn älter als 10 sec	
			os.remove(STRM_CHECK)
			PLog("strm_check_alive_removed, age: %d sec" % diff)
		else:
			PLog("Haupt_PRG: strm_sync_is_running")

	if os.path.exists(STRM_CHECK) == False:					# Lock beachten (Datei strm_check_alive)
		open(STRM_CHECK, 'w').close()						# Lock strm_check_alive anlegen
		PLog("Haupt_PRG: start_strm_sync")
		import resources.lib.strm as strm
		from threading import Thread
		bg_thread = Thread(target=strm.strm_sync, args=())
		bg_thread.start()	
else:
		if os.path.exists(STRM_CHECK):
			PLog("Haupt_PRG: clear_strm_check_alive")	
			os.remove(STRM_CHECK)							# Liste fehlt: Lock strm_check_alive entfernen
		

MERKACTIVE 	= os.path.join(DICTSTORE, 'MerkActive') 		# Marker aktive Merkliste
if os.path.exists(MERKACTIVE):
	os.remove(MERKACTIVE)
MERKFILTER 	= os.path.join(DICTSTORE, 'Merkfilter') 
# Ort FILTER_SET wie filterfile (check_DataStores):
FILTER_SET 	= os.path.join(ADDON_DATA, "filter_set")
AKT_FILTER	= ''
if os.path.exists(FILTER_SET):	
	AKT_FILTER	= RLoad(FILTER_SET, abs_path=True)
AKT_FILTER	= AKT_FILTER.splitlines()						# gesetzte Filter initialiseren 
STARTLIST	= os.path.join(ADDON_DATA, "startlist") 		# Videoliste mit Datum ("Zuletzt gesehen")

try:	# 28.11.2019 exceptions.IOError möglich, Bsp. iOS ARM (Thumb) 32-bit
	from platform import system, architecture, machine, release, version	# Debug
	OS_SYSTEM = system()
	OS_ARCH_BIT = architecture()[0]
	OS_ARCH_LINK = architecture()[1]
	OS_MACHINE = machine()
	OS_RELEASE = release()
	OS_VERSION = version()
	OS_DETECT = OS_SYSTEM + '-' + OS_ARCH_BIT + '-' + OS_ARCH_LINK
	OS_DETECT += ' | host: [%s][%s][%s]' %(OS_MACHINE, OS_RELEASE, OS_VERSION)
except:
	OS_DETECT =''
	
KODI_VERSION = xbmc.getInfoLabel('System.BuildVersion')

PLog('Addon: ClearUp')
# Dict: Simpler Ersatz für Dict-Modul aus Plex-Framework
ARDStartCacheTime = 300						# 5 Min.	
 
days = int(SETTINGS.getSetting('pref_DICT_store_days'))
Dict('ClearUp', days)				# Dict bereinigen 
ClearUp(M3U8STORE, days*86400)		# M3U8STORE bereinigen	

days = int(SETTINGS.getSetting('pref_UT_store_days'))
ClearUp(SUBTITLESTORE, days*86400)	# SUBTITLESTORE bereinigen	
days = int(SETTINGS.getSetting('pref_SLIDES_store_days'))
ClearUp(SLIDESTORE, days*86400)		# SLIDEESTORE bereinigen
days = int(SETTINGS.getSetting('pref_TEXTE_store_days'))
ClearUp(TEXTSTORE, days*86400)		# TEXTSTORE bereinigen

if SETTINGS.getSetting('pref_epgRecord') == 'true':
	epgRecord.JobMain(action='init')						# EPG_Record starten

# Skin-Anpassung:
skindir = xbmc.getSkinDir()
PLog("skindir: %s" % skindir)
sel = SETTINGS.getSetting('pref_content_type')				# 31.03.2023 erweitert: pull request #12 from Trekky12
try:
	sel = re.search(u'\((.*?)\)', sel).group(1)				# Default: "" -> except 
except:
	sel=""
PLog("content_type: %s" % sel)				
xbmcplugin.setContent(HANDLE, sel)

ARDSender = ['ARD-Alle:ard::ard-mediathek.png:ARD-Alle']	# Rest in ARD_NEW, CurSenderZDF s. ZDF_VerpasstWoche
CurSender = ARDSender[0]									# Default ARD-Alle
fname = os.path.join(DICTSTORE, 'CurSender')				# init CurSender (aktueller Sender)
if os.path.exists(fname):									# kann fehlen (Aufruf Merkliste)
	CurSender = Dict('load', "CurSender")					# Übergabe -> Main_NEW (ARDnew)



#----------------------------------------------------------------  
																	
def Main():
	PLog('Main:'); 
	PLog('Addon-Version: ' + VERSION); PLog('Addon-Datum: ' + VDATE)	
	PLog(OS_DETECT)	
	PLog('Addon-Python-Version: %s'  % sys.version)
	PLog('Kodi-Version: %s'  % KODI_VERSION)
			
	PLog(PluginAbsPath)	

	icon = R(ICON_MAIN_ARD)
	label 		= NAME
	li = xbmcgui.ListItem("ARD und ZDF")
	
	
	if SETTINGS.getSetting('pref_use_mvw') == 'true':
		title = 'Suche auf MediathekViewWeb.de'
		tag = "Extrem schnelle Suche im Datenbestand von MediathekView."
		summ = 'Gesucht wird in [B]allen von MediathekView unterstützen Sendern[/B].'
		summ = "%s\n\nBilder sind in den Ergebnislisten nicht enthalten. " % summ
		title=py2_encode(title);
		func = "ardundzdf.Main"
		fparams="&fparams={'title': '%s','sender': '%s' ,'myfunc': '%s'}" % \
			(quote(title), "ARD|ZDF", quote(func))
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.yt.MVWSearch", fanart=R('suche_ardundzdf.png'), 
			thumb=R("suche_mv.png"), tagline=tag, summary=summ, fparams=fparams)
	
	title="Suche in ARD und ZDF"
	tagline = 'gesucht wird in [B]ARD  Mediathek, ZDF Mediathek[/B] und [B]Merkliste[/B].'
	summ = u"Tools für die Suchwortliste: Menü [B]Suchwörter bearbeiten[/B] (siehe Infos + Tools)."
	fparams="&fparams={'title': '%s'}" % quote(title)
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.SearchARDundZDFnew", 
		fanart=R('suche_ardundzdf.png'), thumb=R('suche_ardundzdf.png'), tagline=tagline, 
		summary=summ, fparams=fparams)

	title = "ARD Mediathek"
	tagline = u'die Classic-Version der Mediathek existiert nicht mehr - sie wurde von der ARD eingestellt'
	fparams="&fparams={'name': '%s', 'CurSender': '%s'}" % (title, CurSender)
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.Main_NEW", fanart=R(FANART), 
		thumb=R(ICON_MAIN_ARD), tagline=tagline, fparams=fparams)
			
	if SETTINGS.getSetting('pref_use_zdfmobile') == 'true':
		PLog('zdfmobile_set: ')
		tagline = 'Info: [B]ZDFmobile entfällt ab Juni 2023[/B]'
		summ = ""
		fparams="&fparams={}"
		addDir(li=li, label="ZDFmobile", action="dirList", dirID="resources.lib.zdfmobile.Main_ZDFmobile", 
			fanart=R(FANART), thumb=R(ICON_MAIN_ZDFMOBILE), tagline=tagline, summary=summ, fparams=fparams)
	else:
		tagline = 'Info: [B]ZDFmobile entfällt ab Juni 2023[/B]'
		summ = ""
		fparams="&fparams={'name': 'ZDF Mediathek'}"
		addDir(li=li, label="ZDF Mediathek", action="dirList", dirID="Main_ZDF", fanart=R(FANART), 
			thumb=R(ICON_MAIN_ZDF), tagline=tagline, summary=summ, fparams=fparams)
			
	if SETTINGS.getSetting('pref_use_3sat') == 'true':
		tagline = 'in den Settings kann das Modul 3Sat ein- und ausgeschaltet werden'
		fparams="&fparams={'name': '3Sat'}"									# 3Sat-Modul
		addDir(li=li, label="3Sat Mediathek", action="dirList", dirID="resources.lib.my3Sat.Main_3Sat", 
			fanart=R('3sat.png'), thumb=R('3sat.png'), tagline=tagline, fparams=fparams)
			
	'''	26.04.2023 api V4.0 funktioniert nicht mehr - vorerst abgeschaltet		
	if SETTINGS.getSetting('pref_use_funk') == 'true':
		tag = 'in den Settings kann das Modul FUNK ein- und ausgeschaltet werden'
		tag = u"%s\n\ndie Beiträge sind auch in der ZDF Mediathek enthalten (Menü ZDF-funk)" % tag
		fparams="&fparams={}"													# funk-Modul
		addDir(li=li, label="FUNK", action="dirList", dirID="resources.lib.funk.Main_funk", 
			fanart=R('funk.png'), thumb=R('funk.png'), tagline=tag, fparams=fparams)
	'''		
	if SETTINGS.getSetting('pref_use_childprg') == 'true':
		tagline = 'in den Settings kann das Modul Kinderprogramme ein- und ausgeschaltet werden'
		summ = u"KiKA, ZDFtivi, MausLive u.a."
		fparams="&fparams={}"													# Kinder-Modul
		addDir(li=li, label="Kinderprogramme", action="dirList", dirID="resources.lib.childs.Main_childs", 
			fanart=R('childs.png'), thumb=R('childs.png'), tagline=tagline, summary=summ, fparams=fparams)

	#	26.04.2023 erneuert		
	if SETTINGS.getSetting('pref_use_XL') == 'true':
		tagline = 'in den Settings kann das Modul TagesschauXL ein- und ausgeschaltet werden'
		fparams="&fparams={}"													# TagesschauXL-Modul
		addDir(li=li, label="TagesschauXL", action="dirList", dirID="resources.lib.TagesschauXL.Main_XL", 
			fanart=ICON_MAINXL, thumb=ICON_MAINXL, tagline=tagline, fparams=fparams)
			
	if SETTINGS.getSetting('pref_use_phoenix') == 'true':
		tagline = 'in den Settings kann das Modul phoenix ein- und ausgeschaltet werden'
		fparams="&fparams={}"													# Phoenix-Modul
		addDir(li=li, label="phoenix", action="dirList", dirID="resources.lib.phoenix.Main_phoenix", 
			fanart=R(ICON_PHOENIX), thumb=R(ICON_PHOENIX), tagline=tagline, fparams=fparams)
			
	if SETTINGS.getSetting('pref_use_arte') == 'true':
		tagline = 'in den Settings kann das Modul Arte-Mediathek ein- und ausgeschaltet werden'
		fparams="&fparams={}"													# arte-Modul
		addDir(li=li, label="Arte-Mediathek", action="dirList", dirID="resources.lib.arte.Main_arte", 
			fanart=R('arte_Mediathek.png'), thumb=R('arte_Mediathek.png'), tagline=tagline,
			fparams=fparams)
			
	label = 'TV-Livestreams'
	if SETTINGS.getSetting('pref_epgRecord') == 'true':		
		label = u'TV-Livestreams | Sendungen aufnehmen'; 
	tagline = u'Livestreams von ARD, ZDF und einigen Privaten. Zusätzlich Event Streams von ARD und ZDF.'																																	
	fparams="&fparams={'title': 'TV-Livestreams'}"
	addDir(li=li, label=label, action="dirList", dirID="SenderLiveListePre", 
		fanart=R(FANART), thumb=R(ICON_MAIN_TVLIVE), tagline=tagline, fparams=fparams)
	
	# 29.09.2019 Umstellung Livestreams auf ARD Audiothek
	#	erneut ab 02.11.2020 nach Wegfall web.ard.de/radio/radionet
	# Button für Livestreams anhängen (eigenes ListItem)		# Radio-Livestreams
	tagline = u'die Radio-Livestreams stehen auch in der neuen ARD Audiothek zur Verfügung'
	title = u'Radio-Livestreams'	
	fparams="&fparams={'title': '%s', 'myhome': 'ARD'}" % (title)	
	addDir(li=li, label=title, action="dirList", dirID="AudioStartLive", fanart=R(FANART), 
		thumb=R(ICON_MAIN_RADIOLIVE), tagline=tagline, fparams=fparams)
		
		
	if SETTINGS.getSetting('pref_use_podcast') ==  'true':		# Podcasts / Audiothek
			tagline	= 'ARD Audiothek | Die besten Podcasts der ARD und des Deutschlandradios'
			fparams="&fparams={'title': 'ARD Audiothek'}"
			label = 'ARD Audiothek'
			addDir(li=li, label=label, action="dirList", dirID="AudioStart", fanart=R(FANART), 
				thumb=R(ICON_MAIN_AUDIO), tagline=tagline, fparams=fparams)
						
																# Download-/Aufnahme-Tools. zeigen
	if SETTINGS.getSetting('pref_use_downloads')=='true' or SETTINGS.getSetting('pref_epgRecord')=='true':	
		tagline = 'Downloads und Aufnahmen: Verschieben, Löschen, Ansehen, Verzeichnisse bearbeiten'
		fparams="&fparams={}"
		addDir(li=li, label='Download- und Aufnahme-Tools', action="dirList", dirID="DownloadTools", 
			fanart=R(FANART), thumb=R(ICON_DOWNL_DIR), tagline=tagline, fparams=fparams)	
				
	if SETTINGS.getSetting('pref_showFavs') ==  'true':			# Favoriten einblenden
		tagline = "Kodi's ARDundZDF-Favoriten zeigen und aufrufen"
		fparams="&fparams={'mode': 'Favs'}"
		addDir(li=li, label='Favoriten', action="dirList", dirID="ShowFavs", 
			fanart=R(FANART), thumb=R(ICON_DIR_FAVORITS), tagline=tagline, fparams=fparams)	
				
	if SETTINGS.getSetting('pref_watchlist') ==  'true':		# Merkliste einblenden
		tagline = 'interne Merkliste des Addons'
		fparams="&fparams={'mode': 'Merk'}"
		addDir(li=li, label='Merkliste', action="dirList", dirID="ShowFavs", 
			fanart=R(FANART), thumb=R(ICON_DIR_WATCH), tagline=tagline, fparams=fparams)		
								
	repo_url = 'https://github.com/{0}/releases/'.format(GITHUB_REPOSITORY)
	call_update = False
	if SETTINGS.getSetting('pref_info_update') == 'true': # Updatehinweis beim Start des Addons 
		ret = updater.update_available(VERSION)
		if ret[0] == False:		
			msg1 = "Github ist nicht erreichbar"
			msg2 = 'update_available: False'
			PLog("%s | %s" % (msg1, msg2))
			MyDialog(msg1, msg2, '')
		else:	
			int_lv = ret[0]			# Version Github
			int_lc = ret[1]			# Version aktuell
			latest_version = ret[2]	# Version Github, Format 1.4.1
			
			if int_lv > int_lc:								# Update-Button "installieren" zeigen
				call_update = True
				title = 'neues Update vorhanden - jetzt installieren'
				summ = 'Addon aktuell: ' + VERSION + ', neu auf Github: ' + latest_version
				# Bsp.: https://github.com/rols1/Kodi-Addon-ARDundZDF/releases/download/0.5.4/Kodi-Addon-ARDundZDF.zip
				url = 'https://github.com/{0}/releases/download/{1}/{2}.zip'.format(GITHUB_REPOSITORY, latest_version, REPO_NAME)
				fparams="&fparams={'url': '%s', 'ver': '%s'}" % (quote_plus(url), latest_version) 
				addDir(li=li, label=title, action="dirList", dirID="resources.lib.updater.update", fanart=R(FANART), 
					thumb=R(ICON_UPDATER_NEW), fparams=fparams, summary=summ)
			
	if call_update == False:							# Update-Button "Suche" zeigen	
		title  = 'Addon-Update | akt. Version: ' + VERSION + ' vom ' + VDATE	
		summ='Suche nach neuen Updates starten'
		tag ='Bezugsquelle: ' + repo_url			
		fparams="&fparams={'title': 'Addon-Update'}"
		addDir(li=li, label=title, action="dirList", dirID="SearchUpdate", fanart=R(FANART), 
			thumb=R(ICON_MAIN_UPDATER), fparams=fparams, summary=summ)

	# Menü Einstellungen (obsolet) ersetzt durch Info-Button
	#	freischalten nach Posting im Kodi-Forum

	tag = '[B]Infos, Tools und Filter zu diesem Addon[/B]'					# Menü Info + Tools
	summ= u'- Ausschluss-Filter bearbeiten (nur für Beiträge von ARD und ZDF)'
	summ= u"%s\n- Merkliste bereinigen" % summ
	summ= u'%s\n- Suchwörter bearbeiten (nur für die gleichzeitige Suche in ARD Mediathek und ZDF Mediathek)' % summ

	summ = "%s\n-%s" % (summ, "Download- und Aufnahme-Tools")
	if SETTINGS.getSetting('pref_strm') == 'true':
		summ = "%s\n-%s" % (summ, "strm-Tools")
	if SETTINGS.getSetting('pref_playlist') == 'true':
		summ = "%s\n-%s\n-%s" % (summ, "PLAYLIST-Tools", "Settings inputstream.adaptive")
	summ = "%s\n-%s" % (summ, "Kodis Thumbnails-Ordner bereinigen")
	summ = "%s\n\n%s" % (summ, u"[B]Einzelupdate[/B] (für einzelne Dateien und Module)")
	fparams="&fparams={}" 
	addDir(li=li, label='Infos + Tools', action="dirList", dirID="InfoAndFilter", fanart=R(FANART), thumb=R(ICON_INFO), 
		fparams=fparams, summary=summ, tagline=tag)

	# Updatehinweis wird beim Caching nicht aktualisiert
	if SETTINGS.getSetting('pref_info_update') == 'true':
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
	else:
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
		
#----------------------------------------------------------------
# Aufruf Main
# div. Addon-Infos + Filter (Titel) setzen/anlegen/löschen
# Filter-Button nur zeigen, wenn in Settings gewählt
# Juni 2022 verlagert zum neuen tools-Modul: ShowText, AddonInfos, 
#	AddonStartlist, SearchWordTools, FilterTools.
#
def InfoAndFilter():
	PLog('InfoAndFilter:'); 
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)									# Home-Button
	try:
		import resources.lib.tools
	except:
		pass	
															# Button changelog.txt
	tag= u'Störungsmeldungen bitte via Kodinerds-Forum, Github-Issue oder rols1@gmx.de'
	summ = u'für weitere Infos zu bisherigen Änderungen [B](changelog.txt)[/B] klicken'
	path = os.path.join(ADDON_PATH, "changelog.txt") 
	title = u"Änderungsliste [B](changelog.txt)[/B]"
	title=py2_encode(title)
	fparams="&fparams={'path': '%s', 'title': '%s'}" % (quote(path), quote(title))
	addDir(li=li, label=title, action="dirList", dirID="ShowText", fanart=R(FANART), 
		thumb=R(ICON_TOOLS), fparams=fparams, summary=summ, tagline=tag)		
							
	title = u"Addon-Infos"									# Button für Addon-Infos
	tag = u"[B]Infos zu Version, Cache und Dateipfaden.[/B]" 
	summ = u"Bei aktiviertem Debug-Log erfolgt die Ausgabe auch dort"
	summ = u"%s (nützlich zum Kopieren der Pfade)." % summ
	fparams="&fparams={}" 
	addDir(li=li, label=title, action="dirList", dirID="AddonInfos", fanart=R(FANART), 
		thumb=R(ICON_PREFS), tagline=tag, summary=summ, fparams=fparams)	
			
	if SETTINGS.getSetting('pref_startlist') == 'true':		# Button für LastSeen-Funktion
		maxvideos = SETTINGS.getSetting('pref_max_videos_startlist')
		title = u"Zuletzt gesehen"	
		tag = u"[B]Liste der im Addon gestarteten Videos (max. %s Einträge).[/B]" % maxvideos
		tag = u"%s\n\nSortierung absteigend (zuletzt gestartete Videos zuerst)" % tag
		summ = u"Klick startet das Video (falls noch existent)"
		fparams="&fparams={}" 
		addDir(li=li, label=title, action="dirList", dirID="AddonStartlist", fanart=R(FANART), 
			thumb=R("icon-list.png"), tagline=tag, summary=summ, fparams=fparams)	
		
	if SETTINGS.getSetting('pref_usefilter') == 'true':											
		title = u"Filter bearbeiten"						# Button für Filter
		tag = u"[B]Ausschluss-Filter bearbeiten[/B]\n\nnur für Beiträge von ARD und ZDF" 								
		fparams="&fparams={}" 
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.tools.FilterTools", 
			fanart=R(FANART), thumb=R(ICON_FILTER), tagline=tag, fparams=fparams)
			
	title = u"Merkliste bereinigen"							# Button für Bereinigung der Merkliste 
	tag = u"Nicht mehr erreichbare Beiträge listen und nach Abfrage löschen." 
	tag = u"%s\n\n[B]Ablauf[/B]: enthaltene Url's (Webseiten, Bildverweise) werden angepingt und der Status bewertet." % tag
	tag = u"%s\nEin [B]HTTP Timeout[/B] schließt eine spätere Erreichbarkeit nicht aus." % tag
	tag = u"%s\nSucheinträge werden durchgewinkt." % tag
	summ = u"Die Dauer ist von vielen Faktoren abhängig und nicht kalkulierbar (Testläufe mit 90 Einträgen: ca. 30 sec)"	
	summ = u"%s\n\nEin [B]Backup[/B] der Datei merkliste.xml im userdata-Verzeichnis wird empfohlen" % summ					
	summ = u"%s (insbesondere bei externer Merkliste)." % summ					
	myfunc="resources.lib.merkliste.clear_merkliste"

	fparams="&fparams={'myfunc': '%s', 'fparams_add': 'clear'}"  % quote(myfunc)		
	addDir(li=li, label=title, action="dirList", dirID="start_script",\
		fanart=R(FANART), thumb=R(ICON_DIR_WATCH), tagline=tag, summary=summ, fparams=fparams)	
				
			
	title = u"Suchwörter bearbeiten"						# Button für Suchwörter
	tag = u"[B]Suchwörter bearbeiten (max. 24)[/B]\n\n(nur für die gemeinsame Suche in ARD Mediathek und ZDF Mediathek)" 								
	fparams="&fparams={}" 
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.tools.SearchWordTools", 
		fanart=R(FANART), thumb=R('icon_searchwords.png'), tagline=tag, fparams=fparams)	
			
	# hier ohne Abhängigkeit vom Setting pref_use_downloads:
	tagline = u'[B]Downloads und Aufnahmen[/B]\n\nVerschieben, Löschen, Ansehen, Verzeichnisse bearbeiten'
	fparams="&fparams={}"
	addDir(li=li, label='Download- und Aufnahme-Tools', action="dirList", dirID="DownloadTools", 
		fanart=R(FANART), thumb=R(ICON_DOWNL_DIR), tagline=tagline, fparams=fparams)	
	
				
	if SETTINGS.getSetting('pref_strm') == 'true':											
		title = u"strm-Tools"								# Button für strm-Tools
		tag = u"[B]strm-Tools - Details siehe Addon-Wicki auf Github[/B]"
		tag = u"%s\n\nAbgleichintervall in Stunden\nListen anzeigen\nListeneinträge löschen\n" % tag
		tag = u"%sMonitorreset\nstrm-Log anzeigen\nAbgleich einer Liste erzwingen\n" % tag
		tag = u"%sunterstützte Sender/Beiträge\nzu einem strm-Verzeichnis wechseln" % tag
		myfunc="resources.lib.strm.strm_tools"
		fparams_add = quote('{}')

		fparams="&fparams={'myfunc': '%s', 'fparams_add': '%s'}"  %\
			(quote(myfunc), quote(fparams_add))			
		addDir(li=li, label=title, action="dirList", dirID="start_script",\
			fanart=R(FANART), thumb=R("icon-strmtools.png"), tagline=tag, fparams=fparams)	

	
	# Problem beim Abspielen der Liste - s. PlayMonitor (Modul playlist)
	if SETTINGS.getSetting('pref_playlist') == 'true':
		MENU_STOP = os.path.join(ADDON_DATA, "menu_stop") 	# Stopsignal für Tools-Menü (Haupt-PRG)								
		if os.path.exists(MENU_STOP):						# verhindert Rekurs. in start_script 
			os.remove(MENU_STOP)							# gesetzt in playlist_tools
			
		title = u"PLAYLIST-Tools"							# Button für PLAYLIST-Tools
		myfunc="resources.lib.playlist.playlist_tools"
		fparams_add = quote('{"action": "playlist_add", "add_url": "", "menu_stop": "true"}') # hier json-kompat.
		
		tag = u"[B]Abspielen und Verwaltung der addon-internen Playlist[/B]"
		tag = u"%s\n\nEinträge werden via Kontextmenü von abspielbaren Videos hinzugefügt." % tag
		tag = u"%s\n\nLivestreams werden abgewiesen." % tag			
		summ = u"Die PLAYLIST-Tools stehen auch im Kontextmenü zur Verfügung." 

		fparams="&fparams={'myfunc': '%s', 'fparams_add': '%s'}"  %\
			(quote(myfunc), quote(fparams_add))			
		addDir(li=li, label=title, action="dirList", dirID="start_script",\
			fanart=R(FANART), thumb=R("icon-playlist.png"), tagline=tag, summary=summ, fparams=fparams)	
			
	dz = get_dir_size(THUMBNAILS)							# Thumbnails-Ordner bereinigen
	dz = "[B](%s)[/B]" % dz
	title = u"Kodis Thumbnails-Ordner bereinigen %s" % dz	
	tag = u'[B]Kodis Thumbnails-Ordner bereinigen[/B]'
	summ = u"Das Bereinigen schafft Platz, indem es ältere Bilder entfernt (Auswahl 1-100 Tage)."
	summ = u"%s\nDadurch kann sich die Anzeige älterer Beiträge anfangs verzögern." % summ
	summ = u"%s\n\nDer aktuelle Füllstand %s kann auch im Menü Addon-Infos eingesehen werden." % (summ, dz)
	fparams="&fparams={}"
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.tools.ClearUpThumbnails",\
		fanart=R(FANART), thumb=R("icon-clear.png"), tagline=tag, summary=summ, fparams=fparams)	

	
	addon_id='inputstream.adaptive'; cmd="openSettings"		# Settings inputstream-Addon öffnen
	try:													# Check inputstream-Addon
		inp_vers = xbmcaddon.Addon(addon_id).getAddonInfo('version')
	except:
		inp_vers=""
	PLog("inp_vers: " + inp_vers)			
	if inp_vers:
		title = u"Settings inputstream.adaptive-Addon (v%s) öffnen" % inp_vers
		akt="EIN"
		if SETTINGS.getSetting('pref_UT_ON') == "false":
			akt="AUS"
		tag = u"Bandbreite, Auflösung und weitere Einstellungen."
		tag = u"%s\nDie Nutzung ist [B]%s-[/B]geschaltet (siehe Modul-Einstellungen von ARDundZDF)" % (tag, akt)
		fparams="&fparams={'addon_id': '%s', 'cmd': '%s'}" % (addon_id, cmd)
		addDir(li=li, label=title, action="dirList", dirID="open_addon",\
			fanart=R(FANART), thumb=R("icon-inp.png"), tagline=tag, fparams=fparams)	
			
	
	dt = resources.lib.tools.get_foruminfo()
	dt = "[B]Forum: %s[/B]" % dt		
	title = u"Einzelupdate (einzelne Dateien und Module), %s" % dt	# Update von Einzeldateien
	tag = u'[B]Update einzelner, neuer Bestandteile des Addons vom Github-Repo %s[/B]' % REPO_NAME
	tag = u"%s\n\nNach Abgleich werden neue Dateien heruntergeladen - diese ersetzen lokale Dateien im Addon." % tag
	tag = u"%s\n\nEinzelupdates ermöglichen kurzfristige Fixes und neue Funktionen zwischen den regulären Updates." % tag
	summ = u"Anstehende Einzelupdates werden im Forum kodinerds im Startpost des Addons angezeigt"
	summ = u"%s (%s)." % (summ, dt)
	fparams="&fparams={'PluginAbsPath': '%s'}" % PluginAbsPath
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.EPG.update_single",\
		fanart=R(FANART), thumb=R("icon-update-einzeln.png"), tagline=tag, summary=summ, fparams=fparams)	
		
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)

#---------------------------------------------------------------- 
# Wg.  Problemen mit der xbmc-Funktion executebuiltin(RunScript()) verwenden
#	wie importlib wie in router()
#	Bsp. myfunc: "resources.lib.playlist.items_add_rm" (relatv. Modulpfad + Zielfunktion)
#	fparams_add json-kompat., Bsp.: '{"action": "playlist_add", "url": ""}'
# Um die Rekursion der Web-Tools-Liste zu vermeiden wird MENU_STOP in playlist_tools
#	gesetzt und in InfoAndFilter wieder entfernt.
# Beispiel fparams bei Direktaufruf (is_dict=False):   
#					fparams="{'strmpath': '%s'}" % strmpath	 
#					fparams = quote(fparams)
#					start_script(myfunc, fparams)
#
def start_script(myfunc, fparams_add, is_dict=True):
	PLog("start_script:")
	import importlib
	PLog(type(fparams_add))
	fparams_add = unquote(fparams_add)
	PLog(myfunc); PLog(fparams_add)
	
	l = myfunc.split('.')									# Bsp. resources.lib.updater.update
	PLog(l)
	newfunc =  l[-1:][0]									# Bsp. updater
	dest_modul = '.'.join(l[:-1])

	dest_modul = importlib.import_module(dest_modul )		# Modul laden
	PLog('loaded: ' + str(dest_modul))
	func = getattr(dest_modul, newfunc)	

	if is_dict == False:									# Direktaufruf
		try:
			fparams_add = fparams_add.replace("'", "\"")
			fparams_add = fparams_add.replace('\\', '\\\\')	
		except Exception as exception:
			PLog('router_exception: {0}'.format(str(exception)))	
		PLog(fparams_add)
		
	if fparams_add != '""':									# leer, ohne Parameter?	
		mydict = json.loads(fparams_add)
		PLog("mydict: " + str(mydict));
		func(**mydict)
	else:
		func()

	#xbmc.sleep(500)
	# ohne endOfDirectory wird das Fenster des Videoplayers blockiert (Ladekreis):
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True) 	 
	
#----------------------------------------------------------------
# Aufruf InfoAndFilter
# 18.01.2021 Abgleich mit STARTLIST in items_add_rm (Modul Playlist)
#
def AddonStartlist(mode='', query=''):
	PLog('AddonStartlist:');
	PLog(mode); PLog(query)
	maxvideos = SETTINGS.getSetting('pref_max_videos_startlist')
	
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)										# Home-Button
	img = R("icon-list.png")
	startlist=''

	if os.path.exists(STARTLIST):
		startlist= RLoad(STARTLIST, abs_path=True)				# Zuletzt gesehen-Liste laden
	if startlist == '':
		msg1 = u'die "Zuletzt gesehen"-Liste ist leer'
		MyDialog(msg1, '', '')
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	

	if mode == 'search':										# Suche
		query = get_keyboard_input() 
		if query == None or query.strip() == '': 				# None bei Abbruch
			pass
		else:
			query = query.strip()	
			query = py2_encode(query)							# decode in up_low	

		
	title = u'Suche in der "Zuletzt gesehen"-Liste"'			# Suchbutton
	tag = u"Suche der im Addon gestarteten Videos (max %s)."  % maxvideos
	tag = u"%s\n\nGesucht wird in Titel und Infotext." % tag
	fparams="&fparams={'mode': 'search'}" 
	addDir(li=li, label=title, action="dirList", dirID="AddonStartlist", fanart=img, 
		thumb=R(ICON_SEARCH), tagline=tag, fparams=fparams)	
			
	startlist=py2_encode(startlist)
	startlist= startlist.strip().splitlines()
	PLog(len(startlist))

	cnt=0
	for item in startlist:
		Plot=''
		ts, title, url, thumb, Plot = item.split('###')
		ts = datetime.datetime.fromtimestamp(float(ts))
		ts = ts.strftime("%d.%m.%Y %H:%M:%S")
		Plot_par = "gestartet: [COLOR darkgoldenrod]%s[/COLOR]\n\n%s" % (ts, Plot)
		Plot_par=py2_encode(Plot_par); 		
		Plot_par=Plot_par.replace('\n', '||')					# für router
		tag=Plot_par.replace('||', '\n')
		
		PLog("Satz16:"); PLog(title); PLog(ts); PLog(url); PLog(Plot_par)	
		show = True
		if 	query:												# Suchergebnis anwenden
			q = up_low(query, mode='low'); i = up_low(item, mode='low');
			PLog(q in i)
			show = q in i										# Abgleich 
		
		PLog(show)		
		if show == True:		
			url=py2_encode(url); title=py2_encode(title);  thumb=py2_encode(thumb);
			fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" %\
				(quote_plus(url), quote_plus(title), quote_plus(thumb), quote_plus(Plot_par))
			addDir(li=li, label=title, action="dirList", dirID="PlayVideo", fanart=img, thumb=thumb, 
				fparams=fparams, mediatype='video', tagline=tag)
			cnt = cnt+1 	
	
	PLog(cnt);
	if query:
		if cnt == 0:
			msg1 = u"Suchwort >%s< leider nicht gefunden" % py2_decode(query)
			MyDialog(msg1, '', '')	

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
							
#----------------------------------------------------------------
# Aufruf InfoAndFilter
# Addon-Infos (Pfade, Cache, ..)
# einschl. Log-Ausgabe 
def AddonInfos():
	PLog('AddonInfos:'); 
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button
	dialog = xbmcgui.Dialog()
	t = "     "		# Tab (5)

	a = u"[COLOR red]Addon, System:[/COLOR]"
	a1 = u"%s%s, Version %s vom %s" % (t, ADDON_ID, VERSION, VDATE)
	a2 = u"%sGithub-Releases https://github.com/%s/releases" % (t, GITHUB_REPOSITORY)
	a3 = u"%sOS: %s" % (t, OS_DETECT)
	a4 = u"%sKodi-Version: %s" % (t, KODI_VERSION)
	p1 = u"%s\n%s\n%s\n%s\n%s\n" % (a,a1,a2,a3,a4)
	
	a = u"[COLOR red]Cache:[/COLOR]"
	a1 = u"%s %10s Thumbnails (Kodi gesamt)" %  (t, get_dir_size(THUMBNAILS))
	a2 = u"%s %10s Dict (Variablen, Objekte)" %  (t, get_dir_size(DICTSTORE))
	a3 = u"%s %10s Inhaltstexte (im Voraus geladen)" %  (t, get_dir_size(TEXTSTORE))
	a4 = u"%s %10s Slides (Bilder)" %   (t, get_dir_size(SLIDESTORE))
	a5 = u"%s %10s subtitles (Untertitel)" %   (t, get_dir_size(SUBTITLESTORE))
	a6 = ''
	path = SETTINGS.getSetting('pref_download_path')
	PLog(path); PLog(os.path.isdir(path))
	if path and os.path.isdir(path):
		a6 = "%s %10s Downloads\n" %   (t, get_dir_size(path))
	p2 = u"%s\n%s\n%s\n%s\n%s\n%s\n%s" % (a,a1,a2,a3,a4,a5,a6)

	a = u"[COLOR red]Pfade:[/COLOR]"
	a1 = u"%s [B]Addon-Home:[/B] %s" % (t, PluginAbsPath)
	a2 = u"%s [B]Cache:[/B] %s" % (t,ADDON_DATA)
	fname = WATCHFILE
	a3 = u"%s [B]Merkliste intern:[/B]\n%s %s" % (t, t, WATCHFILE)
	a4 = u"%s [B]Merkliste extern:[/B] nicht aktiviert" % t
	if SETTINGS.getSetting('pref_merkextern') == 'true':	# externe Merkliste gewählt?
		fname = SETTINGS.getSetting('pref_MerkDest_path')
		a4 = u"%s [B]Merkliste extern:[/B]\n%s %s" % (t,t,fname)
	a5 = u"%s [B]Downloadverzeichnis:[/B] %s" % (t,SETTINGS.getSetting('pref_download_path'))
	a6 = u"%s V[B]erschiebeverzeichnis:[/B] %s" % (t,SETTINGS.getSetting('pref_VideoDest_path'))
	filterfile = os.path.join(ADDON_DATA, "filter.txt")
	a7 = u"%s [B]Filterliste:[/B] %s" %  (t,filterfile)
	searchwords = os.path.join(ADDON_DATA, "search_ardundzdf")
	a8 = u"%s [B]Suchwortliste:[/B] %s" %  (t,searchwords)
	fname =  SETTINGS.getSetting('pref_podcast_favorits')
	if os.path.isfile(fname) == False:
		fname = os.path.join(PluginAbsPath, "resources", "podcast-favorits.txt") 
	a9 = u"%s [B]Podcast-Favoriten:[/B]\n%s%s" %  (t,t,fname)		# fname in 2. Zeile
	log = xbmc.translatePath("special://logpath")
	log = os.path.join(log, "kodi.log") 	
	a10 = u"%s [B]Debug-Log:[/B] %s" %  (t, log)
	a11 = u"%s [B]TV-und Event-Livestreams:[/B] %s/%s" % (t, PluginAbsPath, "resources/livesenderTV.xml")
	
	p3 = u"%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n" % (a,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10)
	page = u"%s\n%s\n%s" % (p1,p2,p3)
	
	#--------------------------------------------------					# Module
	mpage = u"\n[COLOR red]Module:[/COLOR]"
	globFiles = "%s/%s/*py" % (PluginAbsPath, "resources/lib")
	files = glob.glob(globFiles) 
	files = sorted(files,key=lambda x: x.upper())
	# PLog(files)			# Debug
	for f in files:
		if "__init__.py" in f:
			continue
		modul = f.split('/')[-1]
		modul = modul.replace('.py', '')
		fcont = RLoad(f, abs_path=True)
		datum = stringextract('Stand:', '#', fcont)
		datum = datum.strip()
		
		datum = "%s %16s (Stand: %s)" % (t, modul, datum)		
		mpage = "%s\n%s" % (mpage, datum) 
	
	page = page + mpage
	PLog(cleanmark(page))
	dialog.textviewer(u"Addon-Infos (Ausgabe auch im Debug-Log bei aktiviertem Plugin-Logging)", page,usemono=True)
	
#	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
#----------------------------------------------------------------
# Aufruf Info_Filter
# 20.01.2020 usemono für textviewer (ab Kodi v18)
# dialog.select ungeeignet (Font zu groß, Zeilen zu schmal)
# 02.02.2021 erweitert mit direkter page-Übergabe
# Hinw.: usemono wirkt nicht, falls im Skin der Font Arial
#	gewählt ist (notwend. für arabische Schrift (ZDFarabic) 
#
def ShowText(path, title, page=''):
	PLog('ShowText:'); 
	
	if page == '':
		page = RLoad(path, abs_path=True)
		page = page.replace('\t', ' ')		# ersetze Tab's durch Blanks
	
	dialog = xbmcgui.Dialog()
	dialog.textviewer(title, page,usemono=True)
	
	return
	
#----------------------------------------------------------------
#  03.06.2021 Main_ARD (Classic) entfernt
# def Main_ARD(name, sender=''):		 		
#---------------------------------------------------------------- 
def Main_ZDF(name=''):
	PLog('Main_ZDF:'); PLog(name)
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button
	
	if SETTINGS.getSetting('pref_use_mvw') == 'true':
		title = 'Suche auf MediathekViewWeb.de'
		tag = "Extrem schnelle Suche im Datenbestand von MediathekView."
		summ = 'Sender: [B]alle Sender des ZDF[/B]' 
		title=py2_encode(title);
		func = "ardundzdf.Main_ZDF"
		fparams="&fparams={'title': '%s','sender': '%s' ,'myfunc': '%s'}" % \
			(quote(title), "ZDF", quote(func))
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.yt.MVWSearch", fanart=R(ICON_MAIN_ARD), 
			thumb=R("suche_mv.png"), tagline=tag, summary=summ, fparams=fparams)
		
	title="Suche in ZDF-Mediathek"
	fparams="&fparams={'query': '', 'title': '%s'}" % title
	addDir(li=li, label=title, action="dirList", dirID="ZDF_Search", fanart=R(ICON_ZDF_SEARCH), 
		thumb=R(ICON_ZDF_SEARCH), fparams=fparams)

	title = 'Startseite' 
	fparams="&fparams={'ID': '%s'}" % title
	addDir(li=li, label=title, action="dirList", dirID="ZDF_Start", fanart=R(ICON_MAIN_ZDF), thumb=R(ICON_MAIN_ZDF), 
		fparams=fparams)

	title = 'ZDF-funk' 
	fparams="&fparams={'title': '%s'}" % (quote(title))
	addDir(li=li, label=title, action="dirList", dirID="Main_ZDFfunk", fanart=R(ICON_MAIN_ZDF), thumb=R('zdf-funk.png'), 
		fparams=fparams)

	title = 'Sendung verpasst' 
	fparams="&fparams={'name': 'ZDF-Mediathek', 'title': 'title'}" 
	addDir(li=li, label=title, action="dirList", dirID="ZDF_VerpasstWoche", fanart=R(ICON_ZDF_VERP), 
		thumb=R(ICON_ZDF_VERP), fparams=fparams)	

	title = 'Sendungen A-Z' 
	fparams="&fparams={'name': '%s'}" % title
	addDir(li=li, label=title, action="dirList", dirID="ZDF_AZ", fanart=R(ICON_ZDF_AZ), 
		thumb=R(ICON_ZDF_AZ), fparams=fparams)

	title = 'Rubriken' 
	fparams="&fparams={'ID': '%s'}" % title
	addDir(li=li, label=title, action="dirList", dirID="ZDF_Start", fanart=R(ICON_ZDF_RUBRIKEN), 
		thumb=R(ICON_ZDF_RUBRIKEN), fparams=fparams)

	title = "ZDF-Sportstudio"
	tag = u"Aktuelle News, Livestreams, Liveticker, Ergebnisse, Hintergründe und Sportdokus. Sportstudio verpasst? Aktuelle Sendungen einfach online schauen!"
	fparams="&fparams={'ID': '%s'}" % title
	addDir(li=li, label=title, action="dirList", dirID="ZDF_Start", fanart=R("zdf-sport.png"), 
		thumb=R("zdf-sport.png"), tagline=tag, fparams=fparams)
		
	title = "Barrierearm"
	tag = u"Alles an einem Ort: das gesamte Angebot an Videos mit Untertiteln, Gebärdensprache und Audiodeskription sowie hilfreiche Informationen zum Thema gebündelt."
	fparams="&fparams={'ID': '%s'}" % title
	addDir(li=li, label="Barrierearm", action="dirList", dirID="ZDF_Start", fanart=R(ICON_ZDF_BARRIEREARM), 
		thumb=R(ICON_ZDF_BARRIEREARM), fparams=fparams)

	title = "ZDFinternational"
	fparams="&fparams={'title': 'ZDFinternational'}"
	tag = "This channel provides selected videos in English, Spanish or Arabic or with respective subtitles."
	summ = 'For Arabic, please set the font of your Skin to "Arial based".'
	fparams="&fparams={'ID': '%s'}" % title
	addDir(li=li, label="ZDFinternational", action="dirList", dirID="ZDF_Start", fanart=R('ZDFinternational.png'), 
		thumb=R('ZDFinternational.png'), tagline=tag, summary=summ, fparams=fparams)

	fparams="&fparams={'s_type': 'Bilderserien', 'title': 'Bilderserien', 'query': 'Bilderserie'}"
	addDir(li=li, label="Bilderserien", action="dirList", dirID="ZDF_Search", fanart=R(ICON_ZDF_BILDERSERIEN), 
		thumb=R(ICON_ZDF_BILDERSERIEN), fparams=fparams)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#----------------------------------------------------------------
def Main_ZDFfunk(title):
	PLog('Main_ZDFfunk:')
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button
	
	title = 'funk_Startseite' 
	fparams="&fparams={'ID': '%s'}" % title
	addDir(li=li, label=title, action="dirList", dirID="ZDF_Start", fanart=R('zdf-funk.png'), thumb=R('zdf-funk.png'), 
		fparams=fparams)

	fparams="&fparams={'name': 'ZDF-funk-A-Z', 'ID': 'ZDFfunk'}"
	addDir(li=li, label="ZDF-funk-A-Z", action="dirList", dirID="ZDF_AZ", fanart=R('zdf-funk-AZ.png'), 
		thumb=R('zdf-funk-AZ.png'), fparams=fparams)

	'''									# 27.04.2023  deaktiviert, api V4.0 nicht mehr verfügbar
	fparams="&fparams={}"											# Button funk-Modul hinzufügen
	addDir(li=li, label="zum FUNK-Modul", action="dirList", dirID="resources.lib.funk.Main_funk", 
		fanart=R('zdf-funk.png'), thumb=R('funk.png'), fparams=fparams)
	'''		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
		
##################################### Start Audiothek ###############################################
# Aufruf: Main
# 24.07.2021 Revision nach Renovierung der Audiothek durch die ARD
# 19.02.2022 Neubau nach Strukturänderungen Web, api-json und
#	Web-json - lokale Doku: Ordner Audiothek
#
def AudioStart(title):
	PLog('AudioStart:')
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)						# Home-Button
					
	title="Suche in ARD Audiothek"				# Button Suche voranstellen
	fparams="&fparams={'title': '%s'}" % title
	addDir(li=li, label=title, action="dirList", dirID="AudioSearch", fanart=R(ICON_MAIN_AUDIO), 
		thumb=R(ICON_SEARCH), fparams=fparams)

	# Button für Livestreams anhängen (eigenes ListItem)		# Livestreams
	title = 'Livestreams'	
	fparams="&fparams={'title': '%s'}" % (title)	
	addDir(li=li, label=title, action="dirList", dirID="AudioStartLive", fanart=R(ICON_MAIN_AUDIO), 
		thumb=R(ICON_AUDIO_LIVE), fparams=fparams)

	img = R(ICON_MAIN_AUDIO)
	title_list = [u'Entdecken|ard-entdecken.png', u'Rubriken|ard-rubriken.png',
			u'Sport|ard-sport.png']								
	for item in title_list:
		title, img = item.split('|')
		tag=''
		if title == u"Entdecken":
			tag = "die Startseite  der Audiothek"
		fparams="&fparams={'title': '%s', 'ID': '%s'}" % (title, title)	
		addDir(li=li, label=title, action="dirList", dirID="AudioStartHome", fanart=R(ICON_MAIN_AUDIO), 
			thumb=R(img), tagline=tag, fparams=fparams)

	# Button für A-Z anhängen 									# A-Z alle Sender
	# 01.08.2021 nach Renovierung der Audiothek durch die ARD entfallen
	
	# Button für Sender anhängen 								# Sender/Sendungen (via AudioStartLive)
	title = 'Sender (Sendungen einzelner Radiosender)'
	fparams="&fparams={}"
	addDir(li=li, label=title, action="dirList", dirID="AudioSenderPrograms", fanart=R(ICON_MAIN_AUDIO), 
		thumb=R("ard-sender.png"), fparams=fparams)
	
	# Button für funk anhängen 									# funk
	title = 'funk: Das Content-Netzwerk von ARD und ZDF'		# Watchdog: ../organizations
	fparams="&fparams={'org': '%s'}" %  title
	addDir(li=li, label=title, action="dirList", dirID="AudioSenderPrograms", fanart=R(ICON_MAIN_AUDIO), 
		thumb=R('funk.png'), fparams=fparams)
	
	# Button für Podcast-Favoriten anhängen 					# Podcast-Favoriten
	title="Podcast-Favoriten"; 
	tagline = u'konfigurierbar mit der Datei podcast-favorits.txt im Addon-Verzeichnis resources'
	summ=''
	fparams="&fparams={'title': '%s'}" % title
	addDir(li=li, label=title, action="dirList", dirID="PodFavoritenListe", fanart=R(ICON_MAIN_POD), 
		thumb=R(ICON_POD_FAVORITEN), tagline=tagline, summary=summ, fparams=fparams)
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
#----------------------------------------------------------------
# 31.07.2021 Revision nach Renovierung der Audiothek durch die ARD
# 19.02.2022 dto
#
def AudioStartHome(title, ID, page='', path=''):	# Auswertung Homepage	
	PLog('AudioStartHome: ' + ID)
	li = xbmcgui.ListItem()
	
	ID = py2_decode(ID)
	if ID == 'Rubriken':							# Rubriken-Liste: eig. api-Call
		path = ARD_AUDIO_BASE + "editorialcategories"
	if ID == 'Sport':								# Menü: Rubrik Sport herausgehoben
		path = 'https://www.ardaudiothek.de/rubrik/sport/42914734'
		ID = "AudioRubrikWebJson_%s" % "42914734"
		Audio_get_cluster_rubrik(li='', url=path, title='Sport', ID=ID)
		return
	if ID == 'Entdecken':
		#path = ARD_AUDIO_BASE + "homescreen"		# Leitseite api
		path = "https://www.ardaudiothek.de/"		# Web: nur teilw. vollständig, Nachladen
							
	page, msg = get_page(path=path)	
	if page == '':	
		msg1 = "Fehler in AudioStartHome:"
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return
	PLog(len(page))	
		
	li = home(li, ID='ARD Audiothek')				# Home-Button
		
	if ID == 'Entdecken':							# Stage Web, Sonderbhdl., Beiträge nicht im api 		
		Audio_get_homescreen(page)					# direkt o. li
	if ID == u'Rubriken':							# Rubrik Sport direkt s.o.
		ID = "AudioStartHome"
		Audio_get_rubriken_web(li, title, path, ID, page)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#----------------------------------------------------------------
# 1. Aufruf: (ID=AudioStartHome) -> Liste der Rubriken via api-Call,
# 2. Aufruf (Rubrik-Webseite in path) -> Audio_get_cluster_rubrik 
#		(Cluster -> Dict) -> Audio_get_cluster_single 
# 
def Audio_get_rubriken_web(li, title, path, ID, page):
	PLog('Audio_get_rubriken_web: ' + ID)
	CacheTime = 86400												# 24 Std.

	if li  == '':
		li = xbmcgui.ListItem()
		li = home(li,ID='ARD Audiothek')							# Home-Button		

	page = Dict("load", "AudioRubriken", CacheTime=CacheTime)		# editorialCategories laden
	if page == False or page == '':									# Cache miss od. leer - vom Sender holen
		page, msg = get_page(path=path)
		Dict("store", "AudioRubriken", page)						
	if page == '':	
		msg1 = "Fehler in Audio_get_rubriken_web:"
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return li
	
	if ID == "AudioStartHome":										# 1. Liste der Rubriken
		jsonObject = json.loads(page)
		if "graphql" in page:										# 18.02.2022 auch möglich (alte Form)
			Obs = jsonObject["_embedded"]['mt:editorialCategories']
		else:
			Obs = jsonObject["data"]['editorialCategories']["nodes"]# Key-Änderung
		PLog(len(Obs))
		base = "https://www.ardaudiothek.de/rubrik/%s"				# Name im Pfad (z.B. ../wissen/..)  nicht nötig
		# base = "https://www.ardaudiothek.de/redirect/%s"			# HTTP-error 301 vermeiden - s. get_page
		img = R("ard-rubriken.png"); thumb = R(ICON_DIR_FOLDER)
		for ob in Obs:
			oid = ob["id"]
			title = ob["title"]
			href = base % oid
			
			PLog('10Satz:');
			PLog(title); PLog(oid); PLog(href);
			
			title=py2_encode(title); href=py2_encode(href);	
			fparams="&fparams={'li': '','url': '%s', 'title': '%s', 'ID': 'Audio_get_rubriken_web'}" % (quote(href), 
				quote(title))
			addDir(li=li, label=title, action="dirList", dirID="Audio_get_cluster_rubrik", \
				fanart=img, thumb=thumb, fparams=fparams)	
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
#----------------------------------------------------------------
# 21.02.2022 Anpassung an renovierte Audiothek
# 	einschl.Event Streams, Ausgliederung AudioSenderPrograms
# 2. Durchlauf mit sender -> PlayAudio
# Auswertung Sender-Programme s. AudioSenderPrograms
#
def AudioStartLive(title, sender='', streamUrl='', myhome='', img='', Plot=''): # Sender / Livestreams 
	PLog('AudioStartLive: ' + sender)
	CacheTime = 6000													# 1 Std.

	li = xbmcgui.ListItem()
	if myhome:
		li = home(li, ID=myhome)
	else:	
		li = home(li, ID='ARD Audiothek')								# Home-Button

	path = "https://api.ardaudiothek.de/organizations"					# api=Webjson				
	page = Dict("load", "AudioSender", CacheTime=CacheTime)
	if page == False or page == '':										# Cache miss od. leer - vom Sender holen
		page, msg = get_page(path=path, JsonPage=True)
		Dict("store", "AudioSender", page)
	msg1 = "Fehler in AudioStartLive:"
	if page == '':	
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return li

	LiveObjekts = blockextract('"organizationName"', page)				# Station: Livestreams + programSets
	PLog(len(LiveObjekts))
	streamList=[]
	now = datetime.datetime.now()										# für streamList
	timemark = now.strftime("%d.%m.%Y")
	
	if sender == '':
		for LiveObj in LiveObjekts:
			liveStreams = stringextract('liveStreams":', 'programSets', LiveObj)
			live_cnt = stringextract('numberOfElements":', ',', liveStreams)
			streamUrl = stringextract('"streamUrl":"', '"', liveStreams)
			if live_cnt == '0':		
				continue
				
			img = stringextract('"image"', '"url1X1"', LiveObj)			# 18.02.2022 neues Format:
			img = stringextract('"url":"', '"', img)	
			img = img.replace('{width}', '640')							# fehlt manchmal
			Plot = stringextract('"synopsis":"', '"', LiveObj)
			Plot = repl_json_chars(Plot)
					
			title = stringextract('"sender":"', '"', liveStreams)		# Sender, z.B BAYERN 1	
			sender = title
			
			add = "zum Livestream"
			tag = "Weiter %s von: [B]%s[/B]" % (add, title)		
															
			PLog('3Satz:');
			PLog(title); PLog(img); PLog(streamUrl); PLog(Plot);
			title=py2_encode(title); sender=py2_encode(sender);
			streamUrl=py2_encode(streamUrl); img=py2_encode(img)
			Plot=py2_encode(Plot)
			fparams="&fparams={'title': '%s', 'sender': '%s', 'streamUrl': '%s', 'myhome': '%s', 'img': '%s', 'Plot': '%s'}" %\
				(quote(title), quote(sender), quote(streamUrl), myhome, quote(img), quote(Plot))	
			addDir(li=li, label=sender, action="dirList", dirID="AudioStartLive", fanart=img, 
				thumb=img, tagline=tag, summary=Plot, fparams=fparams)
			
			# Format: "Dateiname ** Titel Zeitmarke ** Streamlink" -> DownloadText
			fname = make_filenames(title)
			fname = py2_encode(fname)
			# Test erweiterte m3u (für Total Commander überdimensioniert:
			#extinf = '#EXTM3U\n#EXTINF:-1 tvg-name="%s" group-title="ARDundZDF %s" radio="true" tvg-logo="%s"\n%s'
			#extinf = extinf % (title, timemark, img, streamUrl)
			#streamList.append("%s.m3u**#%s" % (fname, extinf))	
			streamList.append("%s.m3u**# %s | ARDundZDF %s**%s" % (fname,title, timemark, streamUrl))	
		
		streamList = py2_encode(streamList)								#Streamlist-Button
		Dict("store", "RadioStreamLinks", streamList)				
		lable = u"[B]Download der Streamlinks (Anzahl: %d)[/B] als m3u-Dateien" % len(streamList)
		tag = u"Ablage als einzelne m3u-Datei je Streamlink im Downloadverzeichnis"
		summ = u"die nachfolgenden Audio-Buttons bleiben beim Download unberücksichtigt."
		fparams="&fparams={'textKey': '%s'}" % "RadioStreamLinks"
		addDir(li=li, label=lable, action="dirList", dirID="DownloadText", fanart=R(ICON_DOWNL), 
			thumb=R(ICON_DOWNL), fparams=fparams, tagline=tag, summary=summ)
		
		ARDAudioEventStreams(li)										# externe Zusätze listen

		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	#-------------------------------------------------------------------
	
	else:																# 2. Durchlauf: einz. Sender
		if streamUrl:													# zum Livestream
			PlayAudio(streamUrl, title, img, Plot)  # direkt	
	return
			
#----------------------------------------------------------------
# 21.02.2022 Anpassung an renovierte Audiothek
# 14.07.2022 
# 1. Lauf Einzelsender, 2. Lauf Sendungen
# Auswertung Livestreams der Sender s. AudioStartLive
#
def AudioSenderPrograms(org=''): 
	PLog('AudioSenderPrograms:')
	PLog(org); 
	CacheTime = 60*5													# 5 min.				

	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Audiothek')									# Home-Button

	path = "https://api.ardaudiothek.de/organizations"					# api=Webjson		
	page = Dict("load", "AudioSender", CacheTime=CacheTime)
	if page == False or page == '':										# Cache miss od. leer - vom Sender holen
		page, msg = get_page(path=path, JsonPage=True)
		Dict("store", "AudioSender", page)
	msg1 = "Fehler in AudioStartLive:"
	if page == '':	
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return li
		
	LiveObjekts = blockextract('"brandingColor"', page)				# Station: Livestreams + programSets
	PLog(len(LiveObjekts))

	#---------------------------------
	if org == '':														# 1. Durchlauf: alle Einzelsender listen
		PLog("stage1:")
		for LiveObj in LiveObjekts:
			PLog(LiveObj[:80])
			liveStreams = stringextract('liveStreams":', 'programSets', LiveObj)
				
			live_cnt = stringextract('numberOfElements":', ',', liveStreams)
			title = stringextract('"sender":"', '"', liveStreams)		# Sender, z.B BAYERN 1
			if live_cnt == '0':											# ARD, funk
				title = stringextract('"organizationName":"', '"', LiveObj)
				synop = stringextract('"synopsis":"', '"', LiveObj)
				if synop:
					title = "%s: %s" % (title, synop[:70])
				
			img = stringextract('"image"', '"url1X1"', LiveObj)			# 18.02.2022 neues Format:
			img = stringextract('"url":"', '"', img)	
			img = img.replace('{width}', '640')							# fehlt manchmal
			tag = "Weiter zu den Sendungen  von %s" % title 
				
			PLog("Sendername: " + org)									# org z.B. BAYERN 1 Franken
			title=py2_encode(title)
			fparams="&fparams={'org': '%s'}" % (quote(title))	
			addDir(li=li, label=title, action="dirList", dirID="AudioSenderPrograms", fanart=img, 
				thumb=img, tagline=tag, fparams=fparams)
				
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	

	#---------------------------------
	if org:															# 2. Durchlauf: programSets listen	
		PLog("stage2: " + org)
		for LiveObj in LiveObjekts:
			PLog(LiveObj[:80])
			liveStreams = stringextract('liveStreams":', 'programSets', LiveObj)
				
			live_cnt = stringextract('numberOfElements":', ',', liveStreams)
			title = stringextract('"sender":"', '"', liveStreams)		# Sender, z.B BAYERN 1
			if live_cnt == '0':											# ARD, funk
				title = stringextract('"organizationName":"', '"', LiveObj)
				synop = stringextract('"synopsis":"', '"', LiveObj)
				if synop:
					title = "%s: %s" % (title, synop[:70])
			PLog(org); PLog(title);	
			PLog(title.find(org))
			if title.find(org) >= 0:
				PLog("found_org: %s, title: %s" % (org, title))
				break			

		pos = LiveObj.find('"programSets"')
		page = LiveObj[pos:]
		PLog(page[:80])	
		items = blockextract('"id":', page)								# 2. Block enthält editorialCategories 		
		PLog(len(items))
		cnt=0
		for item in items:
			try:														# Kategorie aus 2. Block lesen 
				next_item = items[cnt+1]
				PLog("next_item: " + next_item)
			except:
				next_item=''
			cat =  stringextract('"title":"', '"', next_item)	
			cnt=cnt+1
			
			web_url =  stringextract('"sharingUrl":"', '"', item)		
			PLog("web_url: " + web_url)
			href_add = "?offset=0&limit=20"
			if web_url.endswith("/"):
				url_id 	= web_url.split('/')[-2]
			else:
				url_id 	= web_url.split('/')[-1]
			api_url = ARD_AUDIO_BASE + "programsets/%s/%s" % (url_id, href_add)
			
			title = stringextract('"title":"', '"', item)				# PRG, z.B. Blaue Couch
			anz =  stringextract('"numberOfElements":', ',', item)
			if anz == '':
				continue

			img = stringextract('"image"', '"url1X1"', item)			# 18.02.2022 neues Format
			img = stringextract('"url":"', '"', item)	
			img = img.replace('{width}', '640')
			
			
			PLog("prg: %s, url_id: %s" % (title, url_id))
			tag = u"Folgeseiten | Anzahl: %s\nKategorie [B]%s[/B]" % (anz, cat) 
			summ = u"zu den einzelnen Beiträgen:\n%s" % title 
			
			api_url=py2_encode(api_url); title=py2_encode(title)
			fparams="&fparams={'url': '%s', 'title': '%s'}" % (quote(api_url), quote(title))
			addDir(li=li, label=title, action="dirList", dirID="Audio_get_sendung_api", \
				fanart=img, thumb=img, fparams=fparams, tagline=tag, summary=summ)						
	
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	


#----------------------------------------------------------------
# Buttons ARD Audio Event Streams, Bundesliga ARD-Hörfunk,
#	 Sportschau Livestreams, Liste Netcast-Audiostreams
# Audio-Calls:
#	ARDSportAudioXML -> 	SenderLiveResolution		-> PlayAudio
#	ARDSportHoerfunk ->  	ARDSportAudioStreamsSingle 	-> PlayAudio
#	ARDSportAudioStreams ->	ARDSportAudioStreamsSingle 	-> PlayAudio
# Hinw.: Timeouts bei den Sportschau-Audio-Seiten möglich (aktuelle 
#	Livestreams, Netcast-Audiostreams)
# 01.05.2022 Button Bundesliga ARD-Hörfunk auskommentiert (Links defekt),
# 14.06.2022 entfernt, Button "aktuelle LIVESTREAMS(sportschau.de)"
#	verlegt nach ARDnew.ARDSportLive
#
def ARDAudioEventStreams(li=''):
	PLog('ARDAudioEventStreams:')
	endof=False
	if li == '':														# Aufruf ARDSportWDR (ARDnew)
		endof = True
		li = xbmcgui.ListItem()

	channel = u'ARD Audio Event Streams'								# aus livesenderTV.xml								
	title = u"[B]Audio:[/B] ARD Audio Event Streams"					# div. Events, z.Z. Fußball EM2020   
	img = R("radio-livestreams.png")
	tag = u'Reportagen von regionalen und überregionalen Events' 
	img=py2_encode(img); channel=py2_encode(channel); title=py2_encode(title);
	fparams="&fparams={'channel': '%s'}"	% (quote(channel))
	addDir(li=li, label=title, action="dirList", dirID="ARDSportAudioXML", fanart=img, 
		thumb=img, tagline=tag, fparams=fparams)
		
	label = "[B]Audio:[/B] Sport in der Audiothek"					# Querverweis Audiothek Rubrik Sport
	li = xbmcgui.ListItem()
	tag = u"LIVE: 1. und 2. Bundesliga, einschl. Bundesliga-Konferenz, Aktuell informiert und weitere Themen"
	thumb = R("ard-sport.png")
	href = 'https://www.ardaudiothek.de/rubrik/sport/42914734'
	title=py2_encode(title); href=py2_encode(href);
	fparams="&fparams={'li': '','url': '%s', 'title': '%s', 'ID': 'Audio_get_rubriken_web'}" % (quote(href), 
		quote("Sport"))
	addDir(li=li, label=label, action="dirList", dirID="Audio_get_cluster_rubrik", \
		fanart=img, thumb=thumb, tagline=tag, fparams=fparams)	
	 	
					
	title = u"[B]Audio:[/B] Audiostreams auf sportschau.de"						# Button Audiostreams sportschau.de
	href = 'https://www.sportschau.de/audio/index.html'
	img = R("tv-ard-sportschau.png")								
	tag = u'aktuelle Audiostreams der ARD Sportschau.' 
	block = 'class=*mediaplayer'
	title=py2_encode(title); href=py2_encode(href);	img=py2_encode(img);
	block=py2_encode(block);
	fparams="&fparams={'title': '%s', 'path': '%s',  'img': '%s', 'cacheID': 'ARDSport_Audios', 'block': '%s'}" %\
		(quote(title), quote(href), quote(img), quote(block))
	addDir(li=li, label=title, action="dirList", dirID="ARDSportSingleBlock", fanart=img, 
		thumb=img, tagline=tag, fparams=fparams)

	title = u"[B]Audio:[/B] alle Netcast-Audiostreams auf sportschau.de"		# Button Netcast-Audiostreams-Liste
	href = 'https://www.sportschau.de/sportimradio/audiostream-netcast-uebersicht-100.html'
	img = R("tv-ard-sportschau.png")								
	tag = u'Die Übersicht aller Netcast-Audiostreams für die Bundesliga-Übertragungen.' 
	block = 'class=*mediaplayer'
	title=py2_encode(title); href=py2_encode(href);	img=py2_encode(img);
	fparams="&fparams={'title': '%s', 'path': '%s',  'img': '%s', 'cacheID': 'ARDSport_Netcast', 'block': '%s'}" %\
		(quote(title), quote(href), quote(img), quote(block))
	addDir(li=li, label=title, action="dirList", dirID="ARDSportSingleBlock", fanart=img, 
		thumb=img, tagline=tag, fparams=fparams)
	
	if endof:
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	else:	
		return

#----------------------------------------------------------------
# gibt entw. den  HTML- oder den json-Teil der Webseite zurück
# HTML-Inhalt genutzt für Cluster-Liste.
# json-Inhalt weicht für einige Objekte von api-json-Inhalt ab
# 16.01.2023 json-Extraktion wie get_ArtePage
def Audio_get_webslice(page, mode="web"):
	PLog('Audio_get_webslice:')
	
	if mode == "web":
		pos1 = page.find('</head><body>')
		pos2 = page.find('{"props"')
		page = page[pos1:pos2]
	if mode == "json":							# wie get_ArtePage
		mark1 = '{"pageProps'; mark2 = '__N_SSP":true}'		
		pos1 = page.find(mark1)
		pos2 = page.find(mark2)
		PLog(pos1); PLog(pos2)
		if pos1 < 0 and pos2 < 0:
			PLog("json-Daten fehlen")
			page=''								# ohne json-Bereich: leere Seite
		page = page[pos1:pos2+len(mark2)]	
	
	PLog(len(page))
	return page
				
#----------------------------------------------------------------
# extrahiert Einzelbeiträge einer Sendung
# Aufrufer: AudioSenderPrograms + Audio_get_sendung_api (Fallback
#	bei page mit fehlenden durations), Audio_get_cluster_single,
#	Audio_get_homescreen
# 18.02.2022 Anpassung an ARD-Änderungen
#	Web-Url -> AudioWebMP3, next-Url nicht mehr enthalten
# Nutzung Audio_get_items_single  + Audio_get_nexturl wie 
#	Audio_get_sendung_api
# Sammel-Downloads: Liste enthält je nach Quelle mp3_url oder web_url
#	(Auswertung web_url via DownloadMultiple -> AudioWebMP3)
#
def Audio_get_sendung(url, title, page=''):	
	PLog('Audio_get_sendung: ' + title)
	url_org=url; title_org=title

	title_org = title; url_org = url
	PLog(url);  
	base = "https://api.ardaudiothek.de/"
				
	li = xbmcgui.ListItem()
	ID = 'ARD Audiothek'
	li = home(li, ID)				# Home-Button
		
	if page == '':					# Fallback Audio_get_sendung_api?
		page, msg = get_page(path=url, GetOnlyRedirect=True)	
		path = page								
		page, msg = get_page(path)	
		if page == '':	
			msg1 = "Fehler in Audio_get_sendung:"
			msg2 = msg
			MyDialog(msg1, msg2, '')	
			return li
	
	if page.startswith('<!DOCTYPE html>'):
		page = Audio_get_webslice(page, mode="json")				# json ausschneiden
	pos = page.find("nodes")
	PLog(pos)
	if pos > 0:
		page = page[pos:]
		
	page = page.replace('\\"', '*')
	elements = stringextract('"numberOfElements":', ',', page)		# für Mehr anzeigen
	PLog("elements: %s" % elements)
	items = blockextract('"id":', page, '}]},{')					# bis nächste "id" (nicht trennsicher)
	PLog(len(items))
	
	PLog("Mark0")
	cnt=0; dl_cnt=0; downl_list=[]; skip_list=[]
	for item in items:		
		mp3_url=''; web_url=''
		if item.find("publishDate") < 0 and  item.find("publicationStart") < 0:
			continue
		mp3_url, web_url, attr, img, dur, title, summ, source, sender, pubDate = Audio_get_items_single(item)		
		if title in skip_list:										# mögl. bei programsets mit Einzelbeiträgen
			continue
		skip_list.append(title)
		
		tag = "Dauer %s" % dur
		if pubDate:
			tag = "%s | Datum %s" %  (tag, pubDate)
		if sender:
			tag = "%s | Sender %s\n[B]%s[/B]" % (tag, sender, attr)
		summ_par = summ
		
		PLog('5Satz:');
		PLog(title); PLog(tag); PLog(summ[:80]); PLog(mp3_url); PLog(web_url);
		title=py2_encode(title); web_url=py2_encode(web_url); mp3_url=py2_encode(mp3_url);
		img=py2_encode(img); summ_par=py2_encode(summ_par);	
		
		if mp3_url:
			downl_list.append("%s#%s" % (title, mp3_url))
			summ_par = "%s\n\n%s" % (tag, summ)
			summ_par = summ_par.replace('\n', '||')
			fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" % (quote(mp3_url), 
				quote(title), quote(img), quote_plus(summ_par))
			addDir(li=li, label=title, action="dirList", dirID="AudioPlayMP3", fanart=img, thumb=img, 
				fparams=fparams, tagline=tag, summary=summ)			
		else:
			downl_list.append("%s#%s" % (title, web_url))
			
			fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'ID': ''}" % (quote(web_url), 
				quote(title), quote(img), quote_plus(summ_par))
			addDir(li=li, label=title, action="dirList", dirID="AudioWebMP3", fanart=img, thumb=img, 
				fparams=fparams, tagline=tag, summary=summ)	
		cnt=cnt+1

	if cnt  == 0:
		msg1 = u'nichts gefunden'
		msg2 = title_org
		icon = R(ICON_MAIN_AUDIO)		
		xbmcgui.Dialog().notification(msg1,msg2,icon,3000)
		PLog("%s: %s" % (msg1, msg2))
		return
		
	if elements and url_org:
		myfunc = "Audio_get_sendung"	
		Audio_get_nexturl(li, url_org, title_org, elements, cnt, myfunc)# Mehr anzeigen
	
	if len(downl_list) > 1:												# Button Sammel-Downloads
		title=u'[B]Download! Alle angezeigten %d Podcasts speichern?[/B]' % cnt
		summ = u'[B]Download[/B] von insgesamt %s Podcasts' % len(downl_list)	
		Dict("store", 'dl_podlist', downl_list) 

		fparams="&fparams={'key': 'dl_podlist'}" 
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.Podcontent.DownloadMultiple", 
			fanart=R(ICON_DOWNL), thumb=R(ICON_DOWNL), fparams=fparams, summary=summ)
		

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
#----------------------------------------------------------------
# Aufrufer: PodFavoriten (Web-Url -> api umgesetzt), AudioSenderPrograms,
#	Audio_get_search_cluster, Audio_get_homescreen
# json -> strings (Performance)
# Nutzung Audio_get_items_single + Audio_get_nexturl wie Audio_get_sendung
# Sammel-Downloads: Liste enthält je nach Quelle mp3_url oder web_url
#	(Auswertung web_url via DownloadMultiple -> AudioWebMP3)
#
def Audio_get_sendung_api(url, title, page='', home_id='', ID=''):
	PLog('Audio_get_sendung_api: ' + url)
	PLog(ID)
	url_org=url; title_org=title

	li = xbmcgui.ListItem()

	if page == '':
		page, msg = get_page(path=url)
	if page == '':	
		msg1 = "Fehler in Audio_get_sendung_api:"
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return li
	PLog(len(page))
	
	if page.find('"duration"') < 0:									# Fallback -> Audio_get_sendung
		PLog("Fallback_Audio_get_sendung")
		Audio_get_sendung(url, title, page)
		return
		
	if home_id:
		li = home(li, home_id)				# Home-Button
	else:
		li = home(li, 'ARD Audiothek')		# Home-Button
	
	page = page.replace('\\"', '*')	
	elements = stringextract('"numberOfElements":', ',', page)		# für Mehr anzeigen
	PLog("elements: %s" % elements)
	items = blockextract('"duration"', page)
	PLog(len(items))
	
	PLog("Mark1")
	cnt=0; dl_cnt=0; downl_list=[]
	for item in items:
		mp3_url, web_url, attr, img, dur, title, summ, source, sender, pubDate = Audio_get_items_single(item, ID)		
			
		tag = "Dauer %s" % dur
		if pubDate:
			tag = "%s | Datum %s" %  (tag, pubDate)
		if sender:
			tag = "%s | Sender %s\n[B]%s[/B]" % (tag, sender, attr)
		summ_par = summ
		
		PLog('7Satz:');
		PLog(tag); PLog(summ[:80]);
		title=py2_encode(title); web_url=py2_encode(web_url); mp3_url=py2_encode(mp3_url);
		img=py2_encode(img); summ_par=py2_encode(summ_par);	
			
		if mp3_url:
			downl_list.append("%s#%s" % (title, mp3_url))

			fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" % (quote(mp3_url), 
				quote(title), quote(img), quote_plus(summ_par))
			addDir(li=li, label=title, action="dirList", dirID="AudioPlayMP3", fanart=img, thumb=img, 
				fparams=fparams, tagline=tag, summary=summ)			
		else:
			downl_list.append("%s#%s" % (title, web_url))
			
			fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'ID': ''}" % (quote(web_url), 
				quote(title), quote(img), quote_plus(summ_par))
			addDir(li=li, label=title, action="dirList", dirID="AudioWebMP3", fanart=img, thumb=img, 
				fparams=fparams, tagline=tag, summary=summ)
				
		cnt=cnt+1	

	if cnt  == 0:
		msg1 = u'nichts gefunden'
		msg2 = title_org
		icon = R(ICON_MAIN_AUDIO)		
		xbmcgui.Dialog().notification(msg1,msg2,icon,3000)
		PLog("" % (msg1, msg2))
		return
	
	if elements and url_org:
		myfunc = "Audio_get_sendung_api"	
		Audio_get_nexturl(li, url_org, title_org, elements, cnt, myfunc)# Mehr anzeigen
	
	if len(downl_list) > 1:												# Button Sammel-Downloads
		title=u'[B]Download! Alle angezeigten %d Podcasts speichern[/B]' % cnt
		summ = u'[B]Download[/B] von insgesamt %s Podcasts' % len(downl_list)	
		Dict("store", 'dl_podlist', downl_list) 

		fparams="&fparams={'key': 'dl_podlist'}" 
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.Podcontent.DownloadMultiple", 
			fanart=R(ICON_DOWNL), thumb=R(ICON_DOWNL), fparams=fparams, summary=summ)
	

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#-------------------------
# Mehr-Button für myfunc (Audio_get_sendung,  
#	Audio_get_sendung_api)
# 
def Audio_get_nexturl(li, url_org, title_org, elements, cnt, myfunc):
	PLog('Audio_get_nexturl:')
	
	if elements:														# numberOfElements
		PLog(url_org)
		offset = stringextract('offset=', '&', url_org)
		limit=20
		if "limit=" in url_org:
			limit = url_org.split("limit=")[-1]
		PLog(elements); PLog(offset);
		listed = int(offset) + cnt 
		PLog("elements: %s, offset: %s, limit: %s, listed: %d" % (elements, offset, limit, listed))
		if (listed + 1) < int(elements):
			url = url_org.split("offset=")[0]
			url = url + "offset=%d&limit=%d" % (listed, int(limit))	# listed = neuer offset
			tag = u"Mehr (ab Beitrag %s von %s)" % (str(listed+1), elements)
			PLog(url); PLog(tag);
			title_org=py2_encode(title_org); url=py2_encode(url);
			fparams="&fparams={'title': '%s', 'url': '%s'}" % (quote(title_org), quote(url))
			addDir(li=li, label=title_org, action="dirList", dirID=myfunc, fanart=R(ICON_MEHR), 
				thumb=R(ICON_MEHR), fparams=fparams, tagline=tag)		
		return
	
#-------------------------
# extrakt json-Rekord für Audio_get_sendung + 
#	Audio_get_sendung_api
# 
def Audio_get_items_single(item, ID=''):
	PLog('Audio_get_items_single:')
	PLog(ID)
	base = "https://www.ardaudiothek.de"
	
	item = item.replace('\\"', '*')
	mp3_url=''; web_url=''; attr=''; img=''; dur=''; title=''; 
	summ=''; source=''; sender=''; pubDate='';
	
	mp3_url = stringextract('"downloadUrl":"', '"', item)			# api-Seiten ev. ohne mp3_url
	if 	mp3_url == '':
		audios = stringextract('"audios":', '}', item)				# Altern.
		mp3_url = stringextract('"url":"', '"', audios)
	if 	mp3_url == '':	
		web_url = stringextract('"sharingUrl":"', '"', item)		# Weblink
	if 	mp3_url == '' and web_url == "":							# neu ab 25.03.2023 (Web-json)
		web_url = base + stringextract('"path":"', '"', item)

	attr = stringextract('"attribution":"', '"', item)				# Sender, CR usw.
	if attr:
		attr = "Bild: %s" % attr

	img = stringextract('"image":', '},', item)
	img = stringextract('"url":"', '"', img)
	img = img.replace('{width}', '640')
	img = img.replace('16x9', '1x1')								# 16x9 kann fehlen, z,B. bei Suche
	img = img.replace(u'\\u0026', '&')								# 13.03.2022: escape-Zeichen mögl.
	

	dur = stringextract('"duration":', ',', item)					# in Sek.
	dur = dur.replace("}", '')										# 3592} statt 3592,
	dur = seconds_translate(dur)
	if "clipTitle" in item:											# Abschnitt "tracking"
		title = stringextract('"clipTitle":"', '"', item)
	else:
		title = stringextract('"title":"', '",', item)				# '",' gegen Hochkommas im Titel
	title = repl_json_chars(title)
	summ = stringextract('"synopsis":"', '"', item)
	summ = repl_json_chars(summ)
	source = stringextract('"source":"', '"', item)
	sender = stringextract('zationName":"', '"', item)

	pubDate = stringextract('DateAndTime":"', '"', item)			# 2021-11-16T16:12:43+01:00
	if pubDate == '':
		pubDate = stringextract('"publicationDate":"', '"', item)	# 20220120
	if pubDate == '':
		pubDate = stringextract('"publishDate":"', '"', item)		# 2021-05-26T09:26:44+02:00
	if pubDate:
		if len(pubDate) == 25:
			pubDate = "[B]%s.%s.%s, %s:%s[/B]" % (pubDate[8:10],pubDate[5:7],pubDate[0:4],pubDate[11:13],pubDate[14:16])
		if len(pubDate) == 8:			
			pubDate = "[B]%s.%s.%s[/B]" % (pubDate[6:8], pubDate[4:6], pubDate[0:4])
	
	PLog("mp3_url: %s, web_url: %s, attr: %s, img: %s, dur: %s" % (mp3_url, web_url, attr, img, dur))
	PLog("title: %s, summ: %s, source: %s, sender: %s, pubDate: %s" % (title, summ, source, sender, pubDate))
	return mp3_url, web_url, attr, img, dur, title, summ, source, sender, pubDate
							
#----------------------------------------------------------------
# 22.02.2022 Anpassung an ARD-Änderung
# Ausführung: AudioSearch_cluster 
# 26.03.2023 Umstellung Web.json -> api.json
def AudioSearch(title, query='', path=''):
	PLog('AudioSearch:')
	CacheTime = 6000								# 1 Std.
	title_org = title

	# Web.json.: "https://www.ardaudiothek.de/suche/%s/"  			# ähnlich, abweich. Bezeichner 
	base = "https://api.ardaudiothek.de/search?query=%s"
	
	if 	query == '':	
		query = get_query(channel='ARD Audiothek')
	PLog(query)
	if  query == None or query.strip() == '':
		return ""
		
	query = py2_encode(query)										# encode für quote
	query = query.strip()
	query_org = query	
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Audiothek')								# Home-Button
	
	if path == '':													# Folgeseiten
		path = base  % quote(query)
	path_org=path
	
	page, msg = get_page(path=path, do_safe=False)					# nach quote ohne do_safe 	
	if page == '':	
		msg1 = "Fehler in AudioSearch:"
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return
		
	if page.find('>Keine Treffer<') > 0:	
		msg1 = "leider keine Treffer zu:"
		msg2 = query
		MyDialog(msg1, msg2, '')	
		return
		
	AudioSearch_cluster(li, path, title="Suche: %s" % query, key="", query=query)
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
#----------------------------------------------------------------
# 1. Aufruf: lädt Webseite für Suche + ermittelt Cluster im Webteil,
#	erstellt die passenden api-Calls
# 2. Aufruf: führt api-Call aus und übergibt an Audio_get_search_cluster
# entfallen: Suchergebnisse -> PodFavoriten
# 25.03.2023 Umstellung Web -> json nach ARD-Änderungen
#
def AudioSearch_cluster(li, url, title, page='', key='', query=''):
	PLog('AudioSearch_cluster: ' + key)
	PLog(query); PLog(li)
		
	if page == '':													# Permanent-Redirect-Url				
		page, msg = get_page(path=url, do_safe=False, GetOnlyRedirect=True)	
		url = page								
		page, msg = get_page(path=url, do_safe=False)	
		if page == '':	
			msg1 = "Fehler in AudioSearch_cluster:" 
			msg2 = msg
			MyDialog(msg1, msg2, '')	
			return
		PLog(len(page))
		search_url = url											# für Step2
		
	try:
		page = json.loads(page)
		objs = page["data"]["search"]
	except Exception as exception:
		PLog("search_error: " + str(exception))
	PLog(len(objs))

	#--------------------------------								# 2. Aufruf Sendungen, Sammlungen
	if key:
		PLog("Step2:")
		Audio_get_search_cluster(objs, key)							#  -> Verteilung
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	
		return
	#--------------------------------	
	
	PLog("Step1:")													# 1. Aufruf 
	if li  == '':
		li = xbmcgui.ListItem()
		li = home(li,ID='ARD Audiothek')							# Home-Button
				
	# Der zusätzl. Abschnitt "deviceType": "responsive" mit 
	# 	allen Rubriken wird nicht gelistet
	cluster = [u"editorialCategories|Rubriken", 
			u"editorialCollections|Sammlungen", 
			u"programSets|Sendungen",
			u"items|Episoden (Einzelbeiträge)"]
	
	tag = "Folgeseiten"
	for clus in cluster:
		key, tag = clus.split("|")
		PLog("%s | %s" % (key, tag))
		anz = str(objs[key]["numberOfElements"])
		
		if objs[key]["numberOfElements"] > 0:		
			item =  objs[key]["nodes"][0]							# 1. Beitrag
			tag = u"Folgeseiten | [B]%s[/B]" % (tag)
			if key != "items":										# 
				tag = u"%s\nAnzahl: %s" % (tag, anz)
			# Anpassung für string-Auswertung:
			s=str(item); s=s.replace("'", '"'); s=s.replace('": "', '":"'); s=s.replace('", "', '","')
			s = s.replace('\\"', '*')
			mp3_url, web_url, attr, img, dur, title, summ, source, sender, pubDate = Audio_get_items_single(s)
			PLog("1Satz_a:")
			PLog(key); PLog(title); PLog(search_url); PLog(attr);
			
			search_url=py2_encode(search_url); title=py2_encode(title); 	# -> 2. Aufruf mit web_url
			fparams="&fparams={'li': '','url': '%s', 'title': '%s', 'key': '%s'}" % (quote(search_url), 
				quote(title), key)
			addDir(li=li, label=title, action="dirList", dirID="AudioSearch_cluster", \
				fanart=img, thumb=img, fparams=fparams, tagline=tag, summary=summ)	
		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)


#----------------------------------------------------------------
#	20.02.2022 Erneuerung Audiothek
#	Auswertung Mehrfach-Beiträge für AudioSearch_cluster
#	keys: 	editorialCategories 	= Rubriken
#			editorialCollections = Sammlungen -> Audio_get_sendung_api
#			programSets = Sendungen	-> Audio_get_sendung)
#			items = Einzelsendungen (Episoden)
# 	25.03.2023 Anpassungen an ARD-Änderungen
#	27.03.2023 Anbindung Rubriken an Auswertung der Cluster via 
#		Audio_get_cluster_rubrik über Web-Link
#
def Audio_get_search_cluster(objs, key):
	PLog('Audio_get_search_cluster: ' + key)

	li = xbmcgui.ListItem()
	href_add = "offset=0&limit=12"
	
	if key=="items" :											# Einzel (Episoden)
		items =  objs[key]["nodes"]
		PLog(len(items))
		s=str(items); s=s.replace(u"'", '"'); s=s.replace(u'": "', '":"'); s=s.replace(u'", "', '","')
		s = s.replace(u'\\"', '*')
		s = s.replace(u'""', '"*')
		Audio_get_sendung(url="", title="Search_%s" % key, page=s)	
	else:														# Kategorien, Kollektionen, ProgrammSets
		li = home(li,ID='ARD Audiothek')		# Home-Button
		items =  objs[key]["nodes"]
		PLog(len(items))
		cnt=0
		for item in items:
			node_id = item["id"]								# -> api-Path				
			# Anpassung für string-Auswertung:
			s=str(item); s=s.replace("'", '"'); s=s.replace('": "', '":"'); s=s.replace('", "', '","')
			s = s.replace('\\"', '*')
			mp3_url, web_url, attr, img, dur, title, summ, source, sender, pubDate = Audio_get_items_single(s, key)
			tag = "Folgeseiten"
			if "programSets" in key:							# Sendungen der Sender
				tag = "%s\nSender: %s" % (tag, sender)
			href = ARD_AUDIO_BASE  + "%s/%s/?offset=0&limit=20" % (key, node_id) 
			
			PLog('13Satz_a:');
			PLog(title); PLog(href); PLog(img);
			title=py2_encode(title); href=py2_encode(href);	
			
			if key=="editorialCollections" or key=="programSets":# Kollektionen, ProgrammSets
				fparams="&fparams={'url': '%s', 'title': '%s'}" % (quote(href), quote(title))
				addDir(li=li, label=title, action="dirList", dirID="Audio_get_sendung", \
					fanart=img, thumb=img, fparams=fparams, tagline=tag, summary=summ)
			else:												# editorialCategories / Kategorien
				PLog('13Satz_b: ' + href);
				href = "https://www.ardaudiothek.de/rubrik/%s" % node_id
				fparams="&fparams={'li': '','url': '%s', 'title': '%s', 'ID': 'Audio_get_search_cluster'}" %\
					(quote(href), quote(title))
				addDir(li=li, label=title, action="dirList", dirID="Audio_get_cluster_rubrik", \
					fanart=img, thumb=img, fparams=fparams)				
							
			cnt=cnt+1		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	

			
#----------------------------------------------------------------
# Aufrufer: Audio_get_rubriken_web (Liste Rubriken),
#	Audio_get_homescreen
# anders als AudioSearch_cluster wird für Rubriken der json-
#	Teil der Webseite ausgewertet - mit string-funktionen
#	Der Webteil eignet sich nicht wg. fehlender Bilder in den
#	Empfehlungen.
# Aufteilung Web-Beiträge: 1. Highligths, 2. veränderliche
#	Cluster, 3. Meistgehört, 4. Neueste Episoden, 5. Ausgewählte 
#	Sendungen, 6. Alle Sendungen aus dieser Rubrik  
def Audio_get_cluster_rubrik(li, url, title, ID=''):
	PLog('Audio_get_cluster_rubrik: ' + ID)
	PLog(title)
	title_org = title
	CacheTime = 6000												# 1 Std.
	
	if li  == '':
		li = xbmcgui.ListItem()
		li = home(li, ID='ARD Audiothek')							# Home-Button		
		
	if "AudioHomescreen" in ID:										# Stage-Beiträge Startseite
		rubrik_id = ID
	else:
		rid = url.split('/')[-1]
		rubrik_id = "AudioRubrikWebJson_%s" % rid

	page = Dict("load", rubrik_id, CacheTime=CacheTime)				# json-Teil der Webseite schon vorhanden?
	if page == False or page == '':									# Cache miss od. leer - vom Sender holen
		# Name im Pfad fehlt hier noch, daher Redirect:
		page, msg = get_page(path=url, GetOnlyRedirect=True)		# Permanent-Redirect-Url
		url = page								
		page, msg = get_page(path=url)	
	if page == '':	
		msg1 = "Fehler in Audio_get_cluster_rubrik:" 
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return li
	PLog(len(page))
			
	if page.startswith('<!DOCTYPE html>'):							# Webseite musste neu geladen werden
		page = Audio_get_webslice(page, mode="json")				# webslice: json ausschneiden
		page = transl_json(page); page = page.replace('\\"', '*')
		Dict("store", rubrik_id, page)

	#--------------------------------								# Empfehlungen + veränderliche Cluster
	sections = stringextract('"sections":', '"rubricsData":', page)	
	PLog(sections[:80])
	
	PLog('Mark0')
	data=[]; stage=False; cnt=0										# wie Audio_get_cluster_single
	if "AudioHomescreen" in ID:										# AudioHomescreen hier nicht Stage
		data = blockextract('__typename"', stage)
	else:
		if '"type":"STAGE"' in page:								# Stage-Sätze
			data.append(stringextract('"STAGE"', '}}}]},', page))
			stage=True
		data = data + blockextract(']},{"id":', page)				# und restl. Cluster
	PLog(len(data))
	
	for item in data:	
		section_id = stringextract('"id":"', '"', item)				# id":"comedy_satire-100:-8132981499462389106",
		if cnt == 0 and stage:
			section_id = "STAGE"									# nur STAGE auswerten

		tag = u"[B]Folgeseiten[/B]"
		title = stringextract('"title":"', '"', item)				# Cluster-Titel	
		title = repl_json_chars(title)
		pos = item.find('__typename'); item = item[pos:]			# 1. Beitrag
		ftitle = stringextract('"title":"', '"', item)
		img = stringextract('"url1X1":"', '"', item)
		#img = img.replace('{width}', '640')						# fehlt manchmal
		img = img.replace('{width}', '320')
		if img == '':												# fehlt bei nicht verfügb. Livestreams, s.
			continue												#	Audio_get_homescreen (GRID_LIST_COLLAPSIBLE)
			
		tag = "%s\n\n1. Beitrag: %s" % (tag, ftitle)	

		PLog('2Satz:')
		PLog(title); PLog(img); PLog(rubrik_id); PLog(section_id);
		title=py2_encode(title); rubrik_id=py2_encode(rubrik_id); 
		section_id=py2_encode(section_id);
		fparams="&fparams={'title': '%s', 'rubrik_id': '%s', 'section_id': '%s'}" % \
			(quote(title), quote(rubrik_id), quote(section_id))
		addDir(li=li, label=title, action="dirList", dirID="Audio_get_cluster_single", \
			fanart=img, thumb=img, fparams=fparams, tagline=tag)	
		cnt=cnt+1
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#----------------------------------------------------------------
# Aufrufer Audio_get_cluster_rubrik, Audio_get_homescreen (Stage) 
#	listet einz. Cluster oder Stage (ohne section_id)
#	Json-Ausschnitt der Rubrik-Webseite im Dict(rubrik_id)
#
def Audio_get_cluster_single(title, rubrik_id, section_id, page=''):
	PLog('Audio_get_cluster_single: ' + title)
	PLog(rubrik_id); PLog(section_id)

	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Audiothek')			# Home-Button

	if page == '':								# page nicht genutzt
		page = Dict("load", rubrik_id)

	data=[]										# wie Audio_get_cluster_rubrik
	if section_id == "STAGE":					# nur Stage auswerten, Homescreen od. Rubriken
		cluster = stringextract('"sections"', '}}}]},', page)
	else:
		data = data + blockextract(']},{"id":', page)	
		for item in data:						# Cluster section_id suchen 
			if section_id in item:
				PLog("found: " + section_id)
				cluster = item
				break
	PLog(cluster[:300])
	pos = cluster.find('nodes'); cluster = cluster[pos:]
	nodes = blockextract('"__typename":', cluster)	
	PLog(len(nodes))
			
	downl_list=[]; 	href_add = "offset=0&limit=12"	
	for node in nodes:		
		imgalt2=''; web_url=''; mp3_url=''
		mp3_url = stringextract('"downloadUrl":"', '"', node)			# api-Seiten ev. ohne mp3_url
		if 	mp3_url == '':
			audios = stringextract('"audios":', '}', node)				# Altern.
			mp3_url = stringextract('"url":"', '"', audios)
		if 	mp3_url == '':	
			web_url = stringextract('"sharingUrl":"', '"', node)		# Weblink
		
		node_id = stringextract('"id":"','"', node)				# ID der Sendung / des Beitrags / ..	
		typename = stringextract('__typename":"','"', node)		# Typ der Sendung / des Beitrags / ..	
		title = stringextract('"title":"','"', node)	
		dur = stringextract('"duration":',',', node)
		dauer = seconds_translate(dur)
		pubDate = stringextract('"publishDate":"','"', node)
		if pubDate:												# 2021-08-11T07:00:00+00:00
			pubDate = pubDate = "%s.%s.%s %s Uhr" % (pubDate[8:10], pubDate[5:7], pubDate[0:4], pubDate[11:16])
		descr = stringextract('"summary":"','"', node)
		if 	descr == '':
			descr = stringextract('"synopsis":"','"', node)
		if 	descr == '':
			descr = stringextract('"description":"','"', node)
		img = stringextract('"url1X1":"','"', node)				# möglich: "image": null 	
		#img = img.replace('{width}', '640')
		img = img.replace('{width}', '320')
		if img == '':
			img = R(ICON_DIR_FOLDER)
		imgalt1 = stringextract('"description":"','"', node)	# Bildbeschr.	
		imgalt2 = stringextract('"attribution":"','"', node)	# Bild-Autor
		imgalt2 = repl_json_chars(imgalt2)
		org = stringextract('"organizationName":"','"', node)	
		anz = stringextract('"totalCount":','}', node)			# Anzahl bei Mehrfach-Beiträgen
		
		descr	= unescape(descr); descr = repl_json_chars(descr)
		summ_par= descr.replace('\n', '||')
		title = repl_json_chars(title)
		
		PLog('4Satz:');
		PLog("typename: " + typename)
		PLog(title); PLog(img); PLog(web_url); PLog(descr[:40]);
		
		title=py2_encode(title); web_url=py2_encode(web_url);
		img=py2_encode(img); summ_par=py2_encode(summ_par);	

		if typename=="Item" or typename=="EventLivestream":		# Einzelbeitrag
			tag = "[B]Audiobeitrag[/B] | %s Std. | %s | %s\nBild: %s" % (dauer,pubDate,org,imgalt2)
			if typename=="EventLivestream":		
				tag = "[B]EventLivestream[/B]  %s | %s\nBild: %s" % (pubDate,org,imgalt2)
				
			if mp3_url:
				fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" % (quote(mp3_url), 
					quote(title), quote(img), quote_plus(summ_par))
				addDir(li=li, label=title, action="dirList", dirID="AudioPlayMP3", fanart=img, thumb=img, 
					fparams=fparams, tagline=tag, summary=descr)			
			else:	
				fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" % (quote(web_url), 
					quote(title), quote(img), quote_plus(summ_par))
				addDir(li=li, label=title, action="dirList", dirID="AudioWebMP3", fanart=img, thumb=img, 
					fparams=fparams, tagline=tag, summary=descr)
				
						
	#--------------------------------							# Cluster mit Folgeseiten
		if typename=="EditorialCollection" or typename=="ProgramSets" or typename=="ProgramSet":
			if anz: anz = "(%s)" % anz
			if imgalt2: imgalt2 = "Bild: %s" % imgalt2
			tag = u"[B]Folgeseiten[/B] %s\n%s" % (anz, imgalt2)
			if typename=="EditorialCollection":					# api-Call -> web-Url in Audio_get_sendung
				ID="Cluster_Sammlungen"
				href = ARD_AUDIO_BASE  + "editorialcollections/%s/?offset=0&limit=20" % (node_id)
			if typename=="ProgramSets" or typename=="ProgramSet": 	# api-Call -> web-Url in Audio_get_sendung
				ID=typename
				href = ARD_AUDIO_BASE  + "programsets/%s/?offset=0&limit=20" % (node_id)
			
			PLog('4Satz_2:');
			PLog(href)
			if typename=="ProgramSet":							# ProgramSet -> Einzelsendungen
				PLog("->Audio_get_sendung_api")
				fparams="&fparams={'url': '%s', 'title': '%s'}" % (quote(href), quote(title))
				addDir(li=li, label=title, action="dirList", dirID="Audio_get_sendung_api", \
					fanart=img, thumb=img, fparams=fparams, tagline=tag, summary=descr)						
			else:
				PLog("->Audio_get_sendung")
				fparams="&fparams={'url': '%s', 'title': '%s'}" % (quote(href), quote(title))
				addDir(li=li, label=title, action="dirList", dirID="Audio_get_sendung", \
					fanart=img, thumb=img, fparams=fparams, tagline=tag, summary=descr)						
			
		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	
	
#----------------------------------------------------------------
# Startseite https://www.ardaudiothek.de/
# Aufrufer: AudioStartHome
# Besonderheit: Nachladebeiträge ("nodes":[]) - hier Pfad-Nachbildung
#	der java-Funktion (Kennz. graphql im api-Call)
#	Die ermittelten Webadressen werden hier für die weitere Nutzung im
#	Addon zu api-Calls konvertiert.
# 
def Audio_get_homescreen(page='', cluster_id=''):
	PLog('Audio_get_homescreen:')
	CacheTime = 6000												# 1 Std.
	
	path = "https://www.ardaudiothek.de/"
	ID = "AudioHomescreen"
	page = Dict("load", ID, CacheTime=CacheTime)					# Startseite Web laden 
	if page == False or page == '':									# Cache miss od. leer - vom Sender holen
		page, msg = get_page(path=path)
		page = Audio_get_webslice(page, mode="json")				# webslice: json ausschneiden
		page = transl_json(page); page = page.replace('\\"', '*')
		Dict("store", ID, page)										# Audio_get_cluster_rubrik lädt für Stage				
	if page == '':	
		msg1 = "Fehler in Audio_get_homescreen:"
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return
	PLog(len(page))
	
	li = xbmcgui.ListItem()

	#----------------------------------------							# Step 1
	if cluster_id == '':
		PLog("Audio_step1")
		title = ID														# Stage auswerten
		tag = "Folgeseiten"
		img = R(ICON_DIR_FOLDER)
		
		cluster_id = "Highlights"
		label = "[B]%s[/B]" % cluster_id
		fparams="&fparams={'cluster_id': '%s'}" % cluster_id			# Button Highlights				
		addDir(li=li, label=label, action="dirList", dirID="Audio_get_homescreen",
			fanart=R(ICON_MAIN_AUDIO), thumb=img, tagline=tag, fparams=fparams)				
		
		endmark = '"nodes"'
		items = blockextract('"__typename"', page, endmark)				# Nachladebeiträge: "nodes":[]
		PLog(len(items))
		for item in items:
			if item.find('"image"') > 0:
				continue
			if item.find('"id"') < 0:									# ohne Cluster-ID
				continue
			if item.find('"GRID_LIST_COLLAPSIBLE"') > 0:				# Bsp. "LIVE: die Bundesliga"
				continue

			typename =  stringextract('"__typename":"', '"', item)
			cluster_id =  stringextract('"id":"', '"', item)
			title = stringextract('"title":"', '"', item)				# Cluster-Titel	deutsch
			cluster_type = stringextract('"type":"', '"', item)			# Cluster-Titel	engl.
			if title == '' or  title == None:
				continue
			if title == 'Stage':										# -> Highlights, s. Step 2
				continue
			if u'Weiterhören' in title or  u'Meine Sender' in title:	# skip personenbezogene Beiträge 								
				continue
			
			PLog('6Satz:');
			PLog(title); PLog(cluster_id); 
			cluster_id=py2_encode(cluster_id);
			fparams="&fparams={'cluster_id': '%s'}" % cluster_id				
			addDir(li=li, label=title, action="dirList", dirID="Audio_get_homescreen",
				fanart=R(ICON_MAIN_AUDIO), thumb=img, tagline=tag, fparams=fparams)				
				
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	

	else:	
	#----------------------------------------							# Step 2
		PLog("Audio_step2")
		PLog("cluster_id: " + cluster_id)								# ID für Nachladebeiträge (Web: "nodes":[])
		base = "https://www.ardaudiothek.de"
		
		if cluster_id == "Highlights":
			ID = "AudioHomescreen"
			title = cluster_id											# Stage auswerten
			Audio_get_cluster_single(title, rubrik_id=ID, section_id='STAGE') # lädt Dict "AudioHomescreen"
			return	
		
		li = home(li, 'ARD Audiothek')		# Home-Button
		
		# node_load: im Web java-generiert (api-Call graphql), hier mit eingestanzter cluster_id
		node_load='https://api.ardaudiothek.de/graphql?query=query%20WidgetQuery(%24id%3AID!)%7Bsection(id%3A%24id)%7Bid%20title%20type%20nodes%7Bid%20title%20image%7Burl%20url1X1%20description%20attribution%7Dpath%20...%20on%20ProgramSet%7Bid%20synopsis%20publicationService%7Bgenre%20organizationName%7D%7D...%20on%20Item%7BcoreType%20publishDate%20programSet%7Bid%20title%20publicationService%7Btitle%20genre%20path%20organizationName%7D%7Daudios%7Burl%20downloadUrl%20allowDownload%7Dduration%7D...%20on%20EditorialCollection%7Bsummary%20items%7BtotalCount%7D%7D%7D%7D%7D&variables=%7B%22id%22%3A%22entdecken-'
		node_path = node_load + cluster_id.split("entdecken-")[-1] + "%22%7D"
		
		page, msg = get_page(node_path, do_safe=False)					# node_path bereits quotiert
		page = page.replace('\\"', '*')
		
		typ = stringextract('"type":"', '"', page)
		PLog("typ: " + typ)	
		ctitle = stringextract('"title":"', '"', page)					# Cluster-Titel
		pos = page.find("nodes")
		page = page[pos:]
		if '"duration"' in page:
			items = blockextract('"duration"', page)
		else:
			items = blockextract('"id":', page, '}}')
		PLog(len(items))
		
		href_add = "?offset=0&limit=20"
		for item in items:	
			title = stringextract('"title":"', '"', item)
			web_url = stringextract('"path":"', '"', item)
			PLog("web_url: " + web_url) 
			if web_url == '' or title == '':
				continue
			
			node_id = stringextract('"id":"','"', item)					# ID der Sendung / des Beitrags / ..	
			title = stringextract('"title":"', '"', item)
			img = stringextract('"url":"', '"', item)
			#img = img.replace('{width}', '640')						# fehlt manchmal
			img = img.replace('{width}', '320')
			img = img.replace('16x9', '1x1')							# 16x9 kann fehlen (ähnlich Suche)
			summ = stringextract('"synopsis":"', '"', item)	
			# anz = stringextract('"numberOfElements":"', '"', item)	# fehlt
			attr = stringextract('"attribution":"', '"', item)
			genre = stringextract('"genre":"', '"', item)
			org = stringextract('"organizationName":"', '"', item)
			
			summ = repl_json_chars(summ); title = repl_json_chars(title)
			tag = "Cluster: %s | %s | %s" % (ctitle, attr, org)
			
			# Url-Konvertierung Web->Api ähnlich AudioSearch_cluster (o. query), 
			# items-Formate abweichend, Ziel-Verteilung via ID in AudioSearch_cluster:
			# Fallback für fehlende Kennz. in web_url, z.B. Sendungs-Vorschau 
			tag = "[B]Folgeseiten[/B]"
			vert="sendung"
			href = ARD_AUDIO_BASE  + "/items/%s%s" % (node_id, href_add)# Fallback vorangestellt	
						
			if '/sendung/' in web_url:									# "Sendungen"
				href = ARD_AUDIO_BASE  + "programsets/%s/%s" % (node_id, href_add)
			if '/sammlung/' in web_url:									# "Sammlungen"		
				href = ARD_AUDIO_BASE  + "editorialcollections/%s/%s" % (node_id, href_add)  
			if '/rubrik/' in web_url:									# "Rubriken"		
				href = ARD_AUDIO_BASE  + "editorialcategories/%s%s" % (node_id, href_add)  
			if '/episode/' in web_url:									# "Episoden (einzelne Beiträge)"										
				href = ARD_AUDIO_BASE  + "/items/%s%s" % (node_id, href_add) 
				vert='api'				
			
			PLog("8Satz:")
			PLog(title); PLog(href); PLog(img); PLog(summ[:80]); 
			PLog("vert: " + vert)
			
			href=py2_encode(href); title=py2_encode(title); 
			fparams="&fparams={'url': '%s', 'title': '%s'}" % (quote(href), quote(title))
			if vert == "sendung":
				fparams="&fparams={'url': '%s', 'title': '%s'}" % (quote(href), quote(title))
				addDir(li=li, label=title, action="dirList", dirID="Audio_get_sendung", \
					fanart=img, thumb=img, fparams=fparams, tagline=tag, summary=summ)		
			
			if vert == "api":
				fparams="&fparams={'url': '%s', 'title': '%s'}" % (quote(href), quote(title))
				addDir(li=li, label=title, action="dirList", dirID="Audio_get_sendung_api", \
					fanart=img, thumb=img, fparams=fparams, tagline=tag, summary=summ)							

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	

#----------------------------------------------------------------
# MP3 in Webpage (json-Bereich) ermitteln - Vorstufe für AudioPlayMP3
# Aufruf Audio_get_sendung (Webseite Feb. 2022 ohne mp3-Quellen)
# Audio_get_webslice nicht benötigt (url eindeutig ermittelbar)
# no_gui: nur Rückgabe (-> DownloadMultiple)
#
def AudioWebMP3(url, title, thumb, Plot, ID='', no_gui=''):
	PLog('AudioWebMP3: ' + title)
	
	page, msg = get_page(path=url, GetOnlyRedirect=True)	
	url = page								
	page, msg = get_page(path=url)			
	if page == '' and no_gui == '':	
		msg1 = "Fehler in AudioWebMP3:"
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return 
	PLog(len(page))
	
	url = stringextract('"downloadUrl":"','"', page)
	if 	url == '':
		pos = page.find('"audios":')
		if pos >= 0:
			url = stringextract('"url":"','"', page)			# vor downloadUrl
	 
	if url == '' and no_gui == '':	
		msg1 = "AudioWebMP3:"
		msg2 = "leider keine Audioquelle gefunden zu:"
		msg3 = "[B]%s[/B]" % title
		MyDialog(msg1, msg2, msg3)	
	else:
		if no_gui:
			PLog("url: " + url)
			return url
		else:
			AudioPlayMP3(url, title, thumb, Plot, ID='')
		
	return
	
#----------------------------------------------------------------
# Ausgabe Audiobeitrag
# Falls pref_use_downloads eingeschaltet, werden 2 Buttons erstellt
#	(Abspielen + Download).
# Falls pref_use_downloads abgeschaltet, wird direkt an PlayAudio
#	übergeben.
# 01.07.2021 ID variabel für Austausch des Home-Buttons
#
def AudioPlayMP3(url, title, thumb, Plot, ID=''):
	PLog('AudioPlayMP3: ' + title)
	
	if SETTINGS.getSetting('pref_use_downloads') == 'false':
		PLog('starte PlayAudio direkt')
		PlayAudio(url, title, thumb, Plot)  # PlayAudio	direkt
		return
	
	li = xbmcgui.ListItem()
	if ID == '':
		ID='ARD Audiothek'
	li = home(li, ID=ID)						# Home-Button
		
	summary = Plot.replace('||', '\n')			# Display
	 
	PLog(title); PLog(url); PLog(Plot);
	title=py2_encode(title); url=py2_encode(url);
	thumb=py2_encode(thumb); Plot=py2_encode(Plot);
	fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" % (quote(url), 
		quote(title), quote(thumb), quote_plus(Plot))
	addDir(li=li, label=title, action="dirList", dirID="PlayAudio", fanart=thumb, thumb=thumb, fparams=fparams, 
		summary=summary, mediatype='music')
	
	if ".icecastssl." not in url:				# Livestreams ausschließen
		download_list = []						# 2-teilige Liste für Download: 'title # url'
		download_list.append("%s#%s" % (title, url))
		PLog(download_list)
		title_org=title; tagline_org=''; summary_org=Plot
		li = test_downloads(li,download_list,title_org,summary_org,tagline_org,thumb,high=-1)  # Downloadbutton
		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
##################################### Ende Audiothek ###############################################
# ---------------------------------------- Start ARD Sportschau.de ---------------------------------
# 12.06.2022 nach erneutem Umbau der Seite www.sportschau.de abgeschaltet - s. Post 2606 zu
#	Update 4.4.0
#def ARDSport(title):
#def ARDSportEvents():
#def ARDSportPanel(title, path, img, tab_path='', paneltabs=''):
#def ARDSportPanelTabs(title, path, img, tab_path=''):
#def ARDSportHoerfunk(title, path, img):
#def ARDSportTablePre(base, img, clap_title=''):
#def ARDSportTable(path, title, table_path=''):
#def ARDSportAudioStreamsSingle(title, path, img, tag, summ, ID):
#def ARDSportPodcast(path, title):
#def ARDSportEventLive(path, page, title, oss_url='', url='', thumb='', Plot=''):		
#def ARDSportSliderSingleTab(title, path, img, page=''):
					
#--------------------------------------------------------------------------------------------------
# Liste der ARD Audio Event Streams in livesenderTV.xml
#	-> SenderLiveListe -> SenderLiveResolution (Aufruf
#	einz. Sender)
#
def ARDSportAudioXML(channel, img=''):
	PLog('ARDSportAudioXML:') 
	PLog(channel)

	SenderLiveListe(title=channel, listname=channel, fanart=img, onlySender='')
	return
#--------------------------------------------------------------------------------------------------
# Bilder für ARD Sportschau, z.B. Moderatoren
# Einzelnes Listitem in Video-Addon nicht möglich - s.u.
# Slideshow: ZDF_SlideShow
# 17.06.2022 angepasst an Webänderungen
#
def ARDSportBilder(title, path, img):
	PLog('ARDSportBilder:'); 
	PLog(title); PLog(path)
	title_org = title
	icon = R("ard-sportschau.png")

	li = xbmcgui.ListItem()
	li = home(li, ID='ARD')						# Home-Button

	page = ARDSportLoadPage(title, path, "ARDSportBilder") 	# path: cacheID
	if page == '':
		return
	PLog(len(page))
	
	pos = page.find('_topline">Bilderstrecke<')
	if pos < 0:
		pos = page.find('>Bilder<')							# Altern.
		if pos < 0:
			msg1 = u"%s:" % title
			msg2 = u'keine Bilder gefunden'
			xbmcgui.Dialog().notification(msg1,msg2,icon,2000,sound=True)
			return  
		
		
	page = page[pos:]
	cont = stringextract('data-v="', '"', page)				# json-Inhalt (Bildstrecke.json)
	cont = decode_url(cont)
	cont = unescape(cont)
	cont = (cont.replace('\\"','*').replace('<strong>','[B]').replace('</strong>','[/B]'))
	PLog(cont[:30])
	
	content = blockextract('"description"', cont)	
	PLog(len(content))
	if len(content) == 0:
		msg1 = u"%s:" % title
		msg2 = u'keine Bilder gefunden'
		xbmcgui.Dialog().notification(msg1,msg2,icon,2000,sound=True)
		return  
		
		
	fname = make_filenames(title)			# Ablage: Titel + Bildnr
	fpath = os.path.join(SLIDESTORE, fname)
	PLog(fpath)
	if os.path.isdir(fpath) == False:
		try:  
			os.mkdir(fpath)
		except OSError:  
			msg1 = 'Bildverzeichnis konnte nicht erzeugt werden:'
			msg2 = "%s/%s" % (SLIDESTORE, fname)
			PLog(msg1); PLog(msg2); 
			MyDialog(msg1, msg2, '')
			return li	
				
	image = 0; background=False; path_url_list=[]; text_list=[]
	for rec in content:			
		# größere Bilder erst auf der verlinkten Seite für einz. Moderator		
		img_src	= stringextract('"l":"', '"', rec)						# 
		if img_src == "":
			img_src	= stringextract('"m":"', '"', rec)
			
		headline	= stringextract('"title":"', '"', rec)
		headline	= unescape(headline); headline=repl_json_chars(headline)
		summ		= stringextract('"description":"', '"', rec)
		PLog("summ: " + summ[:80]) 	
		
		if img_src:
			#  Kodi braucht Endung für SildeShow; akzeptiert auch Endungen, die 
			#	nicht zum Imageformat passen
			pic_name 	= 'Bild_%04d.jpg' % (image+1)		# Bildname
			local_path 	= "%s/%s" % (fpath, pic_name)
			PLog("local_path: " + local_path)
			title = "Bild %03d" % (image+1)
			PLog("Bildtitel: " + title)
			title = unescape(title)
			lable = "%s: %s" % (title, headline)			# Listing-Titel
			
			thumb = ''
			local_path = os.path.abspath(local_path)
			thumb = local_path
			if os.path.isfile(local_path) == False:			# schon vorhanden?
				# urlretrieve(img_src, local_path)			# umgestellt auf Thread	s.u.		
				# path_url_list (int. Download): Zieldatei_kompletter_Pfad|Podcast, 
				#	Zieldatei_kompletter_Pfad|Podcast ..
				path_url_list.append('%s|%s' % (local_path, img_src))
					
				if SETTINGS.getSetting('pref_watermarks') == 'true':
					txt = "%s\n%s\n%s\n%s\n" % (fname,lable,'',summ)
					text_list.append(txt)	
				background	= True						
				
			PLog("Satz19:");PLog(title);PLog(img_src);PLog(thumb);PLog(summ[0:40]);
			# Lösung mit einzelnem Listitem wie in ShowPhotoObject (FlickrExplorer) hier
			#	nicht möglich (Playlist Player: ListItem type must be audio or video) -
			#	Die li-Eigenschaft type='image' wird von Kodi nicht akzeptiert, wenn
			#	addon.xml im provides-Feld video enthält
			if thumb:										
				local_path=py2_encode(local_path);
				fparams="&fparams={'path': '%s', 'single': 'True'}" % quote(local_path)
				addDir(li=li, label=lable, action="dirList", dirID="ZDF_SlideShow", 
					fanart=thumb, thumb=thumb, fparams=fparams, summary=summ)
				image += 1
			
	if background and len(path_url_list) > 0:				# Übergabe Url-Liste an Thread
		from threading import Thread	# thread_getfile
		textfile=''; pathtextfile=''; storetxt=''; url=img_src; 
		fulldestpath=local_path; notice=True; destdir="Slide-Show-Cache"
		now = datetime.datetime.now()
		timemark = now.strftime("%Y-%m-%d_%H-%M-%S")
		folder = fname 
		background_thread = Thread(target=thread_getpic,
			args=(path_url_list,text_list,folder))
		background_thread.start()
			
	if image > 0:		
		fpath=py2_encode(fpath);
		fparams="&fparams={'path': '%s'}" % quote(fpath) 	# fpath: SLIDESTORE/fname
		addDir(li=li, label="SlideShow", action="dirList", dirID="ZDF_SlideShow", 
			fanart=R('icon-stream.png'), thumb=R('icon-stream.png'), fparams=fparams)
		
		lable = u"Alle Bilder löschen"						# 2. Löschen
		tag = 'Bildverzeichnis: ' + fname 
		summ= u'Bei Problemen: Bilder löschen, Wasserzeichen ausschalten,  Bilder neu einlesen'
		fparams="&fparams={'dlpath': '%s', 'single': 'False'}" % quote(fpath)
		addDir(li=li, label=lable, action="dirList", dirID="DownloadsDelete", fanart=R(ICON_DELETE), 
			thumb=R(ICON_DELETE), fparams=fparams, summary=summ, tagline=tag)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
#--------------------------------------------------------------------------------------------------
# Die Videoquellen des WDR sind in SingleSendung nicht erreichbar. Wir laden
#	die Quelle (2 vorh.) über die Datei ..deviceids-medp-id1.wdr.de..js und
#	übergeben an PlayVideo.
# 26.11.2021 neu nach Änderungen der ARD: Videoquellen: Dekodierung hier - nicht in get_page. 
#	Video-/Audioquellen: Webseite (json embedded, wdr-Link, iframe-Link), Videolink 
#	(Endung .js) -> json-Datei mit Quellen, Videolink (Endung .html, enthalten: 
#	'-ardplayer_image) -> zusammengesetzt zu json-Link).
#	Die Quellen enthalten jeweils unterschiedl. Sets an m3u8-, mp4, -mp3-Quellen, häufig nur
#		1 Quelle.
# Fallback ohne Quellen: Webseiten mit 'media mediaA video' -> ARDSportSliderSingleTab
# Besonderheit: bei einigen Seiten scheitert utf-8-Dekodierung in util. Daher Dekodierung 
#	hier mit py2_decode
# 22.12.2021 auch verwendet von list_WDRstreamlinks->WDRstream mit page (Livesender 
#	WRD-Lokalzeit) 	
# 18.06.2022 ARDSportSliderSingleTab als Fallback entfernt (nach Webänderung obsolet)
def ARDSportVideo(path, title, img, summ, Merk='false', page=''):
	PLog('ARDSportVideo:'); 
	PLog(path); PLog(summ); PLog(len(page))
	summ = summ.replace('||||', ' | ')

	title_org = title
	# Header erforder.?: /wintersport/alle-videos-komplett-uebersicht-100.html
	headers="{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', \
		'Connection': 'keep-alive', 'Accept-Encoding': 'gzip, deflate, br', 'Cache-Control': 'max-age=0'}"
	msg=''
	if page == '':
		page, msg = get_page(path=path, header='', decode=True)		# decode hier i.V.m. py2_decode 						
	if page == '':
		msg1 = 'Seite kann nicht geladen werden.'
		msg2 = msg
		MyDialog(msg1, msg2, '')
		return 
	PLog(len(page))
	page=py2_decode(page)					

		
	# Bsp. video_src: "url":"http://deviceids-medp.wdr.de/ondemand/167/1673848.js"}
	#	-> 	//ardevent2.akamaized.net/hls/live/681512/ardevent2_geo/master.m3u8
	#	derselbe Streamlink wie Direktlink + Hauptmenü
	# 16.06.2019 nicht für die Livestreams geeignet.
	if 'deviceids-medp.wdr.de' in page:								# häufige Quelle
		video_src = stringextract('deviceids-medp.wdr.de', '"', page)
		video_src = 'http://deviceids-medp.wdr.de' + video_src
	else:
		PLog('hole_video_src_iframe:')
		video_src=''
		playerurl = stringextract('webkitAllowFullScreen', '</iframe>', page)
		playerurl = stringextract('src="', '"', playerurl)
		if playerurl:
			base = 'https://' + path.split('/')[2]					# Bsp. fifafrauenwm.sportschau.de
			video_src = base + playerurl
	PLog("video_src: " + video_src)
	
	if video_src == '':
		if 'class="media mediaA video' in page:					# ohne Quellen, aber Videos gefunden
			ARDSportSliderSingleTab(title, path, img, page)			# -> ARDSportSliderSingleTab - obsolet, s.o.
			return
			xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
				
		else:
			if '"videoURL" : "' in page or '"config"' in page:	# Quellen in Seite eingebettet					
				PLog('detect_videoURL:')
				# Je ein HLS + MP4-Link direkt auf der Seite im json-Format
				# Bsp.: www.sportschau.de/tor-des-monats/archiv/april2017tdm100.html
				web = stringextract('"mediaResource"', '</script>', page)	# json-Inhalt ausschneiden
				if web == '':							
					web = stringextract('"streamUrl":"', '"', page)	# z.B. .m3u8-Link auf hessenschau.de/sport
					web = '"videoURL":"' + web + '"'				# komp. für weit. Auswertung
				PLog("web-media oder -config: " + web[:100])
				page = web
				video_src=''										# skip 	'-ardplayer_image-' in video_src
			else:
				msg1 = u'Leider kein Video gefunden: %s' % title 	# keine Chance auf Videoquellen
				msg2 = path
				MyDialog(msg1, msg2, '')
				return
				xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

		
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD')						# Home-Button

	if video_src.endswith('.js'):									# //deviceids-medp-id1.wdr.de/../2581397.js
		page, msg = get_page(video_src)								# json mit (nur) Videoquellen laden
		
	if '"videoURL' in page or '"audioURL' in page:
		page = page.replace('":"', '" : "')						# Anpassung an Web-embedded json
		video_src=''
		
	m3u8_url=''; mp_url=''; title_m3u8=''; title_mp=''					# mp_url: mp4 oder mp3
	if '-ardplayer_image-' in video_src:							# Bsp. Frauen-Fußball-WM
		PLog('-ardplayer_image- in video_src:')
		# Debug-Url's:
		#https://fifafrauenwm.sportschau.de/frankreich2019/nachrichten/fifafrauenwm2102-ardplayer_image-dd204edd-de3d-4f55-8ae1-73dab0ab4734_theme-sportevents.html		
		#->:
		#https://fifafrauenwm.sportschau.de/frankreich2019/nachrichten/fifafrauenwm2102-ardjson_image-dd204edd-de3d-4f55-8ae1-73dab0ab4734.json	
					
		image = stringextract('image-', '_', video_src) 			# json-Pfad neu bauen
		PLog(image)
		path = video_src.split('-ardplayer_image-')[0]
		PLog(path)
		path = path + '-ardjson_image-' + image + '.json'
		PLog(path)
		page, msg = get_page(path)									# json mit videoquellen laden
		
		plugin 	= stringextract('plugin": 0', '_duration"', page) 
		auto 	= stringextract('"auto"', 'cdn"', plugin) 			# master.m3u8 an 1. Stelle		
		m3u8_url= stringextract('stream": "', '"', auto)
		PLog("m3u8_url: " + m3u8_url)
		title_m3u8 = "HLS auto | %s" % title_org
		
		mp 	= stringextract('quality": 3', 'cdn"', page)		# mp4-HD-Quality od. mp3
		mp_url= stringextract('stream": "', '"', mp)
		PLog("mp_url: " + mp_url)
		if mp_url:
			title_mp = "MP4 HD | %s" % title_org
			if mp_url.endswith('.mp3'):
				title_mp = "Audio MP3 | %s" % title_org
	
	else:															# Videoquellen in Webseite?
		videos = blockextract('"videoURL" : "', page, '}')
		videos = videos + blockextract('"audioURL" : "', page, '}')
		PLog(len(videos))
		
		if len(videos) == 0:
			msg1 = u'Leider kein Video gefunden: %s' % title # keine weitere Chance auf Videoquellen
			msg2 = path
			MyDialog(msg1, msg2, '')
			return
			xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
		
		
		for video in videos:
			if "videoURL" in video:
				url= stringextract('"videoURL" : "', '"', video)
			else:
				url= stringextract('"audioURL" : "', '"', video)
			if 'manifest.f4m' in url:					#  manifest.f4m überspringen
				continue
			if url.endswith('.m3u8'):
				m3u8_url = url
				title_m3u8 = "HLS auto | %s" % title_org
			if url.endswith('.mp4'):
				mp_url = url
				title_mp = "MP4 HD | %s" % title_org
			if url.endswith('.mp3'):
				mp_url = url
				title_mp = "MP3 Audio | %s" % title_org		
		
		if m3u8_url == '' and mp_url == '':				# ev. nur Audio verfügbar
			mp_url = stringextract('"audioURL":"', '"', page)
			
		if m3u8_url and m3u8_url.startswith('http') == False:		
			m3u8_url = 'https:' + m3u8_url				# //wdradaptiv-vh.akamaihd.net/..	
		if mp_url and mp_url.startswith('http') == False:		
			mp_url = 'https:' + mp_url				
		
		
	mediatype = 'video'
		
	# Sofortstart - direkt, falls Listing nicht Playable:
	# 04.08.2019 Sofortstart nur noch abhängig von Settings und nicht zusätzlich von  
	#	Param. Merk.
	if SETTINGS.getSetting('pref_video_direct') == 'true': # or Merk == 'true': 	# Sofortstart
		PLog('Sofortstart: ARDSportPanel')
		PLog(xbmc.getInfoLabel('ListItem.Property(IsPlayable)')) 
		PlayVideo(url=m3u8_url, title=title_m3u8, thumb=img, Plot=summ, sub_path="")
		return
	
	PLog("Satz27:")
	PLog("m3u8_url: " + m3u8_url); PLog(title_m3u8);
	PLog(title_mp); PLog("mp_url: " + mp_url)
	
	m3u8_url=py2_encode(m3u8_url); title_m3u8=py2_encode(title_m3u8); 
	title_mp=py2_encode(title_mp); 
	img=py2_encode(img); summ=py2_encode(summ);
	if m3u8_url:
		fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'sub_path': ''}" %\
			(quote_plus(m3u8_url), quote_plus(title_m3u8), quote_plus(img), quote_plus(summ))
		addDir(li=li, label=title, action="dirList", dirID="PlayVideo", fanart=img, thumb=img, fparams=fparams, 
			mediatype=mediatype, tagline=title_m3u8, summary=summ) 
	if mp_url:	
		if mp_url.endswith('.mp3'):
			mediatype = 'audio'
		fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'sub_path': ''}" %\
			(quote_plus(mp_url), quote_plus(title_mp), quote_plus(img), quote_plus(summ))
		addDir(li=li, label=title, action="dirList", dirID="PlayVideo", fanart=img, thumb=img, fparams=fparams, 
			mediatype=mediatype, tagline=title_mp, summary=summ) 
		
			
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
#---------------------------------------------------------------------------------------------------
# Neues  Menü sportschau.de (WDR)
# Ersatz für weggefallene Funktionen. Siehe Start ARD Sportschau.de
# 
def ARDSportWDR(): 
	PLog('ARDSportWDR:')
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Neu')								# Home-Button
	base = "https://images.sportschau.de"
	logo = base + "/image/3fbb1eaf-fb0a-4f1b-a5a9-44a643839cd5/AAABgTjL3GM/AAABgPp7Db4/16x9-1280/sportschau-logo-sendung-100.jpg"
	
	title = u"Startseite"									# Startseite	
	tag = u"Für Groß-Events bitte die vorhandenen Menü-Buttons verwenden."
	cacheID = "Sport_Startseite"
	img = logo
	path = "https://www.sportschau.de"
	title=py2_encode(title); path=py2_encode(path); img=py2_encode(img);
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'cacheID': '%s'}" %\
		(quote(title), quote(path), quote(img), cacheID)
	addDir(li=li, label=title, action="dirList", dirID="ARDSportCluster", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	title = u"Livestreams der Sportschau"
	tag = u"kommende Events: Ankündigungen mit Direktlinks"
	img = logo
	title=py2_encode(title)
	fparams="&fparams={'title': '%s'}" % quote(title)
	addDir(li=li, label=title, action="dirList", dirID="ARDSportLive", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	'''
	title = u"Event: [B]NORDISCHE SKI-WM[/B]"			# Großevent	
	tag = u"Alles zur Nordischen Ski-WM in Planica."
	cacheID = "Sport_SkiWM"
	img = "https://images.sportschau.de/image/237354e3-b9b2-46bf-993a-8ecc48947e7f/AAABhol6U80/AAABg8tMRzY/20x9-1280/constantin-schmid-150.webp"
	path = "https://www.sportschau.de/wintersport/nordische-ski-wm"
	title=py2_encode(title); path=py2_encode(path); img=py2_encode(img);
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'cacheID': '%s'}" %\
		(quote(title), quote(path), quote(img), cacheID)
	addDir(li=li, label=title, action="dirList", dirID="ARDSportCluster", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	
	'''
	
	title = u"Event-Archiv"									# Buttons für ältere Events	
	tag = u"Archiv für zurückliegende Groß-Events."
	img = logo
	fparams="&fparams={}"
	addDir(li=li, label=title, action="dirList", dirID="ARDSportWDRArchiv", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	title = u"Tor des Monats"									# Tor des Monats
	tag = u"Tor des Monats: Hier gibt's Highlights, Clips und ausgewählte Höhepunkte aus der langen Geschichte dieser Rubrik."
	img = "https://images.sportschau.de/image/02d77451-37d2-4f6c-a9e3-13747421eb85/AAABgQuiu3s/AAABgPp7Db4/16x9-1280/tordesmonats-sp-836.jpg" 
	path = "https://www.sportschau.de/tor-des-monats"
	title=py2_encode(title); path=py2_encode(path); 
	img=py2_encode(img); 
	fparams="&fparams={'title': '%s', 'path': '%s','img': '%s'}" %\
		(quote(title), quote(path), quote(img))
	addDir(li=li, label=title, action="dirList", dirID="ARDSportMonatstor", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	title = u"Moderation der Sportschau"						# Moderation
	tag = u"Bildgalerie"
	img = "https://images.sportschau.de/image/908ed0bc-918d-470d-bc61-377be863a818/AAABgUeOYdE/AAABgPp7JiI/16x9-640/alexander-bommes-sportschau-sp-104.jpg" 
	path = "https://www.sportschau.de/sendung/moderation"
	title=py2_encode(title); path=py2_encode(path); 
	img=py2_encode(img); 
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s'}" %\
		(quote(title), quote(path), quote(img))
	addDir(li=li, label=title, action="dirList", dirID="ARDSportHub", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	title = u"ARD Audio Event Streams"							# Audio Event Streams im Haupt-PRG	
	tag = u"Event- und Netcast-Streams, Sport in der Audiothek, Audiostreams auf sportschau.de"
	img = R("radio-livestreams.png")
	fparams="&fparams={}"
	addDir(li=li, label=title, action="dirList", dirID="ARDAudioEventStreams", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
#---------------------------------------------------------------------------------------------------
# Event-Archiv
#	Buttons für ältere Events
# 
def ARDSportWDRArchiv(): 
	PLog("ARDSportWDRArchiv:")
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD')						# Home-Button
	
	title = u"Event: [B]NORDISCHE SKI-WM[/B]"								# Großevent	
	tag = u"Alles zur Nordischen Ski-WM in Planica."
	cacheID = "Sport_SkiWM"
	img = "https://images.sportschau.de/image/237354e3-b9b2-46bf-993a-8ecc48947e7f/AAABhol6U80/AAABg8tMRzY/20x9-1280/constantin-schmid-150.webp"
	path = "https://www.sportschau.de/wintersport/nordische-ski-wm"
	title=py2_encode(title); path=py2_encode(path); img=py2_encode(img);
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'cacheID': '%s'}" %\
		(quote(title), quote(path), quote(img), cacheID)
	addDir(li=li, label=title, action="dirList", dirID="ARDSportCluster", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	title = u"Event: [B]Handball-WM 2023 in Polen und Schweden[/B]"			# Großevent	
	tag = u"Nachrichten, Berichte, Interviews und Ergebnisse zur Handball-WM 2023 in Polen und Schweden mit dem DHB-Team."
	cacheID = "Sport_WMHandball"
	img = "https://images.sportschau.de/image/9741356a-13b2-40ed-93d0-bb70c90ebbd1/AAABhSXiawI/AAABg8tME_8/16x9-1280/handball-wm-bild-100.jpg"
	path = "https://www.sportschau.de/handball/wm"
	title=py2_encode(title); path=py2_encode(path); img=py2_encode(img);
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'cacheID': '%s'}" %\
		(quote(title), quote(path), quote(img), cacheID)
	addDir(li=li, label=title, action="dirList", dirID="ARDSportCluster", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	title = u"Event: [B]Fußball WM 2022 in Katar[/B]"
	tag = u"Hier finden Sie alle Nachrichten, Berichte, Interviews und Ergebnisse zur FIFA WM 2022 in Katar."
	cacheID = "Sport_WMKatar"
	img = "https://images.sportschau.de/image/a12b67b2-9716-4be8-9462-79391892a4c2/AAABgRPCPcU/AAABgPp7Db4/16x9-1280/wm-katar-logo-sp-100.jpg"
	path = "https://www.sportschau.de/fussball/fifa-wm-2022"
	title=py2_encode(title); path=py2_encode(path); img=py2_encode(img);
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'cacheID': '%s'}" %\
		(quote(title), quote(path), quote(img), cacheID)
	addDir(li=li, label=title, action="dirList", dirID="ARDSportCluster", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	title = u"Event: [B]Radsport: Deutschland Tour[/B]"					# Großevent	
	tag = u"Livestreams, Rennberichte, Analysen, Videos, Ergebnisse zur Deutschland Tour."
	cacheID = "DTOUR"
	img = "http://images.sportschau.de/image/d3108676-9108-4c6f-8746-677eb64b3d2f/AAABgiEMZLA/AAABgPp7Tbc/1x1-640/stimmen-achtzehnte-etappe-106.jpg"
	path = "https://www.sportschau.de/radsport/deutschland-tour/"
	title=py2_encode(title); path=py2_encode(path); img=py2_encode(img);
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'cacheID': '%s'}" %\
		(quote(title), quote(path), quote(img), cacheID)
	addDir(li=li, label=title, action="dirList", dirID="ARDSportCluster", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	title = u"Event: [B]European Championships[/B]"						# Großevent	
	tag = u"Neun Europameisterschaften unter einem Dach - vom 11. bis zum 21. August finden die European Championships in München statt."
	cacheID = "ECS"
	img = "https://images.sportschau.de/image/014165c6-378c-4007-84f8-cc1d6fc3df77/AAABgmeih7M/AAABgPp7Db4/16x9-1280/symbolbild-european-championships-100.jpg"
	path = "https://www.sportschau.de/european-championships"
	title=py2_encode(title); path=py2_encode(path); img=py2_encode(img);
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'cacheID': '%s'}" %\
		(quote(title), quote(path), quote(img), cacheID)
	addDir(li=li, label=title, action="dirList", dirID="ARDSportCluster", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	title = u"Event: [B]Die Finals[/B]"						# Großevent	
	tag = u"14 Sportarten, 190 deutsche Meistertitel - vom 23. bis 26. Juni finden in Berlin die Finals statt."
	cacheID = "Finals"
	img = "https://images.sportschau.de/image/825edf08-5ec7-4c15-9aab-2f6cca8a1d8d/AAABgWF00Tc/AAABgPp7Db4/16x9-1280/titelbild-100.jpg"
	path = "https://www.sportschau.de/die-finals"
	title=py2_encode(title); path=py2_encode(path); img=py2_encode(img);
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'cacheID': '%s'}" %\
		(quote(title), quote(path), quote(img), cacheID)
	addDir(li=li, label=title, action="dirList", dirID="ARDSportCluster", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	title = u"Event: [B]Tour de France[/B]"						# Großevent	
	tag = u"Rennberichte, Analysen, Bilder, Ergebnisse und Wertungen zu allen Etappen der Tour de France 2022."
	cacheID = "Sport_TourdeFrance"
	img = "https://images.sportschau.de/image/4caa92cb-1518-4489-8bec-3b0764c14aa8/AAABgQJrLa8/AAABgPp7Db4/16x9-1280/tour-de-france-bild-102.jpg"
	path = "https://www.sportschau.de/radsport/tourdefrance/index.html"
	title=py2_encode(title); path=py2_encode(path); img=py2_encode(img);
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'cacheID': '%s'}" %\
		(quote(title), quote(path), quote(img), cacheID)
	addDir(li=li, label=title, action="dirList", dirID="ARDSportCluster", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	title = u"Event: [B]TOUR DE FRANCE FEMMES[/B]"				# Großevent	
	tag = u"Rennberichte, Analysen, Bilder, Ergebnisse und Wertungen zu allen Etappen der Tour de France Femmes 2022."
	cacheID = "Sport_FRANCEFEMMES"
	img = "https://images.sportschau.de/image/39c37172-4556-4739-a361-76f7fa50eb9a/AAABghr-8j8/AAABgPp7Db4/16x9-1280/giro-donne-feld-100.jpg"
	path = "https://www.sportschau.de/radsport/tour-de-femmes-100.html"
	title=py2_encode(title); path=py2_encode(path); img=py2_encode(img);
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'cacheID': '%s'}" %\
		(quote(title), quote(path), quote(img), cacheID)
	addDir(li=li, label=title, action="dirList", dirID="ARDSportCluster", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	title = u"Event: [B]Leichtathletik-WM 2022 in Eugene[/B]"	# Großevent	
	tag = u"Erstmals findet eine Leichtathletik-WM in den USA statt. News, TV-Zeiten, Livestreams, Ergebnisse zur Weltmeisterschaft in Oregon."
	cacheID = "Sport_WMEugene"
	img = "https://images.sportschau.de/image/13d0db07-7943-415b-951f-2bfc4be7c8e9/AAABgRYL9Ys/AAABgPp7WOA/20x9-1280/leichtathlet-ryan-crouser-100.webp"
	path = "https://www.sportschau.de/leichtathletik/wm"
	title=py2_encode(title); path=py2_encode(path); img=py2_encode(img);
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'cacheID': '%s'}" %\
		(quote(title), quote(path), quote(img), cacheID)
	addDir(li=li, label=title, action="dirList", dirID="ARDSportCluster", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	title = u"Event: [B]FUSSBALL: EM FRAUEN[/B]"	# Großevent	
	tag = u"16 Mannschaften spielen im Juli in England um den Titel bei der Fußball-EM. News, Livestreams, Spielplan und Ergebnisse zur UEFA-Frauen-EM."
	cacheID = "Sport_WMFrauen"
	img = "https://images.sportschau.de/image/46aa5ce0-ec8d-4d74-8f68-b93052194f5a/AAABgWEbjDs/AAABgPp7Db4/16x9-1280/uefa-frauen-em-2022-logo-100.jpg"
	path = "https://www.sportschau.de/fussball/frauen-em"
	title=py2_encode(title); path=py2_encode(path); img=py2_encode(img);
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'cacheID': '%s'}" %\
		(quote(title), quote(path), quote(img), cacheID)
	addDir(li=li, label=title, action="dirList", dirID="ARDSportCluster", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	

	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	
	
#---------------------------------------------------------------------------------------------------
# Untermenüs Tor des Monats
#	Buttons für weitere Untermenüs, Beiträge der Startseite
# 
def ARDSportMonatstor(title, path, img): 
	PLog("ARDSportMonatstor:")
	path_org=path
	img_org=img
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD')						# Home-Button
	
	title = u"Tor des Monats: [B]%s[/B]" % "Abstimmung"					# Menü Abstimmung
	tag = u"Tor des Monats: Hier gibt's Highlights, Clips und ausgewählte Höhepunkte aus der langen Geschichte dieser Rubrik."
	summ = "Folgebeiträge"
	path = "https://www.sportschau.de/tor-des-monats/abstimmung"
	title=py2_encode(title); path=py2_encode(path); 
	img=py2_encode(img); img_org=py2_encode(img_org); 
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s'}" %\
		(quote(title), quote(path), quote(img))
	addDir(li=li, label=title, action="dirList", dirID="ARDSportMonatstorSingle", fanart=img_org, thumb=img, 
		fparams=fparams, tagline=tag, summary=summ)	
	
	title = u"Tor des Monats: [B]%s[/B]" % "Archiv"						# Menü Archiv
	tag = u"Seit über 40 Jahren wählen die Zuschauer der Sportschau ihr Tor des Monats. Über 500 Treffer sind bereits ausgezeichnet worden. Lassen Sie sich zurückversetzen in die Zeit von Netzer, Beckenbauer und Co. und schauen Sie sich die besten Tore seit 1971 nochmal an - mit vielen Videos."
	summ = "Folgebeiträge"
	path = "https://www.sportschau.de/tor-des-monats/archiv"
	title=py2_encode(title); path=py2_encode(path); 
	img = "https://images.sportschau.de/image/f0d59127-0aa3-4ac0-bf76-2c47cb5ff332/AAABgP4SFF4/AAABgPp7Db4/16x9-1280/tdm70er-sp-104.jpg"
	img=py2_encode(img); img_org=py2_encode(img_org); 
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s'}" %\
		(quote(title), quote(path), quote(img))
	addDir(li=li, label=title, action="dirList", dirID="ARDSportMonatstorSingle", fanart=img_org, thumb=img, 
		fparams=fparams, tagline=tag, summary=summ)	
	
	title = u"Tor des Monats: [B]%s[/B]" % u"DIE BESTEN TORSCHÜTZEN"		# Menü DIE BESTEN TORSCHÜTZEN
	tag = u"In den 70ern war es Gerd Müller, in den 80ern Karl-Heinz-Rummenigge und in den 90ern Jürgen Klinsmann. Sie alle vereint eine besondere Auszeichung: In Ihrer Zeit führten sie die TdM-Rangliste an. 2005 betrat Lukas Podolski die Fußball-Bühne und überholte sie alle."
	summ = "Folgebeiträge"
	path = "https://www.sportschau.de/tor-des-monats/statistikspieler-sp-102.html"
	title=py2_encode(title); path=py2_encode(path); 
	img = "https://images.sportschau.de/image/cab85e31-6758-422c-8848-86684d5de288/AAABgP63Crc/AAABgPp7Db4/16x9-1280/statistikspieler-sp-100.jpg"
	img=py2_encode(img); img_org=py2_encode(img_org); 
	fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s'}" %\
		(quote(title), quote(path), quote(img))
	addDir(li=li, label=title, action="dirList", dirID="ARDSportMonatstorSingle", fanart=img_org, thumb=img, 
		fparams=fparams, tagline=tag, summary=summ)	


	#-----------------------------------------							# Beiträge der Startseite
	page = ARDSportLoadPage(title, path_org, "ARDSportMonatstor")
	if page == '':
		return
	
	cnt = ARDSportMedia(li, title, page)
	if cnt == 0:								# Verbleib in Liste
		return		
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	
	
#---------------------------------------------------------------------------------------------------
# Einzelnes Untermenü zu Tor des Monats
# 
def ARDSportMonatstorSingle(title, path, img): 
	PLog("ARDSportMonatstorSingle:")
	
	li = xbmcgui.ListItem()
	
	page = ARDSportLoadPage(title, path, "")
	if page == '':
		return
	
	base = "https://www.sportschau.de"
	if path.endswith("/abstimmung"):
		li = home(li, ID='ARD')						# Home-Button
		cnt = ARDSportMedia(li, title, page)
	if path.endswith("/archiv") or path.endswith("/statistikspieler-sp-102.html"):	
		items = blockextract('data-v="', page)		# Sliderboxen	
		for item in items:
			ARDSportSlider(li, item, skip_list=[], img='')
	if path.endswith("/statistikspieler-sp-102.html"):
		items = blockextract('class="teaser-xs__link"', page)			
		PLog(len(items))
		for item in items:
			url = base + stringextract('href="', '"', item)
			topline = stringextract('__topline">', '</', item)
			title = stringextract('__headline">', '</', item)	
			summ = stringextract('__shorttext">', '</', item)	
			title=repl_json_chars(title); summ=repl_json_chars(summ);
			title=cleanhtml(title)
			title=title.strip(); summ=summ.strip() 
			title_org=title
			title = "%s: [B]%s[/B]" % (topline, title)		
			img = stringextract('src="', '"', item)
			tag = u"Statistik: %s\n ohne Video, ohne Audio" % title_org
		
			PLog("Satz13_pic:")
			PLog(title); PLog(url); PLog(img); PLog(summ[:80]);
			tag = "weiter zum Beitrag %s" % title
			Plot = summ
			title=py2_encode(title); url=py2_encode(url);
			img=py2_encode(img); Plot=py2_encode(Plot);
			
			fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" % (quote(url), 
				quote(title), quote(img), quote_plus(Plot))
			addDir(li=li, label=title, action="dirList", dirID="ARDSportSliderSingle", fanart=img, thumb=img, 
				fparams=fparams, tagline=tag)			

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	
	
#---------------------------------------------------------------------------------------------------
# Laden + Verteilen
def ARDSportHub(title, path, img, Dict_ID=''): 
	PLog('ARDSportHub: ' + title)
	
	base = "https://www.sportschau.de"
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD')						# Home-Button
	
	if "Moderation" in title:
		page = ARDSportLoadPage(title, path, "ARDSportHub")
		if page == '':
			return
		items = blockextract('class="teaser__link"', page)			
		PLog(len(items))
		for item in items:
			url = stringextract('href="', '"', item)					
			if url.startswith("http") == False:
				url = base + url
				
			topline = stringextract('__topline">', '</', item)	# html-Bereich
			title = stringextract('__headline">', '</', item)	
			summ = stringextract('__shorttext">', '</', item)	
			title=repl_json_chars(title); summ=repl_json_chars(summ);
			title=title.strip(); summ=summ.strip() 
			title = "%s: [B]%s[/B]" % (topline, title)		
				
			tag = "[B]Bilderstrecke[/B]" 
			func = "ARDSportBilder"
			if  item.find(">Bilder<") < 0:
				tag = "[B]ohne weitere Bilder[/B]" 
				func = "dummy"
			img = stringextract('src="', '"', item)
			if img == '':
				img = R(ICON_DIR_FOLDER)
			PLog("Satz12_pic:")
			PLog(title); PLog(url); PLog(img); PLog(summ[:80]);
			fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s'}" % (quote(title), 
				quote(url), quote(img))
			addDir(li=li, label=title, action="dirList", dirID=func, fanart=img, thumb=img, 
				fparams=fparams, tagline=tag, summary=summ)
				
	if "[B]Sliderbox" in title:									# einzelner Sliderbeitrag
		page = ARDSportLoadPage(title, path, "ARDSportHub")
		if page == '':
			return
		PLog("slider_from_Dict")
		teaser = Dict("load", Dict_ID)
		skip_list = []; cnt=0
		skip_list = ARDSportSlider(li, teaser, skip_list, img)		# -> addDir			
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
#---------------------------------------------------------------------------------------------------
# Notification: keine Aktion
# verhindert nicht GetDirectory-Error 
def dummy(title="",path="",img=""):
	PLog("dummy:")
	icon = R(ICON_INFO)
	msg1 = "Hinweis:"
	msg2 = 'Button ohne Funktion'		
	xbmcgui.Dialog().notification(msg1,msg2,icon,2000, sound=False)
	return

#---------------------------------------------------------------------------------------------------
# Webseite für Funktion func laden 
# falls cacheID leer, wird sie letztes path-Element (eindeutig!)
#
def ARDSportLoadPage(title, path, func, cacheID=""): 
	PLog('ARDSportLoadPage:')
	PLog('func: ' + func)
	CacheTime = 60*5							# 5 min.
	
	if cacheID == "":
		p = path.split("/")[-1]
		cacheID = "ARDSport_%s" % p
	
	page = Dict("load", cacheID, CacheTime=CacheTime)
	page=''
	if page == False or page == '':								# Cache miss od. leer - vom Sender holen
		page, msg = get_page(path=path)
		if page:
			Dict("store", cacheID, page) 						# Seite -> Cache: aktualisieren	
	if page == '':
		msg1 = "Fehler in %s" % func
		msg2 = 'Seite kann nicht geladen werden.'
		msg3 = msg
		MyDialog(msg1, msg2, msg3)
	
	return page	

##---------------------------------------------------------------------------------------------------
# Großevent der Sportschau
# 1. Aufruf: ARDSportWDR
# 2. Aufruf: ARDSportCluster mit cluster (class="trenner") 
# 24.06.2022 Rückfall-Adresse www.sportschau.de - bei Großevents
#	verlegt der WDR die Ankündigunsseite auf die Startseite
#
def ARDSportCluster(title, path, img, cacheID, cluster=''): 
	PLog('ARDSportCluster: ' + cluster)
	
	new_url, msg = get_page(path=path, GetOnlyRedirect=True)
	if new_url == '':
		path = "https://www.sportschau.de/"
	
	page = ARDSportLoadPage(title, path, "ARDSportCluster")
	if page == '':
		return

	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Neu')								# Home-Button
	
	trenner = 'class="trenner__text">'
	items = blockextract(trenner, page)
	PLog(len(items))
	#-----------------------------------------------			# 1. Durchlauf
	if cluster == '':
		PLog("stage1")
		#------------------
		teaser = blockextract('class="teaser-slider', page)		# vor Cluster: Slider gesamte Seite auswerten	
		PLog(len(teaser))
		if len(teaser) > 0:
			cnt=1
			for item in teaser:
				Dict_ID = "ARDSportSlider_%d" % cnt
				Dict("store", Dict_ID, item)
				title = "[B]Sliderbox %d[/B]" % cnt
				tag = u"Folgeseiten"
				title=py2_encode(title); path=py2_encode(path); 
				img=py2_encode(img); 
				fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'Dict_ID': '%s'}" %\
					(quote(title), quote(path), quote(img), Dict_ID)
				addDir(li=li, label=title, action="dirList", dirID="ARDSportHub", fanart=img, thumb=img, 
					fparams=fparams, tagline=tag)	
				cnt=cnt+1
		#------------------
		for item in items:
			tag=''
			title = stringextract('__headline">', '</', item)
			title_org = title
			topline = stringextract('__topline">', '</', item)
			topline = topline.strip()

			PLog("title: " + title)								# wie stage2
			title = cleanhtml(title); title = title.strip()
			title = unescape(title); title = repl_json_chars(title)
			
			tag = "[B]%s[/B]" % topline
			tag = "%s\nFolgeseiten" % tag
			tag = unescape(tag); 
			
			title=py2_encode(title); path=py2_encode(path); 
			img=py2_encode(img); cluster=py2_encode(cluster);
			fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s', 'cacheID': '%s', 'cluster': '%s'}" %\
				(quote(title), quote(path), quote(img), cacheID, quote(title))
			addDir(li=li, label=title, action="dirList", dirID="ARDSportCluster", fanart=img, thumb=img, 
				fparams=fparams, tagline=tag)
			
	#-----------------------------------------------			# 2. Durchlauf
	else:
		PLog("stage2")
		headline = ">%s<" % cluster
		PLog("headline: " + headline)
		for item in items:
			found=False
			title = stringextract('__headline">', '</', item)
			title = cleanhtml(title); title = title.strip()
			title = unescape(title); title = repl_json_chars(title)
			
			if title in headline:
				PLog("found_cluster: " + headline)
				found=True
				page = item										# Cluster -> page
				break
		if found:
			cnt = ARDSportMedia(li, title, page)
			if cnt == 0:										# Verbleib in Liste
				return		
		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	

#---------------------------------------------------------------------------------------------------
# Livestreams der Sportschau
# Aufruf: ARDSportWDR
#
def ARDSportLive(title): 
	PLog('ARDSportLive:')

	path = "https://www.sportschau.de/streams"
	page = ARDSportLoadPage(title, path, "ARDSportLive")
	if page == '':
		return

	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Neu')								# Home-Button
	
	cnt = ARDSportMedia(li, title, page)
	if cnt == 0:											# Verbleib in Liste
		return		
		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#----------------------------------------------------------------
# aktuelle LIVESTREAMS + Netcast-Audiostreams-Liste von sportschau.de
# Aufrufer: ARDAudioEventStreams
# aktuelle Livestreams: ../audio/index.html
# Alle Netcast-Streams: ../sportimradio/audiostream-netcast-uebersicht-100.html
# ab Juni 2022 beide Webseiten ähnlich
def ARDSportAudioStreams(title, path, img, cacheID):
	PLog('ARDSportAudioStreams:')
	
	page = ARDSportLoadPage(title, path, "ARDSportAudioStreams", cacheID)
	if page == '':
		return
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD')						# Home-Button
	
	cnt = ARDSportMedia(li, title, page)
	if cnt == 0:												# Verbleib in Liste
		return		
		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#---------------------------------------------------------------------------------------------------
# Auswertung mediaplayer-Klassen (quoted:data-v=..)
# Aufrufer ARDSportAudioStreams, ARDSportLive, ARDSportCluster
# Externe Links im html-Code (z.B. NDR, Pferdesport) sind nicht mit 
#	Streamquellen im mediaplayer hinterlegt
# Slider-Auswertung extern für gesamte Seite (hier page=cluster möglich) 
#
def ARDSportMedia(li, title, page): 
	PLog('ARDSportMedia: ' + title)
	base = "https://www.sportschau.de"

	teaser_xs=[]; teaser_slider=[]
	if "Livestreams" in title:
		teaser = blockextract('class="teaser__media"', page)
	elif "Audiostreams" in title:	
		teaser = blockextract('class="mediaplayer', page)
	else:
		teaser = blockextract('class="teaser__media"', page)
		teaser = teaser + blockextract('class="teaser__link"', page,)			
		teaser_xs = blockextract('class="teaser-xs__link"', page)
		
	PLog(len(teaser))
	PLog(len(teaser_xs))
	items = teaser + teaser_xs
	if len(items) == 0:
		icon = R("ard-sportschau.png")
		msg1 = u"%s:" % title
		msg2 = u'keine Videos/Audios/Bilder gefunden'
		xbmcgui.Dialog().notification(msg1,msg2,icon,2000,sound=True)
		return 0 
				
	mediatype=''			
		
	# json.loads scheiterte in cont (char 360) - vermutl. vergessenes Komma:
	cnt=0; skip_list=["dummy"]
	for item in items:		
		player=''; live=False; title='';  mp3_url=''; stream_url=''; 
		img=''; tag=''; summ=''; Plot=''; player="text"
		PLog(item[:60])
		
		topline = stringextract('__topline">', '</', item)
		title = stringextract('__headline">', '</', item)	# html-Bereich
		summ = stringextract('__shorttext">', '</', item)	# html-Bereich, fehlt im json-Bereich
		summ=cleanhtml(summ)
		title=title.replace('"', ''); title=mystrip(title)
		title=cleanhtml(title)
		title=repl_json_chars(title); summ=repl_json_chars(summ);
		title=title.strip(); summ=summ.strip() 
		
		if topline:
			summ = "[B]%s[/B]\n%s" % (topline, summ)	
		title_html=title									# Altern. für ARDSportMediaPlayer		
		summ_html=summ										# dto.	

		#---------------------------------------------------
		if item.find('_topline">Bilderstrecke<') >= 0:		# Ausleitung Bildgalerie
			if item.startswith('class="teaser__link'):
				player = "pics"
				url = stringextract('href="', '"', item)
				skip_list.append(url)
				if url.startswith("http") == False:
					url = base + url
			
				tag = "[B]Bilderstrecke[/B]" 
				img = stringextract('src="', '"', item)
				PLog("Satz12_pic:")
				PLog(title); PLog(url); PLog(img); PLog(summ[:80]);
				fparams="&fparams={'title': '%s', 'path': '%s', 'img': '%s'}" % (quote(title), 
					quote(url), quote(img))
				addDir(li=li, label=title, action="dirList", dirID="ARDSportBilder", fanart=img, thumb=img, 
					fparams=fparams, tagline=tag, summary=summ)
				continue	
		#---------------------------------------------------
		
		if item.find('class="mediaplayer') > 0:
			if player != "pics":
				data  = stringextract('class="mediaplayer', '"MediaPlayer', item) # von slider abgrenzen
				if data:
					player,live,title,mp3_url,stream_url,img,tag,summ,Plot = ARDSportMediaPlayer(li, data)
					title=repl_json_chars(title)

		if len(summ_html) > len(summ):						# Alternative
			summ = summ_html
		if len(title_html) > len(title_html):				# Alternative
			title = title_html
		
		if title in skip_list:								# Doppel in Blöcken möglich
			continue
		skip_list.append(title)
				
		PLog("Satz12:")
		PLog(player); PLog(live); PLog(title); PLog(mp3_url); PLog(stream_url);   
		PLog(img); PLog(summ[:80]);
		title=py2_encode(title); mp3_url=py2_encode(mp3_url); img=py2_encode(img);
		tag=py2_encode(tag); Plot=py2_encode(Plot);
		
		if player == "audio":
			if live:														# netcast Livestream
				fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" % (quote(mp3_url), 
					quote(title), quote(img), quote_plus(Plot))
				addDir(li=li, label=title, action="dirList", dirID="PlayAudio", fanart=img, thumb=img, fparams=fparams, 
					tagline=tag, mediatype='music')	
			else:															# Konserve
				ID="ARD"													# ID Home-Button
				fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'ID': '%s'}" % (quote(mp3_url), 
					quote(title), quote(img), quote_plus(Plot), ID)
				addDir(li=li, label=title, action="dirList", dirID="AudioPlayMP3", fanart=img, thumb=img, 
					fparams=fparams, tagline=tag, summary=summ)
		if player == "video":
			fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" % (quote(stream_url), 
				quote(title), quote(img), quote_plus(Plot))
			addDir(li=li, label=title, action="dirList", dirID="PlayVideo", fanart=img, thumb=img, fparams=fparams, 
				tagline=tag, summary=summ, mediatype='mediatype')	
		
		if player == "text":												# Textbeiträge, Verbleib in Liste
			if item.find('__headline"') < 0:								# Kombi-Satz aus 2 Blöcken mögl.
				continue
				
			img = stringextract('src="', '"', item)
			label = stringextract("<strong>", "</strong>", item)
			if "Audio" in label or "Podcast" in label or "Video" in label:	# ähnlich ARDSportSlider
				url = stringextract('href="', '"', item)
				if url.startswith("http") == False:
					url = base + url
				PLog("Satz12_xslink: %s, %s" % (title,url))
				title=py2_encode(title); url=py2_encode(url);
				img=py2_encode(img); Plot=py2_encode(Plot);
				tag = "weiter zum [B]%s[/B]-Beitrag" % label
				fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" % (quote(url), 
					quote(title), quote(img), quote_plus(Plot))
				addDir(li=li, label=title, action="dirList", dirID="ARDSportSliderSingle", fanart=img, thumb=img, fparams=fparams, 
					tagline=tag, summary=summ)			
			else:
				if img == "":													# kann fehlen
					img = R(ICON_DIR_FOLDER) 								
				tag = "[B]ohne Videos, Audios, Bilder[/B]\nMehr auf sportschau.de.."
				title = "[COLOR grey]%s[/COLOR]" % title
				PLog("Satz12_text: %s" % title)
				fparams="&fparams={}" 
				addDir(li=li, label=title, action="dirList", dirID="dummy", fanart=img, thumb=img, fparams=fparams, 
					tagline=tag, summary=Plot)				
			
		cnt = cnt + 1
	
	return cnt

#----------------------------------------------------------------
# Auswertung Mediaplayerdaten
# 24.07.2022 Anpassung für Tor des Monats ("video/mp4" in url)
#
def ARDSportMediaPlayer(li, item): 
	PLog('ARDSportMediaPlayer:')
	player=''; live=False; title='';  mp3_url=''; stream_url=''; 
	img=''; tag=''; summ=''; Plot='';
	
	cont = stringextract('data-v="', '"', item)				# json-Inhalt zum Player
	cont = decode_url(cont)
	cont = unescape(cont)
	cont = (cont.replace('\\"','*').replace('<strong>','[B]').replace('</strong>','[/B]'))
	PLog(cont[:30])

	player = stringextract('playerType":"', '"', cont)		# audio, video
	media = stringextract('streams":', '"meta"', cont)		# für video dash.mpd, m3u8 + ts
	PLog("media: " + media[:60]); 
	if player == "audio":
		mp3_url = stringextract('url":"', '"', media)		# 1 x mp3
	else:
		urls = blockextract('url":', media)
		for url in urls:									# erste: höchste Auflösung
			if "index.m3u8" in url or "master.m3u8" in url or "video/mp4" in url:
				stream_url = stringextract('url":"', '"', url)
				break
	
	title = stringextract('page_title":"', ',"', cont)		# kann " enthalten
	title=decode_url(title); title=repl_json_chars(title); 
	
	duration = stringextract('durationSeconds":"', '"', cont)
	if duration == '':
		dur = stringextract('content_duration":', ',', cont) # Altern. außerhalb media (int, milli-secs)
		PLog("dur_raw: " + dur)
		try:
			dur = int(dur)
			duration = str(int(dur / 1000))
		except:
			duration=""
	PLog("duration: " + duration); 
	duration = seconds_translate(duration)
		
	imgs = blockextract('"minWidth":', cont, "}")
	if len(imgs) > 0:
		img = stringextract('value":"', '"', imgs[-1])			# letztes=größtes
	mode = stringextract('_broadcasting_type":"', '"', cont)
	if mode == "live":
		live=True
	
	TimeDate=''; tag='';

	if duration:
		if duration == "0 sec":
			duration = "unbekannt"
		
	avail = stringextract('av_original_air_time":"', '"', cont)
	if avail:
		verf = time_translate(avail, day_warn=True)
	
	chapter = stringextract('chapter1":"', '"', cont)
	creator = stringextract('creator":"', '"', cont)
	genre = stringextract('_genre":"', '"', cont)
	geo = stringextract('languageCode":"', '"', cont)
	if geo:
		geo = "Geoblock: %s" % up_low(geo)
	else:
		geo = "Geoblock: NEIN"
	
	if player == "audio":
		tag = "Audio"
	else:
		tag = "Video"
	if live:
		tag = "%s-Livestream" % tag
	tag = "[B]%s[/B]" % tag
	PLog("duration: " + duration)
	if live == False and duration:
		tag = "%s | Dauer %s" % (tag, duration)
	if verf:
		tag = u"%s | Verfügbar ab [B]%s[/B]" % (tag, verf)	
		
	tag = "%s\n%s | %s | %s | %s" % (tag, chapter, creator, genre, geo)

	if summ:
		tag = "%s\n\n%s" % (tag, summ)
	Plot = tag.replace("\n", "||")
	
	PLog("Satz31:")
	PLog(player); PLog(live); PLog(title); PLog(mp3_url); PLog(stream_url); PLog(avail);
		
	return player, live, title, mp3_url, stream_url, img, tag, summ, Plot 

#---------------------------------------------------------------------------------------------------
# Für Seiten mit nur einheitliche Blöcken
# Aufrufer: ARDAudioEventStreams (Audiostreams, Netcast-Audiostreams) 
# bisher nur Blöcke class="mediaplayer
def ARDSportSingleBlock(title, path, img, cacheID, block):
	PLog('ARDSportSingleBlock:')
	
	page = ARDSportLoadPage(title, path, "ARDSportSingleBlock", cacheID)
	if page == '':
		return
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD')						# Home-Button
	
	block = block.replace("*", '"')
	
	teaser = blockextract(block, page)
	PLog(len(teaser))
	
	for item in teaser:
		data  = stringextract('class="mediaplayer', '"MediaPlayer', item) # Ende: MediaPlayer, MediaPlayerInlinePlay
		PLog(data[:60])
		if data:
			player,live,title,mp3_url,stream_url,img,tag,summ,Plot = ARDSportMediaPlayer(li, data)
			PLog("Satz12_single:")
			PLog(player); PLog(live); PLog(title); PLog(mp3_url); PLog(stream_url);   
			PLog(img); PLog(summ[:80]);
			title=py2_encode(title); mp3_url=py2_encode(mp3_url); img=py2_encode(img);
			tag=py2_encode(tag); Plot=py2_encode(Plot);
			
			if player == "audio":												# bei Bedarf für Video ergänzen
				if live:														# netcast Livestream
					fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" % (quote(mp3_url), 
						quote(title), quote(img), quote_plus(Plot))
					addDir(li=li, label=title, action="dirList", dirID="PlayAudio", fanart=img, thumb=img, fparams=fparams, 
						tagline=tag, mediatype='music')	
				else:															# Konserve
					ID="ARD"													# ID Home-Button
					fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'ID': '%s'}" % (quote(mp3_url), 
						quote(title), quote(img), quote_plus(Plot), ID)
					addDir(li=li, label=title, action="dirList", dirID="AudioPlayMP3", fanart=img, thumb=img, 
						fparams=fparams, tagline=tag)
						
	#--------------------														# Abschluss: Slider auswerten	
	teaser = blockextract('class="teaser-slider', page)
	PLog(len(teaser))
	skip_list = []
	for item in teaser:
		skip_list = ARDSportSlider(li, item, skip_list)		# -> addDir	
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#----------------------------------------------------------------
# Auswertung Slider-Beiträge mit json-Bereich
#
def ARDSportSlider(li, item, skip_list, img=''): 
	PLog('ARDSportSlider:')
	base = "https://www.sportschau.de"
	player=''; live=False; title='';  mp3_url=''; stream_url=''; 
	img=''; tag=''; summ=''; Plot='';
	
	cont = stringextract('data-v="', '"', item)				# json-Inhalt zum Player
	cont = decode_url(cont)
	cont = unescape(cont)
	cont = (cont.replace('\\"','*').replace('<strong>','[B]').replace('</strong>','[/B]'))
	PLog(cont[:80])
		
	content = blockextract('"teaserUrl"', cont)
	PLog(len(content))
	#PLog(content)	# Debug
	
	allow_list = ["AUDIO", "VIDEO", "PODCAST",			# Web: groß-/klein-Mix
				"LIVESTREAM"]
	for rec in 	content:
		label = stringextract('label":"', '"', rec)		# audio, video, podcast

		url = stringextract('teaserUrl":"', '"', rec)
		if url.startswith('http') == False:
			url = base + url
		topline = stringextract('topline":"', '"', rec)
		title = stringextract('headline":"', '"', rec)
		if title in skip_list:
			PLog("skip_title: " + title)
			continue
		skip_list.append(title)
		
		img = stringextract('imageUrl":"', '"', rec)
		if img == '':
			pos = rec.find('minWidth":640')				# Altern. minWidth 256 - 960
			if pos > 0:
				img = stringextract('value":"', '"', rec[pos:])
		alt = stringextract('alttext":"', '"', rec)
		cr = stringextract('copyright":"', '"', rec)
		
		summ = "[B]%s[/B] | %s | %s "  % (topline, alt, cr)
	
		allow=False; live=False
		for item in allow_list:							# Abgleich label-Typen
			if item in up_low(label) or '"Tor des Monats' in rec: # Tor des Monats Sätze ohne label
				if "LIVESTREAM" in item:
					live=True
				allow=True; break				
				
		PLog("Satz12_slider:")
		PLog(title); PLog(label); PLog(allow); PLog(topline);
		PLog(url); PLog(img);PLog(alt);PLog(cr);
		title=py2_encode(title); url=py2_encode(url);
		img=py2_encode(img); Plot=py2_encode(Plot);
		
		if allow:
			tag = "weiter zum [B]%s[/B]-Beitrag" % label
			if live:
				tag = tag.replace("-Beitrag", "")
			fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" % (quote(url), 
				quote(title), quote(img), quote_plus(Plot))
			addDir(li=li, label=title, action="dirList", dirID="ARDSportSliderSingle", fanart=img, thumb=img, fparams=fparams, 
				tagline=tag)			
		else:											# nur Textinhalte
			tag = "[B]ohne Videos, Audios, Bilder[/B]\nMehr auf sportschau.de.."
			title = "[COLOR grey]%s[/COLOR]" % title
			PLog("Satz12_slider_text: %s" % title)
			fparams="&fparams={}" 
			addDir(li=li, label=title, action="dirList", dirID="dummy", fanart=img, thumb=img, fparams=fparams, 
				tagline=tag, summary=summ)				
		
	return skip_list

#----------------------------------------------------------------
# einzelner Slider für ARDSportSlider
# 24.07.2022 Anpassung für Tor des Monats (mehrere mediaplayer-Sätze)
#	
def ARDSportSliderSingle(url, title, thumb, Plot, firstblock=False): 
	PLog('ARDSportSliderSingle: ' + title)
	PLog(url); PLog(firstblock);
	cacheID=url.split("/")[-1]

	page = ARDSportLoadPage(title, url, "ARDSportSliderSingle", cacheID)
	if page == '':
		return

	li = xbmcgui.ListItem()
	li = home(li, ID='ARD')						# Home-Button
	
	base = "https://www.sportschau.de"
	mediatype=""
	items=[]
	if "/tor-des-monats/" in url:				# mehrere Beiträge "Tore des Monats"
		items = blockextract('class="mediaplayer', page, '"MediaPlayer"')
		PLog("mediaplayer_items: %d" % len(items))
		if len(items) == 0:						# Beiträge erst auf Folgeseiten
			items = blockextract('<div class="teaser__media">', page)
			PLog("teaserlink_items: %d" % len(items))
			base = "https://www.sportschau.de"
			for item in items:
				if item.find('"teaser__link"') < 0:
					continue

				url = base + stringextract('href="', '"', item)
				img = stringextract('src="', '"', item)
				if img == '':
					img = thumb
				topline = stringextract('__topline">', '</', item)
				title = stringextract('__headline">', '</', item)
				if title == '':
					continue	
				summ = stringextract('__shorttext">', '</', item)	
				title=repl_json_chars(title); summ=repl_json_chars(summ);
				title=cleanhtml(title)
				title=title.strip(); summ=summ.strip() 
				tag = "[B]%s[/B]" % topline
					
				PLog("Satz32:")
				PLog(title); PLog(url);
				url=py2_encode(url); title=py2_encode(title); 
				thumb=py2_encode(thumb); Plot=py2_encode(Plot);
				fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'firstblock': 'True'}" %\
					(quote(url), quote(title), quote(thumb), quote_plus(Plot), )
				addDir(li=li, label=title, action="dirList", dirID="ARDSportSliderSingle", fanart=thumb, thumb=img, 
					fparams=fparams, tagline=tag, summary=summ)		
			xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
			return									# erford. für Abschluss
		else:						
			if firstblock:
				if 'leider nicht im Internet' in page:
					icon = R(ICON_INFO)
					msg1 = u"Beitrag gesperrt"
					msg2 = u"im Internet nicht verfügbar"
					xbmcgui.Dialog().notification(msg1,msg2,icon,2000, sound=False)
					PLog(msg2)
					return
				PLog("firstblock: " + str(items[:1])[:60] )
				items = items[:1]					# nur 1. Block verwenden
			
	else:	
		item = stringextract('class="mediaplayer', '"MediaPlayer"', page)	# erster json-Bereich
		items.append(item) 
		
	if len(items) == 0:							# z.B. Verweis auf https://www.zdf.de/live-tv
		icon = R("ard-sportschau.png")
		msg1 = u"%s:" % title
		msg2 = u'Quelle nicht gefunden/verfügbar'
		xbmcgui.Dialog().notification(msg1,msg2,icon,2000,sound=True)
		return 0 
	
	PLog("Slideritems: %d" % len(items))
	for item in items:
		PLog(item[:80])
		if item.find('data-v="') < 0:			# Playerdaten auf Folgeseite?
			PLog("follow_up:")
			path = base + stringextract('href="', '"', item)
			page, msg = get_page(path)
			item = stringextract('class="mediaplayer', '"MediaPlayer"', page)
			PLog(item[:60])	
		if item.find('data-v="') > 0:	
			player,live,title,mp3_url,stream_url,img,tag,summ,Plot = ARDSportMediaPlayer(li, item)
		else:
			PLog('no_data-v')
			continue
		
		if player == "audio":
			ID="ARD"													# ID Home-Button
			fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'ID': '%s'}" % (quote(mp3_url), 
				quote(title), quote(img), quote_plus(Plot), ID)
			addDir(li=li, label=title, action="dirList", dirID="AudioPlayMP3", fanart=img, thumb=img, 
				fparams=fparams, tagline=tag)
		if player == "video":
			fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" % (quote(stream_url), 
				quote(title), quote(img), quote_plus(Plot))
			addDir(li=li, label=title, action="dirList", dirID="PlayVideo", fanart=img, thumb=img, fparams=fparams, 
				tagline=tag, mediatype='mediatype')	
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

# ---------------------------------------- Ende ARD Sportschau.de ---------------------------------
####################################################################################################
# Aufrufer: Main
def SearchUpdate(title):		
	PLog('SearchUpdate:')
	li = xbmcgui.ListItem()

	ret = updater.update_available(VERSION)	
	#PLog(ret)
	if ret[0] == False:		
		msg1 = 'Updater: Github-Problem'
		msg2 = 'update_available: False'
		PLog("%s | %s" % (msg1, msg2))
		MyDialog(msg1, msg2, '')
		return li			

	int_lv = ret[0]			# Version Github
	int_lc = ret[1]			# Version aktuell
	latest_version = ret[2]	# Version Github, Format 1.4.1
	
	summ = ret[3]			# Changes, cleanSummary: "\n" -> "|"  
	tag = ret[4]			# tag, Bsp. 029
	
	# Bsp.: https://github.com/rols1/Kodi-Addon-ARDundZDF/releases/download/0.5.4/Kodi-Addon-ARDundZDF.zip
	url = 'https://github.com/{0}/releases/download/{1}/{2}.zip'.format(GITHUB_REPOSITORY, latest_version, REPO_NAME)
	PLog(int_lv); PLog(int_lc); PLog(latest_version); PLog(summ);  PLog(url);
	
	if int_lv > int_lc:		# zum Testen drehen (akt. Addon vorher sichern!)			
		title = 'Update vorhanden - jetzt installieren'
		summary = 'Addon aktuell: ' + VERSION + ', neu auf Github: ' + latest_version
		PLog(type(summary));PLog(type(latest_version));

		tagline = cleanhtml(summ)
		thumb = R(ICON_UPDATER_NEW)
		url=py2_encode(url);
		fparams="&fparams={'url': '%s', 'ver': '%s'}" % (quote_plus(url), latest_version) 
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.updater.update", 
			fanart=R(ICON_UPDATER_NEW), thumb=R(ICON_UPDATER_NEW), fparams=fparams, summary=summary, 
			tagline=summ)
			
		title = 'Update abbrechen'
		summary = 'weiter im aktuellen Addon'
		thumb = R(ICON_UPDATER_NEW)
		fparams="&fparams={}"
		addDir(li=li, label=title, action="dirList", dirID="Main", fanart=R(ICON_UPDATER_NEW), 
			thumb=R(ICON_UPDATER_NEW), fparams=fparams, summary=summary)
	else:	
		title = 'Addon ist aktuell | weiter zum aktuellen Addon'
		summary = 'Addon Version ' + VERSION + ' ist aktuell (kein Update vorhanden)'
		summ = summ[:200]				# begrenzen
		tagline = "%s.. | Mehr in changelog.txt" % summ
		thumb = R(ICON_OK)
		fparams="&fparams={}"
		addDir(li=li, label=title, action="dirList", dirID="Main", fanart=R(ICON_OK), 
			thumb=R(ICON_OK), fparams=fparams, summary=summary, tagline=tagline)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
	
####################################################################################################
#							beta.ardmediathek.de / www.ardmediathek.de
#
#					zusätzliche Funktionen für die Betaphase ab Sept. 2018
#					ab Jan 2019 wg. Scrollfunktion haupts. Nutzung der Classic-Version
#					ab April 2019 hier allein Classic-Version - Neu-Version als Modul
#					ab Juni 2021 nach Wegfall Classic hier entfernt: ARDStart, ARDStartRubrik,
#						SendungenAZ, SearchARDundZDF, Search (ARD Classic + Podcast Classic), -
#						gesamt s. changelog.txt.
#						
####################################################################################################

#----------------------------------------------------------------  
# Vorstufe von Search - nur in Kodi-Version.
#	blendet Tastatur ein und fragt Suchwort(e) ab.
#	
def get_query(channel='ARD'):
	PLog('get_query:'); PLog(channel)
	query = get_keyboard_input()			# Modul util
	if  query == None or query.strip() == '':
		return ""
	
	if channel == 'ARD' or channel == 'ARDundZDF':				
		if '|' in query:		# wir brauchen | als Parameter-Trenner in SinglePage
			msg1 = 'unerlaubtes Zeichen in Suchwort: |'
			MyDialog(msg1, '', '')
			return ""
				
		query_ard = query.strip()
		query_ard = query_ard.replace(' ', '+')	# Leer-Trennung = UND-Verknüpfung bei Podcast-Suche 
		
	if channel == 'ZDF' or channel == 'ARDundZDF':				
		query_zdf =query.strip()					# ZDF-Suche
		query_zdf = query_zdf.replace(' ', '+')		# Leer-Trennung bei ZDF-Suche mit +
		
	if channel == 'ARD':	
		return 	query_ard
	if channel == 'ZDF':	
		return 	query_zdf
	if channel == 'ARDundZDF':						# beide queries zusammengesetzt				
		query = "%s|%s" % (query_ard, query_zdf)							
		PLog('query_ARDundZDF: %s' % query);
		return	query
	if channel=='ARD Audiothek' or channel=='phoenix':	# nur strip, quoting durch Aufrufer
		return 	query.strip()
			
#---------------------------------------------------------------- 
#  Search_refugee - erforderlich für Refugee Radio (WDR) - nur
#		Podcasts Classics - 03.06.2021  entfernt
#---------------------------------------------------------------- 

####################################################################################################
# 03.06.2021 entfernt (Classic-Version eingestellt): PODMore							
####################################################################################################

def PodFavoritenListe(title, offset=0):
	PLog('PodFavoritenListe:'); 
	
	title_org = title
	# Default fname: podcast-favorits.txt im Ressourcenverz.
	#	Alternative: Pfad zur persönlichen Datei 
	fname =  SETTINGS.getSetting('pref_podcast_favorits')
	PLog(fname)
	if os.path.isfile(fname) == False:
		PLog('persoenliche Datei %s nicht gefunden' % fname)					
		Inhalt = RLoad(FAVORITS_Pod)		# Default-Datei
	else:										
		try:
			Inhalt = RLoad(fname,abs_path=True)	# pers. Datei verwenden (Name ebenfalls podcast-favorits.txt)	
		except:
			Inhalt = ''
		
	if  Inhalt is None or Inhalt == '' or 'podcast-favorits.txt' not in Inhalt:				
		msg1='Datei podcast-favorits.txt nicht gefunden, nicht lesbar oder falsche Datei.'
		msg2='Bitte Einstellungen prüfen.'
		MyDialog(msg1, msg2, '')
		return
							
	# PLog(Inhalt) 
	bookmarks = []
	lines = Inhalt.splitlines()
	for line in lines:								# skip Kommentarzeilen + Leerzeilen 
		if line.startswith('#'):			
			continue
		if line.strip() == '':		
			continue
		bookmarks.append(line)
		
	rec_per_page = 20								# Anzahl pro Seite
	max_len = len(bookmarks)						# Anzahl Sätze gesamt
	start_cnt = int(offset) 						# Startzahl diese Seite
	end_cnt = int(start_cnt) + int(rec_per_page)	# Endzahl diese Seite
				
	title2 = 'Favoriten %s - %s (%s)' % (start_cnt+1, min(end_cnt,max_len) , max_len)
	li = xbmcgui.ListItem()
	li = home(li,ID='ARD Audiothek')				# Home-Button

	for i in range(len(bookmarks)):
		cnt = int(i) + int(offset)
		# PLog(cnt); PLog(i)
		if int(cnt) >= max_len:				# Gesamtzahl überschritten?
			break
		if i >= rec_per_page:				# Anzahl pro Seite überschritten?
			break
		line = bookmarks[cnt]
		try:		
			title = line.split('|')[0]	
			path = line.split('|')[1]
			title = title.strip(); 
			path = path.strip() 
		except:
			title=''; path=''
		PLog(title); PLog(path)
		if path == '':						# ohne Link kein verwertbarer Favorit
			continue
			
		
		title=title.replace('\'', '')		# z.B. "Stimmt's? - NDR2"
		title=title.replace('&', 'plus')	# &=Trenner für Parameter in router
		PLog(title); PLog(path)
		title=py2_encode(title); path=py2_encode(path);
		
		if path.startswith('http'):			# Server-Url
			summary='Favoriten: ' + title
			fparams="&fparams={'title': '%s', 'path': '%s'}" % \
				(quote(title), quote(path))
			addDir(li=li, label=title, action="dirList", dirID="resources.lib.Podcontent.PodFavoriten", 
				fanart=R(ICON_STAR), thumb=R(ICON_STAR), fparams=fparams, summary=path, 
				tagline=summary)
		else:								# lokales Verz./Share?
			fparams="&fparams={'title': '%s', 'path': '%s'}" % \
				(quote(title), quote(path))
			addDir(li=li, label=title, action="dirList", dirID="resources.lib.Podcontent.PodFolder", 
				fanart=R(ICON_NOTE), thumb=R(ICON_DIR_FOLDER), fparams=fparams, summary=path, 
				tagline=title)		
			
					
	# Mehr Seiten anzeigen:
	PLog(offset); PLog(cnt); PLog(max_len);
	if (int(cnt) +1) < int(max_len): 						# Gesamtzahl noch nicht ereicht?
		new_offset = cnt + int(offset)
		PLog(new_offset)
		summ = 'Mehr (insgesamt ' + str(max_len) + ' Favoriten)'
		title_org=py2_encode(title_org);
		fparams="&fparams={'title': '%s', 'offset': '%s'}" % (quote(title_org), new_offset)
		addDir(li=li, label=summ, action="dirList", dirID="PodFavoritenListe", fanart=R(ICON_MEHR), 
			thumb=R(ICON_MEHR), fparams=fparams, summary=title_org, tagline='Favoriten')

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
####################################################################################################
# 03.06.2021 Classic-Funktionen entfernt: BarriereArmARD, PageControl, SinglePage,
#	SingleSendung
####################################################################################################

#-----------------------
# test_downloads: prüft ob curl/wget-Downloads freigeschaltet sind + erstellt den Downloadbutton
# high (int): Index für einzelne + höchste Video-Qualität in download_list
# 04.01.2021 Anpassung Trennz. Stream_List (Bsp. Parseplaylist, StreamsShow)
# 23.04.2021 Durchreichen von sub_path (Untertitel), leer für mp3-files
def test_downloads(li,download_list,title_org,summary_org,tagline_org,thumb,high, sub_path=''):  
	PLog('test_downloads:')
	PLog('summary_org: ' + summary_org)
	PLog('title_org: ' + title_org)
	PLog('tagline_org: ' + tagline_org)

	PLog(SETTINGS.getSetting('pref_use_downloads')) 			# Voreinstellung: False 
	if check_Setting('pref_use_downloads') == False:			# einschl. Test Downloadverzeichnis
		return
			
	if SETTINGS.getSetting('pref_show_qualities') == 'false':	# nur 1 (höchste) Qualität verwenden
		download_items = get_bestdownload(download_list)
	else:	
		download_items = download_list							# ganze Liste verwenden
	# PLog(download_items)
		
	i=0
	for item in download_items:
		PLog(item)
		item = item.replace('**', '|')							# 04.01.2021 Korrek. Trennz. Stream_List
		quality,url = item.split('#')
		PLog(url); PLog(quality); PLog(title_org)
		if url.find('.m3u8') == -1 and url.find('rtmp://') == -1:
			# detailtxt =  Begleitdatei mit Textinfos zum Video / Podcast:				
			detailtxt = MakeDetailText(title=title_org,thumb=thumb,quality=quality,
				summary=summary_org,tagline=tagline_org,url=url)
			v = 'detailtxt'+str(i)
			Dict('store', v, detailtxt)							# detailtxt speichern 
			if url.endswith('.mp3'):		
				Format = 'Podcast ' 			
			else:	
				Format = 'Video '								# .mp4, .webm, .. 
			#lable = 'Download ' + Format + ' | ' + quality
			lable = 'Download' + ' | ' + quality				# 09.01.2021 Wegfall Format aus Platzgründen 
			dest_path = SETTINGS.getSetting('pref_download_path')
			tagline = Format + 'wird in ' + dest_path + ' gespeichert' 									
			summary = 'Sendung: ' + title_org
			key_detailtxt='detailtxt'+str(i)
			title_par = title_org.replace("\n", "||")			# Bsp. \n s. yt_get
			
			url=py2_encode(url); title_par=py2_encode(title_par); sub_path=py2_encode(sub_path);
			fparams="&fparams={'url': '%s', 'title': '%s', 'dest_path': '%s', 'key_detailtxt': '%s', 'sub_path': '%s'}" % \
				(quote(url), quote(title_par), dest_path, key_detailtxt, quote(sub_path))
			addDir(li=li, label=lable, action="dirList", dirID="DownloadExtern", fanart=R(ICON_DOWNL), 
				thumb=R(ICON_DOWNL), fparams=fparams, summary=summary, tagline=tagline, mediatype='')
			i=i+1					# Dict-key-Zähler
	
	return li
	
#---------------------------
# Aufruf test_downloads (Setting pref_show_qualities=false)
# ermittelt Stream mit höchster Auflösung / höchster Bitrate
#
def get_bestdownload(download_list):
	PLog('get_bestdownload:')
	PLog("download_list:" + str(download_list))
	download_items=[]

	# Filterung Arte-Streams (Sprachen, UT, ..). Bei leerer Liste
	#	erfolgt Abgleich mit download_list unabhängig von Sprachen
	my_list=[]
	pref = SETTINGS.getSetting('pref_arte_streams')
	pref = py2_decode(pref)
	PLog(u"pref: " + pref)
	
	for item in download_list:
		item = py2_decode(item)
		lang = stringextract('[B]', '[/B]', item)
		if item.find(u"//arteptweb") >= 0 and item.find(pref) >= 0:
			if lang == pref: 		# Zusätze berücks. z.B. UT Deutsch	
				my_list.append(item)				
	PLog(len(my_list))
	
	if len(my_list)== 0:							# Arte Fallback Deutsch
		for item in download_list:
			item = py2_decode(item)
			lang = stringextract('[B]', '[/B]', item)
			if u"//arteptweb" in item and lang == u"Deutsch":
				my_list.append(item)				
	PLog(len(my_list))
				
	if len(my_list) > 0:
		download_list = my_list	

	# Full HD (ARD, ZDF): 1920x1080 (funk)
	# high_list: absteigende Qualitäten in diversen Erscheinungen
	high_list =  ["3840x2160", "Full HD", "1920x1080", "1280x1080", "5000kbit",
					"1280x", "veryhigh", "960x720", "960x", "640x540", "640x360"]
	for hl in high_list:					# Abgleich mit Auslösungen
		for item in download_list:
			#PLog("hl: %s | %s" % (hl, item))
			if hl in item:
				download_items.append(item)
				PLog("found1: " + item)
				return download_items

	download_items.append(download_list[0])		# Fallback 1. Stream (ARD, ZDF OK)
	return download_items
	
#-----------------------
# Textdatei für Download-Video / -Podcast -
# 05.07.2020 verlagert nach util:
#def MakeDetailText(title, summary,tagline,quality,thumb,url):	
	
####################################################################################################
# Verwendung von curl/wget mittels Phytons subprocess-Funktionen
# 30.08.2018:
# Zum Problemen "autom. Wiedereintritt" - auch bei PHT siehe Doku in LiveRecord.
# 20.12.2018 Problem "autom. Wiedereintritt" in Kodi nicht relevant.
# 20.01.2020 der Thread zum internen Download wird hier ebenfalls aufgerufen 
# 27.02.2020 Code für curl/wget-Download entfernt
# 30.06.2020 Angleichung Dateiname (Datum) an epgRecord (Bindestriche entf.)
# 23.03.2021 erweitert um Download der Untertitel (sub_path), leer für mp3-files 
# 02.04.2021 Var PIDcurl entfernt (für Kodi obsolet)
# 25.09.2021 Fix Security-Issue Incomplete URL substring sanitization (CodeQL-
#				Check)
#
def DownloadExtern(url, title, dest_path, key_detailtxt, sub_path=''):  
	PLog('DownloadExtern: ' + title)
	PLog(url); PLog(dest_path); PLog(key_detailtxt)
	
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button

	
	if 	SETTINGS.getSetting('pref_generate_filenames') == 'true':	# Dateiname aus Titel generieren
		max_length = 255 - len(dest_path)
		dfname = make_filenames(title.strip(), max_length) 
	else:												# Bsp.: Download_20161218_091500.mp4  oder ...mp3
		now = datetime.datetime.now()
		mydate = now.strftime("%Y%m%d_%H%M%S")	
		dfname = 'Download_' + mydate 
	
	if '?file=.mp3' in url:								# Livestream aus Audiothek?
		msg1 = "Achtung: das ist vermutlich ein Livestream!"
		msg2 = "Download trotzdem durchführen?"
		msg3 = "Ein Abbruch des Downloads ist im Addon nicht möglich!"
		ret=MyDialog(msg1, msg2, msg3, ok=False, yes='JA')
		if ret  == False:
			return		
	
	suffix=''
	if url.endswith('.mp3'):
		suffix = '.mp3'		
		dtyp = 'Podcast '
	else:												# .mp4 oder .webm	
		dtyp = 'Video '
		if 'googlevideo.com/' in url:					# Youtube-Url ist ohne Endung (pytube-Ausgabe)
			suffix = '.mp4'	
		if url.endswith('.mp4') or '.mp4' in url:		# funk: ..920x1080_6000.mp4?hdnts=				
			suffix = '.mp4'		
		if url.endswith('.webm'):				
			suffix = '.webm'		
		
	if suffix == '':
		msg1='DownloadExtern: Problem mit Dateiname. Video: %s' % title
		PLog(msg1)
		MyDialog(msg1, '', '')
		return li

	title = dtyp + 'curl/wget-Download: ' + title
	textfile = dfname + '.txt'
	
	dfname = dfname + suffix							# suffix: '.mp4', '.webm', oder '.mp3'
	
	pathtextfile = os.path.join(dest_path, textfile)	# kompl. Speicherpfad für Textfile
	PLog(pathtextfile)
	detailtxt = Dict("load", key_detailtxt)				# detailtxt0, detailtxt1, ..
	PLog(detailtxt[:60])
	
	PLog('convert_storetxt:')
	dtyp=py2_decode(dtyp); dfname=py2_decode(dfname); detailtxt=py2_decode(detailtxt)
	storetxt = 'Details zum ' + dtyp +  dfname + ':\r\n\r\n' + detailtxt
	
	PLog(sys.platform)
	fulldestpath = os.path.join(dest_path, dfname)	# wie curl_fullpath s.u.
									# Untertiteldatei hinzufügen:
	PLog(dtyp); PLog(SETTINGS.getSetting('pref_load_subtitles'))
	
	from threading import Thread	# thread_getfile
	path_url_list=''; timemark=''; notice=True
	background_thread = Thread(target=thread_getfile, args=(textfile,pathtextfile,storetxt,url,fulldestpath,path_url_list,timemark,notice,sub_path,dtyp))
	background_thread.start()		
				
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
	return										
	
#---------------------------
# interne Download-Routine für MP4, MP3 u.a. mittels urlretrieve 
#	Download-Routine für Bilder: thread_getpic
#	bei Bedarf ssl.SSLContext verwenden - s.
#		https://docs.python.org/2/library/urllib.html
# vorh. Dateien werden überschrieben (wie früher mit curl/wget).
# Aufrufer: DownloadExtern, DownloadMultiple (mit 
#	path_url_list + timemark)
# 	notice triggert die Dialog-Ausgabe.
# Alternativen für urlretrieve (legacy): wget-Modul oder 
#	Request (stackoverflow: alternative-of-urllib-urlretrieve-in-python-3-5)
# 25.01.2022 hinzugefügt nach Ende Einzeldownload: Entfernung Lock DL_CHECK, 
#	Entf. in Monitor epgRecord.get_active_dls nicht sicher
# 19.02.2022 Nachrüstung GetOnlyRedirect vor urlretrieve für Audiothek
#
def thread_getfile(textfile,pathtextfile,storetxt,url,fulldestpath,path_url_list='',timemark='',notice=True,sub_path="",dtyp=""):
	PLog("thread_getfile:")
	PLog(url); PLog(fulldestpath); PLog(len(path_url_list)); PLog(timemark); PLog(notice); 

	icon = R('icon-downl-dir.png')
	try:
		if path_url_list:									# Sammeldownloads (Podcast)
			msg1 = 'Starte Download im Hintergrund'		
			msg2 = 'Anzahl der Dateien: %s' % len(path_url_list)
			msg3 = 'Ablage: ' + SETTINGS.getSetting('pref_download_path')
			ret=MyDialog(msg1, msg2, msg3, ok=False, yes='OK')
			if ret  == False:
				return

			cnt=0
			for item in path_url_list:
				cnt=cnt+1
				msg1 = "Sammeldownloads"
				msg2 = "Podcast: %d von %d" % (cnt, len(path_url_list))
				xbmcgui.Dialog().notification(msg1,msg2,icon,2000,sound=False)
				PLog(item)
				path, url = item.split('|')	
				new_url, msg = get_page(path=url, GetOnlyRedirect=True) # für Audiothek erforderlich
				if new_url == '':							# 30.03.2022 weiter ohne Exception
					msg1 = "Fehler"
					msg2 = "Quelle nicht gefunden: %s" % url.split("/")[-1]
					wicon = R(ICON_WARNING)
					#raise Exception("Quelle nicht gefunden: %s" % url.split("/")[-1])
					xbmcgui.Dialog().notification(msg1,msg2,wicon,2000)
				else:
					urlretrieve(new_url, path)
				#xbmc.sleep(1000*2)							# Debug
			
			msg1 = u'%d Downloads erledigt' % cnt 
			msg2 = u'gestartet: %s' % timemark				# Zeitstempel 
			if notice:
				xbmcgui.Dialog().notification(msg1,msg2,icon,4000)	# Fertig-Info
				xbmc.executebuiltin('Container.NextSortMethod') # OK s.o.

		else:												# Einzeldownload
			vsize=''
			clen = get_content_length(url)
			if clen:
				vsize = " (%s):" % humanbytes(clen)
			else:
				vsize = u" (Größe unbekannt)"
			msg1 = 'Starte Download im Hintergrund'	+ vsize	
			msg2 = fulldestpath	
			msg3 = 'Begleit-Infos in: %s' % textfile
			subget = False
			if SETTINGS.getSetting('pref_load_subtitles') == 'true':		
				if sub_path and 'Video' in dtyp:				# Untertitel verfügbar?
					subget = True
					subname = os.path.split(sub_path)[1]
					msg3 = u"%s\nUntertitel werden zusätzlich geladen" % (msg3)					  

			if notice:
				ret=MyDialog(msg1, msg2, msg3, ok=False, yes='OK')
				if ret  == False:
					return
			if pathtextfile:
				RSave(pathtextfile, storetxt, withcodec=True)	# Text speichern
				
			# Fortschrittsbalken nur mit ermittelter Länge möglich:
			if clen and SETTINGS.getSetting('pref_use_pgbar') == 'true':	# mit Fortschrittsbalken 
				msg = get_chunks(url, clen, fulldestpath)
				if msg:
					raise Exception(msg)
			else:
				if os.path.exists(DL_CNT):						# Datei dl_cnt
					with open(DL_CNT,'r+') as f:				# Anz. Downloads schreiben -> get_active_dls
						line = f.read()
						new_len=clen
						if line == '' or line.startswith('0|'):	# leer / 0
							cnt=0; old_len=0; new_len=clen
							if new_len == '' :					# mögl. Problem in get_content_length
								new_len=0
						else:
							cnt, old_len = line.split("|")
						cnt = int(cnt) + 1; new_len = int(old_len) + int(new_len)
						f.seek(0)								# seek + truncate: alten Inhalt löschen
						line = "%s|%s" % (str(cnt), str(new_len))
						f.write(line)
						f.truncate()
						PLog("line_start_dl: %s" % line)
				else:
					with open(DL_CNT,'w') as f:
						f.write("1|%s" % str(clen))					
				new_url, msg = get_page(path=url, GetOnlyRedirect=True) # für Audiothek erforderlich
				if new_url == '':
					raise Exception("Quelle nicht gefunden")
				urlretrieve(new_url, fulldestpath)				
				#xbmc.sleep(1000*30)	# Debug
			if subget:											# Untertitel holen 
				get_subtitles(fulldestpath, sub_path)
			
			# sleep(10)											# Debug
			line=''
			msg1 = 'Download abgeschlossen:'
			msg2 = os.path.basename(fulldestpath) 				# Bsp. heute_Xpress.mp4
			if notice:
				xbmcgui.Dialog().notification(msg1,msg2,icon,4000)	# Fertig-Info
				if os.path.exists(DL_CNT):						# Datei dl_cnt
					with open(DL_CNT,'r+') as f:				# Anz. Downloads verringern -> get_active_dls
						line = f.read()
						new_len=clen
						cnt, old_len = line.split("|")
						if line != '' and line.startswith('0|') == False:
							cnt = int(cnt) - 1; 
							try:
								new_len = int(old_len) - int(new_len)
								if new_len < 0:
									new_len=0
							except:
								new_len = 0
							line = "%s|%s" % (str(cnt), str(new_len))
						f.seek(0)								# seek + truncate: alten Inhalt löschen
						f.write(line)
						f.truncate()
		
						PLog("line_end_dl: %s" % line)
						if "0|0" in line:						# Lock dl_check_alive entfernen
							PLog("Lock_entfernt")
							if os.path.exists(DL_CHECK):		
								os.remove(DL_CHECK)						
			
				
	except Exception as exception:
		PLog("thread_getfile:" + str(exception))
		if os.path.exists(DL_CHECK):							# Abbruchsignal -> 	epgRecord.get_active_dls
			os.remove(DL_CHECK)						
		msg1 = 'Download fehlgeschlagen'
		msg2 = 'Fehler: %s' % str(exception)		
		if notice:
			MyDialog(msg1, msg2, '')

	return

#---------------------------
# ermittelt Dateilänge für Downloads (leer bei Problem mit HTTPMessage-Objekt)
# Aufrufer: thread_getfile
#
def get_content_length(url):
	PLog('get_content_length:')
	UrlopenTimeout = 3
	try:
		req = Request(url)	
		r = urlopen(req)
		if PYTHON2:					
			h = r.headers.dict
			clen = h['content-length']
		else:
			h = r.getheader('Content-Length')
			clen = h
		# PLog(h)
		
	except Exception as exception:
		err = str(exception)
		PLog(err)
		clen = ''
	
	PLog(clen)
	return clen
	
#---------------------------
# Download stückweise mit Fortschrittsbalken
# Aufrufer: thread_getfile
# Upgrade: xbmcgui.DialogProgressBG (nach Supportende Leia)
#
def get_chunks(url, DL_len, fulldestpath):
	PLog('get_chunks:')
	
	msg=''; DL_len = int(DL_len); get_len = 0	
	
	dp = xbmcgui.DialogProgress()
	fname = fulldestpath.split('/')[-1]				# Dateiname
	dp.create('%s: %s' % (humanbytes(DL_len), fname))
	r = urlopen(url)
	blowup = 1024									# Default 1 MByte	
	CHUNK_len = 1024 * blowup
	if CHUNK_len > DL_len:
		CHUNK_len = DL_len
	PLog("DL_len %s, CHUNK_len %s, fname %s" % (str(DL_len), str(CHUNK_len), fname))


	with open(fulldestpath, 'wb') as f:
		remain = DL_len
		while remain > 0:	
			chunk = r.read(CHUNK_len)
			if not chunk:
				break
			f.write(chunk)
			
			chunk_len = len(chunk)
			get_len = get_len + chunk_len
			remain = DL_len - get_len
			up = 100 * float(get_len) / float(DL_len)	# Prozentsatz
			upround = int(round(up))					# int für DialogProgress erford.
			PLog("up: %s, upround %s" % (str(up), str(upround)))
			line = 'Länge chunk: %s, ausstehend %s von %s' % (str(chunk_len), remain, str(DL_len))
			PLog(line)
			dp.update(upround)
			#xbmc.sleep(1000)	# Debug
			up=up+up
			if (dp.iscanceled()): 
				msg="abgebrochen"
				break
			
	r.close()
	dp.close()
	return msg


#---------------------------
# Untertitel für Download holen
# Aufrufer: thread_getfile
def get_subtitles(fulldestpath, sub_path):
	PLog('get_subtitles:')
	
	PLog("fulldestpath: " + fulldestpath)
	PLog("sub_path: " + sub_path)
	if "|" in sub_path:						# ZDF 2 Links: .sub, .vtt
		 sub_path = sub_path.split('|')[0]
	local_path=''
	sub_path = sub_path_conv(sub_path)		# Untertitel holen + konvertieren
	if isinstance(sub_path, list):			# Liste für PY3 in sub_path_conv
		sub_path = sub_path[0]
	PLog("sub_path2: " + str(sub_path))

	if sub_path.startswith('http'):	# ZDF-Untertitel holen
		local_path = "%s/%s" % (SUBTITLESTORE, sub_path.split('/')[-1])
		local_path = os.path.abspath(local_path)
		try:
			urlretrieve(sub_path, local_path)
		except Exception as exception:
			PLog(str(exception))
			local_path=''
	else:
		local_path = sub_path
			
	if 	local_path:						# Name der UT-Datei an Videotitel anpassen
		suffix=''; ext=''
		if "." in fulldestpath:
			suffix =  "." + fulldestpath.split('.')[-1]
		if "." in local_path:
			ext =  "." + local_path.split('.')[-1]
		PLog("local_path: %s, suffix: %s, ext: %s" % (local_path, suffix, ext))
		
		utsrc = local_path
		if suffix and ext:
			utdest = fulldestpath.replace(suffix, ext)  # Bsp.: .mp4 -> .srt
		else:
			utdest = fulldestpath + ext
		PLog("utdest: " + utdest)
		if '//' not in utdest:		# keine Share
			shutil.copy(utsrc, utdest)					
			os.remove(utsrc)
		else:
			xbmcvfs.copy(utsrc, utdest)	
	return					

#---------------------------
# Download-Routine mittels urlretrieve ähnlich thread_getfile
#	hier für Bilder + Erzeugung von Wasserzeichen (text_list: Titel, tagline,
#	summary)
# Aufrufer: ZDF_BildgalerieSingle + ARDSportBilder 
#	dort Test auf SETTINGS.getSetting('pref_watermarks')
# Container.NextSortMethod sorgt für Listing-Refresh (ohne Sort.-Wirkung) - 
#	dagegen bleiben Container.Refresh und ActivateWindow wirkungslos.
# Testscript: watermark2.py
# Fehler: cannot write mode RGBA as JPEG (LibreElec) - siehe:
#	https://github.com/python-pillow/Pillow/issues/2609
#	Lösung new_image.convert("RGB") OK
# 5 try-Blöcke - 1 Block für Debugzwecke nicht ausreichend
# Problem Windows7: die meisten draw.text-Operationen schlagen fehl -
#	Ursache ev. Kodi 18.5/python3 auf dem Entw.PC (nicht mit
#	python2 getestet).
#
def thread_getpic(path_url_list,text_list,folder=''):
	PLog("thread_getpic:")
	PLog(len(path_url_list)); PLog(len(text_list)); PLog(folder);
	li = xbmcgui.ListItem()

	watermark=False; ok="nein"
	if text_list:										# 
		xbmc_base = xbmc.translatePath("special://xbmc")
		myfont = os.path.join(xbmc_base, "media", "Fonts", "arial.ttf") 
		if os.path.exists(myfont) == False:				# Font vorhanden?
			msg1 = 'Kodi Font Arial nicht gefunden.'
			msg2 = 'Bitte den Font Arial installieren oder die Option Wasserzeichen in den Settings abschalten.'
			MyDialog(msg1, msg2, '')
		else:	
			try:										# PIL auf Android nicht verfügbar
				from PIL import Image, ImageDraw, ImageFont
				watermark=True; ok="ja"
				PLog("Font: " + myfont)
				font = ImageFont.truetype(myfont)
				img_fraction=0.50; fontsize=1		# Text -> Bildhälfte: 
			except Exception as exception:
				PLog("Importerror: " + str(exception))
				watermark=False

	icon = R('icon-downl-dir.png')
	msg1 = 'Starte Download im Hintergrund'		
	msg2 = 'Anzahl der Bilder: %s, Wasserzeichen: %s' % (len(path_url_list), ok)
	msg3 = 'Ordner (Bildersammlungen): ' + folder
	ret=MyDialog(msg1, msg2, msg3, ok=False, yes='OK')
	if ret  == False:
		return
		
		
	i=0; err_url=0; err_PIL=0
	for item in path_url_list:
		PLog(item)
		path, url = item.split('|')					# path: Bilddatei, url: Quelle
		try:										# Server-Probleme abfangen, skip Bild
			urlretrieve(url, path)
			# xbmc.sleep(2000)						# Debug
		except Exception as exception:
			PLog("thread_getpic1: " + str(exception))
			err_url=err_url+1
			watermark = False						# skip Watermark
			
		if watermark:
			try:
				base = Image.open(path).convert('RGBA')
				skip_watermark=False
			except Exception as exception:
				PLog("thread_getpic2: " + str(exception))
				err_PIL=err_PIL+1
				skip_watermark=True
			
			if skip_watermark == False:	
				width, height = base.size
				PLog("Bildbreite, -höhe: %d, %d" % (width, height))
				# 0 = 100% Deckung für helle Flächen
				txtimg = Image.new('RGBA', base.size, (255,255,255,0))
				fz = SETTINGS.getSetting('pref_fontsize')
				if fz == 'auto':
					mytxt_col = 80						# Zeilenbreite 
				else:
					mytxt_col = 100 - int(fz)			# Bsp. 100-20				
				
				mytxt = text_list[i]
				mytxt = wrap(mytxt,mytxt_col)			# Zeilenumbruch
				PLog(mytxt)
				
				try:	
					# für Windows7 Multi- -> Single-Line:	
					import platform						# IOError möglich
					PLog('Plattform: ' + platform.release())
					if platform.release() == "7":
						PLog("Windows7: entferne LFs")	
						mytxt = mytxt.replace('\n', ' | ')
						mytxt = textwrap.fill(mytxt, mytxt_col)
				except Exception as exception:
					PLog("Plattform_Error: " + str(exception))				
								
				if SETTINGS.getSetting('pref_fontsize') == 'auto':
					# fontsize abhängig von Bildgröße:
					while font.getsize(mytxt)[0] < img_fraction*base.size[0]:		
						fontsize += 2
						font = ImageFont.truetype(myfont, fontsize)
						
					fontsize = max(10, fontsize)			# fontsize Minimum 10
				else:
					fontsize = int(SETTINGS.getSetting('pref_fontsize'))
				PLog("Fontsize: %d" % fontsize)
				font = ImageFont.truetype(myfont, fontsize)
				draw = ImageDraw.Draw(txtimg)
				# txtsz = draw.multiline_textsize(mytxt, font)	# exeption Windows7
				# PLog("Größe Bildtext: " + str(txtsz))
				
				w,h = draw.textsize(mytxt, font=font)
				W,H = base.size
				# x,y = 0.5*(W-w),0.90*H-h		# zentriert
				# x,y = W-w,0.90*H-h			# rechts
				x,y = 0.05*(W-w),0.96*(H-h)		# u. links
				PLog("x,y: %d, %d" % (x,y))

				# outlined Text - für helle Flächen erforderlich, aus stackoverflow.com/
				# /questions/41556771/is-there-a-way-to-outline-text-with-a-dark-line-in-pil 
				# try-Block für Draw 
				try:
					outlineAmount = 2
					shadowColor = 'black'
					for adj in range(outlineAmount):					
						draw.text((x-adj, y), mytxt, font=font, fill=shadowColor)	#move right						
						draw.text((x+adj, y), mytxt, font=font, fill=shadowColor)	#move left					
						draw.text((x, y+adj), mytxt, font=font, fill=shadowColor)	#move up					
						draw.text((x, y-adj), mytxt, font=font, fill=shadowColor)	#move down						
						draw.text((x-adj, y+adj), mytxt, font=font, fill=shadowColor)#diagonal left up
						draw.text((x+adj, y+adj), mytxt, font=font, fill=shadowColor)#diagonal right up
						draw.text((x-adj, y-adj), mytxt, font=font, fill=shadowColor)#diagonal left down
						draw.text((x+adj, y-adj), mytxt, font=font, fill=shadowColor)#diagonal right down

					# fill: color, letz. Param: Deckung:
					draw.text((x,y), mytxt, font=font, fill=(255,255,255,255))
				except Exception as exception:
					PLog("thread_getpic3: " + str(exception))
					PLog('draw.text fehlgeschlagen')
					err_PIL=err_PIL+1
					
				new_image = Image.alpha_composite(base, txtimg)
				try:
					new_image.save(path)					# Orig. überschreiben
				except Exception as exception:
					PLog("thread_getpic4: " + str(exception))
					if 'cannot write mode RGBA' in str(exception):
						new_image = new_image.convert("RGB")
						try:
							new_image.save(path)
						except Exception as exception:
							PLog("thread_getpic5: " + str(exception))
							err_PIL=err_PIL+1	
		i=i+1	
	
	msg1 = 'Download erledigt'
	msg2 = 'Ordner: %s' % folder					# Ordnername 
	if err_url or err_PIL:							# Dialog statt Notif. bei Fehlern
		if 	err_url:
			msg3 = u'Fehler: %s Bild(er) nicht verfügbar' % err_url
		else:
			msg3 = u'Fehler: %s Wasserzeichen fehlgeschlagen' % err_PIL
		MyDialog(msg1, msg2, msg3)
	else:	
		xbmcgui.Dialog().notification(msg1,msg2,icon,4000)	# Fertig-Info
	xbmc.executebuiltin('Container.NextSortMethod') # OK (s.o.)
	return li	# ohne ListItem Rekursion möglich
#---------------------------
# Tools: Einstellungen,  Bearbeiten, Verschieben, Löschen
# 11.06.2022 Notif. für Zugang aus Menü Infos+Tools ergänzt
def DownloadTools():
	PLog('DownloadTools:');

	if SETTINGS.getSetting('pref_use_downloads') == 'false':
		msg1 = "Hinweis:"
		msg2 = 'Downloads sind ausgeschaltet'	
		icon = R(ICON_DOWNL_DIR)
		xbmcgui.Dialog().notification(msg1,msg2,icon,3000)

	path = SETTINGS.getSetting('pref_download_path')
	PLog(path)
	dirlist = []
	if os.path.isdir(path) == False:
		msg1='Hinweis:'
		if path == '':		
			msg2='Downloadverzeichnis noch nicht festgelegt.'
		else:
			msg2='Downloadverzeichnis nicht gefunden: '
		msg3=path
		MyDialog(msg1, msg2, msg3)
	else:
		dirlist = os.listdir(path)						# Größe Inhalt? 		
			
	PLog(len(dirlist))
	mpcnt=0; vidsize=0
	for entry in dirlist:
		if entry.find('.mp4') > 0 or entry.find('.webm') > 0 or entry.find('.mp3') > 0:
			mpcnt = mpcnt + 1	
			fname = os.path.join(path, entry)					
			vidsize = vidsize + os.path.getsize(fname) 
	vidsize	= humanbytes(vidsize)
	PLog('Downloadverzeichnis: %s Download(s), %s' % (str(mpcnt), vidsize))
		
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)								# Home-Button
	
	dlpath =  SETTINGS.getSetting('pref_download_path')# Einstellungen: Pfad Downloadverz.
	title = u'Downloadverzeichnis festlegen/ändern: (%s)' % dlpath			
	tagline = 'Das Downloadverzeichnis muss für den Addon-Nutzer beschreibbar sein.'
	summ = ''; 
		
	# summary =    # s.o.
	fparams="&fparams={'settingKey': 'pref_download_path', 'mytype': '0', 'heading': '%s', 'path': '%s'}" % (title, dlpath)
	addDir(li=li, label=title, action="dirList", dirID="DirectoryNavigator", fanart=R(ICON_DOWNL_DIR), 
		thumb=R(ICON_DOWNL_DIR), fparams=fparams, tagline=tagline)

	PLog(SETTINGS.getSetting('pref_VideoDest_path'))
	movie_path = SETTINGS.getSetting('pref_VideoDest_path')
	if SETTINGS.getSetting('pref_VideoDest_path') == '':# Vorgabe Medienverzeichnis (Movieverz), falls leer	
		pass
		# movie_path = xbmc.translatePath('library://video/')
		# PLog(movie_path)
				
	#if os.path.isdir(movie_path)	== False:			# Sicherung gegen Fehleinträge - in Kodi nicht benötigt
	#	movie_path = ''									# wird ROOT_DIRECTORY in DirectoryNavigator
	PLog(movie_path)	
	title = u'Zielverzeichnis zum Verschieben festlegen/ändern (%s)' % (movie_path)	
	tagline = 'Zum Beispiel das Medienverzeichnis.'
	summ = u'Hier kann auch ein Netzwerkverzeichnis, z.B. eine SMB-Share, ausgewählt werden.'
	# summary =    # s.o.
	fparams="&fparams={'settingKey': 'pref_VideoDest_path', 'mytype': '0', 'heading': '%s', 'shares': '%s', 'path': '%s'}" %\
		(title, '', movie_path)
	addDir(li=li, label=title, action="dirList", dirID="DirectoryNavigator", fanart=R(ICON_DOWNL_DIR), 
		thumb=R(ICON_DIR_MOVE), fparams=fparams, tagline=tagline, summary=summ)

	PLog(SETTINGS.getSetting('pref_podcast_favorits'))					# Pfad zur persoenlichen Podcast-Favoritenliste
	path =  SETTINGS.getSetting('pref_podcast_favorits')							
	title = u'Persoenliche Podcast-Favoritenliste festlegen/ändern (%s)' % path			
	tagline = 'Format siehe podcast-favorits.txt (Ressourcenverzeichnis)'
	# summary =    # s.o.
	fparams="&fparams={'settingKey': 'pref_podcast_favorits', 'mytype': '1', 'heading': '%s', 'path': '%s'}" % (title, path)
	addDir(li=li, label=title, action="dirList", dirID="DirectoryNavigator", fanart=R(ICON_DOWNL_DIR), 
		thumb=R(ICON_DIR_FAVORITS), fparams=fparams, tagline=tagline)
		
	if mpcnt > 0:																# Videos / Podcasts?
		dirsize=''
		dirsize = get_dir_size(SETTINGS.getSetting('pref_download_path'))
		summ = u"Größe Downloadverzeichnis: %s | Anzahl Downloads: %s | Größe Video-/Audiodateien: %s" %\
			(dirsize, str(mpcnt), vidsize)		
		title = 'Downloads und Aufnahmen bearbeiten: %s Download(s)' % (mpcnt)	# Button Bearbeiten
		tag = 'Downloads im Downloadverzeichnis ansehen, loeschen, verschieben'
		fparams="&fparams={}"
		addDir(li=li, label=title, action="dirList", dirID="DownloadsList", fanart=R(ICON_DOWNL_DIR), 
			thumb=R(ICON_DIR_WORK), fparams=fparams, summary=summ, tagline=tag)

		if dirlist:
			dest_path = SETTINGS.getSetting('pref_download_path') 
			if path and movie_path:												# Button Verschieben (alle)
				title = 'ohne Rückfrage! alle (%s) Downloads verschieben' % (mpcnt)	
				tagline = 'Verschieben erfolgt ohne Rueckfrage!' 
				summary = 'alle Downloads verschieben nach: %s'  % (movie_path)
				fparams="&fparams={'dfname': '', 'textname': '', 'dlpath': '%s', 'destpath': '%s', 'single': 'False'}" \
					% (dest_path, movie_path)
				addDir(li=li, label=title, action="dirList", dirID="DownloadsMove", fanart=R(ICON_DOWNL_DIR), 
					thumb=R(ICON_DIR_MOVE_ALL), fparams=fparams, summary=summary, tagline=tagline)
			
			title = 'alle (%s) Downloads löschen' % (mpcnt)						# Button Leeren (alle)
			summary = 'alle Dateien aus dem Downloadverzeichnis entfernen'
			fparams="&fparams={'dlpath': '%s', 'single': 'False'}" % dlpath
			addDir(li=li, label=title, action="dirList", dirID="DownloadsDelete", fanart=R(ICON_DOWNL_DIR), 
				thumb=R(ICON_DELETE), fparams=fparams, summary=summary)
	
	# ------------------------------------------------------------------	
	# Aufnahme-Tools			
	if os.path.exists(JOBFILE):													# Jobliste vorhanden?
		title = 'Aufnahme-Jobs verwalten'					
		tag = u'Jobliste EPG-Menü-Aufnahmen: Liste, Job-Status, Jobs löschen'
		fparams="&fparams={'action': 'listJobs'}" 
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.epgRecord.JobMain", fanart=R(ICON_DOWNL_DIR),  
			thumb=R("icon-record.png"), fparams=fparams, tagline=tag)

	if os.path.exists(MONITOR_ALIVE):											# JobMonitor?
		title = 'Aufnahme-Monitor stoppen'					
		tag = u'stoppt das Monitoring für EPG-Aufnahmen (aber keine laufenden Aufnahmen)'
		summ = 'das Setting "Aufnehmen Menü: EPG Sender einzeln" wird ausgeschaltet'
		summ = '%s\n\nZum Restart dieses Menü erneut aufrufen oder das Aufnehmen im Setting wieder einschalten' % summ
		fparams="&fparams={'action': 'stop', 'setSetting': 'true'}" 
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.epgRecord.JobMain", fanart=R(ICON_DOWNL_DIR), 
			thumb=R("icon-stop.png"), fparams=fparams, tagline=tag, summary=summ)
	else:
		title = 'Aufnahme-Monitor starten'					
		tag = u'startet das Monitoring für EPG-Aufnahmen'
		summ = 'das Setting "Aufnehmen Menü: EPG Sender einzeln" wird eingeschaltet'
		fparams="&fparams={'action': 'init', 'setSetting': 'true'}" 
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.epgRecord.JobMain", fanart=R(ICON_DOWNL_DIR), 
			thumb=R("icon-record.png"), fparams=fparams, tagline=tag, summary=summ)

		'''
		title = 'Testjobs starten'												# nur Debug 				
		fparams="&fparams={'action': 'test_jobs'}" 
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.epgRecord.JobMain", fanart=R("icon-record.png"), 
			thumb=R("icon-record.png"), fparams=fparams)
		'''	
		
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
	
#---------------------------
# Downloads im Downloadverzeichnis zur Bearbeitung listen	 	
def DownloadsList():			
	PLog('DownloadsList:')	
	path = SETTINGS.getSetting('pref_download_path')
	
	dirlist = []
	if path == None or path == '':									# Existenz Verz. prüfen, falls vorbelegt
		msg1 = 'Downloadverzeichnis noch nicht festgelegt'
		MyDialog(msg1, '', '')
		return
	else:
		if os.path.isdir(path)	== False:			
			msg1 =  'Downloadverzeichnis nicht gefunden: ' 
			msg2 =  path
			MyDialog(msg1, msg2, '')
			return
		else:
			dirlist = os.listdir(path)						# Größe Inhalt? 		
	dlpath = path

	PLog(len(dirlist))
	mpcnt=0; vidsize=0
	for entry in dirlist:
		if entry.find('.mp4') > 0 or entry.find('.webm') > 0 or entry.find('.mp3') > 0:
			mpcnt = mpcnt + 1	
			fname = os.path.join(path, entry)					
			vidsize = vidsize + os.path.getsize(fname) 
	vidsize	= vidsize/1000000
	PLog('Inhalt: %s Download(s), %s MBytes' % (mpcnt, str(vidsize)))
	
	if mpcnt == 0:
		msg1 = 'Kein Download vorhanden | Pfad:' 
		msg2 = dlpath
		MyDialog(msg1, msg2, '')
		return		
		
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button
	
	# Downloads listen:
	for entry in dirlist:							# Download + Beschreibung -> DirectoryObject
		if entry.find('.mp4') > 0 or entry.find('.webm') > 0 or entry.find('.mp3') > 0:
			localpath = entry
			title=''; tagline=''; summary=''; quality=''; thumb=''; httpurl=''
			fname =  entry							# Dateiname 
			basename = os.path.splitext(fname)[0]	# ohne Extension
			ext =     os.path.splitext(fname)[1]	# Extension
			PLog(fname); PLog(basename); PLog(ext)
			txtfile = basename + '.txt'
			txtpath = os.path.join(path, txtfile)   # kompl. Pfad
			PLog('entry: ' + entry)
			PLog('txtpath: ' + txtpath)
			if os.path.exists(txtpath):
				txt = RLoad(txtpath, abs_path=True)		# Beschreibung laden - fehlt bei Sammeldownload
			else:
				txt = None
				title = entry						# Titel = Dateiname, falls Beschreibung fehlt
			if txt != None:			
				title = stringextract("Titel: '", "'", txt)
				tagline = stringextract("ung1: '", "'", txt)
				summary = stringextract("ung2: '", "'", txt)
				quality = stringextract("taet: '", "'", txt)
				thumb = stringextract("Bildquelle: '", "'", txt)
				httpurl = stringextract("Adresse: '", "'", txt)
				
				if tagline and quality:
					tagline = "%s | %s" % (tagline, quality)
					
				# Falsche Formate korrigieren:
				summary=py2_decode(summary); tagline=py2_decode(tagline);
				summary=repl_json_chars(summary); tagline=repl_json_chars(tagline); 
				summary=summary.replace('\n', ' | '); tagline=tagline.replace('\n', ' | ')
				summary=summary.replace('|  |', ' | '); tagline=tagline.replace('|  |', ' | ')

			else:										# ohne Beschreibung
				# pass									# Plex brauchte hier die Web-Url	aus der Beschreibung
				title = fname
				httpurl = fname							# Berücksichtigung in VideoTools - nicht abspielbar
				summary = 'ohne Beschreibung'
				#tagline = 'Beschreibung fehlt - Beschreibung gelöscht, Sammeldownload oder TVLive-Video'
				
			tag_par= tagline.replace('\n', '||')	
			PLog("Satz20:")
			PLog(httpurl); PLog(summary); PLog(tagline); PLog(quality); # PLog(txt); 			
			if httpurl.endswith('mp3'):
				oc_title = u'Anhören, Bearbeiten: Podcast | %s' % py2_decode(title)
				thumb = R(ICON_NOTE)
			else:
				oc_title=u'Ansehen, Bearbeiten: %s' % py2_decode(title)
				if thumb == '':							# nicht in Beschreibung
					thumb = R(ICON_DIR_VIDEO)

			httpurl=py2_encode(httpurl); localpath=py2_encode(localpath); dlpath=py2_encode(dlpath); 
			title=py2_encode(title); summary=py2_encode(summary); thumb=py2_encode(thumb); 
			tag_par=py2_encode(tag_par); txtpath=py2_encode(txtpath);
			fparams="&fparams={'httpurl': '%s', 'path': '%s', 'dlpath': '%s', 'txtpath': '%s', 'title': '%s','summary': '%s', \
				'thumb': '%s', 'tagline': '%s'}" % (quote(httpurl), quote(localpath), quote(dlpath), 
				quote(txtpath), quote(title), quote(summary), quote(thumb), quote(tag_par))
			addDir(li=li, label=oc_title, action="dirList", dirID="VideoTools", fanart=thumb, 
				thumb=thumb, fparams=fparams, summary=summary, tagline=tagline)
			
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)

#---------------------------
# Downloads im Downloadverzeichnis ansehen, löschen, verschieben
#	zum  Ansehen muss das Video  erneut angefordert werden - CreateVideoClipObject verweigert die Wiedergabe
#		lokaler Videos: networking.py line 224, in load ... 'file' object has no attribute '_sock'
#	entf. unter Kodi (Wiedergabe lokaler Quellen möglich).
#	httpurl=HTTP-Videoquelle, path=Videodatei (Name), dlpath=Downloadverz., txtpath=Textfile (kompl. Pfad)
#	
def VideoTools(httpurl,path,dlpath,txtpath,title,summary,thumb,tagline):
	PLog('VideoTools: ' + path)

	title_org = py2_encode(title)
	
	sub_path=''							# s. 1. Ansehen
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button
	
	dest_path = SETTINGS.getSetting('pref_download_path')
	fulldest_path = os.path.join(dest_path, path)
	if  os.access(dest_path, os.R_OK) == False:
		msg1 = 'Downloadverzeichnis oder Leserecht  fehlt'
		msg2 = dest_path
		PLog(msg1); PLog(msg2)
		MyDialog(msg1, msg2, '')
		xbmcplugin.endOfDirectory(HANDLE)
	
	fsize=''
	if os.path.exists(fulldest_path) == False:	# inzw. gelöscht?
		msg1 = 'Datei nicht vorhanden:'
		msg2 = fulldest_path
		PLog(msg1); PLog(msg2)
		MyDialog(msg1, msg2, '')
		xbmcplugin.endOfDirectory(HANDLE)
	else:
		fsize = os.path.getsize(fulldest_path)  # nur Video bzw. mp3
			
	fulldest_path=py2_encode(fulldest_path); 
	PLog("fulldest_path: " + fulldest_path)
	tagline = u'Größe: %s' % humanbytes(fsize)
	if fulldest_path.endswith('mp4') or fulldest_path.endswith('webm'): # 1. Ansehen
		title = title_org 
		globFiles = "%s*" % fulldest_path.split('.')[0] # Maske o. Endung: Video-, Text-, Sub-Datei
		files = glob.glob(globFiles)
		PLog(files) 
		for src_file in files:
			if src_file.endswith(".srt") or src_file.endswith(".sub"):
				sub_path = src_file
		PLog("sub_path: " + sub_path)
		lable = "Ansehen | %s" % (title_org)
		fulldest_path=py2_encode(fulldest_path); title=py2_encode(title); thumb=py2_encode(thumb);	
		summary=py2_encode(summary); sub_path=py2_encode(sub_path);
		fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'sub_path': '%s'}" %\
			(quote_plus(fulldest_path), quote_plus(title), quote_plus(thumb), 
			quote_plus(summary), quote_plus(sub_path))
		addDir(li=li, label=lable, action="dirList", dirID="PlayVideo", fanart=thumb, tagline=tagline,
			thumb=thumb, fparams=fparams, mediatype='video')
		
	else:										# 'mp3' = Podcast
		if fulldest_path.endswith('mp3'):		# Dateiname bei fehl. Beschreibung, z.B. Sammeldownloads
			title = title_org 											# 1. Anhören
			lable = "Anhören | %s" % (title_org)
			fulldest_path=py2_encode(fulldest_path); title=py2_encode(title); thumb=py2_encode(thumb); 
			summary=py2_encode(summary);	
			fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s'}" % (quote(fulldest_path), 
				quote(title), quote(thumb), quote_plus(summary))
			addDir(li=li, label=lable, action="dirList", dirID="PlayAudio", fanart=thumb, thumb=thumb, 
				fparams=fparams, mediatype='music') 
	
	lable = "Löschen: %s" % title_org 									# 2. Löschen
	tagline = 'Datei: %s..' % path[:28] 
	fulldest_path=py2_encode(fulldest_path);	
	fparams="&fparams={'dlpath': '%s', 'single': 'True'}" % quote(fulldest_path)
	addDir(li=li, label=lable, action="dirList", dirID="DownloadsDelete", fanart=R(ICON_DELETE), 
		thumb=R(ICON_DELETE), fparams=fparams, summary=summary, tagline=tagline)
	
	if SETTINGS.getSetting('pref_VideoDest_path'):	# 3. Verschieben nur mit Zielpfad, einzeln
		VideoDest_path = SETTINGS.getSetting('pref_VideoDest_path')
		textname = os.path.basename(txtpath)
		lable = "Verschieben | %s" % title_org									
		summary = "Ziel: %s" % VideoDest_path
		tagline = u'Das Zielverzeichnis kann im Menü Download-Tools oder in den Addon-Settings geändert werden'
		path=py2_encode(path); textname=py2_encode(textname);
		dlpath=py2_encode(dlpath); VideoDest_path=py2_encode(VideoDest_path);
		fparams="&fparams={'dfname': '%s', 'textname': '%s', 'dlpath': '%s', 'destpath': '%s', 'single': 'True'}" \
			% (quote(path), quote(textname), quote(dlpath), quote(VideoDest_path))
		addDir(li=li, label=lable, action="dirList", dirID="DownloadsMove", fanart=R(ICON_DIR_MOVE_SINGLE), 
			thumb=R(ICON_DIR_MOVE_SINGLE), fparams=fparams, summary=summary, tagline=tagline)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
#---------------------------
# Downloadverzeichnis leeren (einzeln/komplett)
def DownloadsDelete(dlpath, single):
	PLog('DownloadsDelete: ' + dlpath)
	PLog('single=' + single)
	
	msg1 = u'Rückgängig nicht möglich!'
	msg2 = u'Wirklich löschen?'		
	ret=MyDialog(msg1, msg2, msg3='', ok=False, yes='Löschen')
	if ret  == False:
		return
	
	try:
		if single == 'False':
			if ClearUp(os.path.abspath(dlpath), 1) == True:
				error_txt = 'Verzeichnis geleert'
			else:
				raise NameError('Ursache siehe Logdatei')
		else:
			txturl = os.path.splitext(dlpath)[0]  + '.txt' 
			if os.path.isfile(dlpath) == True:							
				os.remove(dlpath)				# Video löschen
			if os.path.isfile(txturl) == True:							
				os.remove(txturl)				# Textdatei löschen
			error_txt = u'Datei gelöscht: ' + dlpath
		PLog(error_txt)			 			 	 
		msg1 = u'Löschen erfolgreich'
		msg2 = error_txt
		xbmcgui.Dialog().notification(msg1,msg2,R(ICON_DELETE),5000)
	except Exception as exception:
		PLog(str(exception))
		msg1 = u'Fehler | Löschen fehlgeschlagen'
		msg2 = str(exception)
		MyDialog(msg1, msg2, '')
	
	return
#---------------------------
# dfname=Videodatei, textname=Textfile,  dlpath=Downloadverz., destpath=Zielverz.
#
def DownloadsMove(dfname, textname, dlpath, destpath, single):
	PLog('DownloadsMove: ');PLog(dfname);PLog(textname);PLog(dlpath);PLog(destpath);
	PLog('single=' + single)

	li = xbmcgui.ListItem()

	if  os.access(destpath, os.W_OK) == False:
		if '//' not in destpath:					# Test entfällt bei Shares
			msg1 = 'Download fehlgeschlagen'
			msg2 = 'Kein Schreibrecht im Zielverzeichnis'
			MyDialog(msg1, msg2, '')
			return li	

	try:
		cnt=0; err_cnt=0
		if single == 'False':						# Verzeichnisinhalt verschieben
			dlpath_list = next(os.walk(dlpath))[2]	# skip .. + dirs		
			ges_cnt = len(dlpath_list)				# Anzahl Dateien
			for fname in dlpath_list:
				src = os.path.join(dlpath, fname)
				if '//' not in destpath:
					dest = os.path.join(destpath, fname)
				else:
					dest = destpath + fname			#  smb://myShare/myVideos/video1.mp4							
				PLog(src); PLog(dest); 
				
				if os.path.isfile(src) == True:	   	# Quelle testen
					if '//' not in destpath:						
						shutil.copy(src, dest)		# konv. kopieren	
					else:
						xbmcvfs.copy(src, dest)		# zu Share kopieren
						
					if xbmcvfs.exists(dest):
						xbmcvfs.delete(src)
						cnt = cnt + 1

			if cnt == ges_cnt:
				msg1 = 'Verschieben erfolgreich'
				msg2 = '%s von %s Dateien verschoben nach: %s' % (cnt, ges_cnt, destpath)
				msg3 = ''
			else:
				msg1 = 'Problem beim Verschieben - Ursache nicht bekannt'
				msg2 = 'verschobene Dateien: %s von %s.' % (cnt, ges_cnt)
				msg3 = 'Vielleicht hilft es, Dateien einzeln zu verschieben (Menü >Downloads bearbeiten<)'
			PLog(msg2)	
			MyDialog(msg1, msg2, msg3)
			return li
				 			 	 
		else:								# Einzeldatei verschieben
			videosrc = os.path.join(dlpath, dfname)	
			globFiles = "%s*" % videosrc.split('.')[0] # Maske o. Endung: Video-, Text-, Sub-Datei
			files = glob.glob(globFiles) 
			PLog(files)
					
			if '//' not in destpath:
				for src_file in files:
					srcname = os.path.split(src_file)[1]
					dest_file = os.path.join(destpath, srcname)
					PLog("srcname %s, dest_file %s" % (srcname, dest_file))	 						
					if os.path.isfile(src_file) == True:	# Quelldatei testen						
						shutil.copy(src_file, dest_file)		
						os.remove(src_file)					# Quelldatei löschen
			else:											# Share
				for src_file in files:
					srcname = os.path.split(src_file)[1]
					dest_file = destpath + srcname
					PLog("srcname %s, dest_file %s" % (srcname, dest_file))	 						
					ret = xbmcvfs.copy(src_file, dest_file)
					PLog(ret)

					if xbmcvfs.exists(dest_file):
						xbmcvfs.delete(src_file)
					else:
						msg = 'Kopieren auf Share %s fehlgeschlagen' % dest_file
						PLog(msg)
						raise Exception(msg)
						break
				
		msg1 = 'Verschieben erfolgreich'
		msg2 = 'Video verschoben: ' + 	dfname
		PLog(msg2)	
		MyDialog(msg1, msg2, '')
		return li

	except Exception as exception:
		PLog(str(exception))
		msg1 = 'Verschieben fehlgeschlagen'
		msg2 = str(exception)
		MyDialog(msg1, msg2, '')
		return li
		
#---------------------------
# Ablage von Texten im Downloadverzeichnis
# Aufruf: AudioStartLive (Liste RadioStreamLinks)
#	textKey -> Dict-Datei 
# data = Liste oder string, je Zeile wird eine Datei erzeugt,
#	"**" splittet Zeile in mehrere Zeilen, 1. Zeile = Dateiname
def DownloadText(textKey):
	PLog('DownloadText: ' + textKey)
	
	data = Dict("load", textKey)
	PLog(type(data))
	if isinstance(data, list) == False:
		data = data.splitlines() 
	textlen = len(data)
	PLog(textlen)
	
	path = SETTINGS.getSetting('pref_download_path')
	PLog(path)
	if path == None or path == '':									# Existenz Verz. prüfen, falls vorbelegt
		msg1 = 'Downloadverzeichnis noch nicht festgelegt'
		MyDialog(msg1, '', '')
		return
	else:
		if os.path.isdir(path)	== False:			
			msg1 =  'Downloadverzeichnis nicht gefunden: ' 
			msg2 =  path
			MyDialog(msg1, msg2, '')
			return
	
	msg1 = "[B]%d Streamlinks[/B] in einzelnen m3u-Dateien speichern?"	 % textlen	
	msg2 = 'Die Ablage erfolgt im Downloadverzeichnis.'
	ret=MyDialog(msg1, msg2, msg3="", ok=False, yes='OK')
	if ret  == False:
		return
			

	msg1 = "DownloadText"
	msg2 = "%d Dateien gespeichert" % textlen
	icon = R('icon-downl-dir.png')
		
	for inline in data:
		lines=[] ; outlines=[]
		lines = inline.split("**")
		f = lines[0]							# Dateiname
		fname = os.path.join(path, f)	 
		del lines[0]
		
		for line in lines:
			outlines.append(line)
		page  = "\n".join(outlines)
		#PLog(page) 	# Debug
		msg = RSave(fname, py2_encode(page), withcodec=False)
		if msg:									# RSave_Exception
			msg2 = msg
			break	 

	xbmcgui.Dialog().notification(msg1,msg2,icon,2000)	
	return			
		
####################################################################################################
# Aufruf Main, Favoriten oder Merkliste anzeigen + auswählen
#	Hinzufügen / Löschen in Watch (Script merkliste.py)
# mode = 'Favs' für Favoriten  oder 'Merk' für Merkliste
# Datenbasen (Einlesen in ReadFavourites (Modul util) :
#	Favoriten: special://profile/favourites.xml 
#	Merkliste: ADDON_DATA/merkliste.xml (WATCHFILE)
# Verarbeitung:
#	Favoriten: Kodi's Favoriten-Menü, im Addon_Listing
#	Merkliste: zusätzl. Kontextmenmü (s. addDir Modul util) -> Script merkliste.py
#	
# Probleme: Kodi's Fav-Funktion übernimmt nicht summary, tagline, mediatype aus addDir-Call
#			Keine Begleitinfos, falls  summary, tagline od. Plot im addDir-Call fehlen.
#			gelöst mit Base64-kodierter Plugin-Url: 
#				Sonderzeichen nach doppelter utf-8-Kodierung
#			07.01.2020 Base64 in addDir wieder entfernt - hier Verbleib zum Dekodieren
#				alter Einträge
# 			Sofortstart/Resumefunktion: funktioniert nicht immer - Bsp. KIKA-Videos.
#				Die Kennzeichnung mit mediatype='video' erfolgt nach Abgleich mit
#				CallFunctions.
#				Kodi verwaltet die Resumedaten getrennt (Merkliste/Originalplatz). 
#
# Ordnerverwaltung + Filter s. Wicki
#	Filter-Deadlock-Sicherungen: 
#		1. ShowFavs bei leerer Liste	2. Kontextmenü -> watch_filter
#		3. Settings (Ordner abschalten)
# 14.11.2021 Home-Button + Sortierung getrennt von globalen Settings
# 16.11.2022 Berücksichtigung ausgewählter Sätze in selected (zunächst für
#	SearchARDundZDFnew)
def ShowFavs(mode, selected=""):			# Favoriten / Merkliste einblenden
	PLog('ShowFavs: ' + mode)				# 'Favs', 'Merk'
	if selected:
		selected = selected.split()
		selected = [int(x) for a,x in enumerate(selected)]
	PLog(selected)
	
	myfilter=''
	if mode == 'Merk':
		if SETTINGS.getSetting('pref_merkordner') == 'true':
			with open(MERKACTIVE, 'w'):			# Marker aktivieren (Refresh in merkliste)
				pass
			if os.path.isfile(MERKFILTER):	
				myfilter = RLoad(MERKFILTER,abs_path=True)
		else:									# Filter entfernen, falls Ordner abgewählt
			if os.path.isfile(MERKFILTER):		# Altern.: siehe Kontextmenü -> watch_filter
				os.remove(MERKFILTER)
				
	PLog('myfilter: ' + myfilter)
	li = xbmcgui.ListItem()						
	li = home(li, ID=NAME)								# Home-Button

	my_items, my_ordner= ReadFavourites(mode)			# Addon-Favs / Merkliste einlesen
	PLog(len(my_items))
	# Dir-Items für diese Funktionen erhalten mediatype=video:
	# 05.12.2020 zdfmobile.ShowVideo entfernt (enthält auch Mehrfachbeiträge)
	# 13.11.2021 ARDStartSingle hinzugefügt
	CallFunctions = ["PlayVideo", "ZDF_getVideoSources",
						"zdfmobile.PlayVideo", "SingleSendung", "ARDStartVideoStreams", 
						"ARDStartVideoMP4", "ARDStartSingle", "PlayVideo", "my3Sat.SingleBeitrag",
						"SenderLiveResolution", "phoenix.get_formitaeten",
						"phoenix.SingleBeitrag", "phoenix.yt.yt_get",
						"arte.SingleVideo", "arte.GetContent"]	

	if mode == 'Favs':														
		tagline = u"Anzahl Addon-Favoriten: %s" % str(len(my_items)) 	# Info-Button
		s1 		= u"Hier werden die ARDundZDF-Favoriten aus Kodi's Favoriten-Menü eingeblendet."
		s2		= u"Favoriten entfernen: im Kodi's Favoriten-Menü oder am Ursprungsort im Addon (nicht hier!)."
		summary	= u"%s\n\n%s"		% (s1, s2)
		label	= u'Infos zum Menü Favoriten'
	else:
		mf = myfilter
		if mf == '':
			mf = "kein Filter gesetzt"
		tagline = u"Anzahl Merklisteneinträge: %s" % str(len(my_items)) 	# Info-Button
		s1		= u"Einträge entfernen: via Kontextmenü hier oder am am Ursprungsort im Addon."
		s2		= u"Merkliste filtern: via Kontextmenü hier.\nAktueller Filter: [COLOR blue]%s[/COLOR]" % mf
		s3		= u"Ordner im Titel der Einträge lassen sich in den Settings ein-/ausschalten"
		if SETTINGS.getSetting('pref_merkordner') == 'true':
			s3 = s3 + u"[COLOR blue] (eingeschaltet)[/COLOR]"
		else:
			s3 = s3 + " (ausgeschaltet)"
		summary	= u"%s\n\n%s\n\n%s"		% (s1, s2, s3)
		label	= u'Infos zum Menü Merkliste'
	

	# Info-Button ausblenden falls Setting true
	if SETTINGS.getSetting('pref_FavsInfoMenueButton') == 'false':		
		fparams="&fparams={'mode': '%s'}"	% mode						# Info-Menü
		addDir(li=li, label=label, action="dirList", dirID="ShowFavs",
			fanart=R(ICON_DIR_FAVORITS), thumb=R(ICON_INFO), fparams=fparams,
			summary=summary, tagline=tagline, cmenu=False) 	# ohne Kontextmenü)	
	
	item_cnt=0; cnt=-1
	for fav in my_items:
		if selected:									# Auswahl (Suchergebnisse) beachten
			cnt = cnt + 1
			if cnt not in selected:	
				continue
		
		#fav = unquote_plus(fav)						# urllib2.unquote erzeugt + aus Blanks!		
		fav = unquote(fav)								# kleineres Übel (unquote_plus entfernt + im Eintrag)
		fav_org = fav		
		
		# PLog('fav_org: ' + fav_org)
		name=''; merkname=''; thumb=''; dirPars=''; fparams='';	ordner=''		
		name 	= re.search(' name="(.*?)"', fav) 			# name, thumb,Plot zuerst
		ordner 	= stringextract(' ordner="', '"',fav) 
		thumb 	= stringextract(' thumb="', '"',fav) 
		Plot_org = stringextract(' Plot="', '"',fav) 		# ilabels['Plot']
		Plot_org = Plot_org.replace(' Plot="', ' Plot=""')  # leer
		if name: 	
			name 	= name.group(1)
			name 	= unescape(name)

		# thumb-Pfad an lokales Addon anpassen (externe Merkliste) -
		# kein Test pref_merkextern (andere Gründe möglich, z.B. manuell
		# kopiert):
		my_thumb = thumb
		if thumb and mode == 'Merk':  # and SETTINGS.getSetting('pref_merkextern') == 'true':
			if thumb.startswith('http') == False:	
				if '/addons/' in thumb:
					home_thumb, icon = thumb.split('/addons/')
					myhome = xbmc.translatePath("special://home")
					my_thumb = "%saddons/%s" % (myhome, icon)
					PLog("home_thumb: %s, my_thumb: %s" % (home_thumb, my_thumb))
		
		if myfilter and len(selected) ==  0:				# Filterabgleich - nicht bei Auswahlliste 
			if 'ohne Zuordnung' in myfilter:				# merkliste.xml: ordner=""
				if ordner:
					continue
			else:
				if ordner != myfilter: 						# ausfiltern
						continue
			
		if mode == 'Merk' and 'plugin://plugin' not in fav:	# Base64-kodierte Plugin-Url
			PLog('base64_fav')
			fav = fav.replace('10025,&quot;', '10025,"')	# Quotierung Anfang entfernen
			fav = fav.replace('&quot;,return', '",return')	# Quotierung Ende entfernen					
			p1, p2 	= fav.split('",return)</merk>')	# Endstück p2: &quot;,return)</merk>
			p3, b64	=  p1.split('10025,"')					# p1=Startstück, b64=kodierter string
			b64_clean = convBase64(b64)						# Dekodierung mit oder ohne padding am Ende
			if b64_clean == False:							# Fehler mögl. bei unkodierter Url
				msg1 = "Problem bei Base64-Dekodierung: %s" % name
				PLog(msg1)
				#MyDialog(msg1, '', '')					# 30.06.2020: nicht mehr verwerfen			
				#continue
			else:	
				b64_clean=unquote_plus(b64_clean)		# unquote aus addDir-Call
				b64_clean=unquote_plus(b64_clean)		# unquote aus Kontextmenü
				#PLog(b64_clean)
				fav		= p3 + '10025,"' + b64_clean + p2 

		fav = fav.replace('&quot;', '"')					# " am Ende fparams
		fav = fav.replace('&amp;', '&')						# Verbinder &
		PLog('fav_b64_clean: ' + fav)
		dirPars	= re.search('action=(.*?)&fparams',fav)		# dirList&dirID=PlayAudio&fanart..
		fparams = stringextract('&fparams={', '}',fav)
		fparams = unquote_plus(fparams)				# Parameter sind zusätzl. quotiert
		PLog('fparams1: ' + fparams);
		
		try:
			dirPars = dirPars.group(1)
		except:
			dirPars = ''
		PLog('dirPars: ' + dirPars);
		mediatype=''										# Kennz. Videos im Listing
		CallFunction = stringextract("&dirID=", "&", dirPars) 
		PLog('CallFunction: ' + CallFunction)
		for f in CallFunctions:								# Parameter Merk='true' anhängen
			if f in CallFunction:			
				if SETTINGS.getSetting('pref_video_direct') == 'true':
					mediatype='video'
					break		
		PLog('mediatype: ' + mediatype)
		
		modul = "Haupt-PRG"
		dirPars = unescape(dirPars); 
		if 'resources.lib.' in dirPars:
			modul = stringextract('resources.lib.', ".", dirPars) 
		
		PLog(name); PLog(thumb); PLog(Plot_org); PLog(dirPars); PLog(modul); PLog(mediatype);
		PLog('fparams2: ' + fparams);
			
		# Begleitinfos aus fparams holen - Achtung Quotes!		# 2. fparams auswerten
		fpar_tag = stringextract("tagline': '", "'", fparams) 
		fpar_summ = stringextract("summ': '", "'", fparams)
		if fpar_summ == '':
			fpar_summ = stringextract("summary': '", "'", fparams)
		fpar_plot= stringextract("Plot': '", "'", fparams) 
		fpar_path= stringextract("path': '", "'", fparams) # PodFavoriten
		
		action=''; dirID=''; fanart=''; summary=''; tagline=''; Plot=''
		if dirPars:
			dirPars = dirPars.split('&')					# 3. addDir-Parameter auswerten
			action	= dirPars[0] # = dirList 				#	ohne fparams, name + thumb s.o.
			del dirPars[0]
			for dirPar in dirPars:
				if 	dirPar.startswith('dirID'):		# dirID=PlayAudio
					dirID = dirPar.split('=')[1]
				if 	dirPar.startswith('fanart'):		
					fanart = dirPar[7:]				# '=' ev. in Link enthalten 
				if 	dirPar.startswith('thumb'):		# s.o. - hier aktualisieren
					thumb = dirPar[6:]				# '=' ev. in Link enthalten 
				if 	dirPar.startswith('summary'):		
					summary = dirPar.split('=')[1]
				if 	dirPar.startswith('tagline'):		
					tagline = dirPar.split('=')[1]
				if 	dirPar.startswith('Plot'):		# zusätzl. Plot in fparams möglich
					Plot = dirPar.split('=')[1]
				#if 	dirPar.startswith('mediatype'):		# fehlt in Kodi's Fav-Funktion 	
				#	mediatype = dirPar.split('=')[1]
		
			
		PLog('dirPars:'); PLog(action); PLog(dirID); PLog(fanart); PLog(thumb);
		PLog(Plot_org); PLog(fpar_plot); PLog(Plot);
		if SETTINGS.getSetting('pref_nohome') == 'true':	# skip Homebutton
			if 'Main' in dirID or  u'Zurück im' in dirID:
				continue	

		
		if summary == '':							# Begleitinfos aus fparams verwenden
			summary = fpar_summ
		if tagline == '':	
			tagline = fpar_tag
		if Plot_org == '':
			Plot = fpar_plot		# fparams-Plot
		else:
			Plot = Plot_org

		if Plot:									# Merkliste: Plot im Kontextmenü (addDir)
			if mode == 'Favs':						# Fav's: Plot ev. in fparams enthalten (s.o.)
				if tagline in Plot:
					tagline = ''
				if summary == '' or summary == None:# Plot -> summary					
					summary = Plot
			else:
				tagline = '' 						# falls Verwendung von tagline+summary aus fparams:
				summary = Plot						#	non-ascii-chars entfernen!
						
		summary = unquote_plus(summary); tagline = unquote_plus(tagline); 
		Plot = unquote_plus(Plot)
		summary = summary.replace('+', ' ')
		summary = summary.replace('&quot;', '"')
			
		Plot=unescape(Plot)
		Plot = Plot.replace('||', '\n')			# s. PlayVideo
		Plot = Plot.replace('+|+', '')	
		if Plot.strip().startswith('stage|'):	# zdfMobile: nichtssagenden json-Pfad löschen
			Plot = 'Beitrag aus zdfMobile' 
		PLog('summary: ' + summary); PLog('tagline: ' + tagline); PLog('Plot: ' + Plot)
		
		if SETTINGS.getSetting('pref_FavsInfo') ==  'false':	# keine Begleitinfos 
			summary='';  tagline=''
			
		PLog('fanart: ' + fanart); PLog('thumb: ' + thumb);
		fparams = fparams.replace('\n', '||')				# json-komp. für func_pars in router()
		fparams = unquote_plus(fparams)
		fparams ="&fparams={%s}" % quote_plus(fparams)		# router-kompatibel			
		PLog('fparams3: ' + fparams)
		fanart = R(ICON_DIR_WATCH)
		if mode == 'Favs':
			fanart = R(ICON_DIR_FAVORITS)
		
		summary = summary.replace('||', '\n')		# wie Plot	
		tagline = tagline.replace('||', '\n')
		
		if modul != "ardundzdf":					# Hinweis Modul
			tagline = "[B]Modul: %s[/B]%s" % (modul, tagline)
		if SETTINGS.getSetting('pref_merkordner') == 'true':	
			merkname = name								# für Kontextmenü Ordner in addDir
			if ordner:									# Hinweis Ordner
				if 'COLOR red' in tagline:				# bei Modul plus LF
					tagline = "[B][COLOR blue]Ordner: %s[/COLOR][/B]\n%s" % (ordner, tagline)
				else:
					tagline = "[B][COLOR blue]Ordner: %s[/COLOR][/B] | %s" % (ordner, tagline)
				
			if SETTINGS.getSetting('pref_WatchFolderInTitle') ==  'true':	# Kennz. Ordner
				if ordner: 
					name = "[COLOR blue]%s[/COLOR] | %s" % (ordner, name)

		sortlabel = "ShowFavs"						# 16.11.2021 z.Z. nicht genutzt
		addDir(li=li, label=name, action=action, dirID=dirID, fanart=fanart, thumb=my_thumb,
			summary=summary, tagline=tagline, fparams=fparams, mediatype=mediatype, 
			sortlabel=sortlabel, merkname=merkname)
		item_cnt = item_cnt + 1
		
	if item_cnt == 0:								# Ordnerliste leer?
		if myfilter:								# Deadlock
			heading = u'Leere Merkliste mit dem Filter: %s' % myfilter
			msg1 = u'Der Filter wird nun gelöscht; die Merkliste wird ohne Filter geladen.'
			msg2 = u'Wählen Sie dann im Kontextmenü einen anderen Filter.'
			MyDialog(msg1,msg2,heading=heading)
			if os.path.exists(MERKFILTER):
				os.remove(MERKFILTER)
			# ShowFavs('Merk')						# verdoppelt Home- + Infobutton
			xbmc.executebuiltin('Container.Refresh')
		else:
			heading = u'Leere Merkliste'
			msg1 = 'Diese Merkliste ist noch leer.'
			msg2 = u'Einträge werden über das Kontextmenü hinzugefügt'
			MyDialog(msg1,msg2,heading=heading)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
#-------------------------------------------------------
# convBase64 dekodiert base64-String für ShowFavs bzw. gibt False zurück
#	Base64 füllt den String mittels padding am Ende (=) auf ein Mehrfaches von 4 auf.
# aus https://stackoverflow.com/questions/12315398/verify-is-a-string-is-encoded-in-base64-python	
# 17.11.2019 mit Modul six zusätzl. unquote_plus erforderlich 
#
def convBase64(s):
	PLog('convBase64:')
	PLog(s[:80])
	try:
		if len(s.strip()) % 4 == 0:
			if PYTHON2:					
				s = base64.decodestring(s)
			else:
				s =  base64.b64decode(s)
				s = s.decode("utf-8") 
			return unquote_plus(s)		
	except Exception as exception:
		PLog(str(exception))
	return False
			
####################################################################################################
# Addon-interne Merkliste : Hinzufügen / Löschen
#	verlagert nach resources/lib/merkliste.py - Grund: bei Verarbeitung hier war kein
#	ein Verbleib im akt. Addon-Listing möglich.
#def Watch(action, name, thumb='', Plot='', url=''):
# 23.01.2021 Wegfall parseLinks_Mp4_Rtmp nach Umstellung auf Sofortstart-Erweiterungen:  				
#def parseLinks_Mp4_Rtmp(page, ID=''):	
#	
####################################################################################################
# 03.06.2021 get_sendungen (Classic) entfernt
####################################################################################################
# LiveListe Vorauswahl - verwendet lokale Playlist
# 
def SenderLiveListePre(title, offset=0):	# Vorauswahl: Überregional, Regional, Privat
	title = unquote(title)
	PLog('SenderLiveListePre:')
	PLog('title: ' + title)
	playlist = RLoad(PLAYLIST)	# lokale XML-Datei (Pluginverz./Resources)
	# PLog(playlist)		# nur bei Bedarf

	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button
		
	liste = blockextract('<channel>', playlist)
	PLog(len(liste))
	
	for element in liste:
		name = stringextract('<name>', '</name>', element)
		if 'ARD Audio Event Streams' in name:							# -> Radio-Livestreams			
			continue
		img = stringextract('<thumbnail>', '</thumbnail>', element) # channel-thumbnail in playlist
		if img.find('://') == -1:	# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
			img = R(img)
		else:
			img = img
		PLog(name); PLog(img); # PLog(element);  # nur bei Bedarf
		
		name=py2_encode(name); 
		fparams="&fparams={'title': '%s', 'listname': '%s', 'fanart': '%s'}" % (quote(name), quote(name), img)
		addDir(li=li, label=name, action="dirList", dirID="SenderLiveListe", fanart=R(ICON_MAIN_TVLIVE), 
			thumb=img, fparams=fparams)

	laenge = SETTINGS.getSetting('pref_LiveRecord_duration')
	if SETTINGS.getSetting('pref_LiveRecord_input') == 'true':
		laenge = "wird manuell eingegeben"

	title = 'EPG Alle JETZT | Recording TV-Live'; 
	summary =u'elektronischer Programmführer\n\nAufnehmen via Kontexmenü, Dauer: %s (siehe Settings)' % laenge
	tagline = 'zeigt die laufende Sendung für jeden Sender | Quelle: tvtoday.de'
	title=py2_encode(title);
	fparams="&fparams={'title': '%s'}" % title
	addDir(li=li, label=title, action="dirList", dirID="EPG_ShowAll", fanart=R('tv-EPG-all.png'), 
		thumb=R('tv-EPG-all.png'), fparams=fparams, summary=summary, tagline=tagline)
							
	title = 'EPG Sender einzeln'; 										# EPG-Button Einzeln anhängen
	if SETTINGS.getSetting('pref_epgRecord') == 'true':		
		title = 'EPG Sender einzeln | Sendungen mit EPG aufnehmen'; 
	tagline = u'zeigt für den ausgewählten Sender ein 12-Tage-EPG | Quelle: tvtoday.de'
	summary='je Seite: 24 Stunden (zwischen 05.00 und 05.00 Uhr des Folgetages)'
	fparams="&fparams={'title': '%s'}" % title
	addDir(li=li, label=title, action="dirList", dirID="EPG_Sender", fanart=R(ICON_MAIN_TVLIVE), 
		thumb=R('tv-EPG-single.png'), fparams=fparams, summary=summary, tagline=tagline)	
		
	PLog(str(SETTINGS.getSetting('pref_LiveRecord'))) 
	if SETTINGS.getSetting('pref_LiveRecord') == 'true':		
		title = 'Recording TV-Live'										# TVLiveRecord-Button anhängen
		summary = u'Sender wählen und direkt aufnehmen.\nDauer: %s (siehe Settings)' % laenge
		tagline = 'Downloadpfad: %s' 	 % SETTINGS.getSetting('pref_download_path') 				
		fparams="&fparams={'title': '%s'}" % title
		addDir(li=li, label=title, action="dirList", dirID="TVLiveRecordSender", fanart=R(ICON_MAIN_TVLIVE), 
			thumb=R('icon-record.png'), fparams=fparams, summary=summary, tagline=tagline)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

	
#-----------------------------------------------------------------------------------------------------
# EPG SenderListe - Liste aus livesenderTV.xml sortiert
# Zeilen-Index: title=rec[0]; EPG_ID=rec[1]; img=rec[2]; link=rec[3];	
# 	EPG-Daten:  -> EPG_ShowSingle ("EPG Sender einzeln")
#	ohne EPG:	-> SenderLiveResolution
# Aufrufer SenderLiveListePre
# 
#
def EPG_Sender(title, Merk='false'):
	PLog('EPG_Sender:')
	
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button
	
	sort_playlist = get_sort_playlist()	# Senderliste + Cache
	# PLog(sort_playlist)
	
	summ = u"für die Merkliste (Kontextmenü) sind die Einträge dieser Liste wegen des EPG besser geeignet"
	summ = u"%s als die Menüs Überregional, Regional und Privat" % summ
	
	for rec in sort_playlist:
		title = rec[0]
		img = rec[2]
		if u'://' not in img:	# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
			img = R(img)
		link = rec[3]
		ID = rec[1]
		
		PLog("Satz13:")
		PLog('title: %s, ID: %s' % (title, ID))
		PLog(img)
		if ID == '':				# ohne EPG_ID
			title = title + ': [B]ohne EPG[/B]' 
			title=py2_encode(title); link=py2_encode(link); img=py2_encode(img); 
			fparams="&fparams={'path': '%s', 'title': '%s', 'thumb': '%s', 'descr': '', 'Merk': '%s'}" %\
				(quote(link), quote(title), quote(img), Merk)
			addDir(li=li, label=title, action="dirList", dirID="SenderLiveResolution", fanart=R('tv-EPG-single.png'), 
				thumb=img, fparams=fparams, tagline='weiter zum Livestream', summary=summ)
		else:
			add = ''
			if SETTINGS.getSetting('pref_epgRecord') == 'true':
				add = u" und zum Aufnehmen via Kontextmenü"
			title=py2_encode(title); link=py2_encode(link);
			fparams="&fparams={'ID': '%s', 'name': '%s', 'stream_url': '%s', 'pagenr': %s}" % (ID, quote(title), 
				quote(link), '0')
			addDir(li=li, label=title, action="dirList", dirID="EPG_ShowSingle", fanart=R('tv-EPG-single.png'), thumb=img, 
				fparams=fparams, tagline='weiter zum EPG' + add, summary=summ)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
#-----------------------------
#	Liste aller TV-Sender wie EPG_Sender, hier mit Aufnahme-Button
def TVLiveRecordSender(title):
	PLog('TVLiveRecordSender:')
	title = unquote(title)
	
	if check_Setting('pref_LiveRecord_ffmpegCall') == False:	
		return
	
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)					# Home-Button
	
	duration = SETTINGS.getSetting('pref_LiveRecord_duration')
	duration, laenge = duration.split('=')
	duration = duration.strip()

	sort_playlist = get_sort_playlist()		# Senderliste + Cache
	PLog('Sender: ' + str(len(sort_playlist)))
	for rec in sort_playlist:
		title 	= rec[0]
		ID 		= rec[1]
		img 	= rec[2]
		if u'://' not in img:	# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
			img = R(img)
		link 	= rec[3]
		if ID == '':				# ohne EPG_ID
			title = title + ': [B]ohne EPG[/B]' 
		if SETTINGS.getSetting('pref_LiveRecord_input') == 'true':
			laenge = "wird manuell eingegeben"
		summ 	= 'Aufnahmedauer: %s' 	% laenge
		summ	= u"%s\n\nStart ohne Rückfrage!" % summ
		tag		= 'Zielverzeichnis: %s' % SETTINGS.getSetting('pref_download_path')
		
		PLog("RecordSender: %s, %s" % (title, link))
		PLog(str(rec))
		title=py2_encode(title); link=py2_encode(link);
		fparams="&fparams={'url': '%s', 'title': '%s', 'duration': '%s', 'laenge': '%s'}" \
			% (quote(link), quote(title), duration, laenge)
		addDir(li=li, label=title, action="dirList", dirID="LiveRecord", fanart=R(rec[2]), thumb=img, 
			fparams=fparams, summary=summ, tagline=tag)
		
	# Wechsel-Button zu den DownloadTools:	
	tagline = 'Downloads und Aufnahmen: Verschieben, Löschen, Ansehen, Verzeichnisse bearbeiten'
	fparams="&fparams={}"
	addDir(li=li, label='Download- und Aufnahme-Tools', action="dirList", dirID="DownloadTools", 
		fanart=R(FANART), thumb=R(ICON_DOWNL_DIR), tagline=tagline, fparams=fparams)	
			
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#-----------------------------
# 30.08.2018 Start Recording TV-Live
# Doku z. PHT-Problemen s. ältere Versionen
#
# 29.04.0219 Erweiterung manuelle Eingabe der Aufnahmedauer
# Check auf ffmpeg-Settings bereits in TVLiveRecordSender, Check auf LiveRecord-Setting
# 	bereits in SenderLiveListePre
# 04.07.2020 angepasst für epgRecord (Eingabe Dauer entf., Dateiname mit Datumformat 
#		geändert, Notification statt Dialog. epgJob enthält Aufnahmestart (Unixformat)
# 		LiveRecord verlagert nach util (import aus  ardundzdf klappt nicht in epgRecord,
#		dto. MakeDetailText).
#		
# 29.06.0219 Erweiterung "Sendung aufnehmen", Call K-Menü <- EPG_ShowSingle
# Check auf Setting pref_epgRecord in EPG_ShowSingle
# 30.08.2020 Wegfall m3u8-Verfahren: Mehrkanal-Check entf. (dto. in LiveRecord)
#
def ProgramRecord(url, sender, title, descr, start_end):
	PLog('ProgramRecord:')
	PLog(url); PLog(sender); PLog(title); 
	PLog(start_end);
			
	now = EPG.get_unixtime(onlynow=True)
	
	start, end = start_end.split('|')				# 1593627300|1593633300
	s = datetime.datetime.fromtimestamp(int(start))
	von = s.strftime("%d.%m.%Y, %H:%M")	
	s = datetime.datetime.fromtimestamp(int(end))
	bis = s.strftime("%d.%m.%Y, %H:%M")	
	PLog("now %s, von %s, bis %s"% (now, von, bis))
	
	#----------------------------------------------				# Voraussetzungen prüfen
	if check_Setting('pref_LiveRecord_ffmpegCall') == False:	# Dialog dort
		return			
	if check_Setting('pref_download_path') == False:			# Dialog dort
		return			
	
	if start == '' or end == '':					# sollte nicht vorkommen
		msg1 = "%s: %s" % (sender, title)
		msg2 = "Sendezeit fehlt - Abbruch"
		MyDialog(msg1, msg2, '')
		return
	if end < now:
		msg1 = "%s: %s\nSendungsende: %s" % (sender, title, bis)
		msg2 = "diese Sendung ist bereits vorbei - Abbruch"
		MyDialog(msg1, msg2, '')
		return

	#----------------------------------------------				# Aufnehmen
	msg2 = "von [B]%s[/B] bis [I][B]%s[/B][/I]" % (von, bis) 	# Stil- statt Farbmarkierung 
	msg3 = "Sendung aufnehmen?" 
	if start < now and end > now:					# laufende Sendung
		msg1 = u"läuft bereits: %s" % title
	else:											# künftige Sendung
		msg1 = u"Aufnehmen: %s" % title 		
	ret = MyDialog(msg1=msg1, msg2=msg2, msg3=msg3, ok=False, cancel='Abbruch', yes='JA', heading='Sendung aufnehmen')
	if ret == False:
		return			
		
	action="setjob"
	# action="test_jobs"	# Debug
	epgRecord.JobMain(action, start_end, title, descr, sender, url)
	return
	
#---------------------------------------------
# Aufruf: EPG_Sender, EPG_ShowAll, TVLiveRecordSender
# get_sort_playlist: Senderliste + Cache 
# erstellt sortierte Playlist für TV-Sender in livesenderTV.xml
#	im Abgleich mit TV-Livestream-Cache
#
def get_sort_playlist():						# Senderliste für EPG + Recording
	PLog('get_sort_playlist:')
	playlist = RLoad(PLAYLIST)					# lokale XML-Datei (Pluginverz./Resources)
	stringextract('<channel>', '</channel>', playlist)	# ohne Header
	playlist = blockextract('<item>', playlist)
	sort_playlist =  []
	zdf_streamlinks = get_ZDFstreamlinks(skip_log=True)				# skip_log: Log-Begrenzung
	ard_streamlinks = get_ARDstreamlinks(skip_log=True)
	iptv_streamlinks = get_IPTVstreamlinks(skip_log=True)
	
	for item in playlist:   
		rec = []
		title = stringextract('<title>', '</title>', item)
		# PLog(title)
		title = up_low(title)										# lower-/upper-case für sort() relevant
		EPG_ID = stringextract('<EPG_ID>', '</EPG_ID>', item)
		img = 	stringextract('<thumbnail>', '</thumbnail>', item)
		link =  stringextract('<link>', '</link>', item)			# url für Livestreaming
		if "<reclink>" in item:
			link =  stringextract('<reclink>', '</reclink>', item)	# abw. Link, zum Aufnehmen geeignet
		
		if 'ZDFsource' in link:
			title_sender = stringextract('<hrefsender>', '</hrefsender>', item)	
			link=''										# Reihenfolge an Playlist anpassen
			# Zeile zdf_streamlinks: "webtitle|href|thumb|tagline"
			for line in zdf_streamlinks:
				items = line.split('|')
				# Bsp.: "ZDFneo " in "ZDFneo Livestream":
				#PLog("ZDFsource: %s || %s" % (title_sender, str(items)))
				if up_low(title_sender) in up_low(items[0]): 
					link = items[1]
					PLog("found: %s || %s" % (title_sender, str(items)))
					break
			if link == '':
				PLog('%s: Streamlink fehlt' % title_sender)	
						
		if 'ARDSource' in link:							# Streamlink für ARD-Sender holen,
			title_sender = stringextract('<hrefsender>', '</hrefsender>', item)	
			link=''										# Reihenfolge an Playlist anpassen
			# Zeile ard_streamlinks: "webtitle|href|thumb|tagline"
			for line in ard_streamlinks:
				#PLog("ARDSource: %s || %s" % (title_sender, str(items)))
				items = line.split('|')
				if up_low(title_sender) in up_low(items[0]): 
					link = items[1]
					break
			if link == '':
				PLog('%s: Streamlink fehlt' % title_sender)
		
		if 'IPTVSource' in link:						# Streamlink für private Sender holen
			title_sender = stringextract('<title>', '</title>', item)	
			link=''										# Reihenfolge an Playlist anpassen
			# Zeile iptv_streamlinks: "Sender|href|thumb|tagline"
			for line in iptv_streamlinks:
				#PLog("IPTVSource: %s || %s" % (title_sender, str(items)))
				items = line.split('|')
				if up_low(title_sender) in up_low(items[0]): 
					link = items[1]
					if items[2]:						# Icon aus IPTVSource?
						img = items[2]
					break
			if link == '':
				PLog('%s: Streamlink fehlt' % title_sender)
		
		rec.append(title); rec.append(EPG_ID);						# Listen-Element
		rec.append(img); rec.append(link);
		sort_playlist.append(rec)									# Liste Gesamt
	
	# Zeilen-Index: title=rec[0]; EPG_ID=rec[1]; img=rec[2]; link=rec[3];	
	sort_playlist = sorted(sort_playlist,key=lambda x: x[0])		# Array-sort statt sort()
	return sort_playlist
	
#-----------------------------------------------------------------------------------------------------
# Aufrufer EPG_Sender (falls EPG verfügbar)
# 	EPG-Daten holen in Modul EPG  (1 Woche), Listing hier jew. 1 Tag, 
#	JETZT-Markierung für laufende Sendung
# Klick zum Livestream -> SenderLiveResolution 
# 29.06.2020 Erweiterung Kontextmenü "Sendung aufnehmen" (s. addDir), 
#	Trigger start_end (EPG-Rekord mit endtime erweitert) -> ProgramRecord
#
def EPG_ShowSingle(ID, name, stream_url, pagenr=0):
	PLog('EPG_ShowSingle:'); 
	Sender = name
	PLog(Sender)

	EPG_rec = EPG.EPG(ID=ID, day_offset=pagenr)		# Daten holen
	PLog(len(EPG_rec))
	
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button
	
	if len(EPG_rec) == 0:			# kann vorkommen, Bsp. SR
		msg1 = 'Sender %s:' % name 
		msg2 = 'keine EPG-Daten gefunden'
		MyDialog(msg1, msg2, '')
		return li
		
	today_human = 'ab ' + EPG_rec[0][7]
			
	for rec in EPG_rec:
		href=rec[1]; img=rec[2]; sname=rec[3]; stime=rec[4]; summ=rec[5]; vonbis=rec[6];
		starttime=rec[0]; endtime=rec[8]; 
		start_end = ''										# Trigger K-Menü
		if SETTINGS.getSetting('pref_epgRecord') == 'true':	
			start_end = "%s|%s" % (starttime, endtime)		# Unix-Format -> ProgramRecord

		if img.find('http') == -1:	# Werbebilder today.de hier ohne http://, Ersatzbild einfügen
			img = R('icon-bild-fehlt.png')
		sname = unescape(sname)
		title = sname
		summ = unescape(summ)
		if 'JETZT' in title:			# JETZT-Markierung unter icon platzieren
			# Markierung für title bereits in EPG
			summ = "[B]LAUFENDE SENDUNG![/B]\n\n%s" % summ
			title = sname
		PLog("title: " + title)
		tagline = 'Zeit: ' + vonbis
		descr = summ.replace('\n', '||')		# \n aus summ -> ||
		title=py2_encode(title); stream_url=py2_encode(stream_url);
		img=py2_encode(img); descr=py2_encode(descr);
		Sender=py2_encode(Sender);
		fparams="&fparams={'path': '%s','title': '%s','thumb': '%s','descr': '%s','Sender': '%s'}" %\
			(quote(stream_url), quote(title), quote(img), quote(descr), quote(Sender))
		addDir(li=li, label=title, action="dirList", dirID="SenderLiveResolution", fanart=R('tv-EPG-single.png'), 
			thumb=img, fparams=fparams, summary=summ, tagline=tagline, start_end=start_end)
			
	# Mehr Seiten anzeigen:
	max = 12
	pagenr = int(pagenr) + 1
	if pagenr < max: 
		summ = u'nächster Tag'
		name=py2_encode(name); stream_url=py2_encode(stream_url);
		fparams="&fparams={'ID': '%s', 'name': '%s', 'stream_url': '%s', 'pagenr': %s}" % (ID, quote(name),
			quote(stream_url), pagenr)
		addDir(li=li, label=summ, action="dirList", dirID="EPG_ShowSingle", fanart=R('tv-EPG-single.png'), 
		thumb=R(ICON_MEHR), fparams=fparams, summary=summ)
		
	# Wechsel-Button zu den DownloadTools:	
	tagline = 'Downloads und Aufnahmen: Verschieben, Löschen, Ansehen, Verzeichnisse bearbeiten'
	fparams="&fparams={}"
	addDir(li=li, label='Download- und Aufnahme-Tools', action="dirList", dirID="DownloadTools", 
		fanart=R(FANART), thumb=R(ICON_DOWNL_DIR), tagline=tagline, fparams=fparams)	
		

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
#-----------------------------------------------------------------------------------------------------
# EPG: aktuelle Sendungen aller Sender mode='allnow'
# Aufrufer SenderLiveListePre (Button 'EPG Alle JETZT')
#	26.04.2019 Anzahl pro Seite auf 20 erhöht (Timeout bei Kodi kein Problem wie bei Plex)  
# sort_playlist: Senderabgleich in livesenderTV.xml mit direkten Quellen + Cachenutzung
#
def EPG_ShowAll(title, offset=0, Merk='false'):
	PLog('EPG_ShowAll:'); PLog(offset) 
	title = unquote(title)
	title_org = title
	title2='Aktuelle Sendungen'
	
	import resources.lib.EPG as EPG
	
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button

	# Zeilen-Index: title=rec[0]; EPG_ID=rec[1]; img=rec[2]; link=rec[3];	
	sort_playlist = get_sort_playlist()				# Senderliste + Cache
	PLog(len(sort_playlist))
	# PLog(sort_playlist)
	
	rec_per_page = 25								# Anzahl pro Seite (Plex: Timeout ab 15 beobachtet)
	max_len = len(sort_playlist)					# Anzahl Sätze gesamt
	start_cnt = int(offset) 						# Startzahl diese Seite
	end_cnt = int(start_cnt) + int(rec_per_page)	# Endzahl diese Seite
	
	icon = R('tv-EPG-all.png')
	xbmcgui.Dialog().notification("lade EPG-Daten",u"max. Anzahl: %d" % rec_per_page,icon,5000)
	
	PLog("walk_playlist")
	for i in range(len(sort_playlist)):
		cnt = int(i) + int(offset)
		# PLog(cnt); PLog(i)
		if int(cnt) >= max_len:				# Gesamtzahl überschritten?
			break
		if i >= rec_per_page:				# Anzahl pro Seite überschritten?
			break
		rec = sort_playlist[cnt]
		# PLog(rec)							# Satz ['ARTE', 'ARTE', 'tv-arte.png', ..

		title_playlist = rec[0]
		m3u8link = rec[3]
		img_playlist = rec[2]	
		if u'://' not in img_playlist:		# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
			img_playlist = R(img_playlist)
		ID = rec[1]
		summ = ''
		
		tagline = 'weiter zum Livestream'
		if ID == '':									# ohne EPG_ID
			title = "[COLOR grey]%s[/COLOR]" % title_playlist + ' | [B]ohne EPG[/B]'
			img = img_playlist
			PLog("img: " + img)
		else:
			# Indices EPG_rec: 0=starttime, 1=href, 2=img, 3=sname, 4=stime, 5=summ, 6=vonbis: 
			rec = EPG.EPG(ID=ID, mode='OnlyNow')		# Daten holen - nur aktuelle Sendung
			# PLog(rec)	# bei Bedarf
			if len(rec) == 0:							# EPG-Satz leer?
				title = "[COLOR grey]%s[/COLOR]" % title_playlist + ' | ohne EPG'
				img = img_playlist			
			else:	
				href=rec[1]; img=rec[2]; sname=rec[3]; stime=rec[4]; summ=rec[5]; vonbis=rec[6]
				PLog("img: " + img)
				if type(img) != list:			# Ursache Listobjekt n.b.
					if img.find('http') == -1:	# Werbebilder today.de hier ohne http://, Ersatzbild einfügen
						img = R('icon-bild-fehlt.png')
				title=py2_decode(title); sname=py2_decode(sname); title_playlist=py2_decode(title_playlist);
				title 	= sname.replace('JETZT', title_playlist)		# JETZT durch Sender ersetzen
				# sctime 	= "[COLOR red] %s [/COLOR]" % stime			# Darstellung verschlechtert
				# sname 	= sname.replace(stime, sctime)
				tagline = '%s | Zeit: %s' % (tagline, vonbis)
				
		descr = summ.replace('\n', '||')
		duration = SETTINGS.getSetting('pref_LiveRecord_duration')
		duration, laenge = duration.split('=')
		laenge = laenge.strip()
		summ 	= "%s\n\n%s" % (summ, u"Kontextmenü: Recording TV-Live (Aufnahmedauer: %s)" % laenge)	
		title = unescape(title)
		
		PLog("Satz14:")
		PLog("title: " + title); PLog(m3u8link); PLog(summ)
		
		title=py2_encode(title); m3u8link=py2_encode(m3u8link);
		img=py2_encode(img); descr=py2_encode(descr); summ=py2_encode(summ);		
		fparams="&fparams={'path': '%s', 'title': '%s', 'thumb': '%s', 'descr': '%s', 'Merk': '%s'}" %\
			(quote(m3u8link), quote(title), quote(img), quote_plus(descr), Merk)
		addDir(li=li, label=title, action="dirList", dirID="SenderLiveResolution", fanart=R('tv-EPG-all.png'), 
			thumb=img, fparams=fparams, summary=summ, tagline=tagline, start_end="Recording TV-Live")

	icon = R('tv-EPG-all.png')
	xbmcgui.Dialog().notification("EPG-Daten geladen", "",icon,2000)
	
	# Mehr Seiten anzeigen:
	# PLog(offset); PLog(cnt); PLog(max_len);
	if (int(cnt) +1) < int(max_len): 						# Gesamtzahl noch nicht ereicht?
		new_offset = cnt 
		PLog(new_offset)
		summ = 'Mehr %s (insgesamt %s)' % (title2, str(max_len))
		title_org=py2_encode(title_org);
		fparams="&fparams={'title': '%s', 'offset': '%s'}"	% (quote(title_org), new_offset)
		addDir(li=li, label=summ, action="dirList", dirID="EPG_ShowAll", fanart=R('tv-EPG-all.png'), 
			thumb=R(ICON_MEHR), fparams=fparams, summary=summ, tagline=title2)

	# Wechsel-Button zu den DownloadTools:	
	tagline = 'Downloads und Aufnahmen: Verschieben, Löschen, Ansehen, Verzeichnisse bearbeiten'
	fparams="&fparams={}"
	addDir(li=li, label='Download- und Aufnahme-Tools', action="dirList", dirID="DownloadTools", 
		fanart=R(FANART), thumb=R(ICON_DOWNL_DIR), tagline=tagline, fparams=fparams)	

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
#-----------------------------------------------------------------------------------------------------
# TV LiveListe - verwendet lokale Playlist livesenderTV.xml
# onlySender: Button nur für diesen Sender (z.B. ZDFSportschau Livestream für Menü
#	ZDFSportLive)
# 23.06.2020 lokale m3u8-Dateien in livesenderTV.xml sind entfallen
#	Ermittlung Streamlinks im Web (link: ARDSource, ZDFsource)
# 26.05.2022 ergänzt um Nutzung iptv_streamlinks für private Sender
#	(link: IPTVSource)
# 05.02.2023 addDir ergänzt mit EPG_ID für Kontextmenü
#
def SenderLiveListe(title, listname, fanart, offset=0, onlySender=''):			
	# SenderLiveListe -> SenderLiveResolution (reicht nur durch) -> Parseplaylist (Ausw. m3u8)
	#	-> CreateVideoStreamObject 
	PLog('SenderLiveListe:')
	PLog(title); PLog(listname)
				
	title2 = 'Live-Sender ' + title
	title2 = title2
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button
			
	playlist = RLoad(PLAYLIST)							# lokale XML-Datei (Pluginverz./Resources)
	playlist = blockextract('<channel>', playlist)
	PLog(len(playlist)); PLog(listname)
	mylist=''
	for i in range(len(playlist)):						# gewählte Channel extrahieren
		item = playlist[i] 
		name =  stringextract('<name>', '</name>', item)
		# PLog(name)
		if py2_decode(name) == py2_decode(listname):	# Bsp. Überregional, Regional, Privat
			mylist =  playlist[i] 
			break
			
	lname = py2_decode(listname)
	# Streamlinks aus Caches laden (Modul util), ab 01.06.2022 für Überregional,
	#	Regional + Privat. get_sort_playlist entfällt hier:
	zdf_streamlinks = get_ZDFstreamlinks()			# Streamlinks für ZDF-Sender 
	ard_streamlinks = get_ARDstreamlinks()			# ard_streamlinks oder ard_streamlinks_UT
	iptv_streamlinks = get_IPTVstreamlinks()		# private + einige regionale

	PLog(OS_DETECT)									# 07.08.2022 kleine Verbesserung mit Delay:
	if "armv7" in OS_DETECT:						# host: [armv7l]
		xbmc.sleep(1000)							# Test: für Raspi (verhind. Klemmer)

	mediatype='' 						# Kennz. Video für Sofortstart
	if SETTINGS.getSetting('pref_video_direct') == 'true':
		if "Audio Event" in title:		# ARD Audio Event Streams (ARDSportAudioXML:)
			mediatype='music'
		else:
			mediatype='video'

	# abweichend - externe Funktion:
	if u'Regional: WDR' in lname:						# Auswertung + Liste WDR Lokalzeit
		url = "https://www1.wdr.de/fernsehen/livestream/lokalzeit-livestream/index.html" 
		wdr_streamlinks = list_WDRstreamlinks(url)		# Webseite
		return
		
	# Zusatzbutton:
	if u'Privat' in listname:							# Suchfunktion IPTV-Private
		title = u"Suche lokale private IPTV-Sender"
		img = R("suche_iptv.png")
		tag = "Quelle: [B]kodi_tv_local.m3u[/B] im jnk22-Repo auf Github"
		summ = "der zuletzt gefundene IPTV-Sender wird unter diesem Suchbutton eingeblendet."
		title=py2_encode(title)	
		fparams="&fparams={'title': '%s'}" % (quote(title))
		addDir(li=li, label=title, action="dirList", dirID="SenderLiveSearch", fanart=img, thumb=img, 
			fparams=fparams, tagline=tag, summary=summ)
			
		iptv_search = Dict("load", "iptv_search")	# letztes Suchergebnis -> Senderbutton
		if iptv_search:
			tvgname,tvgid,thumb,link = iptv_search.splitlines()
			title=py2_encode(tvgname); link=py2_encode(link);
			thumb=py2_encode(thumb); 
			title = "Suchergebnis: [B]%s[/B]" % tvgname
			summ = "zuletzt gefundener IPTV-Sender: [B]%s[/B]" % tvgname
			fparams="&fparams={'path': '%s', 'thumb': '%s', 'title': '%s', 'descr': ''}" % (quote(link), 
				quote(thumb), quote(title))
			addDir(li=li, label=title, action="dirList", dirID="SenderLiveResolution", fanart=R("suche_iptv.png"), 
				thumb=thumb, fparams=fparams, tagline=tag, summary=summ, mediatype=mediatype)		
				
				
	if SETTINGS.getSetting('pref_use_epg') == 'true':		# Vorab-Info: EPG-Nutzung
		if "Audio" in listname == False:					# nicht bei ARD Audio Event Streams 
			icon = R('tv-EPG-all.png')
			msg1 = ""
			msg2 = "wird aktualisiert"
			xbmcgui.Dialog().notification(msg1,msg2,icon,4000)

	liste = blockextract('<item>', mylist)					# Details eines Senders
	PLog(len(liste));
	EPG_ID_old = ''											# Doppler-Erkennung
	sname_old=''; stime_old=''; summ_old=''; vonbis_old=''	# dto.
	summary_old=''; tagline_old=''
	for element in liste:									# EPG-Daten für einzelnen Sender holen 	
		img_streamlink=''									# Austausch Icon
		element = py2_decode(element)	
		link = stringextract('<link>', '</link>', element) 
		link = unescape(link)	
		title_sender = stringextract('<hrefsender>', '</hrefsender>', element) 
		if title_sender == '':
			title_sender = stringextract('<title>', '</title>', element) # IPTVSource-Sender
		PLog(u'Sender: %s, link: %s' % (title_sender, link));

		# --												# Cache 
		if 'ZDFsource' in link:								# Streamlink für ZDF-Sender holen,
			link=''	
			# Zeile zdf_streamlinks: "webtitle|href|thumb|tagline"
			for line in zdf_streamlinks:
				PLog("zdfline: " + line[:40])
				items = line.split('|')
				# Bsp.: "ZDFneo " in "ZDFneo Livestream":
				if up_low(title_sender) == up_low(items[0]): 
					link = items[1]
					break
			if link == '':
				PLog('%s: Streamlink fehlt' % title_sender)
				
		if 'ARDSource' in link:								# Streamlink für ARD-Sender holen, Ermittlung
			link=''											#	Untertitel ab Okt 2022 in PlayVideo
			# Zeile ard_streamlinks: "webtitle|href|thumb|tagline"
			for line in ard_streamlinks:
				PLog("ardline: " + line[:40])
				items = line.split('|')
				if up_low(title_sender) in up_low(items[0]): 
					link = items[1]							# master.m3u8
					break
			if link == '':
				PLog('%s: Streamlink fehlt' % title_sender)
				
		if 'IPTVSource' in link:							# Streamlink für private Sender holen
			link=''	
			# Zeile iptv_streamlinks: "Sender|href|thumb|tagline"
			for line in iptv_streamlinks:
				PLog("iptvline: " + line[:40])
				items = line.split('|')
				if up_low(title_sender) in up_low(items[0]): 
					link = items[1]
					if items[2]:							# Icon aus IPTVSource?
						img_streamlink = items[2]
					break
			if link == '':
				PLog('%s: Streamlink fehlt' % title_sender)
		# --												# Cache 
				
		
		PLog('Mark2')
		# Spezialbehandlung für N24 in SenderLiveResolution - Test auf Verfügbarkeit der Lastserver (1-4)
		# EPG: ab 10.03.2017 einheitlich über Modul EPG.py (vorher direkt bei den Sendern, mehrere Schemata)
		# 								
		title = stringextract('<title>', '</title>', element)
		if onlySender:										# Button nur für diesen Sender
			title=py2_encode(title); onlySender=py2_encode(onlySender) 
			if title != onlySender:
				continue
			
		epg_date=''; epg_title=''; epg_text=''; summary=''; tagline='' 
		EPG_ID = stringextract('<EPG_ID>', '</EPG_ID>', element)	# -> EPG.EPG und Kontextmenü
		PLog(EPG_ID)
		# PLog(SETTINGS.getSetting('pref_use_epg')) 	# Voreinstellung: EPG nutzen? - nur mit Schema nutzbar
		PLog('setting: ' + str(SETTINGS.getSetting('pref_use_epg')))
		if SETTINGS.getSetting('pref_use_epg') == 'true':
			# Indices EPG_rec: 0=starttime, 1=href, 2=img, 3=sname, 4=stime, 5=summ, 6=vonbis:
			try:
				rec = EPG.EPG(ID=EPG_ID, mode='OnlyNow')	# Daten holen - nur aktuelle Sendung
				if rec == '':								# Fehler, ev. Sender EPG_ID nicht bekannt
					sname=''; stime=''; summ=''; vonbis=''
				else:
					sname=py2_encode(rec[3]); stime=py2_encode(rec[4]); 
					summ=py2_encode(rec[5]); vonbis=py2_encode(rec[6])	
			except:
				sname=''; stime=''; summ=''; vonbis=''	
									
			if sname:
				title=py2_encode(title); 
				title = "%s: %s"  % (title, sname)
			if summ:
				summary = py2_encode(summ)
			else:
				summary = ''
			if vonbis:
				tagline = u'Sendung: %s Uhr' % vonbis
			else:
				tagline = ''

		title = unescape(title)	
		title = title.replace('JETZT:', '')					# 'JETZT:' hier überflüssig
		if link == '':										# fehlenden Link im Titel kennz.
			title = "%s | Streamlink fehlt!" %  title	
		summary = unescape(summary)	
				
		if img_streamlink:									# Vorrang Icon aus direkten Quellen	
			img = img_streamlink 
		else:
			img = stringextract('<thumbnail>', '</thumbnail>', element) 
			if img.find('://') == -1:	# Logo lokal? -> wird aus Resources geladen, Unterverz. leider n.m.
				if img:										# kann fehlen, z.B. bei Privaten
					img = R(img)
				else:				
					img = R(ICON_MAIN_TVLIVE)
			
			
		geo = stringextract('<geoblock>', '</geoblock>', element)
		PLog('geo: ' + geo)
		if geo:
			tagline = 'Livestream nur in Deutschland zu empfangen!'
			
		PLog("Satz8:")
		PLog(title); PLog(link); PLog(img); PLog(summary); PLog(tagline[0:80]);
	
		descr = summary.replace('\n', '||')
		if tagline:
			descr = "%s %s" % (tagline, descr)				# -> Plot (PlayVideo) 
		title=py2_encode(title); link=py2_encode(link);
		img=py2_encode(img); descr=py2_encode(descr);	
		fparams="&fparams={'path': '%s', 'thumb': '%s', 'title': '%s', 'descr': '%s'}" % (quote(link), 
			quote(img), quote(title), quote(descr))
		addDir(li=li, label=title, action="dirList", dirID="SenderLiveResolution", fanart=fanart, thumb=img, 
			fparams=fparams, summary=summary, tagline=tagline, mediatype=mediatype, EPG_ID=EPG_ID)		
	
	#  if onlySender== '':		# obsolet seit V4.4.2 
	# RP3b+: Abstürze möglich beim Öffen der Regional-Liste, Log: clean up-Problem mit Verweis auf classes:
	#	N9XBMCAddon9xbmcaddon5AddonE,N9XBMCAddon9xbmcaddon5AddonE.  Ähnlich issue
	#	https://github.com/asciidisco/plugin.video.netflix/issues/576 aber Fix hier nicht anwendbar.
	# s.a. https://forum.kodi.tv/showthread.php?tid=359608
	# Delay nach Laden der Streamlinks ohne Wirkung (s.o. OS_DETECT)
	# Memory-Bereinig. nach router-Ende unwirksam s. Script-Ende)
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
		
#-----------------------------------------------
# Suche nach IPTV-Livesendern - bisher nur lokale private Sender
#	 aus jnk22-Repo - s. Zusatzbutton SenderLiveListe
def SenderLiveSearch(title):
	PLog('SenderLiveSearch:')

	query = get_keyboard_input() 
	if query == None or query.strip() == '': 	# None bei Abbruch
		return SenderLiveListe("", "","")		# dummy, sonst Absturz nach Sofortstart/Suche
	query = query.strip()
	PLog(query)
	
	url = "https://raw.githubusercontent.com/jnk22/kodinerds-iptv/master/iptv/kodi/kodi_tv_local.m3u"
	page, msg = get_page(url)					
	if page == '':	
		msg1 = "Fehler in get_WRDstreamlinks:"
		msg2=msg
		MyDialog(msg1, msg2, '')	
		return
	PLog(page[:60])
	
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button
	
	mediatype='' 						# Kennz. Video für Sofortstart
	if SETTINGS.getSetting('pref_video_direct') == 'true':
		mediatype='video'
	
	items = blockextract('#EXTINF:', page)
	for item in items:
		if up_low(query) in up_low(item):
			PLog("item: %s" % item)
			tag=""
			tvgname = stringextract('tvg-name="', '"', item)
			tvgid = stringextract('tvg-id="', '"', item)
			thumb = stringextract('tvg-logo="', '"', item)
			links = blockextract('https', item)					# 1. logo, 2. streamlink
			link = links[-1]
			tvgname = py2_decode(tvgname); tvgid = py2_decode(tvgid)
			PLog(tvgid)
			if tvgid:
				tag = "tvg-id: [B]%s[/B]" % tvgid
			PLog(tvgname); PLog(tvgid); PLog(thumb); PLog(link);
			iptv_search = "%s\n%s\n%s\n%s" % (tvgname,tvgid,thumb,link)
			Dict("store", "iptv_search", iptv_search)
			
			title=py2_encode(tvgname); link=py2_encode(link);
			thumb=py2_encode(thumb); 
			fparams="&fparams={'path': '%s', 'thumb': '%s', 'title': '%s', 'descr': ''}" % (quote(link), 
				quote(thumb), quote(title))
			addDir(li=li, label=title, action="dirList", dirID="SenderLiveResolution", fanart=R("suche_iptv.png"), 
				thumb=thumb, fparams=fparams, tagline=tag, mediatype=mediatype)		
		
			break
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	
	
#-----------------------------------------------
# WRD-Links 
# Aufruf SenderLiveListe für WDR Lokalzeit
#
def list_WDRstreamlinks(url):
	PLog('list_WDRstreamlinks:')
	wdr_base = "https://www1.wdr.de"
	
	page, msg = get_page(url)					
	if page == '':	
		msg1 = "Fehler in get_WRDstreamlinks:"
		msg2=msg
		MyDialog(msg1, msg2, '')	
		return li
	PLog(len(page))
	
	items = blockextract('hideTeasertext">', page)
	PLog(len(items))	

	li = xbmcgui.ListItem()
	
	for item in items:
		if 'title="Alle Livestreams' in item:
			continue
		path = stringextract('href="', '"', item)
		if path.startswith("/"):
			path = wdr_base + path
		title = stringextract('title="', '"', item)			# href-title
		img = stringextract('srcset="', '"', item)
		if img.startswith("/"):
			img = wdr_base + img
		img_src = stringextract('alt="', 'src=', item)
		img_src = stringextract('title="', '"', img_src)	# alt-title
		summ = img_src
		summ = u"%s\n\n[B]Sendezeit 19.30 - 20.00 Uhr[/B]" % summ
		summ_par = summ.replace('\n', '||')
		
		PLog("Satz28:")
		
		PLog(path);PLog(img); PLog(title); PLog(summ); 
		title=py2_encode(title); summ_par=py2_encode(summ_par)
		path=py2_encode(path); img=py2_encode(img);
		
		fparams="&fparams={'path': '%s', 'title': '%s', 'img': '%s', 'summ': '%s'}" %\
			(quote(path), quote(title), quote(img), quote(summ_par))				
		addDir(li=li, label=title, action="dirList", dirID="WDRstream", fanart=img, thumb=img, 
			fparams=fparams, summary=summ)	
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#-----------------------------------------------
# Livesender WRD-Lokalzeit-Link 
# Aufruf list_WDRstreamlinks
# Nach Sendungsende bleibt der Link unter deviceids-medp.wdr.de noch
#	einige Minuten erhalten, führt jedoch ins Leere. Ohne Link: Notific.
# 04.03.2022 einige Seiten enthalten bereits eine .m3u8-Quelle während 
#	der Lokalzeit - außerhalb Verzweigung via deviceids-medp.wdr.de mit
#	js-Dateilink zum Livestream WDR od. Störungsbild.
#	
def WDRstream(path, title, img, summ):
	PLog('WDRstream:')
	summ = summ.replace( '||', '\n')
	
	page, msg = get_page(path)					
	if page == '':	
		msg1 = "Fehler in WDRstream:"
		msg2=msg
		MyDialog(msg1, msg2, '')	
		return li
	PLog(len(page))
	page=py2_decode(page)					
	
	vonbis = stringextract('>Hier sehen Sie ', ' die Lokalzeit ', page)	# 19.30 - 20.00 Uhr
	PLog('deviceids-medp.wdr.de' in page)
	videos = blockextract('"videoURL" : "', page, '}')			# .m3u8-Quelle vorh.?
	PLog(videos)
	
	mediatype=''									# Kennz. Video für Sofortstart
	if SETTINGS.getSetting('pref_video_direct') == 'true':
		mediatype='video'

	if len(videos) >0:											# wie ARDSportVideo
		PLog("detect_videoURL")
		li = xbmcgui.ListItem()
		li = home(li, ID=NAME)				# Home-Button
		m3u8_url= stringextract('"videoURL" : "', '"', videos[0])
		if m3u8_url and m3u8_url.startswith('http') == False:		
			m3u8_url = 'https:' + m3u8_url						# //wdradaptiv-vh.akamaihd.net/..	
		
		if SETTINGS.getSetting('pref_video_direct') == 'true': 	# Sofortstart
			PLog('Sofortstart: WDRstream')
			PlayVideo(url=m3u8_url, title=title, thumb=img, Plot=summ, sub_path="")
		else:
			summ_par = summ.replace('\n', '||')
			title=py2_encode(title); summ_par=py2_encode(summ_par)
			img=py2_encode(img); m3u8_url=py2_encode(m3u8_url)
			fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'sub_path': ''}" %\
				(quote_plus(m3u8_url), quote_plus(title), quote_plus(img), quote_plus(summ_par))
			addDir(li=li, label=title, action="dirList", dirID="PlayVideo", fanart=img, thumb=img, fparams=fparams, 
				mediatype=mediatype, tagline=title, summary=summ)
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
				 				 
	else:														# keine m3u8-Quelle vorh.
		PLog("no_videoURL")	
		summ = "%s | außerhalb dieser Zeiten zeigen einige Sender den Livestream des WDR" % vonbis
		if 'deviceids-medp.wdr.de' in page:
			PLog("detect_deviceids")
			ARDSportVideo(path, title, img, summ, page=page)
			xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
		else:
			icon=img
			msg1 = u"Sendungszeiten"
			msg2 = vonbis									
			xbmcgui.Dialog().notification(msg1,msg2,icon,3000, sound=True)
	return

#-----------------------------------------------------------------------------------------------------
#	17.02.2018 Video-Sofort-Format wieder entfernt (V3.1.6 - V3.5.0)
#		Forum:  https://forums.plex.tv/discussion/comment/1606010/#Comment_1606010
#		Funktionen: remoteVideo, Parseplaylist, SenderLiveListe, TestOpenPort
#	14.12.2018 für Kodi wieder eingeführt (Kodi erlaubt direkten Playerstart).
#-----------------------------------------------------------------------------------------------------

###################################################################################################
# Auswahl der Auflösungstufen des Livesenders - Aufruf: SenderLiveListe + ARDStartRubrik
#	Herkunft Links: livesenderTV.xml (dto. bei Aufruf durch ARDStartRubrik).
#	descr: tagline | summary
#	Startsender ('' oder true): Aufrufer ARDStartRubrik, ARDStartSingle (ARD-Neu)
# 16.05.2019 Fallback hinzugefügt: Link zum Classic-Sender auf Webseite
#	mögl. Alternative: Senderlinks aus ARD-Neu (s. Watchdog_TV-Live.py).	
# 25.06.2020 Fallback-Code (Stream auf classic.ardmediathek.de/tv/live ermitteln)
#	wieder entfernt - nur für ARD-Sender + selten gebraucht.
# 26.06.2020 Aktualisierung der EPG-Daten (abhängig von EPG-Setting, außer bei 
#	EPG_ShowSingle) - relevant für Aufrufe aus Merkliste.
#	Sender: Sendername bei Aufrufen durch EPG_ShowSingle (title mit EPG-Daten
#			belegt)
#	start_end: EPG-Start-/Endzeit Unix-Format für Kontextmenü (EPG_ShowSingle <-)
# 04.04.2021 Anpassung für Radiosender (z.B. MDR Fußball-Radio Livestream)
# 08.06.2021 Anpassung für Radiosender (Endung /mp3, Code an Funktionsstart)
#
def SenderLiveResolution(path, title, thumb, descr, Merk='false', Sender='', start_end=''):
	PLog('SenderLiveResolution:')
	PLog(title); PLog(descr); PLog(Sender);
	path_org = path

	# Radiosender in livesenderTV.xml ermöglichen (ARD Audio Event Streams)
	link_ext = ["mp3", '.m3u', 'low', '=ard-at']	# auch ../stream/mp3
	switch_audio = False
	for ext in link_ext:
		if path_org.endswith(ext):
			switch_audio = True
	if switch_audio or 'sportradio' in path_org:	# sportradio-deutschland o. passende Ext.
		PLog("Audiolink: %s" % path_org) 
		li = xbmcgui.ListItem()
		li.setProperty('IsPlayable', 'false')			
		PlayAudio(path_org, title, thumb, Plot=title)  # direkt	
		return

	page, msg = get_page(path=path)					# Verfügbarkeit des Streams testen
	if page == '':
		msg1 = u'SenderLiveResolution: Stream nicht verfügbar'
		msg2 = path[:50] + ".."
		msg3 = msg
		PLog(msg1)
		MyDialog(msg1, msg2, msg3)
		# xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False) # Fehlschlag - raus
		return										# endOfDirectory reicht hier nicht
		
	# EPG aktualisieren? Der Titel mit ev. alten EPG-Daten wird durch Sendungstitel
	#	ersetzt. Setting unbeachtet, falls Aufruf mit Sender erfolgt (EPG_ShowSingle):
	if Sender or SETTINGS.getSetting('pref_use_epg') == 'true':
		if Sender:									# EPG_ShowSingle: title=EPG-Daten
			title = Sender
		playlist_img, link, EPG_ID= get_playlist_img(title)
		if EPG_ID:
			rec = EPG.EPG(ID=EPG_ID, mode='OnlyNow')
			if rec:
				sname=py2_encode(rec[3]); stime=py2_encode(rec[4]); 
				summ=py2_encode(rec[5]); vonbis=py2_encode(rec[6])	
				PLog(summ); PLog(stime); PLog(vonbis)
				if sname:								# Sendung ersetzt Titel
					title = sname
				if summ:
					descr = summ
				if vonbis:
					descr = "%s | %s" % (summ, vonbis)
		else:
			descr = "EPG-Daten fehlen"					


	# direkter Sprung hier erforderlich, da sonst der Player mit dem Verz. SenderLiveResolution
	#	startet + fehlschlägt.
	# 04.08.2019 Sofortstart nur noch abhängig von Settings und nicht zusätzlich von  
	#	Param. Merk.
	PLog(SETTINGS.getSetting('pref_video_direct'))
	if SETTINGS.getSetting('pref_video_direct') == 'true': # or Merk == 'true':	# Sofortstart
		PLog('Sofortstart: SenderLiveResolution')
		PlayVideo(url=path, title=title, thumb=thumb, Plot=descr, Merk=Merk)
		return
	
	url_m3u8 = path
	PLog(title); PLog(url_m3u8);

	li = xbmcgui.ListItem()
	if "kikade-" in path or path.startswith("https://kika"):
		li = home(li, ID='Kinderprogramme')			# Home-Button
	else:
		li = home(li, ID=NAME)				# Home-Button
										
	# Spezialbehandlung für N24 - Test auf Verfügbarkeit der Lastserver (1-4),
	# entf. mit Umstellung auf IPTV-Links in V4.3.8
		
	# alle übrigen (i.d.R. http-Links), Videoobjekte für einzelne Auflösungen erzeugen,
	# 	Mehrkanalstreams -> PlayButtonM3u8
	if url_m3u8.endswith('master.m3u8') or url_m3u8.endswith('index.m3u8'): # Vorrang vor .m3u8
		# Parseplaylist -> CreateVideoStreamObject pro Auflösungstufe
		PLog("title: " + title)
		descr = "%s\n\n%s" % (title, descr)
		PLog("descr: " + descr)
		li = Parseplaylist(li, url_m3u8, thumb, geoblock='', descr=descr, live=True)	
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
							
	elif url_m3u8.find('.m3u8') >= 0: 
		# 1 Button für autom. Auflösung (z.B. IPTV-Links) 
		# 
		PLog(url_m3u8)
		if url_m3u8.startswith('http'):			# URL extern? (lokal entfällt Eintrag "autom.")
												# Einzelauflösungen + Ablage master.m3u8:
			li = PlayButtonM3u8(li, url_m3u8, thumb, title, tagline=title, descr=descr)	
									
	else:	# keine oder unbekannte Extension - Format unbekannt,
			# # Radiosender s.o.
		msg1 = 'SenderLiveResolution: unbekanntes Format. Url:'
		msg2 = url_m3u8
		PLog(msg1)
		MyDialog(msg1, msg2, '')

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
		
		
#--------------------------------------------------------------------------------------------------
# Button für Einzelauflösungen für Streamlink url_m3u8
#	ID: Kennung für home
def show_single_bandwith(url_m3u8, thumb, title, descr, ID):
	PLog('show_single_bandwith:'); 
	
	li = xbmcgui.ListItem()
	li = home(li, ID=ID)						# Home-Button
	
	descr = title + "\n\n" + descr
	li = Parseplaylist(li, url_m3u8, thumb, geoblock='', descr=descr)	
	
	xbmcplugin.endOfDirectory(HANDLE)

#-----------------------------
# Aufruf: Parseplaylist (bei Mehrkanalstreams), SenderLiveResolution
# 31.05.2022 umbenannt (vorm. ParseMasterM3u), Code für relative Pfade 
#	entfernt, ausschl. Behandl. .m3u8 (.master.m3u8 in Parseplaylist),
#	Verzicht auf lokale Dateiablage
#
def PlayButtonM3u8(li, url_m3u8, thumb, title, descr, tagline='', sub_path='', stitle=''):	
	PLog('PlayButtonM3u8:'); 
	PLog(title); PLog(url_m3u8); PLog(thumb); PLog(tagline);
	
	li = xbmcgui.ListItem()								# li kommt hier als String an
	title=unescape(title); title=repl_json_chars(title)
	
	tagline	= tagline.replace('||','\n')				# s. tagline in ZDF_get_content
	descr_par= descr; descr_par	 = descr_par.replace('\n', '||')
	descr	 = descr.replace('||','\n')					# s. descr in ZDF_get_content
	title = "autom. | " + title

	title=py2_encode(title); url_m3u8=py2_encode(url_m3u8);
	thumb=py2_encode(thumb); descr_par=py2_encode(descr_par); sub_path=py2_encode(sub_path);
	fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'sub_path': '%s'}" %\
		(quote_plus(url_m3u8), quote_plus(title), quote_plus(thumb), 
		quote_plus(descr_par), quote_plus(sub_path))	
	addDir(li=li, label=title, action="dirList", dirID="PlayVideo", fanart=thumb, thumb=thumb, fparams=fparams, 
		mediatype='video', tagline=tagline, summary=descr) 

	return li
#-----------------------------
# Spezialbehandlung für N24 - Test auf Verfügbarkeit der Lastserver (1-4): wir prüfen
# 	die Lastservers durch, bis einer Daten liefert
def N24LastServer(url_m3u8):	
	PLog('N24LastServer: ' + url_m3u8)
	url = url_m3u8
	
	pos = url.find('index_')	# Bsp. index_1_av-p.m3u8
	nr_org = url[pos+6:pos+7]
	PLog(nr_org) 
	for nr in [1,2,3,4]:
		# PLog(nr)
		url_list = list(url)
		url_list[pos+6:pos+7] = str(nr)
		url_new = "".join(url_list)
		# PLog(url_new)
		try:
			req = Request(url_new)
			r = urlopen(req)
			playlist = r.read()			
		except:
			playlist = ''
			
		PLog(playlist[:20])
		if 	playlist:	# playlist gefunden - diese url verwenden
			return url_new	
	
	return url_m3u8		# keine playlist gefunden, weiter mit Original-url
	
###################################################################################################
def BilderDasErste(path=''):
	PLog("BilderDasErste:")
	PLog(path)
	searchbase = 'https://www.daserste.de/search/searchresult-100.js'
	
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button
	
	if path == '':										# Gesamt-Seitenübersicht laden
		path = 'https://www.daserste.de/search/searchresult-100.jsp?searchText=bildergalerie'
		page, msg = get_page(path)	
		if page == '':
			msg1 = ' Übersicht kann nicht geladen werden.'
			msg2 = msg
			MyDialog(msg1, msg2, '')
			return
	
		pages = blockextract('class="entry page', page)
		for rec in pages:
			href 	= stringextract('href="', '"', rec)
			href	= searchbase + href
			nr 		= stringextract('">', '</a>', rec)	# ..&start=40">5</a
			title 	= "Bildgalerien Seite %s" % nr
			fparams="&fparams={'path': '%s'}" % (quote(href))
			addDir(li=li, label=title, action="dirList", dirID="BilderDasErste", fanart=R(ICON_MAIN_ARD),
				thumb=R('ard-bilderserien.png'), fparams=fparams)
		
	else:	# -----------------------					# 10er-Seitenübersicht laden		
		page, msg = get_page(path)	
		if page == '':
			msg1 = ' %s kann nicht geladen werden.' % title
			msg2 = msg
			MyDialog(msg1, msg2, '')
			return
		
		entries = blockextract('class="teaser">', page)
		for rec in entries:
			headline =  stringextract('class="headline">', '</h3>', rec)
			href =  stringextract('href="', '"', headline)
			title =  cleanhtml(headline); title=mystrip(title)
			title =  title.strip()
			title = unescape(title); title = repl_json_chars(title)		# \n

			dach =  stringextract('class="dachzeile">', '</p>', rec)	# \n
			tag = cleanhtml(dach); tag = unescape(tag); 
			tag = mystrip(tag);	
	
			teasertext =  stringextract('class="teasertext">', '</a>', rec)
			teasertext = cleanhtml(teasertext); teasertext = mystrip(teasertext)
			summ = unescape(teasertext.strip())
			
			
			PLog("Satz21:")
			PLog(href); PLog(title); PLog(summ); PLog(tag);		
			
			href=py2_encode(href); title=py2_encode(title);	
			fparams="&fparams={'title': '%s', 'path': '%s'}" % (quote(title), quote(href))
			addDir(li=li, label=title, action="dirList", dirID="BilderDasErsteSingle", fanart=R(ICON_MAIN_ARD),
				thumb=R('ard-bilderserien.png'), tagline=tag, summary=summ, fparams=fparams)
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
#--------------------------------------------------------------------------------------------------	
# 23.09.2021 Umstellung Bildname aus Quelle statt "Bild_01" (eindeutiger beim
#	Nachladen) - wie ZDF_BildgalerieSingle.
#
def BilderDasErsteSingle(title, path):					  
	PLog("BilderDasErsteSingle:")
	PLog(title)
	
	li = xbmcgui.ListItem()
	
	page, msg = get_page(path)	
	if page == '':
		msg1 = ' %s kann nicht geladen werden.' % title
		msg2 = msg
		MyDialog(msg1, msg2, '')
		return
		
	li = home(li, ID=NAME)				# Home-Button
	content = blockextract('class="teaser">', page)
	PLog("content: " + str(len(content)))
	if len(content) == 0:										
		msg1 = 'BilderDasErsteSingle: keine Bilder gefunden.'
		msg2 = title
		MyDialog(msg1, msg2, '')
		return li
	
	fname = make_filenames(title)			# Ordnername: Titel 
	fpath = os.path.join(SLIDESTORE, fname)
	PLog(fpath)
	if os.path.isdir(fpath) == False:
		try:  
			os.mkdir(fpath)
		except OSError:  
			msg1 = 'Bildverzeichnis konnte nicht erzeugt werden:'
			msg2 = "%s/%s" % (SLIDESTORE, fname)
			PLog(msg1); PLog(msg2)
			MyDialog(msg1, msg2, '')
			return li	
	
	image=0; background=False; path_url_list=[]; text_list=[]
	base = 'https://' + urlparse(path).hostname
	for rec in content:
		# headline, title, dach fehlen
		#	xl ohne v-vars									# json-Bilddaten
		imgs = stringextract('data-ctrl-attributeswap=', 'class="img"', rec)		
		img_src = stringextract("l': {'src':'", "'", imgs)	# Blank vor {	
		if img_src == '':
			img_src = stringextract("m':{'src':'", "'", imgs)		
		if img_src == '':
			continue
		
		img_src = base + img_src	
		img_src = img_src.replace('v-varxs', 'v-varxl')			# ev. attributeswap auswerten 
		
		alt = stringextract('alt="', '"', rec)	
		alt=unescape(alt); 
		title = stringextract('title="', '"', rec)	
		# tag = "%s | %s" % (alt, title)
		tag = alt
		lable = title
		
		teasertext =  stringextract('class="teasertext">', '</a>', rec)
		teasertext = cleanhtml(teasertext); teasertext = mystrip(teasertext)
		summ = unescape(teasertext)
		tag=repl_json_chars(tag) 
		title=repl_json_chars(title); summ=repl_json_chars(summ); 
		PLog("Satz22:")
		PLog(img_src); PLog(title); PLog(tag[:60]); PLog(summ[:60]); 		
			
		#  Kodi braucht Endung für SildeShow; akzeptiert auch Endungen, die 
		#	nicht zum Imageformat passen
		#pic_name 	= 'Bild_%04d.jpg' % (image+1)		# Bildname
		pic_name 	= img_src.split('/')[-1]			# Bildname aus Quelle
		local_path 	= "%s/%s" % (fpath, pic_name)
		PLog("local_path: " + local_path)
		title = "Bild %03d: %s" % (image+1, pic_name)	# Numerierung
		if len(title) > 70:
			title = "%s.." % title[:70]					# Titel begrenzen
		
		PLog("Bildtitel: " + title)
		
		local_path 	= os.path.abspath(local_path)
		thumb = local_path
		if os.path.isfile(local_path) == False:			# schon vorhanden?
			# path_url_list (int. Download): Zieldatei_kompletter_Pfad|Bild-Url, 
			#	Zieldatei_kompletter_Pfad|Bild-Url ..
			path_url_list.append('%s|%s' % (local_path, img_src))

			if SETTINGS.getSetting('pref_watermarks') == 'true':
				txt = "%s\n%s\n%s\n%s\n%s" % (fname,title,lable,tag,summ)
				text_list.append(txt)	
			background	= True											
								
		title=repl_json_chars(title); summ=repl_json_chars(summ)
		PLog('neu:');PLog(title);PLog(img_src);PLog(thumb);PLog(summ[0:40]);
		if thumb:	
			local_path=py2_encode(local_path);
			fparams="&fparams={'path': '%s', 'single': 'True'}" % quote(local_path)
			addDir(li=li, label=title, action="dirList", dirID="ZDF_SlideShow", 
				fanart=thumb, thumb=local_path, fparams=fparams, summary=summ, tagline=tag)

		image += 1
			
	if background and len(path_url_list) > 0:				# Thread-Call mit Url- und Textliste
		PLog("background: " + str(background))
		from threading import Thread						# thread_getpic
		folder = fname 
		background_thread = Thread(target=thread_getpic,
			args=(path_url_list, text_list, folder))
		background_thread.start()

	PLog("image: " + str(image))
	if image > 0:	
		fpath=py2_encode(fpath);	
		fparams="&fparams={'path': '%s'}" % quote(fpath) 	# fpath: SLIDESTORE/fname
		addDir(li=li, label="SlideShow", action="dirList", dirID="ZDF_SlideShow", 
			fanart=R('icon-stream.png'), thumb=R('icon-stream.png'), fparams=fparams)
				
		lable = u"Alle Bilder löschen"						# 2. Löschen
		tag = 'Bildverzeichnis: ' + fname 
		summ= u'Bei Problemen: Bilder löschen, Wasserzeichen ausschalten,  Bilder neu einlesen'
		fparams="&fparams={'dlpath': '%s', 'single': 'False'}" % quote(fpath)
		addDir(li=li, label=lable, action="dirList", dirID="DownloadsDelete", fanart=R(ICON_DELETE), 
			thumb=R(ICON_DELETE), fparams=fparams, summary=summ, tagline=tag)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)  # ohne Cache, um Neuladen zu verhindern
		
	
				  
####################################################################################################
# 29.09.2019 Umstellung Radio-Livestreams auf ARD Audiothek
#	Codebereinigung - gelöscht: 
#		RadioLiveListe, RadioAnstalten, livesenderRadio.xml, 77 Radio-Icons (Autor: Arauco)
#

###################################################################################################
#									ZDF-Funktionen
###################################################################################################
# Startseite der ZDF-Mediathek 
# Neu: April 2023	
#
def ZDF_Start(ID, homeID=""): 
	PLog('ZDF_Start: ' + ID);
	 
	base = "https://zdf-cdn.live.cellular.de/mediathekV2/"		

	if ID=='Startseite' or "tivi_" in ID or "funk_" in ID:
		path = base + "start-page"
		if ID.startswith("tivi"):
			path = base + "document/zdftivi-fuer-kinder-100"
		if "funk_" in ID:
			path = base + "document/funk-126"
		
		# Im Cache wird das jsonObject abgelegt, DictID: "mobile_%s" % ID
		DictID =  "ZDF_%s" % ID
		page = Dict("load", DictID, CacheTime=ZDF_CacheTime_Start)	# 5 min				
		if not page:												# nicht vorhanden oder zu alt						
			icon = R(ICON_MAIN_ZDF)
			if ID.startswith("tivi"):
				icon = GIT_TIVIHOME
			xbmcgui.Dialog().notification("Cache %s:" % ID,"Haltedauer 5 Min",icon,3000,sound=False)

			page, msg = get_page(path)								# vom Sender holen		
			if page == "":
				msg1 = 'Fehler beim Abruf von:'
				msg2 = msg
				MyDialog(msg1, msg2, '')
				return
			else:
				jsonObject = json.loads(page)
				Dict('store', DictID, jsonObject)		# jsonObject -> Dict, ca. 10 MByte, tivi 8.5 MByte
		else:
			jsonObject = page
			
		PLog("jsonObject1: " + str(jsonObject)[:80])
		ZDF_PageMenu(DictID,jsonObject=jsonObject)
		return

	if ID=='Rubriken':
		url = base + "categories-overview"
	if ID=="ZDF-Sportstudio":
		url = base + "document/sport-106"
	if ID=='Barrierearm':
		url = base + "document/barrierefrei-im-zdf-100"
	if ID=='ZDFinternational':
		url = base + "document/international-108"		
	if ID=='ZDFchen':									# ZDFtivi-Sendereihe bis 6 Jahre
		url = base + "document/zdfchen-100"		
	ZDF_RubrikSingle(url, ID, homeID)
				
	return
	
#---------------------------------------------------------------------------------------------------
# Aufruf ZDF_Start mit jsonObject direkt,
#		ZDF_RubrikSingle mit DictID (-> gespeichertes jsonObject)
# mark: Titelmarkierung, z.B. für ZDF_Search
# 13.05.2023 zusätzl. urlkey (Kompensation falls jsonObject fehlt),
#	Format urlkey: "%s#cluster#%d" % (url, obj_id, obj_nr)
# 	
def ZDF_PageMenu(DictID,  jsonObject="", urlkey="", mark="", li="", homeID=""):								
	PLog('ZDF_PageMenu:')
	PLog('DictID: ' + DictID)
	PLog(mark); PLog(homeID); PLog(urlkey)
	li_org=li 
		
	if not jsonObject:
		jsonObject = Dict("load", DictID)
	if not jsonObject:						# aus Url wiederherstellen (z.B. für Merkliste)
		if urlkey:
			PLog("get_from_urlkey:")
			url, obj_id, obj_nr = urlkey.split("#")
			PLog("obj_id: %s, obj_nr: %s" % (obj_id, obj_nr))
			page, msg = get_page(path=url)
			try:
				jsonObject = json.loads(page)
				jsonObject = jsonObject[obj_id][int(obj_nr)]
			except Exception as exception:
				PLog(str(exception))
				jsonObject=""

	if not jsonObject:
		msg1 = u'ZDF_PageMenu: Beiträge können leider nicht geladen werden.'
		MyDialog(msg1, '', '')
		return	
	PLog(str(jsonObject)[:80])
	
		
	if not li:	
		li = xbmcgui.ListItem()
	if "ZDF_tivi" in DictID or "Kinder" in homeID:
		homeID = "Kinderprogramme"
		li = home(li, ID=homeID)
	else:
		li = home(li, ID="ZDF")				# Home-Button
		
	mediatype=''													# Kennz. Videos im Listing
	if SETTINGS.getSetting('pref_video_direct') == 'true':
		mediatype='video'
	PLog('mediatype: ' + mediatype); 
	PLog("stage" in jsonObject); PLog("teaser" in jsonObject); PLog("results" in jsonObject);
		
	if "stage" in jsonObject or "teaser" in jsonObject or "results" in jsonObject:
		PLog('ZDF_PageMenu_stage_teaser')
		stage=False
		if DictID == "ZDF_Startseite" or "tivi_" in DictID or "funk_" in DictID:
			if "stage" in jsonObject:								# <- ZDF-Start, tivi-Start
				entryObject = jsonObject["stage"]
				PLog("stage_len: %d" % len(entryObject))
				stage=True
		if "teaser" in jsonObject:									# ZDF_RubrikSingle
			entryObject = jsonObject["teaser"]
			PLog("teaser: %d" % len(entryObject))
		if  "results" in jsonObject:								# ZDF_Search
			entryObject = jsonObject["results"]
			PLog("results: %d" % len(entryObject))
			
		for entry in entryObject:
			typ,title,tag,descr,img,url,stream,scms_id = ZDF_get_content(entry,mark=mark)
			label=""
			if stage:
				label = "[B]TOP:[/B]"
			label = "%s %s" % (label, title)
			
			PLog("Satz1_1:")
			PLog(stage); PLog(typ); PLog(title);
			title = repl_json_chars(title)
			descr = repl_json_chars(descr)
			if entry["type"]=="video":								# Videos
				if "channel" in entry:								# Zusatz Sender
					sender = entry["channel"]
					tag = "%s | %s" % (tag, sender)
				if stream == "":									# Bsp.: ZDFtivi -> KiKA live
					stream = url
				fparams="&fparams={'path': '%s','title': '%s','thumb': '%s','tag': '%s','summ': '%s','scms_id': '%s'}" %\
					(stream, title, img, tag, descr, scms_id)
				PLog("fparams: " + fparams)	
				addDir(li=li, label=label, action="dirList", dirID="ZDF_getApiStreams", fanart=img, thumb=img, 
					fparams=fparams, tagline=tag, summary=descr, mediatype=mediatype)
			elif entry["type"]=="livevideo":
				fparams="&fparams={'url': '%s', 'title': '%s'}" % (url, title)
				PLog("fparams: " + fparams)	
				addDir(li=li, label=title, action="dirList", dirID="ZDF_Live", fanart=img, 
					thumb=img, fparams=fparams, summary=descr, tagline=tag, mediatype=mediatype)   
			elif entry["type"]=="externalUrl":						# Links zu anderen Sendern
				if "KiKANiNCHEN" in title:
					PLog("Link_KiKANiNCHEN")
					KIKA_START="https://www.kika.de/bilder/startseite-104_v-tlarge169_w-1920_zc-a4147743.jpg"	# ab 07.12.2022
					GIT_KANINCHEN="https://github.com/rols1/PluginPictures/blob/master/ARDundZDF/KIKA_tivi/tv-kikaninchen.png?raw=true"					
					fparams="&fparams={}" 
					addDir(li=li, label=title, action="dirList", dirID="resources.lib.childs.Kikaninchen_Menu", 
						fanart=KIKA_START, thumb=GIT_KANINCHEN, tagline='für Kinder 3-6 Jahre', fparams=fparams)
				if "Zahlen zur" in title:							# Wahlbeiträge, Statistiken
					PLog("skip_externalUrl: " + title)
				
			else:
				fparams="&fparams={'url': '%s', 'title': '%s', 'homeID': '%s'}" % (url, title, homeID)
				PLog("fparams: " + fparams)	
				addDir(li=li, label=label, action="dirList", dirID="ZDF_RubrikSingle", fanart=img, 
					thumb=img, fparams=fparams, summary=descr, tagline=tag)
							
						
	if("cluster" in jsonObject):		# Bsp- A-Z Leitseite -> SingleRubrik
		PLog('ZDF_PageMenu_cluster')
		for counter, clusterObject in enumerate(jsonObject["cluster"]):	# Bsp. "name":"Neu in der Mediathek"
			path = "cluster|%d|teaser" % counter

			try:													# detect PromoTeaser (Web: ganze Breite)
				typ = clusterObject["type"]
				url = clusterObject["promoTeaser"]["url"]
			except:
				typ=""	

			title=""
			if "name" in clusterObject:
				title = clusterObject["name"]
			if title == '':											# "teaser": [.. - kann leer sein
				PLog(str(clusterObject["teaser"])[:60])
				if clusterObject["teaser"]:
					title = clusterObject["teaser"][0]['titel']
			if clusterObject["teaser"]:
				img = ZDF_get_img(clusterObject["teaser"][0])
			if "promoTeaser" in clusterObject:						#  PromoTeaser
				img = ZDF_get_img(clusterObject["promoTeaser"])
				
			tag = "Folgeseiten"
			descr=""
			if  "beschreibung" in clusterObject:
				descr = clusterObject["beschreibung"]
			
			# skip: personalisierten Inhalte, Addon-Menüs:
			skip_list = ['Alles auf einen Blick', u'Das könnte Dich', 'Direkt zu',
						'Mein Programm', 'Deine', 'KiKA live sehen', 'Weiterschauen'
						 ]
			skip=False						
			if title == '':
				PLog('ohne_Titel: %s' % str(clusterObject)[:80])	# ?
				skip = True 
			for t in skip_list:
				# PLog("t: %s, title: %s" % (t, title))
				if title.startswith(t) or title.endswith(t):
					PLog("skip: %s" % title)
					skip = True 
			if skip:
				continue 
				
			path = "cluster|%d|teaser" % counter
			title = repl_json_chars(title)
			descr = repl_json_chars(descr)
			PLog("Satz1_2:")
			PLog(title); PLog(path); PLog(typ);
			
			if typ != "teaserPromo": 
				fparams="&fparams={'path': '%s', 'title': '%s', 'DictID': '%s', 'homeID': '%s'}"  %\
					(path, title, DictID, homeID)
				PLog("fparams: " + fparams)	
				addDir(li=li, label=title, action="dirList", dirID="ZDF_Rubriken", 				
					fanart=img, thumb=img, tagline=tag, summary=descr, fparams=fparams)
			else:													# teaserPromo - s.o.
				fparams="&fparams={'url': '%s', 'title': '%s'}" % (url, title)
				PLog("fparams: " + fparams)	
				addDir(li=li, label=title, action="dirList", dirID="ZDF_RubrikSingle", fanart=img, 
					thumb=img, fparams=fparams, summary=descr, tagline=tag)
					

	if li_org:
		return li
	else:
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

###################################################################################################
# Aufruf: ZDF_PageMenu
# ZDF-Rubriken (Film, Serie,  Comedy & Satire,  Politik & Gesellschaft, ..)
# path: json-key-Pfad (Bsp. cluster|2|teaser)
#
def ZDF_Rubriken(path, title, DictID, homeID=""):								
	PLog('ZDF_Rubriken: ' + DictID)
	PLog("path: " + path)
	path_org = path

	jsonObject = Dict("load", DictID)
	PLog(str(jsonObject)[:80])
	jsonObject, msg = GetJsonByPath(path, jsonObject)
	if jsonObject == '':					# index error
		msg1 = 'Cluster [B]%s[/B] kann nicht geladen werden.' % title
		msg2 = msg
		MyDialog(msg1, msg2, '')
		return
	PLog(str(jsonObject)[:80])
					
	li = xbmcgui.ListItem()
	if homeID:
		li = home(li, ID=homeID)
	else:
		li = home(li, ID='ZDF')						# Home-Button
		
	mediatype=''
	if SETTINGS.getSetting('pref_video_direct') == 'true':
		mediatype='video'
		
	i=0
	PLog("walk_entries: %d" % len(jsonObject))					
	for entry in jsonObject:
		path = path_org + '|%d' % i
		PLog("entry_type: " + entry["type"])
				
		typ,title,tag,descr,img,url,stream,scms_id = ZDF_get_content(entry)
		title = repl_json_chars(title)
		descr = repl_json_chars(descr)
		if typ == "video":	
				if "channel" in entry:									# Zusatz Sender
					sender = entry["channel"]
					tag = "%s | %s" % (tag, sender)
				fparams="&fparams={'path': '%s','title': '%s','thumb': '%s','tag': '%s','summ': '%s','scms_id': '%s'}" %\
					(stream, title, img, tag, descr, scms_id)	
				addDir(li=li, label=title, action="dirList", dirID="ZDF_getApiStreams", fanart=img, thumb=img, 
					fparams=fparams, tagline=tag, summary=descr, mediatype=mediatype)	
		elif typ == "livevideo":
			fparams="&fparams={'url': '%s', 'title': '%s'}" % (url, title)
			PLog("fparams: " + fparams)	
			addDir(li=li, label=title, action="dirList", dirID="ZDF_Live", fanart=img, 
				thumb=img, fparams=fparams, summary=descr, tagline=tag, mediatype=mediatype)   
					
		else:
			fparams="&fparams={'url': '%s', 'title': '%s'}" % (url, title)
			PLog("fparams: " + fparams)	
			addDir(li=li, label=title, action="dirList", dirID="ZDF_RubrikSingle", fanart=img, 
				thumb=img, fparams=fparams, summary=descr, tagline=tag)
													
		i=i+1
		# break		# Test Einzelsatz		
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

###################################################################################################
# einzelne ZDF-Rubrik (Film, Serie,  Comedy & Satire,  Politik & Gesellschaft, ..)
# Cluster-Objekte > 1: Dict-Ablage mit DictID je Cluster -> PageMenu
# einz. Cluster-Objekt: Auswertung Teaser -> wieder hierher, ohne Dict
#
def ZDF_RubrikSingle(url, title, homeID=""):								
	PLog('ZDF_RubrikSingle: ' + title)
	PLog("url: " + url)
	title_org = title
	noicon = R(ICON_MAIN_ZDF)									# notific.

	page=""; AZ=False
	if url.endswith("sendungen-100"):							# AZ ca. 12 MByte -> Dict
		page = Dict("load", "ZDF_sendungen-100", CacheTime=ZDF_CacheTime_AZ)
		AZ=True
	if not page:	
		page, msg = get_page(path=url)
		if not page:												# nicht vorhanden?
			msg1 = 'ZDF_RubrikSingle: [B]%s[/B] kann nicht geladen werden.' % title
			msg2 = msg
			MyDialog(msg1, msg2, '')
			return
		if AZ:
			page = json.loads(page)
			Dict("store", "ZDF_sendungen-100", page)
	
	if "dict" in str(type(page)):								# AZ: json
		jsonObject = page
	else: 
		jsonObject = json.loads(page)
	PLog(str(jsonObject)[:80])
		
	clusterObject, msg = GetJsonByPath("cluster", jsonObject)
	if clusterObject == '':					# index error
		msg1 = 'Rubrik [B]%s[/B] kann nicht geladen werden.' % title
		msg2 = msg
		MyDialog(msg1, msg2, '')
		return
	PLog(str(clusterObject)[:80])
	PLog("Cluster: %d " % len(clusterObject))
	
	if len(clusterObject) == 0:									# z.B. Wahltool, ohne Videos
		msg1 = u"%s" % title
		msg2 = u'keine Videos gefunden'
		xbmcgui.Dialog().notification(msg1,msg2,noicon,2000,sound=True)
		return
	
	#--------------------------------
			
	li = xbmcgui.ListItem()
	if homeID:
		li = home(li, ID=homeID)
	else:	
		li = home(li, ID='ZDF')				# Home-Button
	
	mediatype=''												# Kennz. Videos im Listing
	if SETTINGS.getSetting('pref_video_direct') == 'true':
		mediatype='video'
	PLog('mediatype: ' + mediatype); 
						
	PLog("Seriencheck:")										# Abzweig Serienliste ZDF_FlatListEpisodes
	try:
		docObject = jsonObject["document"]
	except:
		docObject=""
	if docObject:
		if "structureNodePath" in docObject:
			if "/zdf/serien/" in docObject["structureNodePath"]:
				sid = docObject["id"]							# z.B. trigger-point-102
				PLog("Serie: " + sid)
				label = "komplette Liste: %s" % title
				tag = u"Liste aller verfügbaren Folgen | strm-Tools"
				fparams="&fparams={'sid': '%s'}"	% (sid)						
				addDir(li=li, label=label, action="dirList", dirID="ZDF_FlatListEpisodes", fanart=R(ICON_DIR_FOLDER), 
					thumb=R(ICON_DIR_FOLDER), tagline=tag, fparams=fparams)

	cnt=0
	if len(clusterObject) > 1:									# mehrere Cluster
		PLog("walk_cluster: %d" % len(clusterObject))					
		for jsonObject in clusterObject:
			typ = jsonObject["type"]
			title=""
			if "name" in jsonObject:							# kann fehlen oder leer sein
				title = jsonObject["name"]
			if not title:						
				title = title_org
			title = repl_json_chars(title)
			if typ == "videoCarousel":
				title = "[B]Highlights[/B]: %s" % title
			try:
				img = ZDF_get_img(jsonObject["teaser"][0])		# kann fehlen oder leer sein
			except Exception as exception:
				PLog("json_error: " + str(exception))				
				cnt=cnt+1
				continue						# leerer Vorspann: sendungen-mit-audiodeskription-hoerfilme-100
			tag = "Folgeseiten"
			descr = ""
			urlid = url.split("/")[-1]
			DictID = "ZDF_%s_%d" % (urlid, cnt)	# DictID: url-Ende + cluster-nr
			Dict('store', DictID, jsonObject)					# für ZDF_PageMenu
			urlkey = "%s#cluster#%d" % (url, cnt)				# dto
			
			PLog("Satz6_1:")
			urlkey=py2_encode(urlkey)
			fparams="&fparams={'DictID': '%s', 'homeID': '%s', 'urlkey': '%s'}" % (DictID, homeID, quote(urlkey))
			PLog("fparams: " + fparams)	
			addDir(li=li, label=title, action="dirList", dirID="ZDF_PageMenu", fanart=img, 
			thumb=img, fparams=fparams, summary=descr, tagline=tag)
			cnt=cnt+1
	else:														# einzelner Cluster
		teaserObject, msg = GetJsonByPath("0|teaser", clusterObject)
		PLog("walk_teaser: %d" % len(teaserObject))
		PLog("Teaser: %d " % len(teaserObject))
		
		if len(teaserObject) == 0:								# z.B. redakt. Updates zu Ereignissen
			msg1 = u"%s" % title
			msg2 = u'keine Videos gefunden'
			xbmcgui.Dialog().notification(msg1,msg2,noicon,2000,sound=True)
			return						
				
		for entry in teaserObject:
			typ,title,tag,descr,img,url,stream,scms_id = ZDF_get_content(entry)
			title = repl_json_chars(title)
			label = title
			descr = repl_json_chars(descr)
			PLog("Satz6_2:")
			if(entry["type"]=="video"):							# Videos am Seitenkopf
				# path = 'stage|%d' % i	# entf. hier
				PLog("stream: " + stream)
				if "channel" in entry:							# Zusatz Sender
					sender = entry["channel"]
					tag = "%s | %s" % (tag, sender)
				fparams="&fparams={'path': '%s','title': '%s','thumb': '%s','tag': '%s','summ': '%s','scms_id': '%s'}" %\
					(stream, title, img, tag, descr, scms_id)	
				addDir(li=li, label=label, action="dirList", dirID="ZDF_getApiStreams", fanart=img, thumb=img, 
					fparams=fparams, tagline=tag, summary=descr, mediatype=mediatype)
			else:
				fparams="&fparams={'url': '%s', 'title': '%s', 'homeID': '%s'}" % (url, title, homeID)
				addDir(li=li, label=label, action="dirList", dirID="ZDF_RubrikSingle", fanart=img, 
					thumb=img, fparams=fparams, summary=descr, tagline=tag)
					
	ZDF_search_button(li, query=title_org)	
			
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#---------------------------------------------------------------------------------------------------
# Aufruf: ZDF_Rubriken
# Seite enthält alle ZDF-Sender, einschl. EPG für akt. Tag
#
def ZDF_Live(url, title): 										# ZDF-Livestreams von ZDFStart
	PLog('ZDF_Live: '  + url); 
	PLog(title)
	title_org=title
		
	page, msg = get_page(path=url)
	if not page:
		msg1 = u'ZDF_Live: der Stream von [B]%s[/B] kann leider nicht geladen werden.' % title
		MyDialog(msg1, "", '')
		return
	jsonObject = json.loads(page)
	PLog(str(jsonObject)[:80])

	
	for clusterObject in jsonObject["epgCluster"]:
		clusterLive = clusterObject["liveStream"]
		if clusterLive["titel"] == title_org:
			break
	streamsObject = clusterLive["formitaeten"]
	m3u8_url = streamsObject[0]["url"]							# 1. form. = auto
	img = ZDF_get_img(clusterLive)
		
	if SETTINGS.getSetting('pref_video_direct') == 'true':		# Sofortstart
		PLog("Sofortstart_ZDF_Live")
		PlayVideo(url=m3u8_url, title=title_org, thumb=img, Plot=title_org, sub_path="")
		return
	#----------------------
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ZDF')										# Home-Button

	cnt=1; sub_path="";
	for entry in streamsObject:
		url = entry["url"]
		quality = entry["quality"]
		typ = entry["type"]
		lang = entry["language"]
		label = "%d. %s | [B]HLS %s[/B]" % (cnt, title_org, quality)
		Plot = "Typ: %s | %s" % (typ, lang)
		
		PLog("Satz5:")
		PLog(url);PLog(quality);PLog(typ);
		fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'sub_path': '%s'}" %\
			(quote_plus(url), quote_plus(title_org), quote_plus(img), quote_plus(Plot), 
			quote_plus(sub_path))
		addDir(li=li, label=label, action="dirList", dirID="PlayVideo", fanart=img, thumb=img, 
			fparams=fparams, tagline=Plot, mediatype='video') 
		cnt=cnt+1
			

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	
	
#-------------------------
def ZDF_get_img(obj, landscape=False):
	PLog('ZDF_get_img:')
	PLog(str(obj)[:60])	
	
	minWidth=1280					# 1280x720
	if landscape:
		minWidth=1140				# 1140x240
	img=""
	try:
		if("teaserBild" in obj):
			cnt=0
			for width,imageObject in list(obj["teaserBild"].items()):
				if cnt == 0:
					img_first = imageObject["url"]		# Backup
				cnt=cnt+1
				if int(width) >= minWidth:
					img=imageObject["url"]
		if not img:
			if("image" in obj):
				cnt=0
				for width,imageObject in list(obj["image"].items()):
					if cnt == 0:
						img_first = imageObject["url"]	# Backup
					cnt=cnt+1
					if int(width) >= minWidth:
						img=imageObject["url"];
		if not img:										# Backup -> img
			img = img_first
		
	except Exception as exception:
		PLog("get_img_error: " + str(exception))

	if not img:
		img = R(ICON_DIR_FOLDER)
	PLog(img)	
	return img

#---------------------------------------------------------------------------------------------------
# mark: Titelmarkierung, z.B. für ZDF_Search
# 
def ZDF_get_content(obj, maxWidth="", mark=""):
	PLog('ZDF_get_content:')
	PLog(str(obj)[:60])
	PLog(mark)
	
	if not maxWidth:				# Teaserbild, Altern. 1280 für Video
		maxWidth=840
	multi=True; verf=""; url=""; stream=""; scms_id=""
	headline=""
	season=""; episode=""			# episodeNumber, seasonNumber
	
	if "url" in obj:
		url=obj["url"]
	if "headline" in obj:
		headline=obj["headline"]
	title=obj["titel"]
	if title.strip() == "":
		title = headline
	if title.strip() == "":			# mögl.: title/headline mit 1 Blank
		title = obj["id"]

	if mark:
		title = make_mark(mark, title, "", bold=True)	# Titel-Markierung
	
	teaser_nr=''			# wie Serien in ZDF_get_content
	if ("seasonNumber" in obj and "episodeNumber" in obj):
		season = obj["seasonNumber"]
		episode = obj["episodeNumber"]
		teaser_nr = "Staffel %s | Folge %s | " % (season, episode)
		title_pre = "S%02dE%02d" % (int(season), int(episode))
		title = "%s | %s" % (title_pre, title)
	descr=''	
	if("beschreibung" in obj):
		descr = teaser_nr + obj["beschreibung"]	
			
	typ=''	
	if("type" in obj):
		typ = obj["type"]
		
	img="";
	if("teaserBild" in obj):
		for width,imageObject in list(obj["teaserBild"].items()):
			if int(width) <= maxWidth:
				img=imageObject["url"];
	
	dur=''
	if("length" in obj):
		multi = False
		sec = obj["length"]
		if sec:
			dur = time.strftime('%H:%M Std.', time.gmtime(sec))	
		avail=''	
		if("offlineAvailability" in obj):
			avail = obj["offlineAvailability"]
			avail =time_translate(avail, day_warn=True)			# day_warn: noch x Tage!
			avail = u"[B]Verfügbar bis [COLOR darkgoldenrod]%s[/COLOR][/B]" % avail
		fsk = obj["fsk"]
		if fsk == "none":
			fsk = "ohne"
		geo = obj["geoLocation"]
		if geo == "none":
			geo = "ohne"
		length = obj["length"]
		#if "streamApiUrlVoice" in obj:						
		#	stream = obj["streamApiUrlVoice"] # needs api-token
		if "url" in obj:
			stream = obj["url"]
		# stream = obj["cockpitPrimaryTarget"]["url"] 			# Altern. (mit url identisch)
		if "externalId" in obj:
			scms_id = obj["externalId"]
			
		if SETTINGS.getSetting('pref_load_summary') == 'true':	# summary (Inhaltstext) im Voraus holen
			if "sharingUrl" in obj:								# Web-Referenz
				path=obj["sharingUrl"]
				descr_new = get_summary_pre(path, ID='ZDF',skip_verf=True,skip_pubDate=True)  # Modul util
				if 	len(descr_new) > len(descr):
					PLog("descr_new: " + descr_new[:60] )
					descr = descr_new
		

	summ = descr
	if multi:
		tag = "Folgeseiten"
	else:
		tag = "Dauer: %s | FSK: %s | GEO: %s | %s" % (dur, fsk, geo, avail)
	if headline:
		tag = "%s | [B]%s[/B]" % (tag, headline)
	
	
	PLog('Get_content typ: %s | title: %s | tag: %s | descr: %s |img:  %s | url: %s | stream: %s | scms_id: %s' %\
		(typ,title,tag,summ,img,url,stream,  scms_id) )		
	return typ,title,tag,summ,img,url,stream,scms_id

####################################################################################################
# ZDF-Suche:
# 	Voreinstellungen: alle ZDF-Sender, ganze Sendungen, sortiert nach Datum
#	Anzahl Suchergebnisse: 25 - nicht beeinflussbar
#	Format Datum (bisher nicht verwendet)
#		..&from=2012-12-01T00:00:00.000Z&to=2019-01-19T00:00:00.000Z&..
#	ZDF_Search_PATH steht bei Rekursion nicht als glob. Variable zur Verfügung
# 	02.06.2021 Umstellung auf alle Beiträge (statt ganzen Sendungen)
# 	25.04.2023 Umstellung auf zdf-cdn, Pfad für MEHR_Suche (s_type) 
#		identisch (Aufruf ZDF_search_button <- ZDF_RubrikSingle)
# 
def ZDF_Search(query=None, title='Search', s_type=None, pagenr=''):
	PLog("ZDF_Search:")
	if 	query == '':	
		query = get_query(channel='ZDF')
	PLog(query)
	if  query == None or query.strip() == '':
		return ""
	
	query = query.replace(u'–', '-')# verhindert 'ascii'-codec-Error
	query = query.replace(' ', '+')	# Aufruf aus Merkliste unbehandelt	
			
	query_org = query	
	query=py2_decode(query)			# decode, falls erf. (1. Aufruf)

	PLog(query); PLog(pagenr); PLog(s_type)

	ID='Search'
	ZDF_Search_PATH	 = "https://zdf-cdn.live.cellular.de/mediathekV2/search?profile=cellular-5&q=%s&page=%s"
	if s_type == 'Bilderserien':	# im api zdf-cdn nicht verfügbar (bilder-der-woche-100)
		ZDF_Search_PATH	 = 'https://www.zdf.de/suche?q=%s&synth=true&sender=Gesamtes+Angebot&from=&to=&attrs=&abGroup=gruppe-a&page=%s'
		ID=s_type
	
	if pagenr == '':		# erster Aufruf muss '' sein
		pagenr = 1
	path = ZDF_Search_PATH % (query, str(pagenr)) 
	PLog(path)
	path = transl_umlaute(path)
	
	page, msg = get_page(path=path, do_safe=False)	# +-Zeichen für Blank nicht quoten
	if s_type == 'Bilderserien':	# 'ganze Sendungen' aus Suchpfad entfernt:
		ZDF_Bildgalerien(page)
		return
	
	try:
		jsonObject = json.loads(page)
		searchResult = str(jsonObject["totalResultsCount"])
		nextUrl = str(jsonObject["nextPageUrl"])
		nextPage = str(jsonObject["nextPage"])
	except:
		searchResult=""; nextUrl=""; nextPage=""
	PLog("searchResult: "  + searchResult);
	PLog("nextPage: "  + nextPage);
	
	NAME = 'ZDF Mediathek'
	name = 'Suchergebnisse zu: %s (Gesamt: %s), Seite %s'  % (quote(py2_encode(query)), searchResult, pagenr)

	li = xbmcgui.ListItem()

	# Der Loader in ZDF-Suche liefert weitere hrefs, auch wenn weitere Ergebnisse fehlen
	# 22.01.2020 Webänderung 'class="artdirect " >' -> 'class="artdirect"'
	if not searchResult:
		query = (query.replace('%252B', ' ').replace('+', ' ')) # quotiertes ersetzen
		msg2 = msg 
		msg1 = 'Keine Ergebnisse (mehr) zu: %s' % query  
		MyDialog(msg1, msg2, '')
		return li	
				
	query = (query.replace('%252B', ' ').replace('+', ' ')) # quotiertes ersetzen
		
	DictID="ZDF_Search"											# hier dummy
	li=ZDF_PageMenu(DictID, jsonObject=jsonObject, mark=query, li=li)
	
	li = xbmcgui.ListItem()							# Kontext-Doppel verhindern
	PLog("nextUrl: " + nextUrl)
	if nextPage and nextUrl:
		query = query_org.replace('+', ' ')
		pagenr = re.search(u'&page=(\d+)', nextUrl).group(1)
		PLog(pagenr); 
		title = "Mehr Ergebnisse im ZDF zeigen zu: >%s<"  % query
		tagline = u"nächste Seite [B]%s[/B]" % pagenr
		query_org=py2_encode(query_org); 
		fparams="&fparams={'query': '%s', 's_type': '%s', 'pagenr': '%s'}" %\
			(quote(query_org), s_type, pagenr)
		addDir(li=li, label=title, action="dirList", dirID="ZDF_Search", fanart=R(ICON_MEHR), 
			thumb=R(ICON_MEHR), tagline=tagline, fparams=fparams)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
###################################################################################################
# Liste der Wochentage ZDF
# ARD s. ARDnew.SendungenAZ (früherer Classic-Code entfernt)
#
def ZDF_VerpasstWoche(name, title):									# Wochenliste ZDF Mediathek
	PLog('ZDF_VerpasstWoche:')
	PLog(name); 
	 
	sfilter=''
	fname = os.path.join(DICTSTORE, 'CurSenderZDF')				# init CurSenderZDF (aktueller Sender)
	if os.path.exists(fname):									# kann fehlen (Aufruf Merkliste)
		sfilter = Dict('load', 'CurSenderZDF')			
		
	if sfilter == '' or sfilter == False or sfilter == 'false':	# Ladefehler?
		sfilter = 'Alle ZDF-Sender'								# Default Alle ZDF-Sender (nur VERPASST)
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ZDF')						# Home-Button
		
	wlist = list(range(0,7))
	now = datetime.datetime.now()

	for nr in wlist:
		rdate = now - datetime.timedelta(days = nr)
		iDate = rdate.strftime("%d.%m.%Y")		# Formate s. man strftime (3)
		zdfDate = rdate.strftime("%Y-%m-%d")		
		iWeekday =  rdate.strftime("%A")
		punkte = '.'
		if nr == 0:
			iWeekday = 'Heute'	
		if nr == 1:
			iWeekday = 'Gestern'	
		iWeekday = transl_wtag(iWeekday)
		PLog(iDate); PLog(iWeekday);
		#title = ("%10s ..... %10s"% (iWeekday, iDate))	 # Formatierung in Plex ohne Wirkung		
		title =	"%s | %s" % (iDate, iWeekday)
		
		title=py2_encode(title); zdfDate=py2_encode(zdfDate);
		fparams="&fparams={'title': '%s', 'zdfDate': '%s', 'sfilter': '%s'}" % (quote(title), quote(zdfDate), sfilter)
		addDir(li=li, label=title, action="dirList", dirID="ZDF_Verpasst", fanart=R(ICON_ZDF_VERP), 
			thumb=R(ICON_ZDF_VERP), fparams=fparams)
	
	label = "Datum eingeben"							# Button für Datumeingabe anhängen
	tag = u"teilweise sind bis zu 4 Jahre alte Beiträge abrufbar"
	fparams="&fparams={'title': '%s', 'zdfDate': '%s', 'sfilter': '%s'}" % (quote(title), quote(zdfDate), sfilter)
	addDir(li=li, label=label, action="dirList", dirID="ZDF_Verpasst_Datum", fanart=R(ICON_ZDF_VERP), 
		thumb=GIT_CAL, fparams=fparams, tagline=tag)

														# Button für Stationsfilter
	label = u"Wählen Sie Ihren ZDF-Sender - aktuell: [B]%s[/B]" % sfilter
	tag = "Auswahl: Alle ZDF-Sender, zdf, zdfneo oder zdfinfo" 
	fparams="&fparams={'name': '%s', 'title': 'ZDF-Mediathek', 'sfilter': '%s'}" % (quote(name), sfilter)
	addDir(li=li, label=label, action="dirList", dirID="ZDF_Verpasst_Filter", fanart=R(ICON_ZDF_VERP), 
		thumb=R(ICON_FILTER), tagline=tag, fparams=fparams)
		
		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	# True, sonst Rückspr. nach ZDF_Verpasst_Filter
	
#-------------------------
#  03.06.2021 ARD_Verpasst_Filter (Classic) entfernt							
#-------------------------
# Auswahl der ZDF-Sender für ZDF_VerpasstWoche
# bei Abbruch bleibt sfilter unverändert
								
def ZDF_Verpasst_Filter(name, title, sfilter):
	PLog('ZDF_Verpasst_Filter:'); PLog(sfilter); 
	
	stations = ['Alle ZDF-Sender', 'ZDF', 'ZDFneo', 'ZDFinfo']
	if sfilter not in stations:		# Fallback für Version < 4.7.0
		i=0
	else:
		i = stations.index(sfilter)

	dialog = xbmcgui.Dialog()
	d = dialog.select('ZDF-Sendestation wählen', stations, preselect=i)
	if d == -1:						# Fallback Alle
		d = 0
	sfilter = stations[d]
	PLog("Auswahl: %d. %s" % (d, sfilter))
	Dict('store', "CurSenderZDF", sfilter)
	
	return ZDF_VerpasstWoche(name, title)

#-------------------------
# Aufruf ZDF_VerpasstWoche (Button "Datum eingeben")
# xbmcgui.INPUT_DATE gibt akt. Datum vor
# 11.01.2020: Ausgabe noch für 1.1.2016, nicht mehr für 1.1.2015
# sfilter wieder zurück an ZDF_VerpasstWoche
#
def ZDF_Verpasst_Datum(title, zdfDate, sfilter):
	PLog('ZDF_Verpasst_Datum:')
	
	dialog = xbmcgui.Dialog()
	inp = dialog.input("Eingabeformat: Tag/Monat/Jahr (4-stellig)", type=xbmcgui.INPUT_DATE)
	PLog(inp)
	if inp == '':
		return						# Listitem-Error, aber Verbleib im Listing
	d,m,y = inp.split('/')
	d=d.strip(); m=m.strip(); y=y.strip();
	if len(d) == 1: d="0%s" % d	
	if len(m) == 1: m="0%s" % m	
	if len(y) != 4:
		msg1 = 'Jahr bitte 4-stellig eingeben'
		MyDialog(msg1, '', '')
		return
	
	zdfDate = "%s-%s-%s" % (y,m,d)	# "%Y-%m-%d"
	PLog(zdfDate)
	
	# zurück zu ZDF_VerpasstWoche:
	ZDF_Verpasst(title='Datum manuell eingegeben', zdfDate=zdfDate, sfilter=sfilter)
	return
	
#-------------------------
# Aufruf: ZDF_VerpasstWoche, 2 Durchläufe
# 1. Buttons Morgens. Mittags, Abends, Nachts
# 2. Cluster-Ermittl. via DictID, Teaser-Auswertung 

def ZDF_Verpasst(title, zdfDate, sfilter='Alle ZDF-Sender', DictID=""):
	PLog('ZDF_Verpasst:'); PLog(title); PLog(zdfDate); PLog(sfilter);
	PLog("DictID: " + DictID);
	title_org = title

	mediatype=''													# Kennz. Videos im Listing
	if SETTINGS.getSetting('pref_video_direct') == 'true':
		mediatype='video'
	PLog('mediatype: ' + mediatype); 

	li = xbmcgui.ListItem()
	li = home(li, ID='ZDF')						# Home-Button

	# -----------------------------------------						# 2. Durchlauf
	
	if DictID:	
		jsonObject = Dict("load", DictID)
		teaserObject = jsonObject["teaser"]
		PLog(len(teaserObject))
		PLog(str(teaserObject)[:80])
		for entry in teaserObject:
			try:
				typ,title,tag,descr,img,url,stream,scms_id = ZDF_get_content(entry)
				airtime = entry["airtime"]
				t = airtime[-5:]
				title = "[COLOR blue]%s[/COLOR] | %s" % (t, title)	# Sendezeit | Titel
				channel = entry["channel"]
				if sfilter.startswith("Alle") == False:
					PLog("Mark0"); PLog(sfilter); PLog(channel)
					if sfilter != channel:							# filtern
						continue
				tag = "%s | Sender: [B]%s[/B]" % (tag,channel) 
					
				PLog("Satz4:")
				PLog(tag); PLog(title); PLog(stream);
				title = repl_json_chars(title)
				descr = repl_json_chars(descr)
				fparams="&fparams={'path': '%s','title': '%s','thumb': '%s','tag': '%s','summ': '%s','scms_id': '%s'}" %\
					(stream, title, img, tag, descr, scms_id)	
				addDir(li=li, label=title, action="dirList", dirID="ZDF_getApiStreams", fanart=img, thumb=img, 
					fparams=fparams, tagline=tag, summary=descr, mediatype=mediatype)
			except Exception as exception:
				PLog("verpasst_error: " + str(exception))
									
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
		return
	
	# -----------------------------------------							# 1. Durchlauf
	
	path = "https://zdf-cdn.live.cellular.de/mediathekV2/broadcast-missed/" + zdfDate
	page, msg = get_page(path)
	if page == '':
		msg1 = "Abruf fehlgeschlagen | %s" % title
		MyDialog(msg1, msg, '')
		return li 

	jsonObject = json.loads(page)
	clusterObject = jsonObject["broadcastCluster"]
	PLog(str(clusterObject)[:80])
	PLog("Cluster: %d " % len(clusterObject))

	msg1 = title								# Notification Datum + Sender
	if "manuell" in title:
		msg1 = "%s.%s.%s" % (zdfDate[8:10], zdfDate[5:7], zdfDate[0:4])
	msg2 = sfilter
	icon = R(ICON_ZDF_VERP)
	xbmcgui.Dialog().notification(msg1,msg2,icon,5000, sound=False)
	cnt=0
	for jsonObject in clusterObject:
		title = jsonObject["name"]
		img = ZDF_get_img(jsonObject["teaser"][0])
		tag = "Folgeseiten"
		DictID = "ZDF_Verpasst_%d" % cnt	 				# DictID: cluster-nr
		Dict('store', DictID, jsonObject)					# -> ZDF_Verpasst
	
		fparams="&fparams={'title': '%s', 'zdfDate': '%s', 'sfilter': '%s', 'DictID': '%s'}" %\
			(title_org, zdfDate, sfilter, DictID)
		PLog("fparams: " + fparams)	
		addDir(li=li, label=title, action="dirList", dirID="ZDF_Verpasst", fanart=img, 
		thumb=img, fparams=fparams, tagline=tag)
		cnt=cnt+1
		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
####################################################################################################
# ZDF-eigener Zugang via ZDF_Rubriken
# hier: Buchstaben-Icons vorgeschaltet ->  ZDF_AZList
#	einschl. Cache-Nutzung (AZ > 12 MByte)
#	ID=ZDFfunk <- Main_ZDFfunk
#
def ZDF_AZ(name, ID=""):						# name = "Sendungen A-Z"
	PLog('ZDF_AZ: ' + name);
	PLog(ID) 
	li = xbmcgui.ListItem()
	li = home(li, ID='ZDF')						# Home-Button
	
	azlist = list(string.ascii_uppercase)
	azlist.append('0 - 9')

	# Menü A to Z
	for element in azlist:
		title='Sendungen mit ' + element
		fparams="&fparams={'title': '%s', 'element': '%s', 'ID': '%s'}" % (title, element, ID)
		addDir(li=li, label=title, action="dirList", dirID="ZDF_AZList", fanart=R(ICON_ZDF_AZ), 
			thumb=R(ICON_ZDF_AZ), fparams=fparams)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

####################################################################################################
# Laden der Buchstaben-Seite, Auflistung der Sendereihen in 
#	ZDF_get_content -> ZDF_Sendungen (Cluster-Abzweig) -> ZDF_Rubriken 
#		-> ZDF_Sendungen (isvideo=False) / ZDF_BildgalerieSingle
#		-> ZDF_getVideoSources (isvideo=True)
# Buchstaben-Seiten enthalten nur Sendereihen, keine Einzelbeiträge
# 19.11.2020 Integration funk A-Z (ID=ZDFfunk)
#
def ZDF_AZList(title, element, ID=""):					# ZDF-Sendereihen zum gewählten Buchstaben
	PLog('ZDF_AZList: ' + element)
	PLog(title); PLog(ID);
	title_org = title
	
	DictID = "ZDF_sendungen-100"
	path = "https://zdf-cdn.live.cellular.de/mediathekV2/document/sendungen-100"
	msg1 = "Cache ZDF A-Z:"
	if "funk" in ID:
		DictID = "funk-alle-sendungen-von-a-z-100"
		path = "https://zdf-cdn.live.cellular.de/mediathekV2/document/%s" % DictID
		if element == "0 - 9":							# für funk o. Blanks
			element="0-9"
		msg1 = "Cache funk A-Z:"
	jsonObject = Dict("load", DictID, CacheTime=ZDF_CacheTime_AZ)
	if not jsonObject:
		icon = R(ICON_ZDF_AZ)
		xbmcgui.Dialog().notification(msg1,"Haltedauer 30 Min",icon,3000,sound=False)
		page, msg = get_page(path)
		if not page:												# nicht vorhanden?
			msg1 = 'ZDF_AZList: Beiträge können leider nicht geladen werden.' 
			msg2 = msg
			MyDialog(msg1, msg2, '')
			return
		jsonObject = json.loads(page)
		Dict("store", DictID, jsonObject)
		
	li = xbmcgui.ListItem()
	li = home(li, ID='ZDF')						# Home-Button

	PLog(str(jsonObject)[:80])
	jsonObject = jsonObject["cluster"]
	PLog(len(jsonObject))
	PLog(str(jsonObject)[:80])

	AZObject=[]	
	for clusterObject in jsonObject:
		PLog(str(clusterObject)[:12])
		if element in clusterObject["name"]:
			title = clusterObject["name"]
			PLog("found_title: " + title)
			AZObject = clusterObject
			break
	
	if AZObject:
		teaserObject = AZObject["teaser"]
		for entry in teaserObject:
			typ,title,tag,descr,img,url,stream,scms_id = ZDF_get_content(entry)
			title = repl_json_chars(title)
			label = title
			descr = repl_json_chars(descr)
			fparams="&fparams={'url': '%s', 'title': '%s'}" % (url, title)
			PLog("fparams: " + fparams)	
			addDir(li=li, label=label, action="dirList", dirID="ZDF_RubrikSingle", fanart=img, 
				thumb=img, fparams=fparams, summary=descr, tagline=tag)	
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#----------------------------------------------
# MEHR_Suche ZDF nach query (title)
# Aufrufer: ZDF_Sendungen
def ZDF_search_button(li, query):
	PLog('ZDF_search_button:')

	query = (query.replace('|', '').replace('>', '')) # Trenner + Staffelkennz. entfernen
	query_org = query

	query = query.replace(u"Das ZDF ist für den verlinkten Inhalt nicht verantwortlich!", '')
	label = u"Alle Beiträge im ZDF zu >%s< suchen"  % query_org
	query = query.replace(' ', '+')	
	tagline = u"zusätzliche Suche starten"
	summ 	= u"mehr Ergebnisse im ZDF suchen zu >%s<" % query_org
	s_type	= 'MEHR_Suche'						# Suche alle Beiträge (auch Minutenbeiträge)
	query=py2_encode(query); 
	fparams="&fparams={'query': '%s', 's_type': '%s'}" % (quote(query), s_type)
	addDir(li=li, label=label, action="dirList", dirID="ZDF_Search", fanart=R(ICON_MEHR), 
		thumb=R(ICON_MEHR), fparams=fparams, tagline=tagline, summary=summ)
	return
  
#----------------------------------------------
# Ähnlich ARD_FlatListEpisodes (dort entfällt die
#	Liste aller Serien)
# Aufruf ZDF_Sendungen (Abzweig), Button flache Serienliste,
#	zusätzl. Button für ZDF_getStrmList + strm-Tools
#	sid=Serien-ID (Url-Ende)
#	Ablauf: Liste holen via api-Call, Abgleich mit sid,
#		Serieninhalt holen via api-Call
# 	Cache: von der Gesamt-Liste (> 3 MB) werden im Dict nur
#		sid und url gespeichert
# 01.05.2023 Folge direkt holen mit sid statt serien-100
#
def ZDF_FlatListEpisodes(sid):
	PLog('ZDF_FlatListEpisodes: ' + sid)
	CacheTime = 43200											# 12 Std.
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ZDF')										# Home-Button			
	
	#															# headers wg. häufiger timeouts
	headers="{'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36', \
	'Referer': '%s', 'Accept-Encoding': 'gzip, deflate, br', 'Accept': 'application/json, text/plain, */*'}"
	path = "https://zdf-cdn.live.cellular.de/mediathekV2/document/%s" % sid 
	page, msg = get_page(path=path, header=headers, JsonPage=True)
	if page == "":	
		msg1 = "Abbruch  in ZDF_FlatListEpisodes:"
		msg2 = "Die Serien-ID [B]%s[/B] ist nicht (mehr)" % sid
		msg3 = " in der Serienübersicht des ZDF enthalten."
		MyDialog(msg1, msg2, msg3)	
		return
		
	jsonObject = json.loads(page)
	PLog(str(jsonObject)[:80])
		
	#-----------------------------								# strm-Buttons

	mediatype=''												# Kennz. Video für Sofortstart
	if SETTINGS.getSetting('pref_video_direct') == 'true':
		mediatype='video'
		
	#															# Button strm-Dateien gesamte Liste
	if SETTINGS.getSetting('pref_strm') == 'true':
		img = R(ICON_DIR_STRM)
		title = u"strm-Dateien für die komplette Liste erzeugen / aktualisieren"
		tag = u"Verwenden Sie das Kontextmenü, um strm-Dateien für [B]einzelne Videos[/B] zu erzeugen"
		summ = u"[B]strm-Dateien (strm-Bündel)[/B] sparen Platz und lassen sich auch in die Kodi-Bibliothek integrieren."
		summ = u"%s\n\nEin strm-Bündel in diesem Addon besteht aus der strm-Datei mit der Streamurl, einer jpeg-Datei" % summ
		summ = u"%s\nmit dem Bild zum Video und einer nfo-Datei mit dem Begleittext." % summ
		path=py2_encode(path); title=py2_encode(title); 
		fparams="&fparams={'path': '%s', 'title': '%s'}" %\
			(quote(path), quote(title))
		addDir(li=li, label=title, action="dirList", dirID="ZDF_getStrmList", fanart=img, thumb=img, 
			fparams=fparams, tagline=tag, summary=summ)
			
		title = u"strm-Tools"									# Button für strm-Tools
		tag = "Abgleichintervall in Stunden\nListen anzeigen\nListeneinträge löschen\n"
		tag = "%sMonitorreset\nstrm-Log anzeigen\nAbgleich einer Liste erzwingen\n" % tag
		tag = "%sunterstützte Sender/Beiträge\nzu einem strm-Verzeichnis wechseln" % tag
		myfunc="resources.lib.strm.strm_tools"
		fparams_add = quote('{}')

		fparams="&fparams={'myfunc': '%s', 'fparams_add': '%s'}"  %\
			(quote(myfunc), quote(fparams_add))			
		addDir(li=li, label=title, action="dirList", dirID="start_script",\
			fanart=R(FANART), thumb=R("icon-strmtools.png"), tagline=tag, fparams=fparams)	
		
	
	#-----------------------------								# Auswertung Serie

	# Blockmerkmal für Folgen unterschiedlich:					# Blockmerkmale wie ZDF_getStrmList	
	season_title = jsonObject["document"]["titel"]
	season_id 	= jsonObject["document"]["id"]
	staffel_list = jsonObject["cluster"]
	PLog("season_title: %s" % season_title)
	PLog("staffel_list: %d" % len(staffel_list))

	for staffel in 	staffel_list:
		if 	staffel["name"] == "":								# Teaser u.ä.
			continue							
		folgen = staffel["teaser"]								# Folgen-Blöcke	
		PLog("Folgen: %d" % len(folgen))
		for folge in folgen:
			# Abgleich headline/season_title entfällt wg. möglicher Abweichungen
			#	Bsp.: FETT UND FETT/FETT & FETT, daher Abgleich mit brandId
			scms_id = folge["id"]
			try:
				brandId = folge["brandId"]
			except:
				brandId=""
			if season_id != brandId:
				PLog("skip_no_brandId: " + str(folge)[:60])
				continue
			title, url, img, tag, summ, season, weburl = ZDF_FlatListRec(folge)
			if season == '':
				PLog("skip_no_season: " + str(folge)[:60])
				continue
				
			summ_par= summ.replace('\n', '||')
			tag_par= tag.replace('\n', '||')
			PLog("Satz29:")
			PLog(url);PLog(img);PLog(title);PLog(tag);PLog(summ[:80]); 
			url=py2_encode(url); title=py2_encode(title); img=py2_encode(img); 
			tag_par=py2_encode(tag_par);summ_par=py2_encode(summ_par);
			fparams="&fparams={'path': '%s', 'title': '%s', 'thumb': '%s', 'tag': '%s', 'summ': '%s', 'scms_id': '%s'}" %\
				(quote(url), quote(title), quote(img), quote(tag_par), quote(summ_par), scms_id)
			addDir(li=li, label=title, action="dirList", dirID="ZDF_getApiStreams", fanart=img, thumb=img, 
				fparams=fparams, tagline=tag, summary=summ, mediatype=mediatype)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#----------------------------------------------
# Ermittlung Streamquellen für api-call, ähnlich build_Streamlists 
#	aber abweichendes Quellformat
# Aufrufer: ZDF_FlatListEpisodes, ab V4.7.0 auch ZDF_PageMenu,
#	ZDF_Rubriken, ZDF_RubrikSingle, ZDF_Verpasst.
# Mitnutzung get_form_streams wie get_formitaeten  sowie
#	 build_Streamlists_buttons
# gui=False: ohne Gui, z.B. für ZDF_getStrmList
#
def ZDF_getApiStreams(path, title, thumb, tag,  summ, scms_id="", gui=True):
	PLog("ZDF_getApiStreams: " + scms_id)
	
	page, msg = get_page(path)
	if page == '':	
		msg1 = "Fehler in ZDF_getStreamSources:"
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return
	page = page.replace('\\/','/')

	li = xbmcgui.ListItem()
	if gui:
		li = home(li, ID='ZDF')								# Home-Button	
	
	availInfo = stringextract('"availabilityInfo":"',  '"', page) # FSK-Info? -> s.u. Dialog
	availInfo = transl_json(availInfo)
	channel = stringextract('"channel":"',  '"', page)
	
	HLS_List=[]; MP4_List=[]; HBBTV_List=[];				# MP4_List = download_list
	# erlaubte Formate wie build_Streamlists:
	only_list = ["h264_aac_mp4_http_na_na", "h264_aac_ts_http_m3u8_http",	
				"vp9_opus_webm_http_na_na", "vp8_vorbis_webm_http_na_na"
				]	
		
	# Format formitaeten von Webversion abweichend, build_Streamlists
	#	nicht verwendbar
	formitaeten, duration, geoblock, sub_path = get_form_streams(page)
	forms=[]
	if len(formitaeten) > 0:								# Videoquellen fehlen
		forms = stringextract('formitaeten":', ']', formitaeten[0])
		forms = blockextract('"type":', forms)
	PLog("forms: %d" % len(forms))
	
	Plot  = "%s||||%s" % (tag, summ)
	line=''; skip_list=[]
	for form in forms:
		track_add=''; class_add=''; lang_add=''				# class-und Sprach-Zusätze
		typ = stringextract('"type":"', '"', form)
		class_add = stringextract('"class":"',  '"', form)	
		lang_add = stringextract('"language":"',  '"', form)
		if class_add == "main": class_add = "TV-Ton"
		if class_add == "ot": class_add = "Originalton"
		if class_add == "ad": class_add = "Audiodeskription"
		if class_add or lang_add:
			track_add = "[B]%s %s[/B]" % (class_add, lang_add)
			track_add = "%23s" % track_add 				# formatiert
					
		url = stringextract('"url":"',  '"', form)		# Stream-URL
		PLog("url: " + url)
		server = stringextract('//',  '/', url)			# 2 Server pro Bitrate möglich
		if typ not in only_list or url in skip_list:
			continue
		skip_list.append(url)
			
		quality = stringextract('"quality":"',  '"', form)
		mimeType = stringextract('mimeType":"', '"', form)
		
		# bei HLS entfällt Parseplaylist - verschiedene HLS-Streams verfügbar 
		if url.find('master.m3u8') > 0:					# HLS-Stream 
			HLS_List.append('HLS, %s ** AUTO ** %s ** %s#%s' % (track_add, quality,title,url))
		else:
			res='0x0'; bitrate='0'; w=''; h=''			# Default					
			if 'hd":true' in form:	
				w = "1920"; h = "1080"					# Probeentnahme													
			if 'veryhigh' in quality:
				w = "1280"; h = "720"					# Probeentnahme							
			if 'high' in quality:
				w = "960"; h = "540"					# Probeentnahme							
			if 'med' in quality:
				w = "640"; h = "360"					# Probeentnahme							
			if 'low' in quality:
				w = "480"; h = "270"					# Probeentnahme							
			
			if '_' in url:
				try:									# wie build_Streamlists
					bitrate = re.search(u'_(\d+)k_', url).group(1)
					bitrate = "%skbit" % bitrate
				except:
					bitrate = "unbekannt"
			res = "%sx%s" % (w,h)
			title_url = u"%s#%s" % (title, url)
			item = u"MP4, %s | %s ** Bitrate %s ** Auflösung %s ** %s" %\
				(track_add, quality, bitrate, res, title_url)
			PLog("item: " + item)
			PLog("server: " + server)					# nur hier, kein Platz im Titel
			MP4_List.append(item)
			
	ID="ZDF"; HOME_ID = ID
	title_org = title
	
	PLog("HLS_List: " + str(len(HLS_List)))
	#PLog(HLS_List)
	PLog("MP4_List: " + str(len(MP4_List)))
	
	if scms_id:
		HBBTV_List = ZDFSourcesHBBTV(title, scms_id)	# bisher nur MP4-Quellen				
		Dict("store", '%s_HBBTV_List' % ID, HBBTV_List) 
	PLog("HBBTV_List: " + str(len(HBBTV_List)))
		
	Dict("store", '%s_HLS_List' % ID, HLS_List) 
	Dict("store", '%s_MP4_List' % ID, MP4_List) 
		
	if not len(HLS_List) and not len(MP4_List) and not len(HBBTV_List):			
		if gui:										# ohne Gui
			msg = 'keine Streamquellen gefunden - Abbruch' 
			PLog(msg); PLog(availInfo)
			msg1 = u"keine Streamquellen gefunden: [B]%s[/B]"	% title
			msg2=""
			if availInfo:
				msg2 = availInfo
			MyDialog(msg1, msg2, '')

		return HLS_List, MP4_List, HBBTV_List
	
	build_Streamlists_buttons(li,title_org,thumb,geoblock,Plot,sub_path,\
		HLS_List,MP4_List,HBBTV_List,ID,HOME_ID)

	if gui:											# ohne Gui
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	else:
		return

#----------------------------------------------
# erzeugt / aktualsiert strm-Dateien für die komplette Liste 
# Ermittlung Streamquellen für api-call
# Ablauf: Seite path laden, Blöcke wie ZDF_FlatListEpisodes
#	iterieren -> ZDF_FlatListRec -> ZDF_getApiStreams (Streamquelle 
#	ermitteln -> 
# Nutzung strm-Modul: get_strm_path, xbmcvfs_store
# Cache-Verzicht, um neue Folgen nicht zu verpassen.
#
def ZDF_getStrmList(path, title, ID="ZDF"):
	PLog("ZDF_getStrmList:")
	title_org = title
	list_path = path
	icon = R(ICON_DIR_STRM)
	FLAG_OnlyUrl = os.path.join(ADDON_DATA, "onlyurl")
	import resources.lib.strm as strm
	
	page, msg = get_page(path=path)
	if page == '':
		msg1 = "Fehler in ZDF_getStrmList:"
		msg2 = msg
		MyDialog(msg1, msg2, '')
		return
		
	if page.find('"seasonNumber"') < 0:
		msg1 = "[B]seasonNumber[/B] fehlt in den Beiträgen."
		msg2 = "strm-Liste für diese Serie kann nicht erstellt werden."
		MyDialog(msg1, msg2, '')
		return
		
	jsonObject = json.loads(page)
	PLog(str(jsonObject)[:80])
				
	list_title = jsonObject["document"]["titel"]
	list_title = transl_json(list_title)
	PLog("list_title:" + list_title)
	
	strm_type = strm.get_strm_genre()					# Genre-Auswahl
	if strm_type == '':
		return
	strmpath = strm.get_strm_path(strm_type)			# Abfrage Zielverz. != Filme
	if os.path.isdir(strmpath) == False:
		msg1 = "Zielverzeichnis existiert nicht."
		msg2 = u"Bitte Settings überprüfen."
		MyDialog(msg1, msg2, '')
		return
	
	fname = make_filenames(list_title)					# Abfrage Unterverzeichnis Serie
	strmpath = os.path.join(strmpath, fname)
	PLog("list_strmpath: " + strmpath)		
	head = u"Unterverzeichnis für die Serie"
	msg1 = u"Das Addon legt für die Serie folgendes Unterverzeichnis an:"
	if os.path.isdir(strmpath):		
		msg1 = u"Das Addon verwendet für die Serie folgendes Unterverzeichnis:"
	msg2 = u"[B]%s[/B]" % fname
	msg3 = u"Ein vorhandenes Verzeichnis wird überschrieben."
	ret = MyDialog(msg1, msg2, msg3, ok=False, cancel='Abbruch', yes='OK', heading=head)
	if ret != 1:
		return
	if os.path.isdir(strmpath) == False:
		os.mkdir(strmpath)											# Verz. erzeugen, falls noch nicht vorh.
		list_exist=False
	else:
		list_exist=True

	#---------------------
	# Blockmerkmale s. ZDF_FlatListEpisodes:						# Blockmerkmale wie ZDF_FlatListEpisodes
	staffel_list = jsonObject["cluster"]							# Staffel-Blöcke
	if len(staffel_list) == 0:										# ohne Staffel-Blöcke
		staffel_list = blockextract('"headline":"', page)
	season_title = jsonObject["document"]["titel"]
	season_id 	= jsonObject["document"]["id"]
	PLog("season_title: %s" % season_title)
	PLog("staffel_list: %d" % len(staffel_list))
	
	cnt=0; skip_cnt=0; do_break=False
	for staffel in 	staffel_list:
		folgen = staffel["teaser"]								# Folgen-Blöcke	
		PLog("Folgen: %d" % len(folgen))
		for folge in folgen:
			scms_id = folge["id"]								# wie ZDF_FlatListEpisodes
			try:
				brandId = folge["brandId"]
			except:
				brandId=""
			if season_id != brandId:
				PLog("skip_no_brandId: " + str(folge)[:60])
				continue
			title, url, img, tag, summ, season, weburl = ZDF_FlatListRec(folge) # Datensatz
			if season == '':
				PLog("skip_no_season: " + str(folge)[:60])
				continue
			
			fname = make_filenames(title)							# Zieldatei hier ohne Dialog
			PLog("fname: " + fname)
			if SETTINGS.getSetting('pref_strm_uz') == "true":	# Für jede strm-Datei ein Unterverzeichnis
				f = os.path.join(strmpath, fname, "%s.nfo" % fname)
			else:
				f = os.path.join(strmpath, "%s.nfo" % fname)
			PLog("f: " + f)
			if os.path.isfile(f):									# skip vorh. strm-Bundle
				msg1 = u'schon vorhanden:'
				msg2 = title
				xbmcgui.Dialog().notification(msg1,msg2,icon,500,sound=False)
				PLog("skip_bundle: " + f)
				skip_cnt=skip_cnt+1
				continue
			else:
				msg1 = u'neues strm-Bündel:'
				msg2 = title
				xbmcgui.Dialog().notification(msg1,msg2,icon,500,sound=False)
				
			PLog("Satz30:")
			PLog(url);PLog(img);PLog(title);PLog(tag);PLog(summ[:80]); 
			
			msg1 = u'Suche Streamquellen'
			msg2 = title
			xbmcgui.Dialog().notification(msg1,msg2,icon,500,sound=False)
			open(FLAG_OnlyUrl, 'w').close()							# Flag PlayVideo_Direct: kein Videostart
			ZDF_getApiStreams(url, title, img, tag,  summ, gui=False) # Streamlisten bauen, Ablage Url
			url = RLoad(STRM_URL, abs_path=True)					# abgelegt von PlayVideo_Direct
			PLog("strm_Url: " + str(url))
			
			Plot = "%s\n\n%s" % (tag, summ)
			ret = strm.xbmcvfs_store(strmpath, url, img, fname, title, Plot, weburl, strm_type)
			if ret:
				cnt=cnt+1

	#------------------
	PLog("strm_cnt: %d" % cnt)		
	msg1 = u'%d neue STRM-Datei(en)' % cnt
	if cnt == 0:
		msg1 = u'STRM-Liste fehlgeschlagen'
		if list_exist == True:
			msg1 = u'STRM-Liste unverändert'
	msg2 = list_title
	xbmcgui.Dialog().notification(msg1,msg2,icon,3000,sound=True)
		
	#------------------												# Liste synchronisieren?
	# Format: Listen-Titel ## lokale strm-Ablage ##  ext.Url ## strm_type
	item = "%s##%s##%s##%s"	% (list_title, strmpath, list_path, strm_type)
	PLog("item: " + item)
	synclist = strm.strm_synclist(mode="load")						# "strm_synclist"
	if exist_in_list(item, synclist) == True:	
		msg1 = "Synchronsisation läuft"
		msg2 = list_title
		xbmcgui.Dialog().notification(msg1,msg2,icon,3000,sound=True)
		PLog(msg1)
	else:
		sync_hour = strm.strm_tool_set(mode="load")	# Setting laden
		head = u"Liste synchronisieren"
		msg1 = u"Soll das Addon diese Liste regelmäßig abgleichen?"
		msg2 = u"Intervall: %s Stunden" % sync_hour	
		ret = MyDialog(msg1=msg1, msg2=msg2, msg3='', ok=False, cancel='Nein', yes='OK', heading=head)
		if ret == 1:											# Liste neu aufnehmen
			strm.strm_synclist(mode="save", item=item)
			line = "%6s | %15s | %s..." % ("NEU", list_title[:15], "Liste neu aufgenommen")
			strm.log_update(line)

	return

#----------------------------------------------
# holt Details für item
# Aufrufer: ZDF_FlatListEpisodes, ZDF_getStrmList
def ZDF_FlatListRec(item):
	PLog('ZDF_FlatListRec:')
	PLog(str(item)[:80])

	title='';url='';img='';tag='';summ='';season='';
	descr='';weburl=''
	
	if "seasonNumber" in item:
		season =  item["seasonNumber"]						# string
	if season == '':										# Satz verwerfen	
		return title, url, img, tag, summ, season, weburl
		
	episode =  item["episodeNumber"]						# string
	PLog(season); PLog(episode)
	title_pre = "S%02dE%02d" % (int(season), int(episode))	# 31.01.2022 S13_F10 -> S13E10
	PLog("Mark1")
	
	brand =  item["headline"]
	title =	 item["titel"]
	title =  repl_json_chars(title)			
	descr =  item["beschreibung"]
	weburl =  item["sharingUrl"] 							# für Abgleich vor./nicht mehr vorh. 
	fsk =  item["fsk"]
	if fsk == "none":
		fsk = "ohne"
	end =  item["timetolive"]								# Altern.: offlineAvailability
	end = u"[B]Verfügbar bis [COLOR darkgoldenrod]%s[/COLOR][/B]" % end
	geo =  item["geoLocation"]
	if geo == "none":
		geo = "ohne"
	dauer = item["length"]
	dauer = seconds_translate(dauer)
	title = "%s | %s" % (title_pre, title)
	
	img = ZDF_get_img(item)
	url =  item["cockpitPrimaryTarget"]["url"]				# Ziel-Url mit Streamquellen
	
	tag = u"%s | Staffel: %s | Folge: %s\nDauer: %s | FSK: %s | Geo: %s | %s" %\
		(brand, season, episode, dauer, fsk, geo, end)
	
	title = repl_json_chars(title); title = unescape(title); 
	summ = repl_json_chars(descr)

	return title, url, img, tag, summ, season, weburl

#-------------------------
# wertet die (teilw. unterschiedlichen) Parameter von
#	class="bottom-teaser-box"> aus.
# Aufrufer: ZDF_Rubriken, get_teaserElement (loader-
#	Beiträge), 
#
def ZDF_get_teaserbox(page):
	PLog('ZDF_get_teaserbox:')
	teaser_label='';teaser_typ='';teaser_nr='';teaser_brand='';teaser_count='';multi=False
	
	if 'class="bottom-teaser-box">' in page:
		if 'class="teaser-cat-category">' in page:
			if 'cat-category-ellipsis">' in page:
				# teaser_brand =  stringextract('cat-category-ellipsis">', '</', page)	   
				teaser_brand =  stringextract('cat-category-ellipsis">', '<a href=', page)	 
			else:		
				teaser_typ = stringextract('class="teaser-cat-category">', '</', page)   # teaser_brand s.u.
			
		else:
			teaser_label = stringextract('class="teaser-label"', '</div>', page) 
			teaser_typ =  stringextract('<strong>', '</strong>', teaser_label)
				
		PLog('teaser_typ: ' + teaser_typ)
		teaser_label = cleanhtml(teaser_label.strip())					# wird ev. -> title	
		teaser_label = unescape(teaser_label);
		teaser_typ = mystrip(teaser_typ.strip())
		
		if u"teaser-episode-number" in page:
			teaser_nr = stringextract('teaser-episode-number">', '</', page)
		if teaser_typ == u'Beiträge':		# Mehrfachergebnisse ohne Datum + Uhrzeit
			multi = True
			
		# teaser_brand bei Staffeln (vor Titel s.u.)
		if teaser_brand == '':
			# teaser_brand = stringextract('cat-brand-ellipsis">', '</', page)  
			teaser_brand =  stringextract('cat-brand-ellipsis">', '<a href=', page)	 # Bsp. Wilsberg, St. 07 -
		
		teaser_brand = cleanhtml(teaser_brand);
		teaser_brand = mystrip(teaser_brand)
		teaser_brand = (teaser_brand.replace(" - ", "").replace(" , ", ", "))
	
	if teaser_nr == '' and teaser_count == '':							# mögl. Serienkennz. bei loader-Beiträgen,
		ts = stringextract('502_play icon ">', '</div>', page)			# Bsp. der STA
		ts=mystrip(ts); ts=cleanhtml(ts)
		if teaser_typ == '':
			teaser_typ=ts
			
	# Bsp. teaser_label class="teaser-label">4 Teile</div> oder 
	#	class="teaser-label"><div class="ellipsis">3 Teile</div></div>
	if teaser_label == '' and teaser_typ == '':							# z.B. >3 Teile< bei Doku-Titel
		teaser_label = stringextract('class="teaser-label"', '</div>', page)
		try: 
			teaser_typ = re.search(u'>(\d+) Teile', teaser_label).group(0)
		except:
			teaser_typ=''
	teaser_label = mystrip(teaser_label) 
	teaser_label = teaser_label.replace('<div class="ellipsis">', ' ')
	teaser_label = (teaser_label.replace('<strong>', '').replace('</strong>', ''))
	PLog(teaser_label); PLog(teaser_typ);

	PLog('teaser_label: %s,teaser_typ: %s, teaser_nr: %s, teaser_brand: %s, teaser_count: %s, multi: %s' %\
		(teaser_label,teaser_typ,teaser_nr,teaser_brand,teaser_count, multi))
		
	return teaser_label,teaser_typ,teaser_nr,teaser_brand,teaser_count,multi
	
#-------------------------
# ermittelt html-Pfad in json-Listen für ZDF_Rubriken
#	 z.Z. nicht benötigt s.o. (ZDF_BASE+NodePath+sophId)
def ZDF_get_rubrikpath(page, sophId):
	PLog('ZDF_get_rubrikpath: ' + sophId)
	path=''
	if sophId == '':	# Sicherung
		return path
	content =  blockextract('"@type":"ListItem"', page) # Beiträge des Clusters
	PLog(len(content))
	for rec in content:
		path =  stringextract('"url":"', '"', rec)
		if sophId in path:
			PLog("path: " + path)
			return path	
	return	'' 
		
####################################################################################################
# ZDF Barrierefreie Angebote - Vorauswahl
# 25.04.2023 Funktionen BarriereArm + BarriereArmSingle
#	gelöscht - neu in ZDF_Start -> ZDF_RubrikSingle
####################################################################################################

def International(title):
	PLog('International:'); 
	title_org = title
	CacheTime = 6000								# 1 Std.
			
	#path = 'https://www.zdf.de/international/zdfenglish'		# engl. Seite
	#path = 'https://www.zdf.de/international/zdfarabic'		# arab. Seite
	path = 'https://www.zdf.de/international'					# Cluster-Auswertung
	ID="ZDFInternational"
	
	page = Dict("load", ID, CacheTime=CacheTime)
	if page == False or page == '':								# Cache miss od. leer - vom Sender holen
		page, msg = get_page(path=path)
		Dict("store", ID, page) 								# Seite -> Cache: aktualisieren	
	if page == '':
		msg1 = 'Beitrag kann nicht geladen werden.'
		msg2 = msg
		MyDialog(msg1, msg2, '')
		return					
	
	ZDF_Sendungen(path, title, ID, page=page)
				
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)	
	
#-----------------------------------------------------------------------
# vergleicht Titel + Länge eines Beitrags mit den Listen full_shows_ZDF,
#	full_shows_ARD
# title_samml: Titel|Subtitel oder (Long-|Medium-|Short-Titel)
# duration: Minuten-Wert (ARD-sec umrechnen)
# fname: Dateinamen der Liste (full_shows_ZDF, full_shows_ARD)
# Rückgabe: fett-markierter Titel bei entspr. Beitrag, sonst unbeh.
#	Titel
# Aufrufer: ZDF_get_content, get_json_content (ARDnew)
#
def full_shows(title, title_samml, summary, duration,  fname):
	PLog('full_shows:')
	PLog(title_samml); PLog(summary[:60]); PLog(duration); PLog(fname);
	
	if duration == '':									# Sicherung gg. int()-error
		return title
	
	ret = "nofill"										# Return-Flag
	if SETTINGS.getSetting('pref_mark_full_shows') == 'true':
		path = SETTINGS.getSetting('pref_fullshows_path')
		if path == '':
			path = '%s/resources/%s' % (ADDON_PATH, fname)
		else:
			path = "%s/%s" % (SETTINGS.getSetting('pref_mark_full_shows'), fname)
		shows = ReadTextFile(path)
		PLog("path: " + path)
		PLog('full_shows_lines: %d' % len(shows))

		duration=py2_decode(duration)
		if " min" in duration:							# Bsp. "Videolänge 1 min", "33 min · Comedy"
			try:
				duration = re.search(u'(\d+) min', duration).group(1)
			except:
				duration=''
			
		if duration.startswith("Dauer "):				# Bsp. Dauer 0:01 od. Dauer 59 sec
			duration = duration.split("Dauer ")[1]
		if duration.endswith(" sec"):					# Bsp. 59 sec 
			duration = duration.split(" sec")[0]
		if ':' in duration:
			duration = time_to_minutes(duration)
		PLog("duration: " + duration)
		title = title.strip()

		ret = "nofill"									# Return-Flag
		for show in shows:
			st, sdur = show.split("|")					# Bsp. Querbeet|40
			#PLog(duration); PLog(st); PLog(sdur); # PLog(up_low(st) in up_low(title));
			# Show in Datensatz?:
			if up_low(st) in up_low(title_samml) or up_low(st) in up_low(summary): 
				if sdur:
					if ':' in sdur:
						sdur = time_to_minutes(duration)
					PLog("sdur: " + sdur)
					if int(duration) >= int(sdur):
						title = "[B]%s[/B]" % title
						ret = "fill"
				break		
	PLog("%s_return: %s" % (ret, title))
	return title
	
#-------------------------
# Bau HLS_List, MP4_List, HBBTV_List (nur ZDF + Arte)
# Formate siehe StreamsShow						
#	generisch: "Label |  Bandbreite | Auflösung | Titel#Url"
#	fehlende Bandbreiten + Auflösungen werden ergänzt
# Aufrufer: ZDF_getVideoSources, SingleBeitrag (my3Sat)
# formitaeten: Blöcke 'formitaeten' (get_form_streams)
# 08.03.2022 Anpassung für Originalton + Audiodeskription (class_add)
# 21.01.2023 UHD-Streams für Testbetrieb ergänzt (add_UHD_Streams)
#
def build_Streamlists(li,title,thumb,geoblock,tagline,sub_path,formitaeten,scms_id='',ID="ZDF",weburl=''):
	PLog('build_Streamlists:'); PLog(ID)
	title_org = title	
	
	HLS_List=[]; MP4_List=[]; HBBTV_List=[];			# MP4_List = download_list
	skip_list=[]
	# erlaubte Formate wie ZDF_getApiStreams 
	only_list = ["h264_aac_mp4_http_na_na", "h264_aac_ts_http_m3u8_http",	# erlaubte Formate
				"vp9_opus_webm_http_na_na", "vp8_vorbis_webm_http_na_na"]
	for rec in formitaeten:									# Datensätze gesamt, Achtung unicode!
		typ = stringextract('"type":"', '"', rec)
		typ = typ.replace('[]', '').strip()
		facets = stringextract('"facets": ', ',', rec)	# Bsp.: "facets": ["progressive"]
		facets = facets.replace('"', '').replace('\n', '').replace(' ', '') 
		PLog("typ %s, facets %s" % (typ, facets))
		if typ not in only_list:
			continue 
		if "restriction_useragent" in facets:			# Server rodlzdf statt nrodlzdf sonst identisch
			continue 
			
		audio = blockextract('"audio":', rec)			# Datensätze je Typ
		tagline_org=tagline
		PLog("audio_Blocks: " + str(len(audio)))
		# PLog(audio)	# bei Bedarf
		for audiorec in audio:
			mimeCodec = stringextract('"mimeCodec":"',  '"', audiorec)
			if '"cdn":' in audiorec:
				tracks = blockextract('"cdn":', audiorec)		# class-Sätze: main, ot, ad
			else:
				tracks = blockextract('"language":', audiorec)	# class-Sätze in ZDF-funk
			PLog("tracks: " + str(len(tracks)))
			quality = stringextract('"quality":"',  '"', audiorec)
			quality = up_low(quality)
			
			for track in tracks:	
				track_add=''; class_add=''; lang_add=''				# class-und Sprach-Zusätze
				class_add = stringextract('"class":"',  '"', track)	
				lang_add = stringextract('"language":"',  '"', track)
				if class_add == "main": class_add = "TV-Ton"
				if class_add == "ot": class_add = "Originalton"
				if class_add == "ad": class_add = "Audiodeskription"
				if class_add or lang_add:
					track_add = "[B]%s %s[/B]" % (class_add, lang_add)
					track_add = "%23s" % track_add
					
				url = stringextract('"uri":"',  '"', track)			# URL
				# Zusatz audiotrack ff. abschneiden, lädt falsche Playlist ('#EXT-X-MEDIA')
				if '?audiotrack=1' in url:
					url = url.split('?audiotrack=1')[0]					

				PLog("track:"); 
				PLog(class_add); PLog(lang_add); PLog(url); PLog(quality);
				if url:	
					#PLog(skip_list)	# Debug
					if up_low(quality) == 'AUTO' and 'master.m3u8' not in url:	# ZDF-funk: m3u8-Urls nicht verwertbar
						continue												#	(manifest.m3u8)
					url_combi = "%s|%s" % (class_add, url)
					if url_combi in skip_list:
						PLog("skip_url_combi: " + url_combi)
						continue
					skip_list.append(url)	
					
					if url.find('master.m3u8') > 0:					# m3u8 high (=auto) enthält alle Auflösungen
						if 'AUTO' in up_low(quality):				# skip high, med + low
							if track_add:
								HLS_List.append('HLS, %s ** AUTO ** %s ** %s#%s' % (track_add, quality,title,url))
							else:
								HLS_List.append('HLS, automatische Anpassung ** AUTO ** AUTO ** %s#%s' % (title,url))
							Stream_List = Parseplaylist(li, url, thumb, geoblock, tagline,\
								stitle=title,buttons=False, track_add=track_add)
							HLS_List = HLS_List + Stream_List

					else:	
						res='0x0'; bitrate='0'; w='0'; h='0'						# Default funk ohne AzureStructure						
						if 'HD' in quality:							# up_low(quality s.o.
							w = "1920"; h = "1080"					# Probeentnahme													
						if 'VERYHIGH' in quality:
							w = "1280"; h = "720"					# Probeentnahme							
						if 'HIGH' in quality:
							w = "960"; h = "540"					# Probeentnahme							
						if 'MED' in quality:
							w = "640"; h = "360"					# Probeentnahme							
						if 'LOW' in quality:
							w = "480"; h = "270"					# Probeentnahme							
						
						if '://funk' in url:						# funk: anderes Format (nur AzureStructure)
							# Bsp.: ../1646936_src_1024x576_1500.mp4?fv=1
							if '_' in url:
								res = url.split('_')[2]
								bitrate = url.split('_')[3]				# 6000.mp4?fv=2
								bitrate = bitrate.split('.')[0]
								bitrate = bitrate + "000"				# K-Angabe anpassen 
						else:
							if '_' in url:
								try:								# Fehlschlag bei arte-Links
									bitrate = re.search(u'_(\d+)k_', url).group(1)
									bitrate = "%skbit" % bitrate
								except:
									bitrate = "?"
							res = "%sx%s" % (w,h)
						
						PLog(res)
						title_url = u"%s#%s" % (title, url)
						mp4 = "%s" % "MP4"
						if ".webm" in url:
							mp4 = "%s" % "WEBM"
						item = u" %s, %s | %s ** Bitrate %s ** Auflösung %s ** %s" %\
							(mp4, track_add, quality, bitrate, res, title_url)
						MP4_List.append(item)
	
	
	PLog("HLS_List: " + str(len(HLS_List)))
	#PLog(HLS_List)	# Debug
	PLog("MP4_List: " + str(len(MP4_List)))
		
	if not len(HLS_List) and not len(MP4_List):			
		msg = 'keine Streamingquelle gefunden - Abbruch' 
		PLog(msg)
		msg1 = u"keine Streamingquelle gefunden: %s"	% title
		MyDialog(msg1, '', '')	
		return HLS_List, MP4_List, HBBTV_List
	
	# ------------										# HBBTV + UHD-Streams von ZDF + 3sat:
	UHD_DL_list=[]
	if ID == "ZDF":										# ZDF, ZDF-funk							
		HBBTV_List = ZDFSourcesHBBTV(title, scms_id)	# bisher nur MP4-Quellen				
		PLog("HBBTV_List: " + str(len(HBBTV_List)))
		# UHD-Streams erzeugen+testen:					# UHD-Streams -> HBBTV_List
		HBBTV_List, UHD_DL_list = add_UHD_Streams(HBBTV_List)
		Dict("store", '%s_HBBTV_List' % ID, HBBTV_List) 
	if ID == "3sat":									# 3sat 
		HBBTV_List = m3satSourcesHBBTV(weburl, title_org)	 				
		PLog("HBBTV_List: " + str(len(HBBTV_List)))
		# UHD-Streams erzeugen+testen:					# UHD-Streams -> HBBTV_List
		HBBTV_List, UHD_DL_list = add_UHD_Streams(HBBTV_List)
		Dict("store", '%s_HBBTV_List' % ID, HBBTV_List) 
		
	PLog("UHD_DL_list: " + str(len(UHD_DL_list)))
		
	Dict("store", '%s_HLS_List' % ID, HLS_List) 
	# MP4_List = add_UHD_Streams(MP4_List)				# entf., nur in HBBTV-Quellen (?)
	if len(UHD_DL_list) > 0:							# UHD_Liste für Downloads anhängen
		MP4_List = UHD_DL_list + MP4_List
	Dict("store", '%s_MP4_List' % ID, MP4_List) 

		
	tagline = "Titel: %s\n\n%s" % (title_org, tagline)	# s.a. ARD (Classic + Neu)
	tagline=repl_json_chars(tagline); tagline=tagline.replace( '||', '\n')
	Plot=tagline; 
	Plot=Plot.replace('\n', '||')
	
	HOME_ID = ID										# ZDF (Default), 3sat
	PLog('Lists_ready: ID=%s, HOME_ID=%s' % (ID, HOME_ID));
		
	build_Streamlists_buttons(li,title_org,thumb,geoblock,Plot,sub_path,\
		HLS_List,MP4_List,HBBTV_List,ID,HOME_ID)
	
	PLog("build_Streamlists_end")		
	return HLS_List, MP4_List, HBBTV_List
	
#-------------------------
# Aufruf: build_Streamlists
# ZDF-UHD-Streams kennzeichnen
# verfügbare UHD-Streams werden oben in
#	MP4_List (->Downloadliste) eingefügt.
# 24.02.2023 replace("3360k_p36v15", "4692k_p72v16") entfällt
#	mit Auswertung "q5" in ZDFSourcesHBBTV "h265_*", Verfügbarkeits-
#	Ping ebenfalls entbehrlich.
def add_UHD_Streams(Stream_List):
	PLog('add_UHD_Streams:')

	UHD_DL_list=[]; 
	cnt_find=0; cnt_ready=0
	mark="_4692k_"											# bei Bedarf ergänzen
	
	cnt=0
	for item in Stream_List:
		url = item.split("#")[-1]
		PLog(url)
		if url.find(mark) > 0:	 
			item = item.replace("MP4,", "[B]UHD_MP4[/B],")	# Label ändern
			item = item.replace("WEBM,", "[B]UHD_WEBM[/B],")
			Stream_List[cnt] = item							# Stream_List aktualisieren
			UHD_DL_list.append(item)						# add UHD-Download-Streams
			cnt_ready=cnt_ready+1

		cnt=cnt+1

	PLog(u"found_UDH_Template: %d" % cnt_find)
	return Stream_List, UHD_DL_list
	
#-------------------------
# Aufruf: build_Streamlists
# 3sat-HBBTV-MP4-Streams ermitteln, URL-Schema aus
# 	add_UHD_Streams testen + ggfls uhd_list
# Verzicht auf HLS-HBBTV-Streams (bei Bedarf ergänzen)
#
def m3satSourcesHBBTV(weburl, title):
	PLog('m3satSourcesHBBTV: ' + weburl)

	stream_list=[]; HBBTV_List=[]
	base= "http://hbbtv.zdf.de/3satm/dyn/get.php?id="
	 
	try:
		url = weburl.split("/")[-1]				# ../kultur/kulturdoku/kuenstlerduelle-vangogh-gaugin-100.html
		url = url.split(".html")[0]
	except Exception as exception:
		PLog(str(exception))			
		return HBBTV_List

	path = base + url
	page,msg = get_page(path)
	
	mp4uhd_obs={}; mp4_obs={}; hls_obs={}; obs={}
	try:
		objs = json.loads(page)
		PLog(len(objs))
		if "h265_aac_mp4_http_na_na" in objs["vidurls"]:								# UHD -MP4 - bisher unbekannt
			mp4uhd_obs = objs["vidurls"]["h265_aac_mp4_http_na_na"]["main"]["deu"] 		# MP4-Streams
			PLog("h265_mp4" + str(objs["vidurls"]["h265_aac_mp4_http_na_na"]["main"]))
		if "h264_aac_mp4_http_na_na" in objs["vidurls"]:
			mp4_obs = objs["vidurls"]["h264_aac_mp4_http_na_na"]["main"]["deu"] 		# MP4-Streams
			PLog("h264_mp4" + str(objs["vidurls"]["h264_aac_mp4_http_na_na"]["main"]))
		if "h264_aac_ts_http_m3u8_http" in objs["vidurls"]:
			hls_obs = objs["vidurls"]["h264_aac_ts_http_m3u8_http"]["main"]["deu"] 		# HLS-Streams, fehlen ev.
			PLog("h264_hls" + str(objs["vidurls"]["h264_aac_mp4_http_na_na"]["main"]))
	except Exception as exception:
		PLog(str(exception))
		page=""				
	if page == '':
		PLog("no_vidurls_found")		 		
		return HBBTV_List
	
	PLog("mp4uhd_obs: %d, mp4_obs: %d, hls_obs: %d" % (len(mp4uhd_obs), len(mp4_obs), len(hls_obs)))
	objs = dict(mp4uhd_obs, **mp4_obs)							# dicts verbinden
	objs = dict(obs, **hls_obs)	
	PLog(str(objs))												# {'q3': 'http://tvdlzdf-..v15.mp4'}
	
	for obj in objs.items():
		PLog(str(obj))
		qual = obj[0]
		url = obj[1]
		stream_list.append("%s|%s" % (qual, url))
	
	label="deu"	
	HBBTV_List = form_HBBTV_Streams(stream_list,label,title)	# Formatierung wie ZDF-Streams	
	PLog(str(HBBTV_List))
	
	return HBBTV_List
	
#-------------------------
# Sofortstart + Buttons für die einz. Streamlisten
# Aufrufer: build_Streamlists (ZDF, 3sat), ARDStartSingle (ARD Neu),
#	SingleSendung (ARD Classic), XLGetSourcesPlayer
# Plot = tagline (zusammengefasst: Titel (abgesetzt), tagline, summary)
# Kennzeichung mit mediatype='video' vor aufrufenden Funktionenen, z.B.
#	StreamsShow, XLGetSourcesPlayer, ZDF_getApiStreams
#
def build_Streamlists_buttons(li,title_org,thumb,geoblock,Plot,sub_path,\
		HLS_List,MP4_List,HBBTV_List,ID="ZDF",HOME_ID="ZDF"):
	PLog('build_Streamlists_buttons:'); PLog(ID)
	
	if geoblock and geoblock not in Plot:
		Plot = "%s||%s" % (Plot, geoblock) 
	
	tagline = Plot.replace('||', '\n')
	Plot = Plot.replace('\n', '||')
	
	# Sofortstart HLS / MP4 - abhängig von Settings	 	# Sofortstart
	played_direct=False
	if SETTINGS.getSetting('pref_video_direct') == 'true':	
		PLog('Sofortstart: build_Streamlists_buttons, ID: %s' % ID)
		played_direct=True
		img = thumb
		PlayVideo_Direct(HLS_List, MP4_List, title_org, img, Plot, sub_path, HBBTV_List=HBBTV_List,ID=ID)
		return played_direct							# direct-Flag z.B. für ARDStartSingle
		

	# -----------------------------------------			# Buttons Einzelauflösungen
	PLog("Satz3_buttons:")
	title_list=[]
	img=thumb; 
	PLog(title_org); PLog(tagline[:60]); PLog(img); PLog(sub_path);
	
	PLog(str(HBBTV_List))
	
	uhd_cnt_hb = str(HBBTV_List).count("UHD")				# UHD-Kennz. -> Titel ZDF+3sat
	uhd_cnt_hls = str(HLS_List).count("UHD")				# Arte
	uhd_cnt_mp4 = str(MP4_List).count("UHD")
	PLog("uhd_cnt: %d, %d, %d" % (uhd_cnt_hb, uhd_cnt_hls, uhd_cnt_mp4))
	
	title_hb = "[B]HBBTV[/B]-Formate"
	if uhd_cnt_hb:
		title_hb = title_hb + ", einschl. [B]UHD-Streams[/B]"
	title_hls 	= u"[B]Streaming[/B]-Formate"
	if uhd_cnt_hls:
		title_hls = title_hls + ", einschl. [B]UHD-Streams[/B]"
	title_mp4 = "[B]MP4[/B]-Formate und [B]Downloads[/B]"
	if uhd_cnt_mp4:
		title_mp4 = title_mp4 + ", einschl. [B]UHD-Streams[/B]"
	title_hls=repl_json_chars(title_hls); title_hb=repl_json_chars(title_hb);
	title_mp4=repl_json_chars(title_mp4); 
	
	# title_list: Titel + Dict-ID + Anzahl Streams
	title_list.append("%s###%s###%s" % (title_hls, '%s_HLS_List' % ID, len(HLS_List)))
	if ID == "ARDNEU" or ID == "ZDF" or ID == "arte" or ID == "3sat":			# HBBTV: ZDF, arte, 3sat
		listtyp = "%s_HBBTV_List" % ID
		title_list.append("%s###%s###%s" % (title_hb, listtyp, len(HBBTV_List)))	
	title_list.append("%s###%s###%s" % (title_mp4, '%s_MP4_List' % ID, len(MP4_List)))	
	PLog(len(title_list))

	Plot=py2_encode(Plot); img=py2_encode(img);
	geoblock=py2_encode(geoblock); sub_path=py2_encode(sub_path); 
	
	for item in title_list:
		title, Dict_ID, anz = item.split('###')
		if anz == '0':									# skip leere Liste
			continue
		title=py2_encode(title); title_org=py2_encode(title_org);
		fparams="&fparams={'title': '%s', 'Plot': '%s', 'img': '%s', 'geoblock': '%s', 'sub_path': '%s', 'ID': '%s', 'HOME_ID': '%s'}" \
			% (quote(title_org), quote(Plot), quote(img), quote(geoblock), quote(sub_path), Dict_ID, HOME_ID)
		addDir(li=li, label=title, action="dirList", dirID="StreamsShow", fanart=img, thumb=img, 
			fparams=fparams, tagline=tagline, mediatype='')	
	
	return played_direct
	
#-------------------------
# HBBTV Videoquellen (nur ZDF)		
def ZDFSourcesHBBTV(title, scms_id):
	PLog('ZDFSourcesHBBTV:'); 
	PLog("scms_id: " + scms_id) 
	HBBTV_List=[]
	url = "https://hbbtv.zdf.de/zdfm3/dyn/get.php?id=%s" % scms_id
		
	# Call funktioniert auch ohne Header:
	header = "{'Host': 'hbbtv.zdf.de', 'content-type': 'application/vnd.hbbtv.xhtml+xml'}"
	page, msg = get_page(path=url, header=header, JsonPage=True)	
	if page == '':						
		msg1 = u'HBBTV-Quellen nicht vorhanden / verfügbar'
		msg2 = u'Video: %s' % title
		MyDialog(msg1, msg2, '')
		return HBBTV_List
		
	page = page.replace('": "', '":"')				# für funk-Beiträge erforderlich
	PLog('page_hbbtv: ' + page[:100])
				
	streams = stringextract('"streams":', '"head":', page)	# Video-URL's ermitteln
	streams = streams.replace('\\/','/')
	ptmdUrl_list = blockextract('"ptmdUrl":', streams)		# mehrere mögl., z.B. Normal + DGS
	#PLog(ptmdUrl_list)
	PLog(len(ptmdUrl_list))

	q_list=['"q1"', '"q2"', '"q3"', '"q4"', '"q5"']			# Bsp.: "q1": "http://tvdlzdf..
	for ptmdUrl in ptmdUrl_list:							# 1-2
		PLog(ptmdUrl[:200])
		label = stringextract('"label":"', '"', ptmdUrl)
		main_list = blockextract('"main":', ptmdUrl)		#  mehrere mögl., z.B. MP4, m3u8
		stream_list=[]
		for qual in main_list:								# bisher q1, q2, q3, q5 gesehen
			PLog(qual[:80])
			url = stringextract('"url":"',  '"', qual)
			for q in q_list:
				if q in qual:
					q = q[1:-1]
					break
			stream_list.append("%s|%s" % (q, url)) 		
		
		PLog(len(stream_list))
		HBBTV_List = form_HBBTV_Streams(stream_list, label, title)	# Formatierung
		
	PLog(len(HBBTV_List))
	return HBBTV_List
	
#-------------------------
# Aufruf: ZDFSourcesHBBTV, m3satSourcesHBBTV
# Formatierung der Streamlinks ("Qual.|Link")
def form_HBBTV_Streams(stream_list, label, title):
	PLog('form_HBBTV_Streams:')
	HBBTV_List=[]
	
	for stream in stream_list:
		q, url = stream.split("|")
		PLog("q: " + q)
		if q == 'q0':
			quality = u'GERINGE'
			w = "640"; h = "360"					# Probeentnahme	
			bitrate = u"1812067"
			if u'm3u8' in stream:
				bitrate = u"16 MB/Min."
		if q == 'q1':
			quality = u'HOHE'
			w = "960"; h = "540"					# Probeentnahme	
			bitrate = u"1812067"
			if u'm3u8' in stream:
				bitrate = u"16 MB/Min."
		if q == 'q2':
			quality = u'SEHR HOHE'
			w = "1024"; h = "576"					# Probeentnahme							
			bitrate = u"3621101"
			if u'm3u8' in stream:
				bitrate = u"19 MB/Min."
		if q == 'q3':
			quality = u'HD'
			w = "1280"; h = "720"					# Probeentnahme					
			bitrate = u"6501324"
			if u'm3u8' in stream:
				bitrate = u"23 MB/Min."
		if q == 'q4':
			quality = u'Full-HD'
			w = "1920"; h = "1080"					# Probeentnahme,					
			bitrate = u"?"
			if u'm3u8' in stream:
				bitrate = u"?"			
		if q == 'q5':
			quality = u'UHD'
			w = "3840"; h = "2160"					# Probeentnahme						
			bitrate = u"?"
			if u'm3u8' in stream:
				bitrate = u"42 MB/Min"				# geschätzt				
		
		res = "%sx%s" % (w,h)
		
		if u'm3u8' in stream:
			stream_title = u'HLS, Qualität: [B]%s | %s[/B]' % (quality, label) # label: Normal, DGS, .
		else:
			stream_title = u'MP4, Qualität: [B]%s | %s[/B]' % (quality, label)
			try:
				bitrate = re.search(u'_(\d+)k_', url).group(1)	# bitrate überschreiben	
				bitrate = bitrate + "kbit"			# k ergänzen 
			except Exception as exception:			# ts möglich: http://cdn.hbbtvlive.de/zdf/106-de.ts
				PLog(str(exception))
				PLog(url)	

		title_url = u"%s#%s" % (title, url)
		item = u"%s ** Bitrate %s ** Auflösung %s ** %s" %\
			(stream_title, bitrate, res, title_url)
		PLog("item: " + item)
		HBBTV_List.append(item)	
		
	return HBBTV_List

#-------------------------
# 16.01.2022 Auslagerung aus get_formitaeten  
# ermittelt streamurls, duration, geoblock, sub_path
#
def get_form_streams(page):
	PLog('get_form_streams:')
	# Kodi: https://kodi.wiki/view/Features_and_supported_formats#Audio_playback_in_detail 
	#	AQTitle, ASS/SSA, CC, JACOsub, MicroDVD, MPsub, OGM, PJS, RT, SMI, SRT, SUB, VOBsub, VPlayer
	#	Für Kodi eignen sich beide ZDF-Formate xml + vtt, umbenannt in *.sub oder *.srt
	#	VTT entspricht SubRip: https://en.wikipedia.org/wiki/SubRip
#	subtitles = stringextract('"captions"', '"documentVersion"', page)	# Untertitel ermitteln, bisher in Plex-
	subtitles = stringextract('"captions"', ']', page)	# Untertitel ermitteln, bisher in Plex-
	subtitles = blockextract('"class"', subtitles)						# Channels nicht verwendbar
	PLog('subtitles: ' + str(len(subtitles)))
	sub_path = ''													# Format: "local_path|url", Liste 
	if len(subtitles) == 2:											#			scheitert in router
		# sub_xml = subtitles[0]									# xml-Format für Kodi ungeeignet
		sub_vtt = subtitles[1]	
		# PLog(sub_vtt)
		#sub_xml_path = stringextract('"uri": "', '"', sub_xml)# xml-Format
		sub_vtt_path = stringextract('"uri":"', '"', sub_vtt)	
		# PLog('Untertitel xml:'); PLog(sub_xml_path)
		PLog('Untertitel vtt:'); PLog(sub_vtt_path)
		
		# 20.01.2019 Pfad + Url in PlayVideo via listitem.setInfo direkt übergeben
		local_path = "%s/%s" % (SUBTITLESTORE, sub_vtt_path.split('/')[-1])
		local_path = local_path.replace('.vtt', '.sub')				# Endung für Kodi anpassen
		local_path = os.path.abspath(local_path)
		try:
			if os.path.isfile(local_path) == False:					# schon vorhanden?
				urlretrieve(sub_vtt_path, local_path)
		except Exception as exception:
			local_path = ''
			PLog(str(exception))
		sub_path = '%s|%s' % (local_path, sub_vtt_path)						
		PLog(sub_path)
				
	duration = stringextract('duration',  'fsk', page)	# Angabe im Kopf, sec/1000
	duration = stringextract('"value":',  '}', duration).strip()
	PLog(duration)	
	if duration:
		duration = int((int(duration) / 1000) / 60)		# Rundung auf volle Minuten reicht hier 
		duration = max(1, duration)						# 1 zeigen bei Werten < 1
		duration = str(duration) + " min"	
	PLog('duration: ' + duration)
	PLog('page_formitaeten: ' + page[:100])		
	formitaeten = blockextract('formitaeten', page)		# Video-URL's ermitteln
	PLog('formitaeten: ' + str(len(formitaeten)))
	# PLog(formitaeten[0])								# bei Bedarf
				
	geoblock =  stringextract('geoLocation',  '}', page) 
	geoblock =  stringextract('"value": "',  '"', geoblock).strip()
	PLog('geoblock: ' + geoblock);
	if 	geoblock == 'none':								# i.d.R. "none", sonst "de" - wie bei ARD verwenden
		geoblock = ' | ohne Geoblock'
	else:
		if geoblock == 'de':			# Info-Anhang für summary 
			geoblock = ' | Geoblock DE!'
		if geoblock == 'dach':			# Info-Anhang für summary 
			geoblock = ' | Geoblock DACH!'
			
			
	return formitaeten, duration, geoblock, sub_path
	
#-------------------------
# Aufrufer: ZDF_Search (weitere Seiten via page_cnt)
#	Einzelseite -> ZDF_BildgalerieSingle
def ZDF_Bildgalerien(page):	
	PLog('ZDF_Bildgalerien:'); 
	
	if page == '':
		msg1 = 'Seite kann nicht geladen werden: [B]%s[/B]' % title
		msg2 = msg
		MyDialog(msg1, msg2, '')
		return
	
	li = xbmcgui.ListItem()
	li = home(li, ID="ZDF")						# Home-Button
			
				
	page_cnt=0;
	content =  blockextract('class="artdirect"', page)
	for rec in content:	
		infoline = stringextract('infoline-text="', '"', rec)
		if " Bilder " in infoline == False:
			continue
		tag = unescape(infoline); tag=cleanhtml(tag)		# einschl. Anzahl Bilder
			
		category = stringextract('teaser-cat-category">', '</span>', rec)
		category = mystrip(category)
		PLog(category)
		brand = stringextract('brand-ellipsis">', '</span>', rec)
		brand = mystrip(brand)	
		PLog(brand)

		thumb =  stringextract('data-srcset="', ' ', rec)	
		href = stringextract('a href', '</a>', rec)
		path  = stringextract('="', '"', href)
		if path == '':										# Sicherung
			path = 	stringextract('plusbar-url="', '"', rec)
		if path.startswith("http") == False:
			path = "https://www.zdf.de" + path
		title = stringextract('title="', '"', href)			# falls leer -> descr, s.u.
			
		descr = stringextract('description">', '<', rec)
		if descr == '':
			descr = stringextract('teaser-text">', '<', rec) # mehrere Varianten möglich
		if descr == '':
			descr = stringextract('class="teaser-text" >', '<', rec)
		descr = mystrip(descr.strip())
		PLog('descr:' + descr)		# UnicodeDecodeError möglich
		
		if title == '':
			title =  descr		
		
		airtime = stringextract('class="air-time" ', '</time>', rec)
		airtime = stringextract('">', '</time>', airtime)
		if airtime:
			tag = "%s | %s" % (tag, airtime)
		if category:
			tag = "%s | %s" % (tag, category)
		if brand:
			tag = "%s | %s" % (tag, brand)
						
		title = unescape(title); summ = unescape(descr)
		title=repl_json_chars(title); summ=repl_json_chars(summ)	
		PLog('neuer Satz')
		PLog(thumb);PLog(path);PLog(title);PLog(summ);PLog(tag);
		
		path=py2_encode(path); title=py2_encode(title);
		fparams="&fparams={'path': '%s', 'title': '%s'}" % (quote(path), quote(title))	
		addDir(li=li, label=title, action="dirList", dirID="ZDF_BildgalerieSingle", fanart=thumb, thumb=thumb, 
			fparams=fparams, summary=summ,  tagline=tag)
		page_cnt = page_cnt + 1
	
	PLog("Serien: %d" + str(page_cnt))
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#-------------------------
# Lösung mit einzelnem Listitem wie in ShowPhotoObject (FlickrExplorer) hier
#	nicht möglich (Playlist Player: ListItem type must be audio or video) -
#	Die li-Eigenschaft type='image' wird von Kodi nicht akzeptiert, wenn
#	addon.xml im provides-Feld video enthält. Daher müssen die Bilder hier
#	im Voraus geladen werden.
# Ablage im SLIDESTORE, Bildverz. wird aus Titel erzeugt. Falls ein Bild
#	nicht existiert, wird es via urlretrieve geladen.
# 04.02.2020 Umstellung Bildladen auf Thread (thread_getfile).
# 07.02.2020 wegen Rekursion (Rücksprung zu ZDF_getVideoSources) Umstellung:
#	Auswertung des Suchergebnisses (s. ZDF_Search) in ZDF_Bildgalerien,
#	Auswertung Einzelgalerie hier.
# 23.09.2021 Umstellung Bildname aus Quelle statt "Bild_01" (eindeutiger beim
#	Nachladen).
# 19.05.2022 Param. li: Vermeid. Home-Doppel (Aufruf ZDF_get_content)
#
def ZDF_BildgalerieSingle(path, title, li=''):	
	PLog('ZDF_BildgalerieSingle:'); PLog(path); PLog(title)
	title_org = title
	
	
	page, msg = get_page(path=path)	
	if page == '':
		msg1 = 'Seite kann nicht geladen werden: [B]%s[/B]' % title
		msg2 = msg
		MyDialog(msg1, msg2, '')
		return
	
	if li == '':
		li = xbmcgui.ListItem()
		li = home(li, ID="ZDF")						# Home-Button
	
	# gallery-slider-box: echte Bildgalerien, andere spielen kaum eine Rolle
	#	bei Fehlen auf Weiterleitung prüfen (z.B. in lazyload-container):
	if page.find(u'class="content-box gallery-slider-box') < 0:
		PLog('check_extern_link:')
		href=''
		href_list = blockextract('a href=', page, '</a>')
		for h in href_list:
			PLog(h[:80])
			if u'#gallerySlide=0' in h:
				href = stringextract('href="', '"', h)
				break
		if href:
			PLog('get_extern_link')
			page, msg = get_page(path=href)	
		
	content =  stringextract(u'class="content-box gallery-slider-box', u'title="Bilderserie schließen"', page)
	content = blockextract('class="img-container', content)	
	PLog("content: " + str(len(content)))
	
	if len(content) == 0:										
		msg1 = 'ZDF_BildgalerieSingle: keine Bilder gefunden.'
		msg2 = title
		MyDialog(msg1, msg2, '')
		return li
	
	fname = make_filenames(title)			# Ordnername: Titel 
	fpath = os.path.join(SLIDESTORE, fname)
	PLog(fpath)
	if os.path.isdir(fpath) == False:
		try:  
			os.mkdir(fpath)
		except OSError:  
			msg1 = 'Bildverzeichnis konnte nicht erzeugt werden:'
			msg2 = "%s/%s" % (SLIDESTORE, fname)
			PLog(msg1); PLog(msg2)
			MyDialog(msg1, msg2, '')
			return li	

	image=0; background=False; path_url_list=[]; text_list=[]
	for rec in content:				
		category = stringextract('teaser-cat-category">', '</span>', rec)
		category = mystrip(category)
		PLog(category)
		brand = stringextract('brand-ellipsis">', '</span>', rec)
		brand = mystrip(brand)	
		PLog(brand)

		img_links =  stringextract('data-srcset="', '"', rec)	# mehrere Links, aufsteig. Bildgrößen
		img_links = blockextract('http', img_links)
		w_old=0
		for img_link in img_links:
			img_link = img_link.split(' ')[0]					# Link bis 1. Blank: ..?cb=1462007560755 384w 216h
			w=''
			w_h = stringextract('~', '?cb', img_link)			# Bsp.: ..-2014-100~384x216?cb=1462007562325
			PLog(img_link); PLog(w_h)
			if "x" in w_h:
				w  = w_h.split('x')[0]							# Bsp.: 384
				if int(w) > w_old and int(w) <= 1280:			# Begrenz.: 1280 (gesehen: 3840)
					w_old = int(w)
					
		img_src  = img_link
		PLog("img_src: %s, w: %d" % (img_link, w_old))			
					
		href = stringextract('a href', '</a>', rec)
		path  = stringextract('="', '"', href)
		if path == '':										# Sicherung
			path = 	stringextract('plusbar-url="', '"', rec)
		if path.startswith("http") == False:
			path = "https://www.zdf.de" + path
		title = stringextract('title="', '"', href)			# falls leer -> descr, s.u.
			
		descr = stringextract('description">', '<', rec)
		if descr == '':
			descr = stringextract('teaser-text">', '<', rec) # mehrere Varianten möglich
		if descr == '':
			descr = stringextract('class="teaser-text" >', '<', rec)
		descr = mystrip(descr.strip())
		PLog('descr:' + descr)		# UnicodeDecodeError möglich
		
		if title == '':
			title =  descr
		lable = title				# Titel in Textdatei	
				
		
		tag = stringextract('"teaser-info">', '</dd>', rec)		# Quelle
		tag = cleanhtml(tag); tag = mystrip(tag)
		airtime = stringextract('class="air-time" ', '</time>', rec)
		airtime = stringextract('">', '</time>', airtime)
		if airtime:
			tag = "%s | %s" % (tag, airtime)
		if category:
			tag = "%s | %s" % (tag, category)
		if brand:
			tag = "%s | %s" % (tag, brand)
		
				
		if img_src == '':									# Sicherung			
			PLog('Problem in Bildgalerie: Bild nicht gefunden')
		else:		
			if tag:
				tag = "%s | %s" % (tag, title_org)
			
			#  Kodi braucht Endung für SildeShow; akzeptiert auch Endungen, die 
			#	nicht zum Imageformat passen
			# pic_name 	= 'Bild_%04d.jpg' % (image+1)		# Bildname
			pic_name 	= img_src.split('/')[-1]			# Bildname aus Quelle
			if '?' in pic_name:								# Bsp.: ~2400x1350?cb=1631630217812
				pic_name = pic_name.split('?')[0]
			local_path 	= "%s/%s.jpg" % (fpath, pic_name)
			PLog("local_path: " + local_path)
			title = "Bild %03d: %s" % (image+1, pic_name)	# Numerierung
			PLog("Bildtitel: " + title)
			summ = unescape(descr)			
			
			thumb = ''
			local_path 	= os.path.abspath(local_path)
			thumb = local_path
			if os.path.isfile(local_path) == False:			# schon vorhanden?
				# path_url_list (int. Download): Zieldatei_kompletter_Pfad|Bild-Url, 
				#								 Zieldatei_kompletter_Pfad|Bild-Url, ..
				path_url_list.append('%s|%s' % (local_path, img_src))

				if SETTINGS.getSetting('pref_watermarks') == 'true':
					txt = "%s\n%s\n%s\n%s\n" % (fname,title,tag,summ)
					text_list.append(txt)	
				background	= True											
									
			title=repl_json_chars(title); summ=repl_json_chars(summ)
			PLog('neu:');PLog(title);PLog(img_src);PLog(thumb);PLog(summ[0:40]);
			if thumb:	
				local_path=py2_encode(local_path);
				fparams="&fparams={'path': '%s', 'single': 'True'}" % quote(local_path)
				addDir(li=li, label=title, action="dirList", dirID="ZDF_SlideShow", 
					fanart=thumb, thumb=thumb, fparams=fparams, summary=summ, tagline=tag)

			image += 1
			
	if background and len(path_url_list) > 0:				# Thread-Call mit Url- und Textliste
		PLog("background: " + str(background))
		from threading import Thread						# thread_getpic
		folder = fname 
		background_thread = Thread(target=thread_getpic,
			args=(path_url_list, text_list, folder))
		background_thread.start()

	PLog("image: " + str(image))
	if image > 0:	
		fpath=py2_encode(fpath);	
		fparams="&fparams={'path': '%s'}" % quote(fpath) 	# fpath: SLIDESTORE/fname
		addDir(li=li, label="SlideShow", action="dirList", dirID="ZDF_SlideShow", 
			fanart=R('icon-stream.png'), thumb=R('icon-stream.png'), fparams=fparams)
		
		lable = u"Alle Bilder löschen"						# 2. Löschen
		tag = 'Bildverzeichnis: ' + fname 
		summ= u'Bei Problemen: Bilder löschen, Wasserzeichen ausschalten,  Bilder neu einlesen'
		fparams="&fparams={'dlpath': '%s', 'single': 'False'}" % quote(fpath)
		addDir(li=li, label=lable, action="dirList", dirID="DownloadsDelete", fanart=R(ICON_DELETE), 
			thumb=R(ICON_DELETE), fparams=fparams, summary=summ, tagline=tag)
		
				
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)  # ohne Cache, um Neuladen zu verhindern

#-----------------------
# PhotoObject fehlt in kodi - wir speichern die Bilder in SLIDESTORE und
#	übergeben an xbmc.executebuiltin('SlideShow..
# ClearUp in SLIDESTORE s. Modulkopf
# Aufrufer: ZDF_BildgalerieSingle, ARDSportBilder, XL_Bildgalerie,
#	BilderDasErsteSingle
# Um die Wasserzeichen (unten links) zu sehen, sind in Kodi's Player
#	die Schwenkeffekte abzuschalten.  
def ZDF_SlideShow(path, single=None):
	PLog('ZDF_SlideShow: ' + path)
	local_path = os.path.abspath(path)
	PLog(local_path)
	if single:							# Einzelbild
		return xbmc.executebuiltin('ShowPicture(%s)' % local_path)
	else:
		return xbmc.executebuiltin('SlideShow(%s, %s)' % (local_path, 'notrandom'))

	 
####################################################################################################
def Parseplaylist(li, url_m3u8, thumb, geoblock, descr, sub_path='', stitle='', buttons=True, track_add='', live=''):	
#	# master.m3u8 bzw. index.m3u8 auswerten, Url muss komplett sein. 
#  	1. Besonderheit: in manchen *.m3u8-Dateien sind die Pfade nicht vollständig,
#	sondern nur als Ergänzung zum Pfadrumpf (ohne Namen + Extension) angegeben, Bsp. (Arte):
#	delive/delive_925.m3u8, url_m3u8 = http://delive.artestras.cshls.lldns.net/artestras/contrib/delive.m3u8
#	Ein Zusammensetzen verbietet sich aber, da auch in der ts-Datei (z.B. delive_64.m3u8) nur relative 
#	Pfade angegeben werden. Beim Redirect des Videoplays zeigt dann der Pfad auf das Plugin und Plex
#	versucht die ts-Stücke in Dauerschleife zu laden.
#	Wir prüfen daher besser auf Pfadbeginne mit http:// und verwerfen Nichtpassendes - auch wenn dabei ein
#	Sender komplett ausfällt.
#	Lösung ab April 2016:  Sonderbehandlung Arte in Arteplaylists.						
#	ARTE ab 10.03.2017:	 die m3u8-Links	enthalten nun komplette Pfade. Allerdings ist SSL-Handshake erforderlich zum
#		Laden der master.m3u8 erforderlich (s.u.). Zusätzlich werden in	CreateVideoStreamObject die https-Links durch 
#		http ersetzt (die Streaming-Links funktionieren auch mit http).	
#		SSL-Handshake für ARTE ist außerhalb von Plex nicht notwendig!
#  	2. Besonderheit: fast identische URL's zu einer Auflösung (...av-p.m3u8, ...av-b.m3u8) Unterschied n.b.
#  	3. Besonderheit: für manche Sendungen nur 1 Qual.-Stufe verfügbar (Bsp. Abendschau RBB)
#  	4. Besonderheit: manche Playlists enthalten zusätzlich abgeschaltete Links, gekennzeichnet mit #. Fehler Webplayer:
#		 crossdomain access denied. Keine Probleme mit OpenPHT und VLC - betr. nur Plex.
#  	10.08.2017 Filter für Video-Sofort-Format - wieder entfernt 17.02.2018
#	23.02.2020 getrennte Video- und Audiostreams bei den ZDF-Sendern (ZDF, ZDFneo, ZDFinfo - nicht bei 3sat +phoenix)
#		 - hier nur Auflistung der Audiostreams 
#	19.12.2020 Sendungs-Titel ergänzt (optional: stitle)
#	03.03.2020 Erweiterung buttons: falls False keine Buttons sondern Rückgabe als Liste
#		Stream_List (Format s.u.)
#	23.04.2022 Mehrkanalstreams mit Kennung GROUP-ID entfernen (in Kodi nicht verwertbar) - nicht mehr relevant
#		mit Sender-Liste für Einzelauflösungen
#	29.10.2022 Bereinigung Sender-Liste mit mögl. Einzelauflösungen (entfernt: HR, NDR, WDR)
#
	PLog ('Parseplaylist: ' + url_m3u8)
	Stream_List=[]

	if SETTINGS.getSetting('pref_video_direct') == 'true' and buttons:		# nicht für Stream_List
		return li

	playlist = ''
	# seit ZDF-Relaunch 28.10.2016 dort nur noch https
	if url_m3u8.startswith('http') == True :								# URL oder lokale Datei?			
		playlist, msg = get_page(path=url_m3u8)								# URL
		if playlist == '':
			icon = R(ICON_WARNING)
			msg1 = "master.m3u8 fehlt"
			msg2 = 'Fehler: %s'	% (msg)
			xbmcgui.Dialog().notification(msg1, msg2,icon,5000)
			if buttons:
				return li
			else:
				return []													# leere Liste für build_Streamlists				
	else:																	# lokale Datei	
		fname =  os.path.join(M3U8STORE, url_m3u8) 
		playlist = RLoad(fname, abs_path=True)					
	 
	PLog('playlist: ' + playlist[:100])
	PLog('live: ' + str(live))
	skip_list = ["/rbb_brandenburg/",							# keine Mehrkanalstreams: Einzelauflösungen mögl.
				"/srfsgeo/", "/swrbwd/", "/dwstream"
				]
	PLog('#EXT-X-MEDIA' in playlist)
	# live=True: skip 1 Button, Altern.: Merkmal "_sendung_" in url_m3u8
	if '#EXT-X-MEDIA' in playlist:											# Mehrkanalstreams: 1 Button
		skip=False
		for item in skip_list:
			if item in url_m3u8:
				skip=True													# i.d.R. ARD-Streams (nicht alle)
				break
		PLog('skip: ' + str(skip))
		if skip == False and live:											# Mehrkanalstreams: 1 Button
			stitle = "HLS-Stream"
			PLog("jump_PlayButtonM3u8")
			PlayButtonM3u8(li, url_m3u8, thumb, stitle, tagline=track_add, descr=descr)	
			return
	
	
	li = xbmcgui.ListItem()	
	lines = playlist.splitlines()
	# PLog(lines)
	BandwithOld 	= ''			# für Zwilling -Test (manchmal 2 URL für 1 Bandbreite + Auflösung) 
	NameOld 		= []			# für Zwilling -Test bei ZDF-Streams (nicht hintereinander)
	thumb_org=thumb; descr_org=descr 	# sichern
	
	i = 0; li_cnt = 1; url=''
	for i, line in enumerate(lines):
		thumb=thumb_org
		res_geo=''; label=''; BandwithInt=0; Resolution_org=''
		# Abgrenzung zu ts-Dateien (Bsp. Welt24): #EXT-X-MEDIA-SEQUENCE: 9773324
		# Playlist Tags s. https://datatracker.ietf.org/doc/html/rfc8216
		if line.startswith('#EXT-X-MEDIA:') == False and line.startswith('#EXT-X-STREAM-INF') == False:
			continue
		if ',GROUP-ID' in line:							# zusätzl. Mehrkanalstreams (Audio)
			continue
		PLog("line: " + line)
			
		if line.startswith('#EXT-X-STREAM-INF'):	# tatsächlich m3u8-Datei?
			url = lines[i + 1]						# URL in nächster Zeile
			PLog("url: " + url)
			Bandwith = GetAttribute(line, 'BANDWIDTH')
			Resolution = GetAttribute(line, 'RESOLUTION')
			Resolution_org = Resolution				# -> Stream_List

			try:
				BandwithInt	= int(Bandwith)
			except:
				BandwithInt = 0
			if Resolution:	# fehlt manchmal (bei kleinsten Bandbreiten)
				Resolution = u'Auflösung ' + Resolution
			else:
				Resolution = u'Auflösung unbekannt'	# verm. nur Ton? CODECS="mp4a.40.2"
				thumb=R(ICON_SPEAKER)
			Codecs = GetAttribute(line, 'CODECS')
			# als Titel wird die  < angezeigt (Sender ist als thumb erkennbar)
			title='Bandbreite ' + Bandwith
			if url.find('#') >= 0:	# Bsp. SR = Saarl. Rundf.: Kennzeichnung für abgeschalteten Link
				Resolution = u'zur Zeit nicht verfügbar!'
			if url.startswith('http') == False:   		# relativer Pfad? 
				pos = url_m3u8.rfind('/')				# m3u8-Dateinamen abschneiden
				url = url_m3u8[0:pos+1] + url 			# Basispfad + relativer Pfad
			if Bandwith == BandwithOld:	# Zwilling -Test
				title = 'Bandbreite ' + Bandwith + ' (2. Alternative)'
			
			PLog(Resolution); PLog(BandwithInt); 
			# nur Audio (Bsp. ntv 48000, ZDF 96000), 
			if BandwithInt and BandwithInt <=  100000:
				Resolution = Resolution + ' (nur Audio)'
				thumb=R(ICON_SPEAKER)
			res_geo = Resolution+geoblock
			BandwithOld = Bandwith
		else:
			continue

		label = "%s" % li_cnt + ". " + title
		if res_geo:
			label = "%s | %s" % (label, res_geo)
						
		# quote für url erforderlich wg. url-Inhalt "..sd=10&rebase=on.." - das & erzeugt in router
		#	neuen Parameter bei dict(parse_qs(paramstring)
		Plot = descr_org
		if "\n" in Plot:
			Plot = repl_dop(Plot.splitlines())
			Plot = "\n".join(Plot)
		Plot = Plot.replace('\n', '||')	
		descr = Plot.replace('||', '\n')		
	
		if descr.strip() == '|':			# ohne EPG: EPG-Verbinder entfernen
			descr=''
			
		if url.startswith('http') == False: # kompl. Pfad fehlt - Bsp.: one, kika
			continue
		
		summ=''
		if stitle:
			summ = u"Sendung: %s" % py2_decode(stitle)
		
		PLog("SatzParse:")
		PLog(title); PLog(label); PLog(url[:80]); PLog(thumb); PLog(Plot[:80]); PLog(descr[:80]); 
		
		if buttons:															# Buttons, keine Stream_List
			title=py2_encode(title); url=py2_encode(url);
			thumb=py2_encode(thumb); Plot=py2_encode(Plot); 
			sub_path=py2_encode(sub_path);
			fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'sub_path': '%s'}" %\
				(quote_plus(url), quote_plus(title), quote_plus(thumb), quote_plus(Plot), 
				quote_plus(sub_path))
			addDir(li=li, label=label, action="dirList", dirID="PlayVideo", fanart=thumb, thumb=thumb, fparams=fparams, 
				mediatype='video', tagline=descr, summary=summ) 
		else:																# nur Stream_List füllen
			# Format: "HLS Einzelstream | Bandbreite | Auflösung | Titel#Url"
			if Resolution_org=='':
				Resolution_org = "Audiostream"
			PLog("append: %s, %s.." % (str(BandwithInt), Resolution_org))
			Stream_List.append(u'HLS-Stream ** Bitrate %s ** Auflösung %s ** %s#%s' %\
				(str(BandwithInt), Resolution_org, stitle, url)) # wie Downloadliste
			if track_add:													# TV-Ton deu, Originalton eng usw.
				Stream_List[-1] = Stream_List[-1].replace("HLS-Stream", "HLS, %s" % track_add)
		
		li_cnt = li_cnt + 1  	# Listitemzähler												
  	
	if i == 0:	# Fehler
		line1 = 'Kennung #EXT-X-STREAM-INF / #EXT-X-MEDIA fehlt'
		line2 = 'oder den Streamlinks fehlt http / https'
		MyDialog(line1, line2, '')
	
	if buttons:
		return li
	else:
		return Stream_List
		
####################################################################################################
# Ausführung nur ohne Sofortstart - bei Sofortstart ruft build_Streamlists_buttons
#	PlayVideo_Direct auf (Auswahl Format/Qualität -> PlayVideo).
# Streambuttons HLS / MP4 (ID-abh.), einschl. Downloadbuttons bei MP4-Liste
# Streamliste wird aus Dict geladen (Datei: ID)
#	Bandbreite + Auflösung können fehlen (Qual. < hohe, Audiostreams)
# Formate:
#	"HLS automatische Anpassung ** auto ** auto ** Titel#Url"  	# master.m3u8
# 	"HLS Einzelstream ** Bandbreite ** Auflösung ** Titel#Url" (wie Downloadliste)"
#
#	"MP4 Qualität: niedrige ** leer **leer ** Titel#Url"	
#	"MP4 Qualität: Full HD ** Bandbreite ** Auflösung ** Titel#Url"
# Anzeige: aufsteigend (beide Listen)
# Aufrufer: build_Streamlists_buttons (Aufrufer: ARDStartSingle (ARD Neu), 
#	build_Streamlists (ZDF,  my3Sat), SingleSendung (ARD Classic)
# 
# Plot = tagline (zusammengefasst: Titel, tagline, summary)
# 10.11.2021 Sortierung der MP4-Liste von Auflösung nach Bitrate geändert
# 05.05.2022 Wechsel-Button zu den DownloadTools hinzugefügt 
#
def StreamsShow(title, Plot, img, geoblock, ID, sub_path='', HOME_ID="ZDF"):	
	PLog('StreamsShow:'); PLog(ID)
	title_org = title; 
	
	li = xbmcgui.ListItem()
	li = home(li, ID=HOME_ID)						# Home-Button

	Stream_List = Dict("load", ID)
	#PLog(Stream_List)
	PLog(len(Stream_List))

	# bei Kennzeichnung einz. Stream mit unbekannt keine Sortierung
	if 'MP4_List' in ID and "Bitrate unbekannt" in str(Stream_List) == False:
		if "Bitrate" in str(Stream_List):
			Stream_List = sorted(Stream_List,key=lambda x: int(re.search(u'Bitrate (\d+)', x).group(1)))

	title_org=py2_encode(title_org);  img=py2_encode(img);
	sub_path=py2_encode(sub_path); 	Plot=py2_encode(Plot); 
	
	tagline_org = Plot.replace('||', '\n')

	cnt=1
	for item in Stream_List:
		item = py2_encode(item)
		PLog("item: " + item[:80])
		label, bitrate, res, title_href = item.split('**')
		bitrate = bitrate.replace('Bitrate 0', 'Bitrate ?')			# Anpassung für funk ohne AzureStructure
		res = res.replace('0x0', '?')								# dto.
		PLog(title_href)
		title, href = title_href.split('#')
		
		PLog(title); PLog(tagline_org[:80]); PLog(sub_path)
		tagline = tagline_org
	
		label = "%d. %s | %s| %s" % (cnt, label, bitrate, res)
		cnt = cnt+1
		href=py2_encode(href); title=py2_encode(title);
		
		# 17.06.2021 Absturz mit 'video' nach Sofortstart aus Kontextmenü nicht
		#	mehr relevant
		fparams="&fparams={'url': '%s', 'title': '%s', 'thumb': '%s', 'Plot': '%s', 'sub_path': '%s'}" %\
			(quote_plus(href), quote_plus(title_org), quote_plus(img), 
			quote_plus(Plot), quote_plus(sub_path))
		addDir(li=li, label=label, action="dirList", dirID="PlayVideo", fanart=img, thumb=img, fparams=fparams, 
			tagline=tagline, mediatype='video')
	
	if 'MP4_List' in ID:
		# ohne check Error mögl. (LibreElec 10.0) - setLabel=None in addDir
		if check_Setting('pref_use_downloads'):						
			summ=''
			li = test_downloads(li,Stream_List,title,summ,tagline,img,high=-1, sub_path=sub_path) # Downloadbutton(s)
			
			# Wechsel-Button zu den DownloadTools:	
			tagline = 'Downloads und Aufnahmen: Verschieben, Löschen, Ansehen, Verzeichnisse bearbeiten'
			fparams="&fparams={}"
			addDir(li=li, label='Download- und Aufnahme-Tools', action="dirList", dirID="DownloadTools", 
				fanart=R(FANART), thumb=R(ICON_DOWNL_DIR), tagline=tagline, fparams=fparams)			

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
			    
####################################################################################################
#						Hilfsfunktionen - für Kodiversion augelagert in Modul util.py
####################################################################################################
# Bsp. paramstring (ab /?action):
#	url: plugin://plugin.video.ardundzdf/?action=dirList&dirID=Main_ARD&
#	fanart=/resources/images/ard-mediathek.png&thumb=/resources/images/ard-mediathek.png&
#	params={&name=ARD Mediathek&sender=ARD-Alle:ard::ard-mediathek.png}
# 17.11.2019 mit Modul six + parse_qs erscheinen die Werte als Liste,
#	Bsp: {'action': ['dirList']}, vorher als String: {'action': 'dirList'}.
#	fparams wird hier in unicode erwartet, s. py2_decode(fparams) in addDir
#---------------------------------------------------------------- 
def router(paramstring):
	# paramstring: Dictionary mit
	# {<parameter>: <value>} Elementen
	paramstring = unquote_plus(paramstring)
	PLog(' router_params1: ' + paramstring)
	PLog(type(paramstring));
		
	if paramstring:	
		params = dict(parse_qs(paramstring[1:]))
		PLog(' router_params_dict: ' + str(params))
		try:
			if 'content_type' in params:
				if params['content_type'] == 'video':	# Auswahl im Addon-Menü
					Main()
			PLog('router action: ' + params['action'][0]) # hier immer action="dirList"
			PLog('router dirID: ' + params['dirID'][0])
			PLog('router fparams: ' + params['fparams'][0])
		except Exception as exception:
			PLog(str(exception))

		if params['action'][0] == 'dirList':			# Aufruf Directory-Listing
			newfunc = params['dirID'][0]
			func_pars = params['fparams'][0]

			# Modul laden, Funktionsaufrufe + Parameterübergabe via Var's 
			#	s. 00_Migration_ardundzdf.txt
			# Modulpfad immer ab resources - nicht verkürzen.
			# Direktsprünge: Modul wird vor Sprung in Funktion geladen.
			if '.' in newfunc:						# Funktion im Modul, Bsp.:				
				l = newfunc.split('.')				# Bsp. resources.lib.updater.update
				PLog(l)
				newfunc =  l[-1:][0]				# Bsp. updater
				dest_modul = '.'.join(l[:-1])
				
				PLog(' router dest_modul: ' + str(dest_modul))
				PLog(' router newfunc: ' + str(newfunc))
				
				dest_modul = importlib.import_module(dest_modul )		# Modul laden
				PLog('loaded: ' + str(dest_modul))
				#PLog(' router_params_dict: ' + str(params))			# Debug Modul-params
				
				try:
					# func = getattr(sys.modules[dest_modul], newfunc)  # falls beim Start geladen
					func = getattr(dest_modul, newfunc)					# geladen via importlib
				except Exception as exception:
					PLog(str(exception))
					func = ''
				if func == '':						# Modul nicht geladen - sollte nicht
					li = xbmcgui.ListItem()			# 	vorkommen - s. Addon-Start
					msg1 = "Modul %s ist nicht geladen" % dest_modul
					msg2 = "oder Funktion %s wurde nicht gefunden." % newfunc
					msg3 = "Ursache unbekannt."
					PLog(msg1)
					MyDialog(msg1, msg2, msg3)
					xbmcplugin.endOfDirectory(HANDLE)

			else:
				func = getattr(sys.modules[__name__], newfunc)	# Funktion im Haupt-PRG OK		
			
			PLog(' router func_getattr: ' + str(func))		
			if func_pars != '""':		# leer, ohne Parameter?	
				# func_pars = unquote_plus(func_pars)		# quotierte url auspacken - entf.
				PLog(' router func_pars unquote_plus: ' + str(func_pars))
				try:
					# Problem (spez. Windows): Parameter mit Escapezeichen (Windows-Pfade) müssen mit \\
					#	behandelt werden und werden dadurch zu unicode-Strings. Diese benötigen in den
					#	Funktionen eine UtfToStr-Behandlung.
					# Keine /n verwenden (json.loads: need more than 1 value to unpack)
					func_pars = func_pars.replace("'", "\"")		# json.loads-kompatible string-Rahmen
					func_pars = func_pars.replace('\\', '\\\\')		# json.loads-kompatible Windows-Pfade
					
					PLog("json.loads func_pars: " + func_pars)
					PLog('json.loads func_pars type: ' + str(type(func_pars)))
					mydict = json.loads(func_pars)
					PLog("mydict: " + str(mydict)); PLog(type(mydict))
				except Exception as exception:
					PLog('router_exception: {0}'.format(str(exception)))
					mydict = ''
				
				# PLog(' router func_pars: ' + str(type(mydict)))
				if 'dict' in str(type(mydict)):				# Url-Parameter liegen bereits als dict vor
					mydict = mydict
				else:
					mydict = dict((k.strip(), v.strip()) for k,v in (item.split('=') for item in func_pars.split(',')))			
				PLog(' router func_pars: mydict: %s' % str(mydict))
				func(**mydict)
			else:
				func()
		else:
			PLog('router action-params: ?')
	else:
		# Plugin-Aufruf ohne Parameter
		Main()

#---------------------------------------------------------------- 
PLog('Addon_URL: ' + PLUGIN_URL)		# sys.argv[0], plugin://plugin.video.ardundzdf/
PLog('ADDON_ID: ' + ADDON_ID); PLog(SETTINGS); PLog(ADDON_NAME);PLog(SETTINGS_LOC);
PLog(ADDON_PATH);PLog(ADDON_VERSION);
PLog('HANDLE: ' + str(HANDLE))
PLog('PluginAbsPath: ' + PluginAbsPath)

PLog('Addon: Start')
if __name__ == '__main__':
	try:
		router(sys.argv[2])
		# Memory-Bereinig. unwirksam gegen Raspi-Klemmer (s. SenderLiveListe)
		#del get_ZDFstreamlinks, get_ARDstreamlinks, get_IPTVstreamlinks
	except Exception as e: 
		msg = str(e)
		PLog('network_error: ' + msg)

























