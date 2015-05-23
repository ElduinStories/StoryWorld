#Graph generator experiment 
import json
import copy

#Use JSON storage for relations

#initialize a graph
def initGraph():
	return {}

#Create a Vertex
def createVertex(graph, vid):
	if (vid in graph.keys()):
		#Throw error vertex already exists
		raise ValueError("Vertex already exists")

	graph[vid] = {"inc":[],"con":{}}
	return

def edgeExist(graph, tail, head):
	if (head not in graph.keys()):
		#throw error
		raise ValueError("Head vertex doesn't exists")
	if (tail not in graph.keys()):
		#throw vertex does not exist error
		raise ValueError("Tail vertex doesn't exists")

	if (head in graph[tail]["con"].keys()):
		return True
	else:
		return False

#Create edge from tail to head with attached data
def createEdge(graph, tail, head, data={}):
	if (tail not in graph.keys()):
		#throw error
		raise ValueError("Head vertex doesn't exists")
	if (head not in graph.keys()):
		#throw vertex does not exist error
		raise ValueError("Tail vertex doesn't exists")

	if (edgeExist(graph, tail, head)):
		#edge already exists
		raise ValueError("Edge already exists")

	graph[tail]["con"][head] = data
	if (tail not in graph[head]["inc"]):
		graph[head]["inc"].append(tail)
	return

#Remove an edge
def deleteEdge(graph, tail, head):
	if (not edgeExist(graph, tail, head)):
		#edge doesn't exists
		raise ValueError("Edge doesn't exist")

	graph[head]["inc"].remove(tail)
	del graph[tail]["con"][head]
	return

#Remove all connections to vertex vid and then the vertex itself 
def deleteVertex(graph, vid):
	if (vid not in graph.keys()):
		#throw error
		raise ValueError("Vertex does not exist")
		return

	links = graph[vid]["con"].keys()
	for k in links:
		deleteEdge(graph, vid, k)

	links = copy.copy(graph[vid]["inc"])
	print links
	for k in links:
		print k
		deleteEdge(graph, k, vid)

	del graph[vid]
	return

#Edit Edge Data
def editEdge(graph, tail, head, data={}):
	if (not edgeExist(graph, tail, head)):
		#edge doesn't exists
		raise ValueError("Edge doesn't exist")

	graph[tail]["con"][head] = data
	return

def test():
	#Time for some testing
	print "Begining tests"
	pop = initGraph()
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

	#add some vertices
	print "\n\n\n\nCreate some vertices"
	createVertex(pop,"vone")
	createVertex(pop,"vtwo")
	createVertex(pop,"vthree")
	createVertex(pop,"vfour")
	createVertex(pop,"vfive")
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

	print "\n\n\n\nTesting failure to add vertex that exists"
	try:
		createVertex(pop,"vfive")
	except ValueError:
		print "Successfully Failed"
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

	#Create some edges
	#an impossible one first
	print "\n\n\n\nTesting failure of edge creation"
	try:
		createEdge(pop,"vone","vsix","bob")
	except ValueError:
		print "Successfully Failed"
	try:
		createEdge(pop,"vsix","vone","bob")
	except ValueError:
		print "Successfully Failed"
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

	#now some real ones
	print "\n\n\n\nCreating some real edges"
	createEdge(pop,"vone","vtwo","bob")
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

	createEdge(pop,"vone","vfive",{"cat":"loud"})
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

	#test failure of creating an edge that exists
	print "\n\n\n\nTesting failure to create edge that already exists"
	try:
		createEdge(pop,"vone","vfive",{"cat":"soft"})
	except ValueError:
		print "Successfully Failed"
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

	#A bunch more
	print "\n\n\n\nCreating a bunch of edges"
	createEdge(pop,"vtwo","vone")
	createEdge(pop,"vtwo","vfive")
	createEdge(pop,"vthree","vtwo")
	createEdge(pop,"vthree","vfive")
	createEdge(pop,"vfour","vone")
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

	#editing an edge (that doesn't exist three ways)
	print "\n\n\n\nTesting Fail edge editing"
	try:
		editEdge(pop,"vsix","vone",{"dog":"bob"})
	except ValueError:
		print "Successfully Failed"
	try:
		editEdge(pop,"vone","vsix",{"dog":"bob"})
	except ValueError:
		print "Successfully Failed"
	try:
		editEdge(pop,"vone","vfour",{"dog":"bob"})
	except ValueError:
		print "Successfully Failed"
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

	#Real edge editing
	print "\n\n\n\nTesting Edge editing for real"
	editEdge(pop,"vone","vtwo",{"dog":"bob"})
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

	#Test deleting an edge (no fail testing since same as edit)
	print "\n\n\n\nTesting edge deletion"
	deleteEdge(pop,"vfour","vone")
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

	#Test deleting a vertex (failure testing)
	print "\n\n\n\nTesting fail vertex deleting"
	try:
		deleteVertex(pop,"vsix")
	except ValueError:
		print "Successfully Failed"
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

	#Test deleting a vertex for real
	print "\n\n\n\nTesting vertex deletion (for real)"
	deleteVertex(pop,"vfour")
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

	deleteVertex(pop,"vtwo")
	print json.dumps(pop, indent=4, separators=(',',':'), sort_keys=True)

if __name__ == '__main__':
	test()