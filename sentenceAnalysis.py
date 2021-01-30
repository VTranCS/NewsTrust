from textblob import TextBlob

#Checks for words that are incorrectly capitalized - More than the first letter in a word in capitalized
def capitalization(tweet):
    tweet = "".join(x for x in tweet if (x.isalpha() or x==" "))
    print(tweet)
    counter = 0
    for word in tweet.split():
        for x in word:
            if x.isupper(): counter+=1 
    return counter/ (len(tweet)-tweet.count(" "))



#returns the size of the longest sentence in the tweet
def sentenceComplexity(tweet):
    tweet = tweet.replace("!", ".")
    tweet = tweet.replace("?", ".")
    print(tweet)
    tweet = "".join(x for x in tweet if (x.isalpha() or x==" " or x=='.'))
    sentences = tweet.split(".")

    for x in range(len(sentences)): 
        if sentences[x][0] == " ": 
            sentences[x] = sentences[x][1:]

    if len(sentences)==1 and "." not in tweet: return -1
    print(sentences)
    return max([len(x.split(" ")) for x in sentences])

test = ""

#returns the number of words that are considered mispelled - not an English word
def mispells(tweet):
    tweet = tweet.lower()
    counter=0
    blob = TextBlob(tweet)
    words = blob.words
    for x in words:
        if x != x.correct():
            counter+=1
            print(x)
    return counter


print(mispells(test))



