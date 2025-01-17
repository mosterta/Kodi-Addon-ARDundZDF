# -*- coding: utf-8 -*-
################################################################################
#				ARDnew.py - Teil von Kodi-Addon-ARDundZDF
#			neue Version der ARD Mediathek, Start Beta Sept. 2018
#
# 	dieses Modul nutzt die Webseiten der Mediathek ab https://www.ardmediathek.de/
#	bzw. den eingebetteten json-Code und die verknüpften api-Calls.
#
#	04.11.2019 Migration Python3
#	21.11.2019 Migration Python3 Modul kodi_six + manuelle Anpassungen
#
################################################################################
# 	<nr>43</nr>										# Numerierung für Einzelupdate
#	Stand: 30.04.2023

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
	try:									# https://github.com/xbmc/xbmc/pull/18345 (Matrix 19.0-alpha 2)
		xbmc.translatePath = xbmcvfs.translatePath
	except:
		pass

# Python
import string, re
import  json		
import datetime, time
import math							# für math.ceil (aufrunden)


# Addonmodule + Funktionsziele (util_imports.py)
import ardundzdf					# -> SenderLiveResolution, Parseplaylist, BilderDasErste, BilderDasErsteSingle
from resources.lib.util import *


# Globals
ICON					= "icon.png"
ICON_MAIN_ARD 			= 'ard-mediathek.png'			
ICON_ARD_AZ 			= 'ard-sendungen-az.png'
ICON_ARD_VERP 			= 'ard-sendung-verpasst.png'			
ICON_ARD_RUBRIKEN 		= 'ard-rubriken.png' 
ICON_ARD_BARRIEREARM 	= 'ard-barrierearm.png'
			
ICON_SEARCH 			= 'ard-suche.png'						
ICON_ZDF_SEARCH 		= 'zdf-suche.png'				
ICON_DIR_FOLDER			= "Dir-folder.png"
ICON_DIR_STRM			= "Dir-strm.png"
ICON_SPEAKER 			= "icon-speaker.png"
ICON_MEHR 				= "icon-mehr.png"

ARDSender = ['ARD-Alle:ard::ard-mediathek.png:ARD-Alle', 'Das Erste:daserste:208:tv-das-erste.png:Das Erste', 
	'BR:br:2224:tv-br.png:BR Fernsehen', 'HR:hr:5884:tv-hr.png:HR Fernsehen', 'MDR:mdr:1386804:tv-mdr-sachsen.png:MDR Fernsehen', 
	'NDR:ndr:5898:tv-ndr-niedersachsen.png:NDR Fernsehen', 'Radio Bremen:radiobremen::tv-bremen.png:Radio Bremen TV', 
	'RBB:rbb:5874:tv-rbb-brandenburg.png:rbb Fernsehen', 'SR:sr:5870:tv-sr.png:SR Fernsehen', 
	'SWR:swr:5310:tv-swr.png:SWR Fernsehen', 'WDR:wdr:5902:tv-wdr.png:WDR Fernsehen',
	'ONE:one:673348:tv-one.png:ONE', 'ARD-alpha:alpha:5868:tv-alpha.png:ARD-alpha', 
	'tagesschau24:tagesschau24::tv-tagesschau24.png:tagesschau24', 'phoenix:phoenix::tv-phoenix.png:phoenix', 
	'KiKA::::KiKA']

ADDON_ID      	= 'plugin.video.ardundzdf'
SETTINGS 		= xbmcaddon.Addon(id=ADDON_ID)
ADDON_NAME    	= SETTINGS.getAddonInfo('name')
SETTINGS_LOC  	= SETTINGS.getAddonInfo('profile')
ADDON_PATH    	= SETTINGS.getAddonInfo('path')	# Basis-Pfad Addon
ADDON_VERSION 	= SETTINGS.getAddonInfo('version')
PLUGIN_URL 		= sys.argv[0]				# plugin://plugin.video.ardundzdf/
HANDLE			= int(sys.argv[1])
FANART = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/fanart.jpg')
ICON = xbmc.translatePath('special://home/addons/' + ADDON_ID + '/icon.png')

ARDStartCacheTime = 300						# 5 Min.	
USERDATA		= xbmc.translatePath("special://userdata")
ADDON_DATA		= os.path.join("%sardundzdf_data") % USERDATA

# Anpassung Kodi 20 Nexus: "3.0.0" -> "3."
if 	check_AddonXml('"xbmc.python" version="3.'):						# ADDON_DATA-Verzeichnis anpasen
	PLog('ARDnew_python_3.x.x')
	ADDON_DATA	= os.path.join("%s", "%s", "%s") % (USERDATA, "addon_data", ADDON_ID)

DICTSTORE 		= os.path.join(ADDON_DATA, "Dict") 
SLIDESTORE 		= os.path.join(ADDON_DATA, "slides") 
SUBTITLESTORE 	= os.path.join(ADDON_DATA, "subtitles") 
TEXTSTORE 		= os.path.join(ADDON_DATA, "Inhaltstexte")

# Ort FILTER_SET wie filterfile (check_DataStores):
FILTER_SET 	= os.path.join(ADDON_DATA, "filter_set")
AKT_FILTER	= RLoad(FILTER_SET, abs_path=True)
AKT_FILTER	= AKT_FILTER.splitlines()					# gesetzte Filter initialiseren 

fname = os.path.join(DICTSTORE, 'CurSender')			# init CurSender (aktueller Sender)
if os.path.exists(fname) == False:						# kann fehlen (Aufruf Merkliste)
	Dict('store', "CurSender", ARDSender[0])			# Default: ARD-Alle

DEBUG			= SETTINGS.getSetting('pref_info_debug')
NAME			= 'ARD und ZDF'

#----------------------------------------------------------------
# CurSender neu belegt in Senderwahl
def Main_NEW(name='', CurSender=''):
	PLog('Main_NEW:'); 
	PLog(name); PLog(CurSender)
			
	if CurSender == '' or up_low(str(CurSender)) == "FALSE":			# Ladefehler?
		CurSender = ARDSender[0]
	if ':' in CurSender:				# aktualisieren	
		Dict('store', "CurSender", CurSender)
		PLog('sender: ' + CurSender); 
		CurSender=py2_encode(CurSender);
	
	sendername, sender, kanal, img, az_sender = CurSender.split(':')	# sender -> Menüs
	sender_summ = 'Sender: [B]%s[/B] (unabhängig von der Senderwahl)' % "ARD-Alle"
	
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)				# Home-Button
	def_tag = 'Sender: [B]%s[/B]' % sendername
	
	if SETTINGS.getSetting('pref_use_mvw') == 'true':
		title = 'Suche auf MediathekViewWeb.de'
		tag = "Extrem schnelle Suche im Datenbestand von MediathekView."
		summ = 'Sender: [B]alle Sender des ARD[/B]' 
		title=py2_encode(title); sender="ARD"
		func = "resources.lib.ARDnew.Main_NEW"
		fparams="&fparams={'title': '%s','sender': '%s' ,'myfunc': '%s'}" % \
			(quote(title), "ARD", quote(func))
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.yt.MVWSearch", fanart=R(ICON_MAIN_ARD), 
			thumb=R("suche_mv.png"), tagline=tag, summary=summ, fparams=fparams)
		
	title = 'Suche in ARD-Mediathek'
	tag = def_tag + " (Suchbereich)"
	title=py2_encode(title);
	fparams="&fparams={'title': '%s', 'sender': '' }" % quote(title) 	# sender -> ARDSearchnew
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDSearchnew", fanart=R(ICON_MAIN_ARD), 
		thumb=R(ICON_SEARCH), tagline=tag, fparams=fparams)
	
	title = 'Startseite'	
	tag = def_tag
	title=py2_encode(title);
	fparams="&fparams={'title': '%s', 'sender': '%s'}" % (quote(title), sender)
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDStart", fanart=R(ICON_MAIN_ARD), thumb=R(img), 
		tagline=tag, fparams=fparams)

	# Retro-Version ab 12.11.2020, V3.5.4
	# 16.06.2021 auch erreichbar via ARD-Startseite/Premium_Teaser_Themenwelten	
	# 07.04.2023 Web-Call -> api-Call	
	path = "https://api.ardmediathek.de/page-gateway/pages/ard/editorial/retro?embedded=false" 
	title = "ARD Mediathek RETRO"
	erbe = u"[COLOR darkgoldenrod]%s[/COLOR]" % "UNESCO Welttag des Audiovisuellen Erbes"
	tag = u'Die ARD Sender öffneten zum %s ihre Archive und stellen zunehmend zeitgeschichtlich relevante Videos frei zugänglich ins Netz' % erbe
	tag = u"%s\n\nDeutsche Geschichte und Kultur nacherleben: Mit ARD Retro können Sie in die Zeit der 1950er und frühen 1960er Jahre eintauchen. Hier stoßen Sie auf spannende, informative und auch mal kuriose Sendungen aus den Anfängen der Fernsehgeschichte des öffentlich-rechtlichen Rundfunks." % tag
	tag = u"%s\n\nMehr: NDR ardretro100.html" % tag
	title=py2_encode(title); path=py2_encode(path);
	fparams="&fparams={'title': '%s', 'sender': '%s', 'path': '%s'}" % (quote(title), sender, quote(path))
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDStart", fanart=R(ICON_MAIN_ARD), 
		thumb=R('ard-mediathek-retro.png'), tagline=tag, fparams=fparams)

	# 07.04.2023 Web-Call -> api-Call	
	path = "https://api.ardmediathek.de/page-gateway/pages/ard/editorial/entdecken?embedded=false" 
	title = "ARD Mediathek Entdecken"
	tag = 'Inhalte der ARD-Seite [B]%s[/B]' % "ENTDECKEN"
	summ = sender_summ	
	title=py2_encode(title); path=py2_encode(path);
	fparams="&fparams={'title': '%s', 'sender': '%s', 'path': '%s'}" % (quote(title), sender, quote(path))
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDStart", 
		fanart=R(ICON_MAIN_ARD), thumb=R('ard-entdecken.png'), tagline=tag, summary=summ, fparams=fparams)

	# 25.12.2021 als eigenständiges Menü (zusätzl. zum Startmenü) - wie Web:
	#	href wie get_ARDstreamlinks
	title = 'Livestreams'
	tag = "Die [B]Livestreams[/B] der ARD"
	summ = 'Sender: [B]%s[/B] (unabhängig von der Senderwahl)' % "ARD-Alle"
	summ = "%s\n\n Fehlende regionale Sender, z.B. BR-Nord, finden sich im Hauptmenü TV-Livestreams" % summ
	img = R("ard-livestreams.png")
	ID = 'Livestream'
	href = 'https://api.ardmediathek.de/page-gateway/widgets/ard/editorials/4hEeBDgtx6kWs6W6sa44yY?pageNumber=0&pageSize=24'
	href=py2_encode(href); title=py2_encode(title); 
	fparams="&fparams={'path': '%s', 'title': '%s', 'widgetID': '', 'ID': '%s'}" %\
		(quote(href), quote(title), ID)
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDStartRubrik", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag, summary=summ)																							

	title = 'Sendung verpasst'
	tag = def_tag
	fparams="&fparams={'title': 'Sendung verpasst', 'CurSender': '%s'}" % (quote(CurSender))
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDVerpasst", 
		fanart=R(ICON_MAIN_ARD), thumb=R(ICON_ARD_VERP), tagline=tag, fparams=fparams)
	
	title = 'Sendungen A-Z'
	tag = def_tag
	fparams="&fparams={'title': 'Sendungen A-Z', 'CurSender': '%s'}" % (quote(CurSender))
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.SendungenAZ", 
		fanart=R(ICON_MAIN_ARD), thumb=R(ICON_ARD_AZ), tagline=tag, fparams=fparams)
						
	# 07.04.2023 Web-Call -> api-Call, 14.04.2023 ARDStart -> ARDRubriken	
	path = "https://api.ardmediathek.de/page-gateway/pages/ard/editorial/sport?embedded=false" 
	title = 'ARD Sport'
	summ = sender_summ	
	img = R("ard-sport.png")
	fparams="&fparams={}"
	title=py2_encode(title); path=py2_encode(path);
	fparams="&fparams={'li': '', 'path': '%s'}" % quote(path)
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDRubriken", 
		fanart=img, thumb=img, summary=summ, fparams=fparams)
			
	# ARD Sportschau nach Web-Änderung abgeschaltet - s. Forum Post vom 12.06.2022
	#	Ausgesuchte Inhalte sportschau.de in ARDSportWDR
	title = u"ARD sportschau.de (WDR)"					# Button WDR sportschau.de -> Hapt_PRG
	tag = u"Auszüge - einschließlich Audio Event Streams"
	img = R("ard-sportschau.png")
	fparams="&fparams={}"
	addDir(li=li, label=title, action="dirList", dirID="ardundzdf.ARDSportWDR", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag)	
			
	# 27.11.2021 als eigenständiges Menü (vorher an wechselnden Pos. im Startmenü):
	title = 'Barrierearm'
	tag = "Barrierefreie Inhalte in der ARD Mediathek"
	summ = sender_summ	
	img = R(ICON_ARD_BARRIEREARM)
	href = 'https://api.ardmediathek.de/page-gateway/pages/ard/editorial/barrierefrei?embedded=true'
	href=py2_encode(href); title=py2_encode(title); 
	fparams="&fparams={'path': '%s', 'title': '%s'}" % (quote(href), quote(title))
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDStartRubrik", fanart=img, thumb=img, 
		fparams=fparams, tagline=tag, summary=summ)																							

	title = 'Bildgalerien Das Erste'	
	fparams="&fparams={}" 
	addDir(li=li, label=title, action="dirList", dirID="BilderDasErste", fanart=R(ICON_MAIN_ARD),
		thumb=R('ard-bilderserien.png'), fparams=fparams)

	title 	= u'Wählen Sie Ihren Sender | aktuell: [B]%s[/B]' % sendername	# Senderwahl
	tag = "die Senderwahl ist wirksam in [B]%s[/B], [B]%s[/B] und [B]%s[/B]" % ("ARD Mediathek", "A-Z", "Sendung verpasst")
	title=py2_encode(title);
	fparams="&fparams={'title': '%s'}" % quote(title)
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.Senderwahl", fanart=R(ICON_MAIN_ARD), 
		thumb=R('tv-regional.png'), tagline=tag, fparams=fparams) 

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
		 		
