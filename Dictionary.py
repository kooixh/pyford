from .apiconnect import ApiConnect
import json


class Dictionary():

    def __init__(self):
        self.apiconnect = ApiConnect()

    #get the lemmatron of the word, i.e. base word
    def getLemmatron(self,word):
        results = []
        r = self.apiconnect.lemmatronReq(word)
        if r == None:
            print ("No internet connection")
            return results
        if r.status_code == 404:
            return results
        res = json.loads(r.text)


        for i in res["results"]:
            lxentry = i["lexicalEntries"]
            for j in lxentry:
                inf = j["inflectionOf"]
                for k in inf:
                    results.append(str(k["text"]))

        return results

    #Get the definitions of a given word.
    def getDefinitions(self,word):
        results = [] #array to store results

        #find the base form of the word
        w = self.getLemmatron(word)
        if len(w) == 0:
            return results
        r = self.apiconnect.sendRequest(w[0])
        #if word does not exists in dictionary
        if r.status_code == 404:
            return results
        res = json.loads(r.text) #parse request body into dict


        #unwrap the json 
        for i in res["results"]:
            lxentry = i["lexicalEntries"]
            for j in lxentry:
                entries = j["entries"]
                for k in entries:
                    sen = k["senses"]
                    for l in sen:
                        defi = l["definitions"]
                        for m in defi:
                            results.append(str(m))
        return results


    def getSynonyms(self,word):
        w = self.getLemmatron(word)
        if len(w) == 0:
            return []
        r = self.apiconnect.sendRequest(w[0],"synonyms")
        results = []
        if r.status_code == 404:
            return results
        res = json.loads(r.text)

        for i in res["results"]:
            for j in i["lexicalEntries"]:
                for k in j["entries"]:
                    for l in k["senses"]:
                        if "subsenses" in l:
                            for m in l["subsenses"]:
                                if "synonyms" in m:
                                    syns = m["synonyms"]
                                    for n in syns:
                                        results.append(str(n["text"]))
        return results

    def getAntonyms(self,word):
        w = self.getLemmatron(word)
        if len(w) == 0:
            return []
        r = self.apiconnect.sendRequest(w[0],"antonyms")
        results = []
        if r.status_code == 404:
            return results
        res = json.loads(r.text)

        for i in res["results"]:
            for j in i["lexicalEntries"]:
                for k in j["entries"]:
                    for l in k["senses"]:
                        if "antonyms" in l:
                            ants = l["antonyms"]
                            for m in ants:
                                results.append(str(m["text"]))
        return results


    def getDomain(self,word):
        w = self.getLemmatron(word)
        if len(w) == 0:
            return []
        r = self.apiconnect.sendRequest(w[0])
        if r.status_code == 404:
            return []
        res = json.loads(r.text) # parse json
        results = []

        for i in res["results"]:
            for j in i["lexicalEntries"]:
                for k in j["entries"]:
                    for l in k["senses"]:
                        if "domains" in l:
                            for m in l["domains"]:
                                results.append(str(m))

        return results
