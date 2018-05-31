# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
import requests
import re
import string

app_id = '1ff626b7'
app_key = '20c9a88fc9b180f103a992a63a66c0c3'

language = 'en'
word_id = 'calm'

url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower() + '/synonyms'

r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

#print("code {}\n".format(r.status_code))
#print("text \n" + r.text)
#print("json \n" + json.dumps(r.json()))

synonyms = []

full_synonyms = ""
for result in r.json()["results"]:
    for lexentry in result["lexicalEntries"]:
        for entry in lexentry["entries"]:
            for sense in entry["senses"]:
                for synonym in sense["synonyms"]:
                    #print synonym["text"]
                    synonym_text = str(synonym["text"])
                    full_synonyms += synonym_text + " "
                    synonyms.append(synonym_text.replace("'", ''))

print full_synonyms