#---------------------------------------------------------------- 
# Startseite der Mediathek - passend zum ausgewählten Sender -
# 27.10.2019 Laden aus Cache nur noch bei Senderausfall - vorheriges Laden mit ARDStartCacheTime
#	als 1. Stufe störte beim Debugging
#
# 27.05.2020 ARD hat das Seitenlayout geändert:
#	der Scrollmechanismus entfällt. Aufrufer ohne aktiv. Java-Script erhalten eine kompl. Startseite.
#	Für die Auswertung geeignet ist nur der untere Teil. Er enthält ab window.__FETCHED_CONTEXT__
#	die json-Inhalte.
#	Wir extrahieren in ARDStart die Container, jeweils mit den Bildern des 1. Beitrags.
#	Weiterverarbeitung in ARDStartRubrik (path -> json-Seite)
#	Frühere Kopf-Doku entfernt - siehe commits zu V<=3.0.3
#	Problem Stringauswertung: die ersten 4 Container folgen doppelt (bei jedem Sender) - Abhilfe: 
#		Abgleich mit Titelliste. Wg. Performance Verzicht auf json-/key-Auswertung.
# 30.09.2021 Sonderbehdl. spaltenübergreifender Titel mit Breitbild (Auswert. descr, skip Bild)
# 29.06.2022 Abzweig ARDStartRegion für neuen Cluster "Unsere Region" 
# 07.04.2023 Wechsel Web-Call (ardmediathek.de) -> api-Call (api.ardmediathek.de) - embedded
#	json identisch
def ARDStart(title, sender, widgetID='', path=''): 
	PLog('ARDStart:'); 
	
	CurSender = Dict("load", 'CurSender')		
	sendername, sender, kanal, img, az_sender = CurSender.split(':')
	senderimg = img
	PLog(sender); PLog(img)	
	summ = 'Mediathek des Senders [B] %s [/B]' % sendername
		
	if sender == "ard":
		base = "https://api.ardmediathek.de/page-gateway/pages/ard/editorial/mainstreamer-webpwa-nichtaendern?embedded=false"
	else:
		base = "https://api.ardmediathek.de/page-gateway/pages/%s/home?embedded=false" % sender

	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Neu')								# Home-Button

	if path == '':
		path = base
	page, msg = get_page(path)								# api-source ohne Cache
	PLog(len(page))
	page = page.replace('\\"', '*')							# quotierte Marks entf.
	
	container = blockextract ('compilationType":', page)  	# widgets-Container json (Swiper + Rest)
	PLog(len(container))
	title_list=[]											# für Doppel-Erkennung

	cnt=0
	for cont in container:
		tag=""; summ=""
		descr =  stringextract('"description":"', '"', cont)
		ID	= stringextract('"id":"', '"', cont)			# id vor pagination
		pos = cont.find('"pagination"')						# skip ev. spaltenübergreifendes Bild mit 
		if pos > 0:											# descr (Bsp. Bundestagswahl 2021)
			cont = cont[pos:]
			
		title 	= stringextract('"title":"', '"', cont)
		if title in title_list:								# Doppel? - s.o.
			break
		title_list.append(title)
		title = repl_json_chars(title)
				
		ID	= stringextract('"id":"', '"', cont)
		anz= stringextract('"totalElements":', '}', cont)
		anz= mystrip(anz)
		PLog("anz: " + anz)
		if anz == '1':
			tag = u"%s Beitrag" % anz
		else:
			if anz == "null": anz='mehrere'
			tag = u"%s Beiträge" % anz
			
		if descr:
			tag = "%s\n\n%s" % (tag, descr)

		path 	= stringextract('"href":"', '"', cont)
		path = path.replace('&embedded=false', '')			# bzw.  '&embedded=true'
		if "/region/" in path and '{regionId}' in path:		# Bild Region laden, Default Berlin
			region="be"; rname="Berlin"; partner="rbb"		# Default-Region, Änderung in ARDStartRegion
			path = path.replace('{regionId}', region)
		img_path = path.split("pageSize")[0] + "pageSize=1"	# 1. Beitrag reicht
		img = img_preload(ID, img_path, title, 'ARDStart')
		
		if 'Livestream' in title or up_low('Live') in up_low(title):
			if 'Konzerte' not in title:						# Corona-Zeit: Live-Konzerte (keine Livestreams)
				ID = 'Livestream'
		else:
			ID = 'ARDStart'			
		
		PLog('Satz_cont1:');
		func = "ARDStartRubrik"								# Default-Funktion
		if "Unsere Region" in title:						# nur in Startseite ARD-Alle				
			items = Dict("load", 'ARD_REGION')
			rname = "Berlin"; partner = "rbb"
			if "|" in str(items):
				region,rname,partner = items.split("|")
			tag = u"aktuelle Region: [B]%s[/B]" % rname
			summ = u"Partnersender: [B]%s[/B]" % partner
			func = "ARDStartRegion"							# neu ab 29.06.2022
		# todo: ARDStartRubrik -> ARDRubriken (Bsp.: Button 'ARD Sport' in Main_NEW)
		
		if cnt == 1:										# neu ab 12.02.2023: ev. "Regionales"-Menü hinter Stage
			regio_kat = [									# nach Bedarf ergänzen + auslagern
				"mdr|MDR+|https://www.ardmediathek.de/sendung/mdr/Y3JpZDovL21kci5kZS9tZHJwbHVz|https://api.ardmediathek.de/image-service/images/urn:ard:image:eab36fa8ffdb27da?w=640&ch=4bc0c7d930d596d9",
				"mdr|Sport im Osten|https://www.ardmediathek.de/sendung/mdr/Y3JpZDovL21kci5kZS9zZW5kZXJlaWhlbi82ODlhYzU5My1mOWFkLTQ3MTAtOTczMS1lMTNiZTEwODZkMGM|https://api.ardmediathek.de/image-service/images/urn:ard:image:4b8aeaada557019e?w=1600&ch=50fb95aed76b8244&imwidth=1600"
				]
			PLog("regio_check: " + sender)
			for item in regio_kat:
				region, reg_title, reg_path, reg_img= item.split("|")
				if region == sender:
					if reg_img == "":
						reg_img = R(senderimg)
					reg_tag = "besondere regionale Inhalte des %s" % up_low(sender)
					reg_path=py2_encode(reg_path); reg_title=py2_encode(reg_title); 
					fparams="&fparams={'path': '%s', 'title': '%s', 'widgetID': '', 'ID': '%s'}" %\
						(quote(reg_path), quote(reg_title), ID)
					addDir(li=li, label=reg_title, action="dirList", dirID="resources.lib.ARDnew.%s" % func, fanart=reg_img, thumb=reg_img, 
						tagline=reg_tag, fparams=fparams)
					cnt=cnt+1
			
		PLog(path); PLog(title); PLog(ID); PLog(anz); PLog(img); 
		path=py2_encode(path); title=py2_encode(title); 
		fparams="&fparams={'path': '%s', 'title': '%s', 'widgetID': '', 'ID': '%s'}" %\
			(quote(path), quote(title), ID)
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.%s" % func, fanart=img, thumb=img, 
			tagline=tag, summary=summ, fparams=fparams)
		cnt=cnt+1	

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
				
#-----------------------------------------------------------------------
# 19.10.2020 Ablösung img_via_id durch img_preload nach Änderung 
#	der ARD-Startseite: lädt das erste img ermittelt in geladener
#	Seite oder ID.img aus dem Cache - Löschfrist: Setting Slide Shows)
#
def img_preload(ID, path, title, caller, icon=ICON_MAIN_ARD):
	PLog("img_preload: " + title)
	PLog(caller); PLog(path)

	if caller == 'ARDStart' or  caller == 'ARDRubriken':
		leer_img = R(ICON_DIR_FOLDER)
	else:
		leer_img = R("icon-bild-fehlt.png")

	img=''
	oname = os.path.join(SLIDESTORE, "ARDNeu_Startpage")
	fname = os.path.join(oname, ID)
	# PLog(fname)
	
	if os.path.isdir(oname) == False:
		try:  
			os.mkdir(oname)								# UZ-Verz. ARDNeu_Startpage erzeugen
		except OSError as exception:
			msg = str(exception)
			PLog(msg)
			
	if os.path.exists(fname):							# img aus Cache laden
		PLog('img_cache_load: ' + fname)	
		return fname
	else:
		PLog('img_cache_leer')	
		page, msg = get_page(path=path)					# ganze Seite von Sender laden	
		if page=='':
			return leer_img								# Fallback 
	
	img = stringextract('src":"', '"', page)			# Pfad zum 1. img
	if img == '':
		return leer_img									# Fallback 
	
	img = img.replace('{width}', '720')
	urlretrieve(img, fname)								# img -> Cache
	icon = R(icon)
	msg1 = "Lade Bild"
	msg2 = title										# Dateiname bei ARD neu nichtssagend
	xbmcgui.Dialog().notification(msg1,msg2,icon,2000, sound=False)	 
		
	PLog('img_cache_fill: ' + fname)	
	return fname										# lokaler img-Pfad
	
#---------------------------------------------------------------------------------------------------
# Auflistung der Rubriken in json-Inhalt page (json bei html-Seite
#	in script id="fetchedContextValue")
# Hinw.: vorerst Verzicht auf ev. Topnavigation (Submenüs), außer 
#	Sportseite
#
def ARDRubriken(li, path="", page=""): 
	PLog('ARDRubriken:')
	li_org=li

	if page == '':
		skip_subs=False
		page, msg = get_page(path)
	else:
		skip_subs=True									# Subrubriken nicht erneut listen					
	PLog(len(page))
	page = page.replace('\\"', '*')						# quotierte Marks entf.

	if li == "":
		li = xbmcgui.ListItem()
		li = home(li, ID='ARD Neu')						# Home-Button		

	try:
		obs = json.loads(page)
		PLog(str(obs)[:80])
		widgets = obs["widgets"]						# "teasers" hier leer			
	except Exception as exception:
		PLog(str(exception))
		return
	PLog(len(widgets))	

	for s in widgets:	
		PLog(str(s)[:60])	
		img_alt=""; anz="null"
		
		typ = s["type"]
		title = s["title"]
		if title.startswith("Subrubriken"):					# wurde hier bereits gelistet, s.o.
			if skip_subs:
				continue
		if title == "Rubriken":								# rekursiv zur Startseite
			continue
		ID = s["id"]	

		if "links" in s:
			path = s["links"]["self"]["href"]
			path = path.replace('&embedded=false', '')		# bzw. true
			
		try:
			imgsrc 	= s["images"]["aspect16x9"]
			img 	= imgsrc["src"]
			img = img.replace('{width}', '640')
			img_alt = 	imgsrc["alt"]
		except:
			img=""
		if img == "":
			img = img_preload(ID, path, title, 'ARDRubriken')			
		
		tag = "Folgeseiten"
		if 	img_alt:
			tag =  u"%s\Bild: %s" % (tag, img_alt)
		
		ID = 'ARDStartRubrik'
		PLog('Satz_cont2:');
		PLog(title); PLog(ID); PLog(anz); PLog(img); PLog(path);
		path=py2_encode(path); title=py2_encode(title); 
		fparams="&fparams={'path': '%s', 'title': '%s', 'widgetID': '', 'ID': '%s'}" %\
			(quote(path), quote(title), ID)
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDStartRubrik", 
			fanart=img, thumb=img, tagline=tag, fparams=fparams)
			
	if li_org == "":
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	else:	
		return

