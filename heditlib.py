#!/usr/bin/env python
from os import path
import sys
import os
import json
import shutil
import re
import hashlib

#global hdir = ".hedit"

#def init()
#	global hdir
#	prd = stripEnd(sys.argv[0])
#	cwd = os.getcwd()
#	swd = path.join(cwd,hdir)
#	if(os.path.exists(path.join(cwd,hdir))): #TODO this needs to be improved slightly.
#		print "Already initiated"
#		exit()
#	os.makedirs(swd)
#	os.makedirs(path.join(swd,'templates'))
#	os.makedirs(path.join(swd,'events'))

	#Create Index file
#	shutil.copy(path.join(prd,"defaults/index.json"),swd)

	#Copy Templates
#	shutil.copytree(path.join(prd,"defaults/objs"),path.join(swd,'templates'))

	#Create Standard Info Data
#	shutil.copy(path.join(prd,"defaults/stdinfo.json"),swd)


def validate(value):
	return True

def recursiveFill(base,fill):
	if (isinstance(fill,dict)):
		#do recursive key filling
		for k in fill.keys():
			base['value'][k] = {'value':{},'meta':{'index':len(base['value'])}}#,'context':{}}
			recursiveFill(base['value'][k],fill[k])
	else:
		base['value'] = fill

	return

def cleanPath(path):
	while('' in path):
		path.remove('')
	return path

def constructObj(path, obj):
	#Creates an object that is only the data recursively
	#Scan path for requested portion

	temp = obj
	for i in xrange(len(path)):
		if(path[i]!=""):
			if(path[i] not in temp.keys()):
				#path does not exist
				return {}
			if(i != len(path)-1):
				temp = temp[path[i]]['value']
			else:
				temp = temp[path[i]]

	retobj = {}
	if(isinstance(temp['value'], dict)):
		for k in temp['value'].keys():
			retobj[k] = constructObj([k],temp['value'])
	else:
		retobj = temp['value']

	return retobj



	# This function Checks if the format of value is valid (i.e it must have the key:{'value':value,'context':context}) format

#		-> "create" <path,(context),(value),(template,(set[]))>
#			Creates a field at path with key and sets it to value or pulls from template. New objects are created by passing an empty path.
#			- path : The path to the dict which you want to create a field. If there are intermediary fields missing they will be added automatically
#			- value (optional) : Sets the "value" to supplied argument
#			- meta (optional) : Sets "meta" to supplied argument
#			- context (optional) : Sets "context" to the supplied argument
#			- template (optional) : Copies the template specified by argument into "value"
#				- set[] (optional) : An array of paths rooted at this field (as keys) with values which it sets at those paths
#			** If field already exists -- Throw error

def doCreate(action,obj):
	# Test required format is adhered to
#	print json.dumps(obj, indent=4, separators=(',',':'), sort_keys=True)
	actionkeys = action.keys()
	vf = False
	cf = False
	if('path' not in actionkeys):
		return {'code':400, 'resp':'Improperly formed action'}
	if('value' in actionkeys):
		vf = True
		if not validate(action['value']):
			return {'code':400, 'resp':'Improperly formed value'}
	if('context' in actionkeys):
		cf = True

	path = cleanPath(action['path'].split('/'))	

	temp = obj
	for i in xrange(len(path)):
		if(path[i]!=""):
			if(path[i] not in temp.keys()):
				#This part of the path does not exist. Create it
				temp[path[i]] = {'value':{},'meta':{'index':len(temp)}}#,'context':{}}
			if(i != len(path)-1):
				temp = temp[path[i]]['value']
			else:
				temp = temp[path[i]]

#	print "PATHING"
#	print path
#	print json.dumps(obj, indent=4, separators=(',',':'), sort_keys=True)
#	print json.dumps(temp, indent=4, separators=(',',':'), sort_keys=True)

	# Value Setting
	if(vf):
		recursiveFill(temp,action['value'])
	elif('template' in actionkeys):
		#copy from template
		# Get Templates folder path
		# Read JSON template
		# set 'value' to template (default values are pre-set)
		if('set' in actionkeys):
			#Set values of template
			fillervariableineedtodelete = 1

	# Context Setting
	if(cf):
		#Straight copy.
		temp['context'] = action['context']

	return {'code':200,'resp':'success'}


#		-> "modify" <path, (part, (method)), value>
#			Modifies field object values.
#			- path : The path to the field you wish to edit. The last component is the key of the field.
#			- part (optional) : Selects the component of the field value to edit. Options ("context", "value") Default: "value"
#				- method : Selects method for modification. options ("merge", "replace")
#			- value : The value to set the specified component to.

