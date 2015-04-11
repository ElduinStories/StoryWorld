#!/usr/bin/python
import sys, tempfile, os, json
import json_delta as jd
from subprocess import call

#join all the elements (convert ints in path to strings)
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

def validate(value):
	return true

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
		actionkeys = action.keys()
		if('path' not in actionkeys):
			raise ValueError("Improperly formed action: Missing \'path\' argument")
		if('type' not in actionkeys):
			raise ValueError("Improperly formed action: Missing \'type\' argument")

		d.append(pathsplit(action["path"]))

		if (action['type'] == "modify"):
			if('value' not in actionkeys):
				raise ValueError("Improperly formed action: Missing \'value\' argument")
			d.append(action['value'])
			diff.append(d)
		elif (action['type'] == "delete"):
			diff.append(d)
		else:
			raise ValueError("Improper action: Unsupported action type")

	return diff


EDITOR = os.environ.get('EDITOR','vim')

fname = sys.argv[1]
with open(fname,'r') as fin:
	jin = json.load(fin)
	#now we have it create a temp file write the json there and open it in vim

	with tempfile.NamedTemporaryFile(suffix=".tmp") as tempfile:
		json.dump(jin, tempfile, indent=4, separators=(',',':'), sort_keys=True)
		tempfile.flush()
		call([EDITOR, tempfile.name])
		tempfile.seek(0)
		jnew = json.load(tempfile)

print json.dumps(jin, indent=4, separators=(',',':'), sort_keys=True)
print json.dumps(jnew, indent=4, separators=(',',':'), sort_keys=True)

diff = jd.diff(jin, jnew)

print json.dumps(diff, indent=4, separators=(',',':'), sort_keys=True)

jout = jd.patch(jin, diff, False)
jd.patch(jin, diff, True)

#print json.dumps(jin, indent=4, separators=(',',':'), sort_keys=True)
#print json.dumps(jout, indent=4, separators=(',',':'), sort_keys=True)

actions = toActions(diff)
diff2 = toDiff(actions)

print json.dumps(actions, indent=4, separators=(',',':'), sort_keys=True)
#print json.dumps(diff2, indent=4, separators=(',',':'), sort_keys=True)

if (diff == diff2):
	print "Diffs match!"

#diff3 = jd.diff(jin, [])
#print json.dumps(diff3, indent=4, separators=(',',':'), sort_keys=True)
#ac = toActions(diff3)
#print json.dumps(ac, indent=4, separators=(',',':'), sort_keys=True)