###################################################			
#---------------------------------------------------------------------------------------------------
# 29.06.2022 Auswertung Cluster "Unsere Region"
# Default-Region: Berlin (wie Web), ID=change: Wechsel
# widgetID transportiert hier region-Triple (Bsp. be|Berlin|rbb)
#
def ARDStartRegion(path, title, widgetID='', ID=''): 
	PLog('ARDStartRegion:')
	PLog(widgetID)	
	PLog(ID)	
	title_org = title
	base = "https://api.ardmediathek.de/page-gateway/widgets/"

	if widgetID:											# frisch gewechselt
		region,rname,partner = widgetID.split("|")
		Dict("store", 'ARD_REGION', "%s|%s|%s" % (region,rname,partner)) 
	else:
		region=""; rname=""; partner=""; 
		page = Dict("load", 'ARD_REGION')
		try:
			region,rname,partner = page.split("|")
		except Exception as exception:
			PLog(str(exception))
	if region == "": 										# Default-Region
		region="be"; rname="Berlin"; partner="rbb"
	
		 
	path = base + "ard/region/6YgzSO0C7huVaGgzM5mq19/%s?pageNumber=0&pageSize=100" % region
	page, msg = get_page(path=path)
	if page == '':	
		msg1 = "Fehler in ARDStartRegion: %s"	% title
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return
		
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Neu')							# Home-Button
	regions = stringextract('regions":', '"links"', page)
	PLog(len(regions))
	#------------------------							# Änderungsliste Region
	if "change" in ID:
		PLog("do_change:")
		PLog(regions[:60])
		img = R(ICON_DIR_FOLDER)
		items = blockextract('"id"', regions)
		for item in items:
			region = stringextract('id":"', '"', item)
			rname = stringextract('name":"', '"', item)
			partner = stringextract('partner":"', '"', item)
			
			widgetID = "%s|%s|%s" % (region,rname,partner)
			title = u"Region: [B]%s[/B]" % rname
			tag = u"Partnersender: [B]%s[/B]" % partner
		
			title=py2_encode(title); widgetID=py2_encode(widgetID);
			fparams="&fparams={'path': '', 'title': '%s', 'widgetID': '%s', 'ID': ''}" %\
				(quote(title), quote(widgetID))
			addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDStartRegion", 
				fanart=img, thumb=img, tagline=tag, fparams=fparams)
	
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
		return
	
	#------------------------							# Auswertung Region
	PLog("do_region:")
	ID = "ARDStartRubrik"
	mark=''	
	li = get_json_content(li, page, ID, mark)			# Auswertung Rubriken + Live-/Eventstreams
	icon = R(ICON_DIR_FOLDER)
	img = icon
	msg1 = "Region"
	msg2 = rname										# Dateiname bei ARD neu nichtssagend
	xbmcgui.Dialog().notification(msg1,msg2,icon,2000, sound=False)	 
	
																	
	if 	'"pagination":'	in page:						# Scroll-Beiträge
		PLog('pagination_Rubrik:')
		title = "Mehr zu >%s<" % title_org				# Mehr-Button	 
		li = xbmcgui.ListItem()							# Kontext-Doppel verhindern
		pages, pN, pageSize, totalElements, next_path = get_pagination(page)	# Basis 0		
		
		if next_path:	
			summ = u"insgesamt: %s Seite(n) , %s Beiträge" % (pages, totalElements)
			pN = int(pN)+1								# nächste pageNumber, Basis 0
			tag = "weiter zu Seite %s" % str(pN)
			PLog(summ); PLog(next_path)

			title_org=py2_encode(title_org); next_path=py2_encode(next_path); mark=py2_encode(mark);
			fparams="&fparams={'title': '%s', 'path': '%s', 'pageNumber': '%s', 'pageSize': '%s', 'ID': '%s', \
				'mark': '%s'}" % (quote(title_org), quote(next_path), str(pN), pageSize, ID, quote(mark))
			addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDPagination", 
				fanart=R(ICON_MEHR), thumb=R(ICON_MEHR), summary=summ, tagline=tag, fparams=fparams)	

	label = u"Region ändern"
	tag = u"aktuelle Region: [B]%s[/B]" % rname
	path=py2_encode(path); title=py2_encode(title); 
	fparams="&fparams={'path': '%s', 'title': '%s', 'ID': 'change'}" %\
		(quote(path), quote(title_org))
	addDir(li=li, label=label, action="dirList", dirID="resources.lib.ARDnew.ARDStartRegion", 
		 fanart=img, thumb=img, tagline=tag, fparams=fparams)
		
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#---------------------------------------------------------------------------------------------------
# Auflistung einer Rubrik aus ARDStart - geladen wird das json-Segment für die Rubrik, z.B.
#		page.ardmediathek.de/page-gateway/widgets/ard/editorials/5zY7iWtNzGagawo0A86Y6U?pageNumber=0&pageSize=12
#		path enthält entweder den Link zur html-Seite www.ardmediathek.de (ID=Swiper) oder den Link
#		zur json-Seite der gewählten Rubrik (früherer Abgleich html-Titel / json-Titel entfällt).
#		Die json-Seite kann Verweise zu weiteren Rubriken enthalten, z.B. bei Staffeln / Serien - Trigger hier
#			 mehrfach=True
#
# Aufrufe: Rubriken aus ARDStart, Sendereihen aus A-Z-Seiten, Mehrfachbeiträge aus ARDSearchnew
# 28.05.2020 getrennte Swiper-Auswertung entfällt nach Änderung der ARD-Seiten
# 18.04.2023 Cache für Startseite entfällt (obsolet - api-Call)
#		
def ARDStartRubrik(path, title, widgetID='', ID='', img=''): 
	PLog('ARDStartRubrik: %s' % ID); PLog(title); PLog(path)	
	title_org = title
	
	CurSender = Dict("load", 'CurSender')				# init s. Modulkopf
	sendername, sender, kanal, img, az_sender = CurSender.split(':')
	PLog(sender)	
		
	li = xbmcgui.ListItem()
	if ID == "ARDRetroStart":
		li = home(li, ID=NAME)							# Home-Button -> Hauptmenü
	else:
		li = home(li, ID='ARD Neu')						# Home-Button

	page, msg = get_page(path=path, GetOnlyRedirect=True)
	path = page
	page, msg = get_page(path=path)	
	if page == '':	
		msg1 = "Fehler in ARDStartRubrik: %s"	% title
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return li
	PLog(len(page))
	page = page.replace('\\"', '*')						# quotierte Marks entf.

#----------------------------------------
	mark=''
	container = blockextract ('compilationType":', page)# Test auf Rubriken
	PLog(len(container))
	if len(container) > 1:
		PLog("ARDStartRubrik_more_container")
		ARDRubriken(li, page=page)						# direkt
	else:												# detect Staffeln/Folgen
		# cnt = page.count(u'"Folge ')					# falsch positiv für "alt":"Folge 9"
		if 'hasSeasons":true' in page and '"heroImage":' in page:
			PLog('Button_FlatListARD')					# Button für flache Liste
			label = u"komplette Liste: %s" % title
			tag = u"Liste aller verfügbaren Folgen"
			if SETTINGS.getSetting('pref_usefilter') == 'false':
				add = u"Voreinstellung: Normalversion.\nFür Hörfassung und weitere Versionen "
				add = u'%sbitte das Setting "Beiträge filtern / Ausschluss-Filter" einschalten' % add
				tag = u"%s\n\n%s" % (tag, add)
			title=py2_encode(title); path=py2_encode(path)			
			fparams="&fparams={'path': '%s', 'title': '%s'}"	% (quote(path), quote(title))						
			addDir(li=li, label=label, action="dirList", dirID="resources.lib.ARDnew.ARD_FlatListEpisodes", 
				fanart=ICON, thumb=R(ICON_DIR_FOLDER), tagline=tag, fparams=fparams)
		
		if ID != "Livestream":	
			ID = "ARDStartRubrik"	
		if "Subrubriken" in title_org:				# skip Subrubrik Übersicht
			mark="Subrubriken"
		li = get_json_content(li, page, ID, mark)																
#----------------------------------------
	
	# 24.08.2019 Erweiterung auf pagination, bisher nur AutoCompilationWidget
	#	pagination mit Basispfad immer vorhanden, Mehr-Button abhängig von Anz. der Beiträge
	if 	'"pagination":'	in page:						# Scroll-Beiträge
		PLog('pagination_Rubrik:')
		title = "Mehr zu >%s<" % title_org				# Mehr-Button	 
		li = xbmcgui.ListItem()							# Kontext-Doppel verhindern
		pages, pN, pageSize, totalElements, next_path = get_pagination(page)	# Basis 0		
		
		if next_path:	
			summ = u"insgesamt: %s Seite(n) , %s Beiträge" % (pages, totalElements)
			pN = int(pN)+1								# nächste pageNumber, Basis 0
			tag = "weiter zu Seite %s" % str(pN)
			PLog(summ); PLog(next_path)
			
			title_org=py2_encode(title_org); next_path=py2_encode(next_path); mark=py2_encode(mark);
			fparams="&fparams={'title': '%s', 'path': '%s', 'pageNumber': '%s', 'pageSize': '%s', 'ID': '%s', \
				'mark': '%s'}" % (quote(title_org), quote(next_path), str(pN), pageSize, ID, quote(mark))
			addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDPagination", 
				fanart=R(ICON_MEHR), thumb=R(ICON_MEHR), summary=summ, tagline=tag, fparams=fparams)	
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#---------------------------------------------------------------------------------------------------
# ermittelt aus page die Parameter für pagination oder AutoCompilationWidget (Scroll-Seiten Rubriken)
# Rückgabe: Pfad mit inkrementierter pageNumber oder  leerer Pfad', falls Beiträge für weitere
#	Seiten fehlen. 
# Nicht für ARDSearchnew - eigene Scrollverwaltung (Parameterbez., Pfad bleibt api-Call)
# Bsp. nur pagination: 				Startseite/Tatort & Polizeiruf
# Bsp. AutoCompilationWidget:	Startseite/Filme nach Rubriken/Alle Filme
# Bsp. Pfade (Auszug): 	/page-gateway/widgets/ard/compilation/, /page-gateway/widgets/ard/asset/,
#						/page-gateway/widgets/ard/editorials/
# pageNumber, pageSize, totalElements: Basis 0
#
def get_pagination(page):
	PLog("get_pagination:")

	pagination	= stringextract('pagination":', '"type"', page)
	pageNumber 	= stringextract('pageNumber":', ',"', pagination)
	pageSize 	= stringextract('pageSize":', ',"', pagination)
	totalElements 	= stringextract('totalElements":', '},', pagination)
	href 		= stringextract('href":"', '"', pagination)	# akt. Pfad mit widgetID
	if '?' in href:
		href		= href.split('?')[0]					# trennt pageNumber + pageSize ab
		
	if 'AutoCompilationWidget' in page:
		PLog('AutoCompilationWidget')
		widget 	= stringextract('AutoCompilationWidget', '"type"', page)
		widgetID= stringextract('Widget:', '"', widget)
		href = href.replace('pages/ard', 'widgets/ard')		# leicht verändert!
		PLog(widget[:100]);PLog(widgetID)
	
	href = href.replace('{', '')							# { statt " möglich		
	PLog('href_akt: %s' % href)
	PLog('pageNumber: %s, pageSize: %s, totalElements:%s ' % (pageNumber, pageSize, totalElements))
	if pageSize == '' or totalElements == '' or totalElements == 'null':	# Sicherung 
		return "", "", "", "", ""
	
	next_path=''; pN=''
	pages = float(totalElements) / float(pageSize)
	pages = int(math.ceil(pages))					# aufrunden für Seitenrest
	
	
	pN = int(pageNumber) + 1			# nächste pageNumber 
	if pN < int(pages):
		next_path = "%s?pageNumber=%d&pageSize=%s" % (href, pN, pageSize)
	PLog(pN);PLog(pageSize);PLog(totalElements);PLog(pages);
	PLog(next_path)
	
	return pages, pN, pageSize, totalElements, next_path
#---------------------------------------------------------------------------------------------------
# 1. Aufrufer: ARDStartRubrik mit pageNumber='1' - Seite 0 bereits ausgewertet
#	dann rekursiv (Mehr-Button) mit den ermittelten Werten pageNumber + pageSize
# Neuer Pfad wird hier mit den ermittelten Werten pageNumber + pageSize zusammengesetzt, Bsp.: 
#	http://page.ardmediathek.de/page-gateway/widgets/ard/compilation/3lCyQCGpIIkaos2EQqIu6q?pageNumber=0&pageSize=24
# Alternative: api-Call via get_api_call 
#	 27.06.2020 Alternative entfällt nach ARD-Änderungen - s. ARDSearchnew,
#		get_api_call entfernt
#
def ARDPagination(title, path, pageNumber, pageSize, ID, mark): 
	PLog('ARDPagination: ' + ID)
	PLog(path)
	
	title_org 	= title 
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Neu')								# Home-Button

	page, msg = get_page(path)					
	if page == '':	
		msg1 = "Fehler in ARDPagination: %s"	% title
		msg2=msg
		MyDialog(msg1, msg2, '')	
		return li
	PLog(len(page))	
	page = page.replace('\\"', '*')							# quotierte Marks entf.
	
	
	li = get_json_content(li, page, ID, mark)
	
	if 	'"pagination":'	in page:				# z.B. Scroll-Beiträge zu Rubriken
		title = "Mehr zu >%s<" % title_org		# Mehr-Button	 # ohne Pfad
		li = xbmcgui.ListItem()							# Kontext-Doppel verhindern
		pages, pN, pageSize, totalElements, next_path  = get_pagination(page)
		
		# Mehr-Button, falls noch nicht alle Sätze ausgegeben		
		if next_path:
			summ = u"insgesamt: %s Seite(n) , %s Beiträge" % (pages, totalElements) 
			pN = int(pN)+1								# nächste pageNumber, Basis 0
			tag = "weiter zu Seite %s" % pN	
			
			PLog(summ); PLog(next_path)
			title_org=py2_encode(title_org); next_path=py2_encode(next_path); mark=py2_encode(mark);
			fparams="&fparams={'title': '%s', 'path': '%s', 'pageNumber': '%s', 'pageSize': '%s', 'ID': '%s', \
				'mark': '%s'}" % (quote(title_org), quote(next_path), pN, pageSize, ID, quote(mark))
			addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDPagination", 
				fanart=R(ICON_MEHR), thumb=R(ICON_MEHR), summary=summ, tagline=tag, fparams=fparams)	
	
	xbmcplugin.endOfDirectory(HANDLE)
	
