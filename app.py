from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
def welcome():
    return "<h1>Welcome to home page.</h1>"

@app.route("/about", methods=["GET"])
def about():
    return "Welcome to About Page."

# Variable rule
@app.route('/success/<score>')
def success(score):
    return "The person has passed and score is: "+ score


if __name__ =="__main__":
    app.run(debug=True)