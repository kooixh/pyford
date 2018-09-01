import requests
import json

app_id = 'You app id'
app_key = 'Your app key'
language = 'en' #en only

class ApiConnect():

    def lemmatronReq(self,word):
        try:
            lemurl = "https://od-api.oxforddictionaries.com:443/api/v1/inflections/"+language+"/"+word
            return requests.get(lemurl, headers = {'app_id' : app_id, 'app_key' : app_key})
        except(requests.exceptions.ConnectionError):
            return None

    def sendRequest(self,word,type=None):
        try:
            url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/'+language + '/'
            if type != None:
                url += word +'/'+type
            else:
                url += word
            return requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})
        except(requests.exceptions.ConnectionError):
            return None
