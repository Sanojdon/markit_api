import requests
import json

class Markit:
	def __init__(self):
		self.lookup_url = "http://dev.markitondemand.com/Api/v2/Lookup/json"
		self.quote_url = "http://dev.markitondemand.com/Api/v2/Quote/json"

	def company_search(self,string):
		result = self.lookup_url + "?input=" + string
		try:
			r = requests.get(result)
			data = json.loads(r.text)
			return (data)
		except:
			print("Connection Failure!!")
		
		
	def get_quote(self,string):
		result = self.quote_url + "?symbol=" + string
		try:
			r = requests.get(result)
			data = json.loads(r.text)
			return (data)
		except:
			print("Connection Error!!")