#---------------------------------------------------------------------------------------------------
# Ähnlich ZDF_FlatListEpisodes, flache Liste aller Folgen
#	ohne Zusätze (Teaser usw.)
# Aufruf ARDStartRubrik ('hasSeasons":true')
#
def ARD_FlatListEpisodes(path, title):
	PLog('ARD_FlatListEpisodes:')
	
	page, msg = get_page(path)	
	if page == '':	
		msg1 = u"Fehler in ARD_FlatListEpisodes: %s"	% title
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return
	PLog(len(page))
	page = page.replace('\\"', '*')						# quotierte Marks entf.

	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)									# Home-Button -> HauptmenüARDStartSingle:

	mediatype=''
	if SETTINGS.getSetting('pref_video_direct') == 'true':	# Sofortstart?
		mediatype='video'
		
	versions = [u'Normalfassung', u'Hörfassung', u'Originalversion (OV)']
	if page.find(u'(OV)') < 0 and page.find(u'(Originalversion)') < 0: 	# Varianten OV
		versions.remove(u'Originalversion (OV)')
	if page.find(u'Hörfassung') < 0:
		versions.remove(u'Hörfassung')
	PLog("versions" + str(versions))

	vers='Normalfassung'								# Default: Normalfassung
	if u'Hörfassung' in page or u'(OV)' in page or 'Originalfassung' in page or '(Originalversion)' in page:	
		if SETTINGS.getSetting('pref_usefilter') == 'true':	# Abfrage Audiodeskription / Originalfassung
			head = u"bitte Filter wählen"
			ret = xbmcgui.Dialog().select(head, versions)
			if ret < 0:
				PLog("Abbruch")
				#return  crasht Addon nach Video, Liste wird erneut durchlaufen - nach Filterwahl OK 
				xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)					
			v = versions[ret]; 
			vers = py2_decode(v)
			
	#---------------------										# Button strm-Dateien gesamte Liste
	if SETTINGS.getSetting('pref_strm') == 'true':
		img = R(ICON_DIR_STRM)
		title = u"strm-Dateien für die komplette Liste erzeugen / aktualisieren"
		tag = u"Verwenden Sie das Kontextmenü, um strm-Dateien für [B]einzelne Videos[/B] zu erzeugen"
		summ = u"[B]strm-Dateien (strm-Bündel)[/B] sparen Platz und lassen sich auch in die Kodi-Bibliothek integrieren."
		summ = u"%s\n\nEin strm-Bündel in diesem Addon besteht aus der strm-Datei mit der Streamurl, einer jpeg-Datei" % summ
		summ = u"%s\nmit dem Bild zum Video und einer nfo-Datei mit dem Begleittext." % summ
		url = path
		url=py2_encode(url); title=py2_encode(title); 
		fparams="&fparams={'path': '%s', 'title': '%s'}" %\
			(quote(url), quote(title))
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARD_getStrmList", fanart=img, thumb=img, 
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

	#---------------------
	
	items = blockextract('availableTo":', page)					# Videos
	PLog("items_list: %d" % len(items))
	for item in items:
		if "Folge " in item == False:
			continue
		title, url, img, tag, summ, season, weburl, ID = ARD_FlatListRec(item, vers) # Datensatz
		if title == '':											# skipped
			continue
		summ_par = summ.replace('\n', '||')
		
		url=py2_encode(url); title=py2_encode(title); summ_par=py2_encode(summ_par);
		fparams="&fparams={'path': '%s', 'title': '%s', 'summary': '%s', 'ID': '%s'}" %\
			(quote(url), quote(title), quote(summ_par), ID)
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDStartSingle", fanart=img, thumb=img, 
			fparams=fparams, tagline=tag, summary=summ, mediatype=mediatype)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
#----------------------------------------------
# holt Details für item
# Aufrufer: ARD_FlatListEpisodes, ARD_getStrmList
# Titel enthält Staffel-/Folgen-Kennz., Bsp.: Folge 1: Das Seil <S01/E01>
# vers: Version, z.B. Hörfassung
#
def ARD_FlatListRec(item, vers):
	PLog('ARD_FlatListRec: ' + vers)
	vers_list=[]	 
	if 'Original' in vers:
		vers_list = [u'(OV)', u'(Original']
	if u'Hörfassung' in vers:
		vers_list = [u'Hörfassung']

	title='';url='';img='';tag='';summ='';
	season='';episode='';descr='';weburl=''; ID=''
	
	title = stringextract('"longTitle":"', '"', item)
	if title == "":
		title =  stringextract('"mediumTitle":"', '"', item)
	PLog("title: " + title)
	title_org=title
	
	if 'Normal' in vers:								# Version berücksichtigen?
		if u'Hörfassung' in title or u'(OV)' in title or u'Original' in title:
			PLog("skip_title: " + title)	
			return '', url, img, tag, summ, season, weburl, ID
	else:
		skip=True
		v=''
		for v in vers_list:
			PLog(title.find(v))
			if title.find(v) >= 0:
				skip=False; break
		if skip == True:
			PLog("skip: %s" % v)	
			return '', url, img, tag, summ, season, weburl, ID
	
	#---------------------								# Staffel-/Folge-Erkennung
	se=''
	try:												# hinter Folge in Titel kann ":" fehlen
		se = title
		if ":" in se:
			se = se.split(":")[-1]						# manchmal zusätzl. im Titel: ..(6):.. 
		se = re.search(u'\((.*?)\)', se).group(1)		# Bsp. (S03/E12)
		season = re.search(u'S(\d+)', se).group(1)
		episode = re.search(u'E(\d+)', se).group(1)
	except Exception as exception:
		PLog(str(exception))
	if season == '' and episode == '':					# Alternative: ohne Staffel, nur Folgen
		try: 
			episode = re.search(u'\((\d+)\)', title).group(1)									
			season = "0"
		except Exception as exception:
			PLog(str(exception))	
	PLog(season); PLog(episode)
	
	if episode == '':
		title=''
		PLog("no_episode")	
		return '', url, img, tag, summ, season, weburl, ID	
	
	if title.startswith("Folge "):						# Austausch "Folge 1" -> S01E01
		if ":" in title:								# mögl. Titel: "Folge 28 (S03/E12)"
			pos = title.find(":")
			if pos > 0:
				title = title[pos+1:]
			title = "S%02dE%02d %s" % (int(season), int(episode), title)
		else:
			title = "S%02dE%02d Folge %02d Staffel %s" % (int(season), int(episode), int(episode), season)
	else:
		title = "S%02dE%02d %s" % (int(season), int(episode), title)

	if u"Hörfassung" in title_org and title.find(u"Hörfassung") < 0:
		title = u"%s - %s" % (title, u"Hörfassung")	
	
	producer =  stringextract('"producerName":"', '"', item)
	descr =  stringextract('"synopsis":"', '"', item)
	web = stringextract('"homepage"', '"hasSeasons"', item)
	weburl =  stringextract('"href":"', '"', web) # für Abgleich vor./nicht mehr vorh. 
	fsk =  stringextract('Rating":"', '"', item)
	if up_low(fsk) == "NONE":
		fsk = "ohne"
	end =  stringextract('availableTo":"', '"', item)
	end = time_translate(end, day_warn=True)
	end = u"[B]Verfügbar bis [COLOR darkgoldenrod]%s[/COLOR][/B]" % end
	# geo =  stringextract('Rating":"', '"', item)		# Geo fehlt
	dauer = stringextract('"duration":', ',', item)
	dauer = seconds_translate(dauer)
	Type =  stringextract('groupingType":"', '"', item)	
	
	img = stringextract('"aspect16x9"', '"title"', item)		# Bild
	# PLog(img)	# Debug
	img =  stringextract('"src":"', '"', img)
	img = img.replace('{width}', '720')
	
	target =  stringextract('"target":', '}', item)	# Ziel-Url mit Streamquellen
	url =  stringextract('"href":"', '"', target)	
	ID =  stringextract('"id":"', '"', target)
	
	tag = u"Staffel: %s | Folge: %s\nDauer: %s | FSK: %s | %s | Hersteller: %s | %s" %\
		(season, episode, dauer, fsk, end, producer, Type)
	
	title = unescape(title)
	summ = repl_json_chars(descr)
	PLog('Satz3:');
	PLog(title); PLog(url); PLog(img); PLog(tag); PLog(summ[:80]);
	PLog(season); PLog(weburl);

	return title, url, img, tag, summ, season, weburl, ID
		
#----------------------------------------------
# wie ZDF_getStrmList
# erzeugt / aktualsiert strm-Dateien für die komplette Liste 
# Ermittlung Streamquellen für api-call
# Ablauf: Seite path laden, Blöcke wie ARD_FlatListEpisodes
#	iterieren -> ZDF_FlatListRec -> ZDF_getApiStreams (Streamquelle 
#	ermitteln -> 
# Nutzung strm-Modul: get_strm_path, xbmcvfs_store
# Cache-Verzicht, um neue Folgen nicht zu verpassen.
#
def ARD_getStrmList(path, title, ID="ARD"):
	PLog("ARD_getStrmList:")
	title_org = title
	list_path = path
	icon = R(ICON_DIR_STRM)
	FLAG_OnlyUrl	= os.path.join(ADDON_DATA, "onlyurl")
	import resources.lib.strm as strm
	
	page, msg = get_page(path=path)
	if page == '':
		msg1 = "Fehler in ARD_getStrmList:"
		msg2 = msg
		MyDialog(msg1, msg2, '')
		return

	pos = page.find("synopsis")							# Serien-Titel (vorgegeben)
	list_title =  stringextract('"title":"', '"', page[pos:])			
	list_title = transl_json(list_title)
	PLog("list_title:" + list_title)
	
	#---------------------								# wie ZDF_getStrmList
	strm_type = strm.get_strm_genre()					# Genre-Auswahl
	if strm_type == '':
		return
	strmpath = strm.get_strm_path(strm_type)			# Abfrage Zielverz. != Filme
	if os.path.isdir(strmpath) == False:
		msg1 = "Zielverzeichnis existiert nicht."
		msg2 = u"Bitte Settings überprüfen."
		MyDialog(msg1, msg2, '')
		return
	
	#---------------------								# Abfrage Version
	versions = [u'Normalfassung', u'Hörfassung', u'Originalversion (OV)']
	if page.find(u'(OV)') < 0 and page.find(u'(Originalversion)') < 0: 	# Varianten OV
		versions.remove(u'Originalversion (OV)')
	if page.find(u'Hörfassung') < 0:
		versions.remove(u'Hörfassung')

	vers='Normalfassung'								# Default: Normalfassung
	if u'Hörfassung' in page or u'(OV)' in page or 'Originalfassung' in page or '(Originalversion)' in page:	
		if SETTINGS.getSetting('pref_usefilter') == 'true':	# Abfrage Audiodeskription / Originalfassung
			head = u"bitte Filter wählen"
			ret = xbmcgui.Dialog().select(head, versions)
			if ret < 0:
				PLog("Abbruch")
				return							
			v = versions[ret]; 
			vers = py2_decode(v)	
	#---------------------										
		
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
		os.mkdir(strmpath)								# Verz. erzeugen, falls noch nicht vorh.
		list_exist=False
	else:
		list_exist=True

	#---------------------
	cnt=0; 
	items = blockextract('availableTo":', page)					# Videos
	for item in items:
		if "Folge " in item == False:
			continue
		title, url, img, tag, summ, season, weburl, ID = ARD_FlatListRec(item, vers) # Datensatz
		if title == '':											# skipped
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
			PLog("%s %s" % (msg1, msg2))
			xbmcgui.Dialog().notification(msg1,msg2,icon,500,sound=False)
					
		Plot = "%s\n\n%s" % (tag, summ)
		msg1 = u'Suche Streamquellen'
		msg2 = title
		xbmcgui.Dialog().notification(msg1,msg2,icon,500,sound=False)
		open(FLAG_OnlyUrl, 'w').close()							# Flag PlayVideo_Direct: kein Videostart
		ARD_get_strmStream(url, title, img, Plot) 				# Streamlisten bauen, Ablage Url
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
		
	#------------------													# Liste synchronisieren?
	# Format: Listen-Titel ## lokale strm-Ablage ##  ext.Url ## strm_type
	item = "%s##%s##%s##%s"	% (list_title, strmpath, list_path, strm_type)
	PLog("item: " + item)
	synclist = strm.strm_synclist(mode="load")							# "strm_synclist"
	if exist_in_list(item, synclist) == True:	
		msg1 = "Synchronsisation läuft"
		msg2 = list_title
		xbmcgui.Dialog().notification(msg1,msg2,icon,3000,sound=True)
		PLog(msg1)
	else:
		if cnt > 0:
			sync_hour = strm.strm_tool_set(mode="load")	# Setting laden
			head = u"Liste synchronisieren"
			msg1 = u"Soll das Addon diese Liste regelmäßig abgleichen?"
			msg2 = u"Intervall: %s Stunden" % sync_hour	
			ret = MyDialog(msg1=msg1, msg2=msg2, msg3='', ok=False, cancel='Nein', yes='OK', heading=head)
			if ret == 1:												# Liste neu aufnehmen
				strm.strm_synclist(mode="save", item=item)
				line = "%6s | %15s | %s..." % ("NEU", list_title[:15], "Liste neu aufgenommen")
				strm.log_update(line)
				line = "strm-Serie|%s|%s" % (list_title, vers)
				Dict("store", 'strmListVersion_%s' % list_title, line) # load: do_sync_ARD 

	return
		
#----------------------------------------------
# Ermittlung Streamquellen für ARD_getStrmList
#	ähnlich ZDF_getApiStreams
# Ablauf: Seite url laden, HLS_List + MP4_List
#	bauen, strm-Url via PlayVideo_Direct ermitteln
#	(dort Abgleich Settings pref_direct_format +
#	pref_direct_quality, Ablage STRM_URL)
# Plot: tag + summ von Aufrufer zusammengelegt
def ARD_get_strmStream(url, title, img, Plot):
	PLog('ARD_get_strmStream:'); 
	
	page, msg = get_page(url)
	if page == '':	
		msg1 = "Fehler in ARD_get_strmStream: %s"	% title
		PLog("%s | %s" % (msg1, msg))	
		return
	PLog(len(page))
	page= page.replace('\\u002F', '/')						# 23.11.2019: Ersetzung für Python3 geändert
	page= page.replace('+++\\n', '+++ ')					# Zeilentrenner ARD Neu
			
	# -----------------------------------------				# Extrakt Videoquellen
	PLog("anz_plugin: %d" % page.count("_plugin"))			# todo: Relevanz _plugin=2 prüfen

	try:
		sub_path=""
		VideoObj = json.loads(page)["widgets"][0]
		if "_subtitleUrl" in VideoObj["mediaCollection"]["embedded"]: # kann fehlen
			sub_path = VideoObj["mediaCollection"]["embedded"]["_subtitleUrl"]
		PLog("sub_path: " + sub_path)
		mediaArray = VideoObj["mediaCollection"]["embedded"]["_mediaArray"]
		StreamArray = VideoObj["mediaCollection"]["embedded"]["_mediaArray"][0]["_mediaStreamArray"]
		PLog("VideoObj: %d, mediaArray: %d, StreamArray: %d" % (len(VideoObj),len(mediaArray), len(StreamArray)))
	except Exception as exception:
		PLog(str(exception))
		msg1 = u'keine Videoquellen gefunden'
		PLog(msg1)
		# MyDialog(msg1, '', '')							# strm o. Dialog (Task)
		return
	
	# Formate siehe StreamsShow								# HLS_List + MP4_List anlegen
	#	generisch: "Label |  Bandbreite | Auflösung | Titel#Url"
	#	fehlende Bandbreiten + Auflösungen werden ergänzt
	call = "ARD_get_strmStream"
	HBBTV_List=''											# nur ZDF
	HLS_List = ARDStartVideoHLSget(title, StreamArray, call)	# Extrakt HLS
	PLog("HLS_List: " + str(HLS_List)[:80])
	MP4_List = ARDStartVideoMP4get(title, StreamArray, call)	# Extrakt MP4
	PLog("MP4_List: " + str(MP4_List)[:80])

	# Abgleich Settings, Ablage STRM_URL
	thumb = img
	PlayVideo_Direct(HLS_List, MP4_List, title, thumb, Plot) 
	
	return
	
