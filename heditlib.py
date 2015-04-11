#!/usr/bin/env python
from os import path
from subprocess import call
from validate import *
import sys, tempfile, os, json, shutil, re, hashlib
import json_delta as jd

#=================================================================================================================
#Path Functions
def pathjoin(patharray):
	pathstr = ""
	for e in patharray:
		if (e != ""):
			pathstr = pathstr + "/" + str(e)
	return pathstr

def pathsplit(pathstr):
	patharray = pathstr.split("/")
	while('' in patharray):
		patharray.remove('')
	return patharray

def pathTo(pathstr, obj):
	#Returns the sub object following the path provided
	path = pathsplit(pathstr)	

	temp = obj
	for i in xrange(len(path)):
		if(path[i]!=""):
			if(path[i] not in temp.keys()):
				raise ValueError("Invalid Path Requested")
			temp = temp[path[i]]
	return temp

#The purpose of this function is to clean out any arrays and replace them with numbered dicts
def cleanLists(value):
	if (isinstance(value, dict)):
		#recursive with existing keys
		ret = {}
		keys = value.keys()
		for k in keys:
			ret[k] = cleanLists(value[k])

		return ret

	elif (isinstance(value, list)):
		#recursive with numbered keys
		ret = {}
		k = 0
		for v in value:
			ret[str(k)] = cleanLists(v)
			k = k + 1

		return ret
	else:
		#Normal type just return it
		return value

#Actions/ Events functions
def toActions(diff):
	actions = []
	for d in diff:
		apath = pathjoin(d[0])
		
		#construct action
		action = {}
		action["path"] = apath
		if (len(d)==2):
			#Modify
			action["type"] = "modify"
			action["value"] = cleanLists(d[1])
			try:
				validateValue(action['value'])
			except ValueError:
				raise ValueError("Conversion to Action failed: Value could not be repaired.")
		elif (len(d)==1):
			#Delete
			action["type"] = "delete"
		else:
			raise ValueError("Improper diff")

		actions.append(action)

	return actions

def toDiff(actions):
	diff = []
	for action in actions:
		d = []

		#Purform Action Validation (All in one)
		try:
			validateAction(action)
		except ValueError:
			raise ValueError("Unable to convert to Diff: Invalid Action")

		d.append(pathsplit(action["path"]))

		if (action['type'] == "modify"):
			d.append(action['value'])
			diff.append(d)
		elif (action['type'] == "delete"):
			diff.append(d)

	return diff

def doEvent(event, obj):
	try:
		validateEvent(event)
	except ValueError:
		raise ValueError("Unable to do Event: Invalid Event")

	diff = toDiff(event['actions'])
	jd.patch(obj, diff, True)
	return


# History Managing functions
def initHistory():
	# Constructs a blank history object
	return {'timeline':{},'start':'','end':'','events':{}}

def findSlot(time, history):
	# Find bounding events
	if (history['start']==''):
		return {'prev':'','next':'','time':time,'state':''}
	else:
		prev = ''
		next = history['start']

		while(prev != history['end']):
			if(time<history['timeline'][next]['time']):
				return {'prev':prev,'next':next,'time':time,'state':''}
			prev = next
			next = history['timeline'][next]['next']
		return {'prev':history['end'],'next':'','time':time,'state':''}


def addEvent(event, time, eid, history):
	# This function needs to add an event to the history object. This includes placing the event in the correct time slot.
	# Store the event
	try:
		validateEvent(event)
	except ValueError:
		raise ValueError("Could not add event: Invalid Event Object")

	history['events'][eid] = event

	# Add to timeline
	# Construct the timeline entry
	entry = findSlot(time, history)
	history['timeline'][eid] = entry

	# Adjust other pointers
	if (entry['prev']==''):
		history['start'] = eid
	else:
		history['timeline'][entry['prev']]['next'] = eid
	if (entry['next']==''):
		history['end'] = eid
	else:
		history['timeline'][entry['next']]['prev'] = eid

	return

def main():
	# Test 1: Simple Create
	tobj = {}
	tact = {'type':'create','path':'firstobj','value':'Hello World!'}

	doAction(tact, tobj)

	#print tobj

	rcobj = cleanObj(['firstobj'],tobj)
	#print json.dumps(rcobj, indent=4, separators=(',',':'), sort_keys=True)

	# Test 2: Longer Path starting with /
	tobj = {}
	tact = {'type':'create','path':'/firstobj/firstvalue','value':'Hello World!'}

	doAction(tact, tobj)

	#print tobj


	rcobj = constructObj(['firstobj'],tobj)
	#print json.dumps(rcobj, indent=4, separators=(',',':'), sort_keys=True)

	# Test 3: Create with more complex value
	tobj = {}
	tact = {'type':'create','path':'/firstobj/names','value':{'one':{'firstname':'Tyler','lastname':'Jackson'},'two':{'firstname':'Tyler','lastname':'Buist'}}}

	doAction(tact, tobj)

	#print tobj
	print json.dumps(tobj, indent=4, separators=(',',':'), sort_keys=True)

	rcobj = cleanObj(['firstobj'],tobj)
	print json.dumps(rcobj, indent=4, separators=(',',':'), sort_keys=True)

	#Looks like Create is working correctly

if __name__ == '__main__':
	main()