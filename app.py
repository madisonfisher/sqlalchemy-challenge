from flask import Flask, jsonify

#set up
app = Flask(__name__)

#routes
@app.route("/")
def home():
    return (
        f'Welcome to the Hawaii weather API!</br>'
        f'The following routes are available: </br>'
        f'Precipitation Data: /api/v1.0/precipitation</br>'
        f'Station Data: /api/v1.0/stations</br>'
        f'Temperature Observations (TOBS) Data: /api/v1.0/tobs</br>'
        f'Min, Avg, Max Temperature when supplied a start date: /api/v1.0/start_date*</br>'
        f'Min, Avg, Max Temperature when supplied a start and end date: /api/v1.0/start_date/end_date*</br>'
        f'*Supply date as %Y-%m-%d</br>'
    )




#end
if __name__ == "__main__":
    app.run(debug=True)