####################################################################################################
#							ARD Retro www.ardmediathek.de/ard/retro/
#				als eigenst. Menü, Inhalte auch via Startseite/Menü/Retro erreichbar
# 07.04.2023 Direkt-Call in Main_NEW, ARDRetro() nach Wechsel zu api-Call entfernt
####################################################################################################

####################################################################################################
#						ARD Sport (neu) www.ardmediathek.de/ard/sport/
#				als eigenst. Menü, Inhalte auch via Startseite/Menü/Sport erreichbar
# 07.04.2023 Direkt-Call in Main_NEW, ARDSportneu() nach Wechsel zu api-Call entfernt
####################################################################################################

#---------------------------------------------------------------------------------------------------
# Auswertung für ARDStartRubrik + ARDPagination + ARDSearchnew 
#	Mehrfach- und Einzelsätze
# mark: farbige Markierung in title (z.B. query aus ARDSearchnew) 
# Seiten sind hier bereits senderspezifisch.
# Aufrufe Direktsprünge
# 07.04.2023 skip Subrubrik Übersicht (aktuelle Seite)
# 14.04.2023 get_page_content -> get_json_content 
# gelöscht: def get_page_content(li, page, ID, mark='', mehrzS=''): 
#		
#---------------------------------------------------------------------------------------------------
# 14.04.2023 get_page_content -> get_json_content 
#
def get_json_content(li, page, ID, mark='', mehrzS=''): 
	PLog('get_json_content: ' + ID); PLog(mark)
	ID_org=ID; PLog(type(page))

	CurSender = Dict("load", 'CurSender')						# Debug, Seite bereits senderspez.
	sendername, sender, kanal, img, az_sender = CurSender.split(':')
	PLog(sender)												#-> href
	mediatype=''; pagetitle=''
	
	PLog(page[:80])
	page_obs = json.loads(page)
	if "teasers" in page_obs:
		obs =page_obs["teasers"]
	if "widgets" in page_obs:
		obs =page_obs["widgets"][0]["teasers"]	
	PLog("obs: %d" % len(obs))
	
	# typ-Info Einzelbeträge: ["live", "event", "broadcastMainClip",
	#				"ondemand", "poster"]
	
	for s in obs:
		PLog("Mark10")
		PLog(str(s)[:60])
		uhr=''; ID=ID_org; duration='';	summ=''; availableTo='';
		matRat="Ohne"
		typ = s["type"]
		if "availableTo" in s:
			availableTo = s["availableTo"]

		typ = s["type"]
		if "duration" in s or "broadcastedOn" in s:				# broadcastedOn: Livestream
			mehrfach = False									# Default Einzelbetrag
		else:
			mehrfach = True										# Default weitere Rubriken		

		try:
			imgsrc 	= s["images"]["aspect16x9"]
			img 	= imgsrc["src"]
			img = img.replace('{width}', '640')
			img_alt = 	imgsrc["alt"]
		except:
			img = R(ICON_DIR_FOLDER)							# Bsp.: Subrubriken
		
		title = s["longTitle"]
		title = repl_json_chars(title)
		if mark:												# Markierung Suchbegriff 						
			PLog(title); PLog(mark)
			title = title.strip() 
			title = make_mark(mark, title, "", bold=True)		# -> util
			
		if mehrzS:												# Setting pref_more
			title = u"Mehr: %s" % title	
		if mark == "Subrubriken":
			if title.startswith(u"Übersicht"):					# skip Subrubrik Übersicht (rekursiv, o. Icons) 
				PLog("skip_Übersicht")
				continue				
		
		href = 	s["links"]["target"]["href"]
		if ID != "Livestream" and mehrfach == False:			# Einzelbeiträge außer Live
			PLog("eval_video:")	
			if "publicationService" in s:
				pubServ = s["publicationService"]["name"]
			else:
				pubServ = s["show"]["publisher"]["name"]
			if "maturityContentRating" in s:
				matRat = s["maturityContentRating"]
				matRat = matRat.replace('NONE', 'Ohne')
			if "duration" in s:
				duration = s["duration"]						# sec-Wert
				duration = seconds_translate(duration)			# 0:15
			if duration and pubServ:										
				duration = u'Dauer %s | [B]%s[/B]' % (duration, pubServ)
			if 	matRat:
				if duration == '':
					duration = "Dauer unbekannt"
				duration = u"%s | FSK: %s\n" % (duration, matRat)
				
			if "show" in s:		
				if s["show"]:									# null?
					summ = s["show"]["synopsis"]				# Zusammenfassung
			PLog(summ[:60])	
			if summ == None:
				summ = ""
			summ = repl_json_chars(summ)
				
			verf = availableTo									# s.o.
			if "live" not in typ:								# nicht in Livestreams
				if verf == None:
					verf=""
				verf = time_translate(verf, day_warn=True)
				if verf:
					summ = u"[B]Verfügbar bis [COLOR darkgoldenrod]%s[/COLOR][/B]\n\n%s" % (verf, summ)
				if "broadcastedOn" in s:
					pubDate = s["broadcastedOn"]
					pubDate = time_translate(pubDate)
					pubDate = u" | Sendedatum: [COLOR blue]%s Uhr[/COLOR]\n\n" % pubDate	
					if u'erfügbar bis' in summ:	
						summ = summ.replace('\n\n', pubDate)	# zwischen Verfügbar + summ  einsetzen
					else:
						summ = "%s%s" % (pubDate[3:], summ)
				if duration and summ:
					summ = "%s\n%s" % (duration, summ)	
		else:
			summ = title
			
		if "Sendedatum:" in summ:	
			uhr = summ.split(' ')[-2]
		summ = repl_json_chars(summ)	
			
		# ARDVerpasstContent: Zeit im Titel, Langfass. tagline:
		if 'broadcast' in typ and uhr:							# EPG: broadcastMainClip								
			title = "[COLOR blue]%s[/COLOR] | %s" % (uhr, title) 			
			pubServ = s["publicationService"]["name"]							# publicationService (Sender)
			if pubServ:
				summ = "%sSender: %s" % (summ, pubServ)		
		
		if SETTINGS.getSetting('pref_usefilter') == 'true':		# Filter
			filtered=False
			for item in AKT_FILTER: 
				if up_low(item) in py2_encode(up_low(str(s))):
					filtered = True
					break		
			if filtered:
				PLog('filtered: <%s> in %s ' % (item, title))
				continue		
	
		PLog('Satz:');
		PLog(mehrfach); PLog(title); PLog(href); PLog(img); PLog(summ[:60]); 
		PLog(duration); PLog(availableTo);
		
		if mehrfach:
			summ = "Folgeseiten"
			href=py2_encode(href); title=py2_encode(title); 
			fparams="&fparams={'path': '%s', 'title': '%s'}" % (quote(href), quote(title))
			addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDStartRubrik", \
				fanart=img, thumb=img, fparams=fparams, summary=summ, mediatype='')	
		else:
			PLog("eval_settings:")	
			if pagetitle == '':									# pagetitle -> title_samml
				if "homepage" in s:								# Home-Titel kann fehlenden Sendungstitel enthalten
					pagetitle = s["homepage"]
					pagetitle = stringextract('"title":"', '"', pagetitle)
			title_samml = "%s|%s" % (title, pagetitle)			# Titel + Seitentitel (A-Z, Suche)
			if SETTINGS.getSetting('pref_mark_full_shows') == 'true':
				if ID != "Search":								# Vorrang Suchmarkierung vor full_shows					
					if "duration" in s:
						dur = s["duration"]; 
						dur = str(int(dur))					
						title = ardundzdf.full_shows(title, title_samml, summ, dur, "full_shows_ARD")	

			if SETTINGS.getSetting('pref_load_summary') == 'true':	# summary (Inhaltstext) im Voraus holen
				summ_new = get_summary_pre(path=href, ID='ARDnew', duration=duration)  # Modul util
				if 	summ_new:
					summ = summ_new
					
			if SETTINGS.getSetting('pref_video_direct') == 'true':	# Sofortstart?
				mediatype='video'
			
			if typ == "live"  or typ == "event" :					# Livestream in Stage od. ARD Sport
				ID = "Livestream"								
				summ = "%s | [B]Livestream[/B]" % summ
			else:
				ID=ID_org
			PLog("Satz_cont3: typ: %s, ID: %s" % (typ, ID))
			
			summ_par = summ.replace('\n', '||')
			href=py2_encode(href); title=py2_encode(title); summ_par=py2_encode(summ_par);
			fparams="&fparams={'path': '%s', 'title': '%s', 'summary': '%s', 'ID': '%s'}" %\
				(quote(href), quote(title), quote(summ_par), ID)
			addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDStartSingle", fanart=img, thumb=img, 
				fparams=fparams, summary=summ, mediatype=mediatype)	
																										
	return li	

