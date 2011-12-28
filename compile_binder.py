#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import unicodedata
import shutil
from os.path import join, getsize

_PROJECT = 'Gruvan'
_BASEDIR = '../../Documents/Scrivener Exports/'+_PROJECT
_DESTDIR = '../../Dropbox/'+_PROJECT
_OUTLINE = _BASEDIR+'/outline.txt'
_MANUSCRIPTFOLDER = 'Draft'
_OUTFILE = _BASEDIR+'/outline.html'

def htmlencode(string):
	string = string.replace('å','&aring;')
	string = string.replace('ä','&auml;')
	string = string.replace('ö','&ouml;')
	string = string.replace('Å','&Aring;')
	string = string.replace('Ä','&Auml;')
	string = string.replace('Ö','&Ouml;')
	return string

def find_scene(scenename):
	for root, dirs, files  in os.walk(_BASEDIR):
		for file in files:
			nfc = unicodedata.normalize('NFC', unicode(file,'utf-8'))
			if (nfc == scenename):
				return join(root,file);
			

def get_chapter(file):
	dirs = file.split('/');
	dirs.reverse()
	dirs.pop(0)
	dirs.reverse()
	chapter = '';
	adding = False
	for dir in dirs:
		if adding:
			if len(chapter) > 0:
				chapter += '/'
			chapter += dir
			
		if dir == _MANUSCRIPTFOLDER:
			adding = True
	return chapter

def get_filename(file):
	dirs = file.split('/')
	dirs.reverse()
	return _MANUSCRIPTFOLDER+"/"+get_chapter(file)+"/"+dirs.pop(0)
			
def get_metadata(file):	
	mdatafile = open(file.replace('.txt', '_Metadata.txt'), 'r');	
	properties = True
	metadata = {"Chapter":get_chapter(file)}
	metadata['Synopsis'] = '';
	metadata['Filename'] = get_filename(file)
	for line in mdatafile:
		if line.rstrip() == '':
			properties = False
		if (properties):
			key, value = line.split(':', 1)
			metadata[key] = value;
		else:
			metadata['Synopsis'] += htmlencode(line)
	return metadata
	
outline = open(_OUTLINE, 'r')
of = open(_OUTFILE, 'w')

of.write("<html><head><title>"+_PROJECT+" - Manuscript Outline</title></head><body>")
of.write("<table border=\"1\">")
of.write("<tr><th>Kapitel</th><th>Scen</th><th>Synopsis</th><th>POV</th><th>Status</th><th>Storlek</th><th>Modified</th></tr>")
			
for scene in outline:	
	scenename = unicode(scene.rstrip()+".txt", 'utf-8')
	#print "Looking for scene:", scenename
	scene = htmlencode(scene)
	file = find_scene(scenename)
	if (file):
		#print "Found it at:",file
		metadata = get_metadata(file);
		of.write("<tr>")
		of.write("<td>"+metadata['Chapter']+"</td>")
		of.write("<td><a href=\""+metadata['Filename']+"\">"+scene+"</a></td><td>"+metadata['Synopsis']+"</td>")
		of.write("<td>"+metadata['POV']+"</td>")
		of.write("<td>"+metadata['Status']+"</td>")
		of.write("<td>"+str(getsize(file))+"</td>")
		of.write("<td>"+metadata['Modified']+"</td>")
		of.write("</tr>")
of.write("</table></body></html>")
of.close()

if os.path.exists(_DESTDIR):
	shutil.rmtree(_DESTDIR)
os.rename(_BASEDIR, _DESTDIR)