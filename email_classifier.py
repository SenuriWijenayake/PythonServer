import nltk
from nltk import bigrams
from nltk import trigrams
from googlegeocoder import GoogleGeocoder
geocoder = GoogleGeocoder()
import string
from itertools import chain
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier as nbc
from nltk.corpus import CategorizedPlaintextCorpusReader
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
import re

def classify_emails():
    stop_words = set(stopwords.words("english"))

    lemmatizer = WordNetLemmatizer()

    mydir = '/home/ubuntu/nltk_data/corpora/gmail'

    all_words = []
    filtered_words = []
    removedPuncuations_words = []
    lematized_words = []
    test_filter = []

    mr = CategorizedPlaintextCorpusReader(mydir, r'(?!\.).*\.txt', cat_pattern=r'(hotel|flight|other)/.*', encoding='latin-1')
    stop = stopwords.words('english')
    documents = [([w for w in mr.words(i) if w.lower() not in stop and w.lower() not in string.punctuation], i.split('/')[0]) for i in mr.fileids()]

    word_features = FreqDist(chain(*[i for i,j in documents]))
    word_features = word_features.keys()[:100]

    def word_feats(document):
        words = set(document)
        features = {}
        for w in word_features:
            features[w] = (w in words)

        return dict(features)

    negids = mr.fileids('hotel')
    posids = mr.fileids('flight')
    neutralids = mr.fileids('other')

    negfeats = [(word_feats(mr.words(fileids=[f])), 'hotel') for f in negids]
    posfeats = [(word_feats(mr.words(fileids=[f])), 'flight') for f in posids]
    neutralfeats = [(word_feats(mr.words(fileids=[f])), 'other') for f in neutralids]

    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4
    neutralcutoff = len(neutralfeats)*3/4

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff] + neutralfeats[:neutralcutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:] + neutralfeats[neutralcutoff:]

    classifier = nltk.NaiveBayesClassifier.train(trainfeats)
    print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testfeats))*100)

    print ('accuracy:', nltk.classify.util.accuracy(classifier, testfeats)*100)


    file_content = open("/home/ubuntu/nltk_data/corpora/gmail/hotel/h12.txt").read()
    tokens = nltk.word_tokenize(file_content)

    test_sent_features = {word.lower(): (word in tokens) for word in mr.words()}

    file_content = open("/home/ubuntu/nltk_data/corpora/gmail/hotel/h12.txt").read()
    tokens = nltk.word_tokenize(file_content)
    tri_tokens = trigrams(tokens)

    cities = []
    matchedIndex = []
    tokenized = []
    addresses = []
    district = ['Akarawita','Angamuwa','Avissawella','Batawala','Battaramulla','Batugampola','Bope','Boralesgamuwa','Borella','Dedigamuwa','Dehiwala','Deltara','Habarakada','Handapangoda','Hanwella','Hewainna','Hiripitya','Hokandara','Homagama','Horagala','Kaduwela','Kahawala','Kalatuwawa','Madapatha','Maharagama','Malabe','Meegoda','Padukka','Pannipitiya','Piliyandala','Pitipana','Homagama','Polgasowita','Puwakpitiya','Ranala','Siddamulla','Slave Island','Sri Jayawardenapura','Talawatugoda','Tummodara','Waga','Watareka','Dickwella']

    for i in tokens:
        tokenized.append(i)

    pattern = re.compile("\d+")
    for i in tokenized:
        if pattern.match(i):
            matchedIndex.append(tokenized.index(i))
            print ("match"+i)
            print (tokenized.index(i))

        else:
            print ("not match")

    for t in tokenized:
        for i in district:
            if t.lower()==i.lower():
                cities.append(tokenized.index(t))

    distance= 200
    start = 0
    end = 0

    for t in cities:
        for i in matchedIndex:
            dis = t-i;
            if (dis<=distance and dis>0):
                distance=dis
                start=t
                end=i
            else:
                print ("higher")

    address = ""

    for token in range(end,start+1):
        address+=tokenized[(token)]
        print (address)
        addresses.append(address)

    for address in addresses:
        try:
            search = geocoder.get(address)
        except ValueError:
            continue
        first_result = search[0]

    output =  [first_result.geometry.location.lat,first_result.geometry.location.lng]


    stri = ','.join(map(str, output))
    return stri