#---------------------------------------------------------------------------------------------------
# Ermittlung der Videoquellen für eine Sendung - hier Aufteilung Formate Streaming + MP4
# Bei Livestreams (m3u8-Links) verzweigen wir direkt zu SenderLiveResolution.
# Videodaten unterteilt in _plugin":0 und _plugin":1,
# Falls path auf eine Rubrik-Seite zeigt, wird zu ARDStartRubrik zurück verzweigt 
#	(sofern keine Streams vorhanden)
# 02.05.2019 erweitert: zusätzl. Videos zur Sendung angehängt - s.u.
# 28.05.2020 Stream-Bezeichner durch ARD geändert
# 19.10.2020 Mehr-Auswertung an ARD-Änderungen angepasst: get_ardsingle_more entfällt,
#	Auswertung durch get_page_content nach entfernung des 1. elements und 
#	page="\n".join(gridlist). mehrzS verhindert Rekursion.	
# 13.11.2020 Anpassung an ARDRetro: Switch Home-Button via ID=ARDRetroStart (dto. in
#	ARDStartVideoStreams + ARDStartVideoMP4, Änderung mehrzS (ID -> Flag, Rekurs.-Stop)
# 05.01.2021 Anpassung für Sofortstart-Format: HLS_List + MP4_List -> PlayVideo_Direct
#	(Streamwahl -> PlayVideo)
# 21.01.2021 Nutzung build_Streamlists_buttons (Haupt-PRG), einschl. Sofortstart
# 25.01.2021 no-cache-Header für Verpasst- und A-Z-Beiträge
# 14.02.2023 HBBTV-Quellen (http://tv.ardmediathek.de/dyn/get?id=video%3A..)
#
def ARDStartSingle(path, title, summary, ID='', mehrzS=''): 
	PLog('ARDStartSingle: %s' % ID);
	title_org = title

	headers=''
	# Header für Verpasst-Beiträge (ARDVerpasstContent -> get_json_content)
	if ID == 'EPG' or ID == 'A-Z':											
		headers = "{'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma':'no-cache',\
			'Expires': '0'}"		

	page, msg = get_page(path, header=headers)
	if page == '':	
		msg1 = "Fehler in ARDStartSingle: %s"	% title
		msg2=msg
		MyDialog(msg1, msg2, '')	
		xbmcplugin.endOfDirectory(HANDLE)
	PLog(len(page))
	page= page.replace('\\u002F', '/')						# 23.11.2019: Ersetzung für Python3 geändert
	page= page.replace('+++\\n', '+++ ')					# Zeilentrenner ARD Neu
	

	elements = blockextract('"availableTo":', page)			# möglich: Mehrfachbeiträge? z.B. + Hörfassung
	IsPlayable = xbmc.getInfoLabel('ListItem.Property(IsPlayable)') # 'true' / 'false'
	PLog("IsPlayable: %s" % IsPlayable)	
	if len(elements) > 1:
		if '_quality"' not in page:							# Keine Quellen -> Abbruch
			msg1 = u"[B]%s[/B] enthält keine Videoquellen"	% title
			msg2 = u"Mögliche Ursache: Altersbeschränkung"
			msg3 = u"Eine Suche in MediathekViewWeb könnte helfen."
			MyDialog(msg1, msg2, msg3)	
			return											# hebt IsPlayable auf (Player-Error: skipping ..)			
			
	if len(elements) == 0:									# möglich: keine Video (dto. Web)
		msg1 = u'keine Beiträge zu %s gefunden'  % title
		PLog(msg1)
		MyDialog(msg1, '', '')
		xbmcplugin.endOfDirectory(HANDLE)	
	PLog('elements: ' + str(len(elements)))	
	PLog("anz_plugin: %d" % page.count("_plugin"))			# todo: Relevanz _plugin=2 prüfen
		
	try:
		sub_path=""
		VideoObj = json.loads(page)["widgets"][0]
		if "_subtitleUrl" in VideoObj["mediaCollection"]["embedded"]: # kann fehlen
			sub_path = VideoObj["mediaCollection"]["embedded"]["_subtitleUrl"]
		PLog("sub_path: " + sub_path)
		mediaArray = VideoObj["mediaCollection"]["embedded"]["_mediaArray"]
		StreamArray = VideoObj["mediaCollection"]["embedded"]["_mediaArray"][0]["_mediaStreamArray"]
		PLog("VideoObj: %d, mediaArray: %d, StreamArray: %d" % (len(VideoObj),len(mediaArray), len(StreamArray)))
	except Exception as exception:
		PLog(str(exception))
		msg1 = u'keine Videoquellen gefunden'
		PLog(msg1)
		MyDialog(msg1, '', '')
		return	
	
	li = xbmcgui.ListItem()
	if ID == "ARDRetroStart":
		li = home(li, ID=NAME)								# Home-Button -> Hauptmenü
	else:
		if ID != 'Livestream':								# ohne home - Nutzung durch Classic
			li = home(li, ID='ARD Neu')						# Home-Button
			
	img = VideoObj["image"]["src"]
	img = img.replace('{width}', '640')
	geoblock = VideoObj["geoblocked"]						# false, true
	if geoblock:											# Geoblock-Anhang für title, summary
		geoblock = ' | Geoblock: JA'
		title = title + geoblock
	else:
		geoblock = ' | Geoblock: nein'
	PLog("geoblock: " + geoblock)	
					
	# Livestream-Abzweig, Bsp. tagesschau24:	
	# 	Kennzeichnung Livestream: 'class="day">Live</p>' in ARDStartRubrik.
	#	für Menü TV-Livestreams s. get_ARDstreamlinks
	# todo: Umstellung -> json
	if ID	== 'Livestream':								# Livestreams -> SenderLiveResolution		
		VideoUrls = blockextract('_quality', page)			# 2 master.m3u8-Url (1 x UT)
		PLog(len(VideoUrls))
		href_ut=''
		for video in VideoUrls:
			href = stringextract('stream":"', '"', video)	
			PLog(href)
			if '_ut_' in href or '_sub' in href:				# UT-Stream filtern, bisher nur ARD, HR
				href_ut = href

		if SETTINGS.getSetting('pref_UT_ON') == 'true':	
			if href_ut:
				href = href_ut
		
		if href.startswith('//'):
			href = 'https:' + href
		PLog('Livestream_Abzweig: ' + href)
		return ardundzdf.SenderLiveResolution(path=href, title=title, thumb=img, descr=summary)
		
	# -----------------------------------------			# Extrakt Videoquellen
	# 17.02.2023 Umstellung string -> json
	# Formate siehe StreamsShow							# HLS_List + MP4_List anlegen
	#	generisch: "Label |  Bandbreite | Auflösung | Titel#Url"
	#	fehlende Bandbreiten + Auflösungen werden ergänzt
	call = "ARDStartSingle"
	HLS_List = ARDStartVideoHLSget(title, StreamArray, call)	# Extrakt HLS
	PLog("HLS_List: " + str(HLS_List)[:80])
	HBBTV_List = ARDStartVideoHBBTVget(title, path)				# HBBTV (MP4), eigene Quellen
	PLog("HBBTV_List: " + str(HBBTV_List)[:80])
	MP4_List = ARDStartVideoMP4get(title, StreamArray, call)	# MP4
	Dict("store", 'ARDNEU_HLS_List', HLS_List) 
	Dict("store", 'ARDNEU_HBBTV_List', HBBTV_List) 
	Dict("store", 'ARDNEU_MP4_List', MP4_List) 
	PLog("download_list: " + str(MP4_List)[:80])
	
	if len(HLS_List) == 0 and len(HBBTV_List) == 0 and len(MP4_List) == 0:
		msg1 = "keine Streamingquelle gefunden: %s"	% title
		PLog(msg1)
		MyDialog(msg1, '', '')	
		return li	
	
	#----------------------------------------------- 
	# Nutzung build_Streamlists_buttons (Haupt-PRG), einschl. Sofortstart
	# 
	PLog('Lists_ready:');
	# summ = get_summary_pre(path, ID='ARDnew', page=page)	# entfällt mit summary aus get_json_content 
	Plot = "Titel: %s\n\n%s" % (title_org, summary)				# -> build_Streamlists_buttons
	PLog('Plot:' + Plot)
	thumb = img; ID = 'ARDNEU'; HOME_ID = "ARD Neu"
	
	played_direct = ardundzdf.build_Streamlists_buttons(li,title_org,thumb,geoblock,Plot,sub_path,\
		HLS_List,MP4_List,HBBTV_List,ID,HOME_ID)

	# -----------------------------------------		# mehr (Videos) zur Sendung,
	if mehrzS or played_direct:						# skip bei direktem Aufruf
		return										# 13.11.2021 notw. für Rückspr. z. Merkliste
		xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

	PLog('Mehr_Test')
	# zusätzl. Videos zur Sendung (z.B. Clips zu einz. Nachrichten). element enthält 
	#	Sendungen ab dem 2. Element (1. die Videodaten)
	# 19.10.2020 Funktion get_ardsingle_more entfällt
	# 15.04.2023 Auswertung Mehr-Beiträge -> json
	if len(elements) > 1 and SETTINGS.getSetting('pref_more') == 'true':
		gridlist = elements[1:]						# hinter den Videodaten (1. Element)
		PLog('gridlist_more: ' + str(len(gridlist)))	
		s = json.loads(page)["widgets"][1]			
		page  = json.dumps(s)
		PLog(page[:100])
		get_json_content(li, page, ID=ID, mehrzS=True, mark='')	
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#----------------------------
# auto-Stream master.m3u8 aus VideoUrls ermitteln, 
#	via li in Einzelauflösungen zerlegen
# Aufrufer ARDStartSingle (Länge VideoUrls > 0) und
# 	ARD_get_strmStream
#
def ARDStartVideoHLSget(title, StreamArray, call=""): 
	PLog('ARDStartVideoHLSget: ' + call); 
	PLog(str(StreamArray)[:100])
	
	HLS_List=[]; Stream_List=[];
	title = py2_decode(title)
	
	for video in  StreamArray:				
		#PLog(str(video)[:100])
		if video["_quality"] == "auto":	# master.m3u8
			href =  video["_stream"]	# Video-Url
			if href.startswith('http') == False:
				href = 'https:' + href
			quality = u'automatisch'
			HLS_List.append(u'HLS automatische Anpassung ** auto ** auto ** %s#%s' % (title,href))
			break
			
	li=''; img=''; geoblock=''; descr='';					# für Stream_List n.b.
	if href:
		Stream_List = ardundzdf.Parseplaylist(li, href, img, geoblock, descr, stitle=title, buttons=False)
		if type(Stream_List) == list:						# Fehler Parseplaylist = string
			HLS_List = HLS_List + Stream_List
		else:
			HLS_List=[]
	#PLog(Stream_List)
	
	return HLS_List

#----------------------------
# HBBTV-Quellen laden 
# json-Quelle:	tv.ardmediathek.de/..
# Aufrufer ARDStartSingle
#
def ARDStartVideoHBBTVget(title, path): 
	PLog('ARDStartVideoHBBTVget:'); 
	PLog(path)

	base = "http://tv.ardmediathek.de/dyn/get?id=video%3A"
	HBBTV_List=[];
	title = py2_decode(title)
	
	if "?devicetype=" in path:					# ID ermitteln
		path = path.split("?devicetype=")[0]
	ID = path.split("/")[-1]
	path = base + ID + "&client=ard"
		
	page, msg = get_page(path, do_safe=False)					
	if page == '':	
		PLog(msg)
		return HBBTV_List

	try:
		page = json.loads(page)
		
		streams = page["video"]["streams"][0]
		PLog("streams0: %d" % len(streams))
		PLog(str(streams)[:80])
	except Exception as exception:
		PLog(str(exception))
		return HBBTV_List
	
	for stream in streams["media"]:
		PLog(str(stream)[:80])
		quality = stream["forcedLabel"]
		w = stream["maxHResolutionPx"] 
		h = stream["maxVResolutionPx"]
		res = "%sx%s" % (str(w),str(h))	
		href = stream["url"]
		if "_internationalerton_" in href:		# vermutl. identisch mit "_sendeton_"-Url
			continue
		try:						
			bitrate = re.search(u'-(\d+)kbit', href).group(1)
			bitrate = "%skbit" % bitrate
		except:
			bitrate = "?"
		
		PLog("hbbtv_bitrate: %s, res: %s" % (bitrate, res)) 
		if "3840x" in res:
			quality = "UHD_MP4"
		title_url = u"%s#%s" % (title, href)
		item = u"MP4 Qualität: [B]%10s[/B] ** Bitrate %s ** Auflösung %s ** %s" % (quality, bitrate, res, title_url)
		item = py2_decode(item)
		HBBTV_List.append(item)

	return HBBTV_List

#----------------------------
# holt Downloadliste mit MP4-Videos
# altes Format: "Qualität: niedrige | Titel#https://pdvideosdaserste.."
# neues Format:	"MP4 Qualität: Full HD ** Bandbreite ** Auflösung ** Titel#Url"
# Format ähnlich ARDStartVideoHBBTVget (Label abweichend)
def ARDStartVideoMP4get(title, StreamArray, call=""):	
	PLog('ARDStartVideoMP4get:'); 
			
	href=''; quality=''
	title = py2_decode(title)
	qlist = [u"0|niedrige|480x270", u"1|mittlere|640x360", u"2|hohe|960x540", 
			u"3|sehr hohe|1280x720", u"4|Full HD|1920x1080",
	]
	download_list = []	
	# 2-teilige Liste für Download: 'title # url'

	for stream in StreamArray:
		PLog(str(stream)[:80])
		qual = str(stream["_quality"])
		if qual == "auto":						# in HLS-List
			continue
			
		quality =  "?"
		for q in qlist:
			q_val,  q_text, q_res = q.split("|")
			if qual in q_val:
				quality = q_text
				break
		if "_width" in stream and "_height" in stream: # können in TagesschauXL fehlen
			w = stream["_width"] 
			h = stream["_height"]
			res = "%sx%s" % (str(w),str(h))
		else:
			PLog("res_missing")
			res = q_res
		href = stream["_stream"]
		if "_internationalerton_" in href:		# vermutl. identisch mit "_sendeton_"-Url
			continue
		try:						
			bitrate = re.search(u'-(\d+)kbit', href).group(1)
			bitrate = "%skbit" % bitrate
		except:
			bitrate = "?"
		
		PLog("mp4_bitrate: %s, res: %s" % (bitrate, res)) 
		if "3840x" in res:
			quality = "UHD_MP4"
		title_url = u"%s#%s" % (title, href)
		item = u"MP4 Qualität: [B]%10s[/B] ** Bitrate %s ** Auflösung %s ** %s" % (quality, bitrate, res, title_url)
		item = py2_decode(item)
		download_list.append(item)
	
	#PLog(download_list)
	return download_list			
			
