# Imports the Google Cloud client library
from google.cloud import language_v1
import math

#returns a tuple containing the normalized direction and magnitude of sentiment
# (out of five using gaussian model)
def sentimentDetection(tweet):
    normMagnitude = 0
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=tweet, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    normDirection = (3.7 / (.3 * math.sqrt(2*math.pi))) * math.e** (-1 * (.5 * (sentiment.score)**2)/.09)
    normMagnitude = (7.5 / (.6 * math.sqrt(2*math.pi))) * math.e** (-1 * (.5 * (sentiment.score)**2)/.36)
    print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))
    print("Normalized Sentiment: {}, {}".format(normDirection, normMagnitude))

foo = ""
sentimentDetection(foo)