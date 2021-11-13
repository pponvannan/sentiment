from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pickle

sent = SentimentIntensityAnalyzer()


pickle_out = open("sent.pkl", "wb")
pickle.dump(sent, pickle_out)
pickle_out.close()
