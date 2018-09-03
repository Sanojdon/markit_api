import requests
import json

class LiveData:
	def __init__(self):
		self.api = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="
		self.daily = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
		
	def live_chart(self, sym):
		result = self.daily + sym + "&interval=10min&apikey=W5L233YW2OUU1N86"
		try:
			r = requests.get(result)
			data = json.loads(r.text)
			return (data)
		except:
			print("Connection Error!!")

