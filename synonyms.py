# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
import requests

def find_synonyms(word_id):
    app_id = '1ff626b7'
    app_key = '20c9a88fc9b180f103a992a63a66c0c3'

    language = 'en'
    #word_id = 'calm'

    #for each word in string find synonyms
    full_synonyms = ""
    word_id = word_id.lower()
    list_of_words = word_id.split()
    print list_of_words
    for word in list_of_words:
        print "word: " + word
        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word + '/synonyms'

        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

        synonyms = []
        try:
            for result in r.json()["results"]:
                for lexentry in result["lexicalEntries"]:
                    for entry in lexentry["entries"]:
                        for sense in entry["senses"]:
                            for synonym in sense["synonyms"]:
                                #print synonym["text"]
                                synonym_text = str(synonym["text"])
                                #take synonyms with one word
                                if " " in synonym_text:
                                    continue
                                full_synonyms += synonym_text + " "
                                synonyms.append(synonym_text.replace("'", ''))
        except ValueError:
            continue

    #print full_synonyms
    return full_synonyms