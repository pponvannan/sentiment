# 1. Library imports
import uvicorn
import regex
from fastapi import FastAPI
from sanr import San
import pickle

# 2. Create the app object
app = FastAPI()
pickle_in = open("sent.pkl", "rb")
sdn = pickle.load(pickle_in)


# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello, World'}


# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {'Welcome To ML model': f'{name}'}


@app.post('/sentiment')
def predict_output(data1: San):
    data1 = data1.dict()
    description = data1['description']
    ticket_id = data1['ticket_id']
    prediction = sdn.polarity_scores(description)
    pred_pos = prediction['pos']
    pred_neg = prediction['neg']
    pred_neu = prediction['neu']
    pred_comp = prediction['compound']

    if prediction['compound'] > 0.05:
        pred_sentiment_status = 'positive'
    elif prediction['compound'] < -0.5:
        pred_sentiment_status = 'negative'
    elif prediction['compound'] >= -0.05 and prediction['compound'] < 0.05:
        pred_sentiment_status = 'neutral'

    import mysql.connector

    # establishing the connection
    conn = mysql.connector.connect(
        user='root', password='Anna@1974', host='localhost', database='sentdb')

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    sql = "INSERT INTO snt (ticket_id, pred_sentiment_status, pred_pos, pred_neg, pred_neu, pred_comp) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (ticket_id, pred_sentiment_status, pred_pos, pred_neg, pred_neu, pred_comp)
    cursor.execute(sql, val)

    conn.commit()

    print(cursor.rowcount, "record inserted.")

    return {"TicketID": ticket_id}, prediction, {"SentimentStatus": pred_sentiment_status}, {"Positive score": pred_pos}, {"Negative score": pred_neg},{"Neutral score": pred_neu}, {"Compound score": pred_comp}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