def doModify(action,obj):
	actionkeys = action.keys()
	vf = False
	mf = False
	if('path' not in actionkeys):
		return {'code':400, 'resp':'Improperly formed action'}
	if('part' in actionkeys):
		vf = True
		if(action['part'] == 'context'):
			vf = False
	if(vf):
		if not validate(action['value']):
			return {'code':400, 'resp':'Improperly formed value'}
	if('method' in actionkeys):
		mf = True
		if(action['method']=='replace'):
			mf = False

	#now dowit
	#traverse path
	path = cleanPath(action['path'].split('/'))
	temp = obj
	for i in xrange(len(path)):
		if(path[i]!=""):
			if(path[i] not in temp.keys()):
				#This part of the path does not exist. Create it
				temp[path[i]] = {'value':{},'meta':{'index':len(temp)}}#,'context':{}}
			if(i != len(path)-1):
				temp = temp[path[i]]['value']
			else:
				temp = temp[path[i]]

	if(vf):
		if(not mf):
			recursiveFill(temp,action['value'])
		else:
			temp['value']={} #clear then fill
			recursiveFill(temp,action['value'])
	else:
		temp['context'] = action['value']


def doDelete(action,obj):
	path = cleanPath(action['path'].split('/'))
	temp = obj
	for i in xrange(len(path)-1):
		if(path[i] not in temp.keys()):
			return {'code':404, 'resp':'Invalid Path'}
		if(path[i]!=""):
			temp = temp[path[i]]['value']
	if(path[-1] not in temp.keys()):
		return {'code':404, 'resp':'Invalid Path'}
	else:
		del temp[path[-1]]
		return {'code':200, 'resp':'Successful Delete'}


def doAction(action, obj):
	#action is a dict passed in
	if(action['type']=='create'):
		#Test if valid
		doCreate(action, obj)

	elif(action['type']=='modify'):
		#Test if valid
		doModify(action, obj)

	elif(action['type']=='delete'):
		#Test if valid
		doDelete(action,obj)
	else:
		return {'code':400, 'resp':'Action not found'}

def doEvent(event, obj):
#	print "Printing event"
#	print json.dumps(event, indent=4, separators=(',',':'), sort_keys=True)
#	print "Doing Event"
	for a in event['actions']:
#		print "doing action"
#		print json.dumps(a, indent=4, separators=(',',':'), sort_keys=True)
		doAction(a, obj)

# History Managing functions
def initHistory():
	# Constructs a blank history object
	return {'timeline':{},'start':'','end':'','events':{}}

def findSlot(time, history):
	# Find the space to place it in
	# This is in a separate function to more easily facilitate more advanced searching later. (Can be merged with function below)
	if (history['start']==''):
		return {'prev':'','next':'','time':time}
	else:
		prev = ''
		next = history['start']

		while(prev != history['end']):
			if(time<history['timeline'][next]['time']):
				return {'prev':prev,'next':next,'time':time}
			prev = next
			next = history['timeline'][next]['next']
		return {'prev':history[end],'next':'','time':time}


def addEvent(event, time, eid, history):
	# This function needs to add an event to the history object. This includes placing the event in the correct time slot.
	# Store the event
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


#testing

#Actions[]: {}
#	type:
#		-> "create" <path,key,(meta),(context),(value),(template,(set[]))>
#			Creates a field at path with key and sets it to value or pulls from template. New objects are created by passing an empty path.
#			- path : The path to the dict which you want to create a field. If there are intermediary fields missing they will be added automatically
#			- key : The key of the field you are creating.
#			- value (optional) : Sets the "value" to supplied argument
#			- meta (optional) : Sets "meta" to supplied argument
#			- context (optional) : Sets "context" to the supplied argument
#			- template (optional) : Copies the template specified by argument into "value"
#				- set[] (optional) : An array of paths rooted at this field (as keys) with values which it sets at those paths
#			** If field already exists -- Throw error
#
#		-> "modify" <path, (part, (method)), value>
#			Modifies field object values.
#			- path : The path to the field you wish to edit. The last component is the key of the field.
#			- part (optional) : Selects the component of the field value to edit. Options ("meta", "context", "value") Default: "value"
#				- method : Selects method for modification. options ("merge", "append", "overwrite")
#			- value : The value to set the specified component to.
#
#		-> "rm-field" <path>
#			Removes a field specified by path and all subfields. This can be used to remove anything from entries in a list to whole objects. Note care should be taken as this could break references.


def main():
	# Test 1: Simple Create
	tobj = {}
	tact = {'type':'create','path':'firstobj','value':'Hello World!'}

	doAction(tact, tobj)

	#print tobj

	rcobj = constructObj(['firstobj'],tobj)
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

	rcobj = constructObj(['firstobj'],tobj)
	print json.dumps(rcobj, indent=4, separators=(',',':'), sort_keys=True)

	#Looks like Create is working correctly

if __name__ == '__main__':
	main()