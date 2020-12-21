import urequests

def run_code():

	url = response = urequests.get('http://jsonplaceholder.typicode.com/albums/1')

	print(response.text)