####################################################################################################
# Auflistung 0-9 (1 Eintrag), A-Z (einzeln) 
# 10.11.2019 Verzicht auf Abgleich Button/Webseite (Performance, lange Ladezeit).
# 28.05.2020 ARD-Änderungen - s. SendungenAZ_ARDnew
# 25.01.2021 Laden + Caching der Link-Übersicht, Laden der Zielseite in 
#	SendungenAZ_ARDnew
# 		
def SendungenAZ(title, CurSender=''):		
	PLog('SendungenAZ: ' + title)
	PLog(CurSender)

	if CurSender == '' or CurSender == False or CurSender == 'false':	# Ladefehler?
		CurSender = ARDSender[0]
	if ':' in CurSender:				# aktualisieren	
		Dict('store', "CurSender", CurSender)
		PLog('sender: ' + CurSender); 
		CurSender=py2_encode(CurSender);
	sendername, sender, kanal, img, az_sender = CurSender.split(':')
	PLog(sender)
		
	title2 = title + ' | aktuell: %s' % sendername
	# no_cache = True für Dict-Aktualisierung erforderlich - Dict.Save() reicht nicht			 
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Neu')						# Home-Button
		
	# Link-Übersicht laden:
	# azlist = list(string.ascii_uppercase)			# 25.01.2021 A-Z - nicht mehr benötigt
	# azlist.insert(0,u'#')	
	path = 'https://api.ardmediathek.de/page-gateway/pages/%s/editorial/experiment-a-z?embedded=false' % sender
	page = Dict("load", 'ARDnew_AZ_%s' %sender, CacheTime=ARDStartCacheTime)
	if page == False:										# nicht vorhanden oder zu alt
		page, msg = get_page(path)		
		if page == '':	
			msg1 = u"Fehler in SendungenAZ:"
			msg2 = msg
			MyDialog(msg1, msg2, '')	
			return li
		else:	
			Dict("store", 'ARDnew_AZ_%s' %sender, page) 	# Seite -> Cache: aktualisieren	
	
	# Buchstabenblock: "title":"#","href":"https://api...
	pat = '"urlId":'									# Link-Blöcke (title":" 2x enth.)
	gridlist = blockextract(pat, page)	
	PLog('pat: %s, gridlist: %d' % (pat, len(gridlist)))			
	if len(gridlist) == 0:				
		msg1 = u'Keine Beiträge gefunden zu %s' % button	
		MyDialog(msg1, '', '')					
		return li	
							
	for grid in gridlist:
		button = stringextract('title":"', '"', grid)
		#if button == 'Z':	# Debug
		#	PLog(grid)
		if ' A-Z' in button:								# Gesamtlink
			continue
			
		title = "Sendungen mit " + button
		anz = stringextract('totalElements":', '}', grid)
		href = stringextract('href":"', '"', grid)
		tag = u'Gezeigt wird der Inhalt für [B]%s[/B]' % sendername
		
		PLog('Satz1:');
		PLog(button); PLog(anz); PLog(href); 
		href=py2_encode(href); title=py2_encode(title); 	
		fparams="&fparams={'title': '%s', 'button': '%s', 'href': '%s'}" % (title, button, quote(href))
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.SendungenAZ_ARDnew",\
			fanart=R(ICON_ARD_AZ), thumb=R(ICON_ARD_AZ), tagline=tag, fparams=fparams)
			
	title 	= u'Wählen Sie Ihren Sender | aktuell: [B]%s[/B]' % sendername	# Senderwahl
	title=py2_encode(title); caller='resources.lib.ARDnew.SendungenAZ'
	tag = "die Senderwahl ist wirksam in [B]%s[/B], [B]%s[/B] und [B]%s[/B]" % ("ARD Mediathek", "A-Z", "Sendung verpasst")
	fparams="&fparams={'title': '%s', 'caller': '%s'}" % (quote(title), caller)
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.Senderwahl", fanart=R(ICON_MAIN_ARD), 
		thumb=R('tv-regional.png'), tagline=tag, fparams=fparams)																	
										
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
####################################################################################################
# Auflistung der A-Z-Buttons bereits in SendungenAZ einschl. Kennz. "Keine Inhalte".
#
# Weiterverarbeitung in ARDStartRubrik.
#
# 28.05.2020 ARD-Änderungen: 
#	Scroll-Mechanismus, Gruppen-Fallback + die bisherigen API-Calls entfallen.
#	Die kompl. Startseite wird auch nicht mehr benötigt, ist aber wie in ARDStart
#	erhältlich und enthält die gesamte Übersicht a-Z (ca. 2MByte).
#	Hier nutzen wir einen api-Call, jweils mit dem betref. Buchstaben 
#	Alternative: kompl. Startseite laden + ab window.__FETCHED_CONTEXT__ 
#				die Beitragstitel im json-Inhalt mit button abgleichen.
# 17.12.2020 Button '#' für ARD-Alle nicht mehr verfügbar - Umstellung
#	auf neuen api-Link (experiment-a-z). Die json-Seite enthält für den
#	gewählten Sender alle Beiträge A-Z, jeweils in Blöcken für einz.
#	Buchstaben.
#	Zusätzl. Cachenutzung (ARD_AZ_ard: 1,5 MByte)
# 25.01.2021 die grouping-Links funktionieren nicht mehr bei allen Beiträgen-
#	Umstellung auf "editorial"-Links (i.d.R. 2x vorh., Auswahl "embedded"),
#	Verzicht auf Laden + Caching der Gesamtseite, stattdessen in SendungenAZ
#	Laden der Link-Übersicht mit embedded-Zusatz und hier Laden der Zielseite
#
def SendungenAZ_ARDnew(title, button, href): 
	PLog('SendungenAZ_ARDnew:')
	PLog('button: ' + button); 
	title = title	
	title_org = title

	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Neu')								# Home-Button

	CurSender = Dict("load", 'CurSender')		
	sendername, sender, kanal, img, az_sender = CurSender.split(':')
	PLog(sender)
	
	# der Link lädt die kompl. Beiträge A-Z, ausgewertet wird der passende Buchstabenblock
	# Alternative (vor V3.7.1): Link ohne Zusatz  lädt die kompl. Beiträge A-Z
	href = href.replace('&embedded=false', '')				# ohne entspr. Header nur leere Seite
	page, msg = get_page(href)		
	if page == '':	
		msg1 = u"Fehler in SendungenAZ_ARDnew: %s"	% title
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return li
	PLog(len(page))
	page = page.replace('\\"', '*')						# quotierte Marks entf., Bsp. \"query\"
			
	ID = 'A-Z'
	li = get_json_content(li, page, ID, mark="")																	
			
	# 24.08.2019 Erweiterung auf pagination, bisher nur AutoCompilationWidget
	#	pagination mit Basispfad immer vorhanden, Mehr-Button abhängig von Anz. der Beiträge
	if 	'"pagination":'	in page:						# Scroll-Beiträge
		PLog('pagination_Rubrik:')
		title = "Mehr zu >%s<" % title_org				# Mehr-Button	 
		li = xbmcgui.ListItem()							# Kontext-Doppel verhindern
		pages, pN, pageSize, totalElements, next_path = get_pagination(page)	# Basis 0
		mark=''		
		if next_path:	
			summ = u"insgesamt: %s Seite(n) , %s Beiträge" % (pages, totalElements)
			pN = int(pN)+1								# nächste pageNumber, Basis 0
			tag = "weiter zu Seite %s" % str(pN)
			PLog(summ); PLog(next_path)
			
			title_org=py2_encode(title_org); next_path=py2_encode(next_path); mark=py2_encode(mark);
			fparams="&fparams={'title': '%s', 'path': '%s', 'pageNumber': '%s', 'pageSize': '%s', 'ID': '%s', \
				'mark': '%s'}" % (quote(title_org), quote(next_path), str(pN), pageSize, ID, quote(mark))
			addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDPagination", 
				fanart=R(ICON_MEHR), thumb=R(ICON_MEHR), summary=summ, tagline=tag, fparams=fparams)	
														

	xbmcplugin.endOfDirectory(HANDLE)	
#----------------------------------------------------------------

# Suche in beiden Mediatheken
#	Abruf jeweils der 1. Ergebnisseite
#	Ohne Ergebnis -> Button mit Rücksprung hierher
#	Ergebnis ZDF: -> ZDF_Search (erneuter Aufruf Seite 1, weitere Seiten dort rekursiv)
#		Ablage in Dict nicht erf., Kodi-Cache ausreichend.
# 22.08.2019 myhash und erste pageNumber geändert durch ARD (0, vorher 1) - dto. in ARDSearchnew
# 27.06.2020 api-Codeanteile entfernt - s. SearchARDnew
# 01.03.2023 ARD-Suchpfad wie SearchARDundZDFnew (page.ardmediathek -> api.ardmediathek)
#
def SearchARDundZDFnew(title, query='', pagenr=''):
	PLog('SearchARDundZDFnew:');
	query_file 	= os.path.join(ADDON_DATA, "search_ardundzdf")
	
	if query == '':														# Liste letzte Sucheingaben
		query_recent= RLoad(query_file, abs_path=True)
		if query_recent.strip():
			search_list = ['neue Suche']
			query_recent= query_recent.strip().splitlines()
			query_recent=sorted(query_recent, key=str.lower)
			search_list = search_list + query_recent
			ret = xbmcgui.Dialog().select('Sucheingabe', search_list, preselect=0)
			if ret == -1:
				PLog("Liste Sucheingabe abgebrochen")
				return ardundzdf.Main()
			elif ret == 0:
				query = ''
			else:
				query = search_list[ret]
				query = "%s|%s" % (query,query)							# doppeln			
	
	if query == '':
		query = ardundzdf.get_query(channel='ARDundZDF') 
	if  query == None or query.strip() == '':
		# return li														# getting plugin Error
		return ardundzdf.Main()
		
	query=py2_encode(query)		# decode, falls erf. (1. Aufruf)
	PLog(query)
	query_ard = query.split('|')[0]
	query_zdf = query.split('|')[1]
	
	tag_negativ =u'neue Suche in ARD und ZDF starten'					# ohne Treffer
	tag_positiv =u'gefundene Beiträge zeigen'							# mit Treffer
	store_recents = False												# Sucheingabe nicht speichern
	
	li = xbmcgui.ListItem()
	li = home(li, ID=NAME)												# Home-Button
	
	#------------------------------------------------------------------	# 1. Suche ARD
	sendername, sender, kanal, img, az_sender = ARDSender[0].split(':') # in allen Sendern
	sender = 'ard'
	pageNumber = 0
	
	query_lable = query_ard.replace('+', ' ')
	path = 'https://api.ardmediathek.de/search-system/mediathek/%s/search/vods?query=%s&pageNumber=%s&pageSize=24' % (sender, query_ard, pageNumber)
	icon = R(ICON_SEARCH)
	xbmcgui.Dialog().notification("ARD-Suche",query_lable,icon,1000, sound=False)
	page, msg = get_page(path,JsonPage=True)					
		
	vodTotal =  stringextract('"totalElements":', '}', page)	# Beiträge?
	gridlist = blockextract( '"mediumTitle":', page) 			# Sicherung
	vodTotal=py2_encode(vodTotal); query_lable=py2_encode(query_lable);
	PLog(query_ard)
	if len(gridlist) == 0 or vodTotal == '0':
		label = "[B]ARD[/B] | nichts gefunden zu: %s | neue Suche" % query_lable
		title="Suche in ARD und ZDF"
		title=py2_encode(title); 
		fparams="&fparams={'title': '%s'}" % quote(title)
		addDir(li=li, label=label, action="dirList", dirID="resources.lib.ARDnew.SearchARDundZDFnew", 
			fanart=R('suche_ardundzdf.png'), thumb=R('suche_ardundzdf.png'), tagline=tag_negativ, fparams=fparams)
	else:	
		store_recents = True											# Sucheingabe speichern
		PLog(type(vodTotal)); 	PLog(type(query_lable)); 			
		title = "[B]ARD[/B]: %s Video(s)  | %s" % (vodTotal, query_lable)
		query_ard=py2_encode(query_ard); title=py2_encode(title); 
		fparams="&fparams={'query': '%s', 'title': '%s', 'sender': '%s','offset': '0'}" %\
			(quote(query_ard), quote(title), sender)
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDSearchnew", 
			fanart=R('suche_ardundzdf.png'), thumb=R('suche_ardundzdf.png'), tagline=tag_positiv, fparams=fparams)
		
	#------------------------------------------------------------------	# 2. Suche ZDF
	ZDF_Search_PATH	 = 'https://zdf-cdn.live.cellular.de/mediathekV2/search?profile=cellular-5&q=%s&page=%s'
	if pagenr == '':		# erster Aufruf muss '' sein
		pagenr = 1
	path_zdf = ZDF_Search_PATH % (quote(query_zdf), pagenr) 	
	path_zdf = transl_umlaute(path_zdf)
	
	query_lable = (query_zdf.replace('%252B', ' ').replace('+', ' ')) 	# quotiertes ersetzen 
	query_lable = unquote(query_lable)
	icon = R(ICON_ZDF_SEARCH)
	xbmcgui.Dialog().notification("ZDF-Suche",query_lable,icon,1000, sound=False)
	page, msg = get_page(path_zdf)										# json.load erst hier				
	
	try:
		jsonObject = json.loads(page)
		searchResult = str(jsonObject["totalResultsCount"])
		nextUrl = str(jsonObject["nextPageUrl"])
		nextPage = str(jsonObject["nextPage"])
	except:
		searchResult=""; nextUrl=""; nextPage=""
	PLog("searchResult: "  + searchResult);
	PLog("nextPage: "  + nextPage);

	query_lable=py2_encode(query_lable); searchResult=py2_encode(searchResult);
	if searchResult == '':												# Sprung hierher
		label = "[B]ZDF[/B] | nichts gefunden zu: %s | neue Suche" % query_lable
		title="Suche in ARD und ZDF"
		title=py2_encode(title);
		fparams="&fparams={'title': '%s'}" % quote(title)
		addDir(li=li, label=label, action="dirList", dirID="resources.lib.ARDnew.SearchARDundZDFnew", 
			fanart=R('suche_ardundzdf.png'), thumb=R('suche_ardundzdf.png'), tagline=tag_negativ, fparams=fparams)
	else:	
		store_recents = True											# Sucheingabe speichern
		title = "[B]ZDF[/B]: %s Video(s)  | %s" % (searchResult, query_lable)
		query_zdf=py2_encode(query_zdf); title=py2_encode(title);
		fparams="&fparams={'query': '%s', 'title': '%s', 'pagenr': '%s'}" % (quote(query_zdf), 
			quote(title), pagenr)
		addDir(li=li, label=title, action="dirList", dirID="ZDF_Search", fanart=R('suche_ardundzdf.png'), 
			thumb=R('suche_ardundzdf.png'), tagline=tag_positiv, fparams=fparams)
					
	#------------------------------------------------------------------	# 3. Suche Merkliste
	PLog("search_merk: " + query_ard)
	my_items, my_ordner = ReadFavourites('Merk')
	if len(my_items) > 0:
		q_org = query_ard.replace('+', ' ')
		q=py2_decode(up_low(q_org))
		selected=""; cnt=0; found=0
		for item in my_items:
			name = stringextract('merk name="', '"', item)
			ordner = stringextract('ordner="', '"', item)
			Plot = stringextract('Plot="', '"', item)
			name=py2_decode(name); Plot=py2_decode(Plot)				# Abgleich Name + Plot
			ordner=py2_decode(ordner)
			if q in up_low(name) or q in up_low(Plot) or q in up_low(ordner):
				selected = 	"%s %s" % (selected,  str(cnt))				# Indices
				found=found+1	
			cnt=cnt+1
		PLog(selected)
			
		if len(selected) == 0:											# Sprung hierher
			label = "[B]Merkliste[/B] | nichts gefunden zu: %s | neue Suche" % q_org
			title="Suche in ARD und ZDF"
			title=py2_encode(title);
			fparams="&fparams={'title': '%s'}" % quote(title)
			addDir(li=li, label=label, action="dirList", dirID="resources.lib.ARDnew.SearchARDundZDFnew", 
				fanart=R('suche_ardundzdf.png'), thumb=R('suche_ardundzdf.png'), tagline=tag_negativ, fparams=fparams)		
		else:
			title = u"[B]Merkliste[/B]: %s Einträge  | %s" % (found, q_org)
			if len(selected) == 1:
				title = u"[B]Merkliste[/B]: %s Eintrag  | %s" % (found, q_org)
			q=py2_encode(q); title=py2_encode(title);
			fparams="&fparams={'mode': 'Merk', 'selected': '%s'}" % selected.strip()
			addDir(li=li, label=title, action="dirList", dirID="ShowFavs", fanart=R('suche_ardundzdf.png'), 
				thumb=R('suche_ardundzdf.png'), tagline=tag_positiv, fparams=fparams)		
	
	
	#-----------------------------------
	# Länge begrenzt auf 24, Änderung angleichen -> tool.SearchWordWork
	if 	store_recents:													# Sucheingabe speichern
		query_recent= RLoad(query_file, abs_path=True)
		query_recent= query_recent.strip().splitlines()
		if len(query_recent) >= 24:										# 1. Eintrag löschen (ältester)
			del query_recent[0]
		query_ard=py2_encode(query_ard)
		if query_ard not in query_recent:								# query_ard + query_zdf ident.
			query_recent.append(query_ard)
			query_recent = "\n".join(query_recent)
			query_recent = py2_encode(query_recent)
			RSave(query_file, query_recent)								# withcodec: code-error
			
	xbmcplugin.endOfDirectory(HANDLE)
	
