import sys
import requests

try:
	path = sys.argv[1]
except:
	exit("Pass one argument, the path of the web server.")

#confirm the server is running, or quit testing immediately
try:
	r = requests.post(path, json = {'test': 200})
	if r.status_code != 200:
		print("Failure: initial test - server did not return correct response")
	else:
		print("Success: initial test")
except Exception, e:
	print("Failure: initial test - " + str(e))
	exit("Cannot continue testing unless the server is running normally!")

def request_test(test_name, problem_statement, expected_value=False):
	try:
		r = requests.post(path, json={'data': problem_statement})
		if r.status_code != 200:
			print("Failure: " + test_name + " - server returned status " + str(r.status))
		elif expected_value and r.json()['prediction'] != expected_value:
			print("Failure: " + test_name + " - server returned incorrect response")
		else:
			print("Success: " + test_name)
	except Exception, e:
		print("Failure: " + test_name + " - " + str(e))

#test normal cases
request_test("Simple Problem Statement 1",
	("Given an array of tuples, where each tuple contains a student ID and the student's gpa,"
	" return the same array sorted by ascending order of each tuple's gpa."))
request_test("Simple Problem Statement 2",
	("The centroid of a polygon is determined by taking the sum of each vertex's positional "
	"coordinates, and dividing the vector by the number of vertices.  The input for this problem"
	" is an array of tuples, where each tuple represents the cartesian coordinates of a polygon."
	"  You must return the centroid of the polygon"))

#test unusual cases
request_test("Unusual Problem Statement 1",
	("China done done"))
request_test("Unusual Problem Statement 2", "\\\nn      $n        \\\"")
request_test("Unusual Problem Statement 3", "exit()")

#test boundary cases
request_test("Boundary Problem Statement 1", "")
request_test("Boundary Problem Statement 2",
	("sdfhualkbdfjsuhiladfkuhliybjkefhdkulhiykbejrhdfuhliryjahgdbfknulhijbhrdfzkuvjbhdfaaknu"
	"sdbjkhasfdkvygbjfhduvykbjardufhliykbjfhearudihkybjfharudfidyjrudifbhdkyruehilyjruiajhbe"
	"dfsbyjhuygkruhligbkyuhlibjuhrliybrhuykrbykvhervyhbrhkybsryeruhyvdfguhjdfhgusdguhuksgkdd"
	"bghbfgjhfbjhfdjfgvhfdbjfuhjuhwjuhqjwujiefofpofgpofgproifgkflgkgmfnvhbndhfbhdghddsbazxbc"
	"hgfjghruiutyurieowpqwoslaksmxnzbxchvjhgfdhjwierufgyhfdjfughfdjefhdiwopqoskdjhfdjsduhfff"))

# TODO: accuracy cases
