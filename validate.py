#Validation Functions
def validateTime(time):
	if(not isinstance(time, dict)):
		raise ValueError("Invalid  : Not a dict!")
	tkeys = time.keys()
	if('system' not in tkeys):
		raise ValueError("Invalid Time-Object: Missing \'system\' field")
	if('date' not in tkeys):
		raise ValueError("Invalid Time-Object: Missing \'date\' field")
	return

def validateValue(value):
	if (isinstance(value, dict)):
		#recursive with existing keys
		ret = {}
		keys = value.keys()
		for k in keys:
			ret[k] = validateValue(value[k])
		return

	elif (isinstance(value, list)):
		raise ValueError("Invalid Value: Values cannot have lists!")
	else:
		#Normal type just return it
		return

def validateAction(action):
	if(not isinstance(action, dict)):
		raise ValueError("Invalid Action: Not a dict!")
	akeys = action.keys()
	if ('type' not in akeys):
		raise ValueError("Invalid Action: Missing \'type\' field")
	if ('path' not in akeys):
		raise ValueError("Invalid Action: Missing \'path\' field")

	if (action['type']=="modify"):
		if ('value' not in akeys):
			raise ValueError("Invalid Action: Missing \'value\' for modify action")
		else:
			try:
				validateValue(action['value'])
			except ValueError:
				raise ValueError("Invalid Action: Improperly formed value!")
	elif (action['type']=="delete"):
		pass
	else:
		raise ValueError("Invalid Action: Unsupported action type!")

	return

def validateEvent(event):
	if(not isinstance(event, dict)):
		raise ValueError("Invalid Event: Not a dict!")
	ekeys = event.keys()
	if ('time' not in ekeys):
		raise ValueError("Invalid Event: Missing \'time\' field")
	if ('desc' not in ekeys):
		raise ValueError("Invalid Event: Missing \'desc\' field")
	if ('actions' not in ekeys):
		raise ValueError("Invalid Event: Missing \'actions\' array")

	if (not isinstance(event['actions'], list)):
		raise ValueError("Invalid Event: Actions field is not a list!")

	try:
		validateTime(event['time'])
	except ValueError:
		raise ValueError("Invalid Event: Improperly formed time object")

	for a in event['actions']:
		try:
			validateAction(a)
		except ValueError:
			raise ValueError("Invalid Event: Improperly formed action")

	return

def validateStory(story):
	if(not isinstance(story, dict)):
		raise ValueError("Invalid Story: Not a dict!")
	skeys = story.keys()
	if ('summary' not in skeys):
		raise ValueError("Invalid Story: Missing \'summary\' field")
	if ('events' not in skeys):
		raise ValueError("Invalid Story: Missing \'events\' list")

	if (not isinstance(story['events'], list)):
		raise ValueError("Invalid Story: Events field is not a list!")

	for e in story['events']:
		try:
			validateEvent(e)
		except ValueError:
			raise ValueError("Invalid Story: Improperly formed event")
	return

def 