#---------------------------------------------------------------- 
# Suche in Mediathek
# Statt des api-Calls funktioniert auch https://www.ardmediathek.de/ard/search/%s
# 	(Auswertung anpassen).
# Scrollbeiträge hier leicht abweichend von ARDStartRubrik (s.u. Mehr-Button).
# 22.08.2019 myhash (sha256Hash) und erste pageNumber geändert durch ARD (0, vorher 1)
#	Suche im Web vorangestellt (Webcheck): Check auf Sendungen /Mehrfachbeiträge) - Auswertung 
#		 in ARDStartRubrik, einschl. Scroll-Beiträge 
# Webcheck: abgeschaltet bei SearchARDundZDFnew (nur Einzelbeiträge, wie ZDF-Suche)
# Die Suchfunktion arbeitet nur mit Einzelworten, Zusammensetzung möglich z.B. G7-Gipfel
# 27.06.2020 die Web-Url "www.ardmediathek.de/ard/suche/.." funktioniert nicht mehr -
#	Webcheck entfällt, gesamte Suchfunktion jetzt script-gesteuert. api-Call ebenfalls 
#	geändert - das Zusammensetzen mit extensions + variables entfällt.  
# 26.09.2021 Suche nach Sendungen möglich aber verworfen, da zusätzl. Suche erforderlich
#	 (Suchstring: ../ard/search/grouping?searchString=..) 
# 14.03.2022 nach Sofortstart-Abbruch springt Kodi erneut nach get_keyboard_input - Addon-
#	Absturz bei Abbruch der Eingabe. Abhilfe: return ersetzt durch Aufruf Main_NEW.
# 22.03.2023 api-Suche umgestellt page-gateway/widgets  -> search-system/mediathek, um
#	Videos von Sendereihen zu erfassen (Bsp. "2 für 300")
#
def ARDSearchnew(title, sender, offset=0, query=''):
	PLog('ARDSearchnew:');	
	PLog(title); PLog(sender); PLog(offset); PLog(query);

	if sender == '':								# Sender gewählt?
		CurSender = Dict("load", 'CurSender')		
		sendername, sender, kanal, img, az_sender = CurSender.split(':')
	PLog("sender: " + sender)
	
	if query == '':
		query = get_keyboard_input() 
		if query == None or query.strip() == '': 	# None bei Abbruch
			PLog(query)
			# return								# Absturz nach Sofortstart-Abbruch					
			Main_NEW(NAME)
			
	query = query.strip()
	#query = query.replace(' ', '+')				# für Merkliste - 01.03.2023 nicht mehr relevant 	
	query_org = query	
	query=py2_decode(query)							# decode, falls erf. (1. Aufruf)
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Neu')								# Home-Button
	
	# ----------------------------------------------------- # Suchstring umgestellt, s.o.
	PLog(query)
	path = 'https://api.ardmediathek.de/search-system/mediathek/%s/search/vods?query=%s&pageNumber=%s&pageSize=24' % (sender, query, offset)

	page, msg = get_page(path,JsonPage=True)					
	PLog(len(page))
	if page == '':											
		msg1 = "Fehler in ARDSearchnew, Suche: %s"	% query
		msg2 = msg
		MyDialog(msg1, msg2, '')	
		return li
	
	gridlist = blockextract( '"availableTo"', page) 		# Beiträge?
	if len(gridlist) == 0:				
		msg1 = u'keine Beiträge gefunden zu: %s'  % query
		PLog(msg1)
		MyDialog(msg1, '', '')
		xbmcplugin.endOfDirectory(HANDLE)		
	PLog('gridlist: ' + str(len(gridlist)))	
	
	ID='Search' 	# mark für farbige Markierung
	li = get_json_content(li, page, ID, mark=unquote(query))																	
	
															# Mehr-Button:
	title = "Mehr zu >%s<" % unquote(query)		
	li = xbmcgui.ListItem()									# Kontext-Doppel verhindern
	offset = int(offset) +1
	vodTotal	= stringextract('"totalElements":', '}', page)
	vodPageSize = stringextract('"pageSize":', ',', page)
	pages = float(vodTotal) / float(vodPageSize)
	pages = int(math.ceil(pages))					# aufrunden für Seitenrest

	summ = u"insgesamt: %s Seite(n) , %s Beiträge" % (str(pages), vodTotal) 
	tag = "weiter zu Seite %s" % str(offset+1)				# Basis 0
	PLog("vodTotal %s, vodPageSize %s" % (vodTotal, vodPageSize))
	PLog("offset %s, pages %s" % (str(offset),str(pages)))
	if int(offset) < int(pages):	
		query=py2_encode(query); title=py2_encode(title); 
		fparams="&fparams={'query': '%s', 'title': '%s', 'sender': '%s','offset': '%s'}" %\
			(quote(query), quote(title), quote(sender), str(offset))
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDSearchnew", fanart=R(ICON_MEHR), 
			thumb=R(ICON_MEHR), summary=summ, tagline=tag, fparams=fparams)																	
				
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#---------------------------------------------------------------- 
# ARDVerpasst - Liste Wochentage
# 29.05.2020 Änderung der Webseite durch die ARD. HTML steht nicht mehr
#	zur Verfügung, Ermittlung der timeline-Sender im Web entfällt.
#	Statt dessen forder wir mit dem gewählten Sender die entspr. 
#	json-Seite an. Verarbeitung in ARDVerpasstContent 	
# CurSender neubelegt in Senderwahl
#
def ARDVerpasst(title, CurSender=''):
	PLog('ARDVerpasst:');
	PLog(CurSender)
	
	if CurSender == '' or CurSender == False or CurSender == 'false':	# Ladefehler?
		CurSender = ARDSender[0]
	if ':' in CurSender:				# aktualisieren	
		Dict('store', "CurSender", CurSender)
		PLog('sender: ' + CurSender); 
		CurSender=py2_encode(CurSender);
	sendername, sender, kanal, img, az_sender = CurSender.split(':')
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Neu')								# Home-Button

	wlist = list(range(0,7))
	now = datetime.datetime.now()

	for nr in wlist:
		rdate = now - datetime.timedelta(days = nr)
		startDate = rdate.strftime("%Y-%m-%dT03:30:00.000Z")
		myDate  = rdate.strftime("%d.%m.")		# Formate s. man strftime (3)
		
		rdate2 = now - datetime.timedelta(days = nr-1)
		endDate = rdate2.strftime("%Y-%m-%dT03:29:59.000Z")

		iWeekday = rdate.strftime("%A")
		iWeekday = transl_wtag(iWeekday)
		iWeekday = iWeekday[:2].upper()
		if nr == 0:
			iWeekday = 'HEUTE'	
		if nr == 1:
			iWeekday = 'GESTERN'	
		title =	"%s %s" % (iWeekday, myDate)	# DI 09.04.
		tagline = "Sender: [B]%s[/B]" % sendername	
		
		PLog(title); PLog(startDate); PLog(endDate)
		CurSender=py2_encode(CurSender); 
		fparams="&fparams={'title': '%s', 'startDate': '%s', 'endDate': '%s','CurSender': '%s'}" %\
			(title,  startDate, endDate, quote(CurSender))
		addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.ARDVerpasstContent", fanart=R(ICON_ARD_VERP), 
			thumb=R(ICON_ARD_VERP), fparams=fparams, tagline=tagline)
			
	title 	= u'Wählen Sie Ihren Sender | aktuell: [B]%s[/B]' % sendername	# Senderwahl
	tag = "die Senderwahl ist wirksam in [B]%s[/B], [B]%s[/B] und [B]%s[/B]" % ("ARD Mediathek", "A-Z", "Sendung verpasst")
	title=py2_encode(title); caller='resources.lib.ARDnew.ARDVerpasst'
	fparams="&fparams={'title': '%s', 'caller': '%s'}" % (quote(title), caller)
	addDir(li=li, label=title, action="dirList", dirID="resources.lib.ARDnew.Senderwahl", fanart=R(ICON_MAIN_ARD), 
		thumb=R('tv-regional.png'), tagline=tag, fparams=fparams) 
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)

#---------------------------------------------------------------- 
# ARDVerpasstContent - Inhalt des gewählten Tages
#	Seite html (Uhrzeit, Titel, Link) / json (Blöcke "shortTitle") 
# Ablauf: 	1. Senderliste (Aufruf ohne timeline_sender od. /ard/ im Pfad)
#			2. Einzelsender (Aufruf mit timeline_sender)
# 28.08.2019 timeline_sender nicht mehr auf den Datumsseiten verfügbar,
#	nur noch auf der Einstiegsseite ../ard/program/
# 02.03.2020 wieder leere html-Seite bei Zusatz ?devicetype=pc (nur Heute),
#	geändert in ?devicetype=mobile. Header: vermutl. cache-control
#	entscheident (nicht geklärt).
# 29.05.2020 Änderung der Webseite durch die ARD - s. ARDVerpasst,
#	der 2-fache Durchlauf (Senderliste / Sendungen) entfällt
# 
def ARDVerpasstContent(title, startDate, endDate, CurSender):
	PLog('ARDVerpasstContent:');
	PLog(title);  PLog(startDate); PLog(endDate); PLog(CurSender);
	
	sendername, sender, kanal, img, az_sender = CurSender.split(':')
	PLog(sendername); PLog(sender); 
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Neu')							# Home-Button

	base = "https://page.ardmediathek.de/page-gateway/compilations/ard/pastbroadcasts"
	base = base.replace('/ard/', '/%s/' % sender)
	# 09.01.2022 Anz. 100 kann bei ARD-Alle (ard) fehlschlagen -> 200 
	path = base + "?startDateTime=%s&endDateTime=%s&pageNumber=0&pageSize=200" % (startDate, endDate)
	
	page, msg = get_page(path)
	if page == '':	
		msg1 = 'Fehler in ARDVerpasstContent'
		msg2=msg
		msg3=path
		MyDialog(msg1, msg2, msg3)	
		return li
	PLog(len(page))
									
	gridlist = blockextract( 'broadcastedOn', page) 
	if len(gridlist) == 0:				
		msg1 = u'keine Beiträge gefunden zu:'
		msg2 = '%s | %s'  % (title, sendername)
		PLog("%s | %s" % (msg1, msg2))
		MyDialog(msg1, msg2, '')
		return li
			
	PLog('gridlist: ' + str(len(gridlist)))	
	# dateformat: 2022-05-23T03:30:00.000Z
	# Bereichsangabe (Datum, Uhrzeit) zu lang für notification:
	msg1 = "%s.%s.%s" % (startDate[8:10], startDate[5:7], startDate[0:4])
	msg2 = sendername
	icon = R(ICON_ARD_VERP)
	xbmcgui.Dialog().notification(msg1,msg2,icon,5000, sound=False)
	
	try:
		obs = json.loads(page)
		PLog(len(obs))
	except Exception as exception:
		PLog(str(exception))
	
	for s in obs:										# ARD-Alle: einz. Sender auspacken
		PLog(str(s)[:80])
		page  = json.dumps(s)
		li = get_json_content(li, page, ID='EPG', mark='')																	
	
	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
	
#----------------------------------------------------------------
# convHour z.Z. nicht genutzt
#	string zeit, int offset - Bsp. 15:00, 2
# 	s.a. util.time_translate für ISO8601-Werte
#	21.11.2019 entfallen, ersetzt durch convHour
#		(Format durch ARD geändert)
# convHour - Format zeit: 2:10 PM od. 5:40 AM,
#	ohne Zeitversatz
def convHour(zeit):	
	PLog('convHour: ' + zeit);
	zeit, tz = zeit.split(' ')
	hour, minutes = zeit.split(':')

	if tz.strip() == 'PM':			# Nachmittagszeit
		hour = int(hour) + 12
		hour = str(hour)
		PLog(hour)
		PLog(type(hour));
		if hour == "24":
			hour = "00"	

	zeit = "%02s:%s" % (hour, minutes)
	PLog(zeit)
	return zeit

####################################################################################################
# Senderformat Sendername:Sender (Pfadbestandteil):Kanal:Icon
#	Bsp.: 'ARD-Alle:ard::ard-mediathek.png', Rest s. ARDSender[]
# caller ARDVerpasst, sonst Main_NEW
# 26.09.2021 Settting pref_disable_sender entfernt - "Sender:" in 
#	Titel entfällt.
# 		
def Senderwahl(title, caller=''):	
	PLog('Senderwahl:'); PLog(caller)
	
	li = xbmcgui.ListItem()
	li = home(li, ID='ARD Neu')							# Home-Button
	
	if caller == '':
		caller = "resources.lib.ARDnew.Main_NEW"
	
	for entry in ARDSender:								# entry -> CurSender in Main_ARD
		if 'KiKA' in entry:								# bisher nicht in Base- und AZ-URL enthalten
			continue
		sendername, sender, kanal, img, az_sender = entry.split(':')
		PLog(entry)
		tagline = 'Mediathek des Senders [B] %s [/B]' % sendername
		PLog('sendername: %s, sender: %s, kanal: %s, img: %s, az_sender: %s'	% (sendername, sender, kanal, img, az_sender))
		title = sendername
		entry=py2_encode(entry); 			
		if 'ARDVerpasst' in caller:
			fparams="&fparams={'title': 'Sendung verpasst', 'CurSender': '%s'}" % quote(entry)
		elif 'SendungenAZ' in caller: 
			fparams="&fparams={'title': 'Sendungen A-Z', 'CurSender': '%s'}" % quote(entry)
		else:	
			fparams="&fparams={'name': 'ARD Mediathek', 'CurSender': '%s'}" % quote(entry)
		addDir(li=li, label=title, action="dirList", dirID="%s" % caller, fanart=R(img), thumb=R(img), 
			tagline=tagline, fparams=fparams)

	xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=True)
####################################################################################################






	
		

