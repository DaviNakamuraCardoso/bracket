import requests 
import pprint

while True: 
   api_requesting =  requests.get("https://api.battlemetrics.com/servers/3411152?include=player")
   if api_requesting.status_code == 200: 
      # Do something when the bot responds

      print(api_requesting)
      pprint.pprint(api_requesting.json())
   else: 
      time.sleep(5)
      print("We have a problem")
      
      # Do something else when the bot does not respond
