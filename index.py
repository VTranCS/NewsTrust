from flask import Flask, render_template, request
import Score
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True)

@app.route('/getTwitterData', methods=["GET"])
def getTwitterData():
    data = request.args.get("twitstat")
    result = Score.process_tweet_url(data)
    return result