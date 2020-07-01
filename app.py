from flask import Flask, request, url_for, render_template
import pickle
import numpy as np
import json

app = Flask(__name__)


__City = None
__data_columns = None
model = pickle.load(open("Crop_model.pickle","rb"))

def get_estimated_price(input_json):
    try:
        loc_index = __data_columns.index(input_json['City'].lower())
    except:
        loc_index = -1
    x = np.zeros(27)
    x[0] = input_json['avgTemp']
    x[1] = input_json['Rainfall']
    if loc_index>=0:
        x[loc_index] = 1
    result = abs(int(model.predict([x])[0]))
    return result




def get_location_names():
    return __City

def load_saved_artifacts():
    print("Loading the saved artifacts...start !")
    global __data_columns
    global __City
    global model

    with open("columns.json") as f:
        __data_columns = json.loads(f.read())["data_columns"]
        __City = __data_columns[2:]

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predict_home_price', methods=["POST" ,"GET"])
def predict_home_price():
    
    if request.method == 'POST':
        input_json = {
            "City" : request.form['City'],
            "avgTemp" : float(request.form['avgTemp']),
            "Rainfall" : float(request.form['Rainfall'])
        }
        result = get_estimated_price(input_json)
        if result == 1:
            result = "Arhar/Tur"
        elif result == 2:
            result = "Bajra"
        elif result == 3:
            result= "Dry chillies"
        elif result == 4:
            result = "Groundnut"
        elif result == 5:  
            result ="Jowar"
        elif result == 6:
            result="Moong Green-Gram"
        elif result == 7:
            result ="Moth"
        elif  result==8:
            result ="Other-Kharif-pulses"
        elif result == 9:
            result ="Urad"
        elif result == 10:
            result ="Banana"
        elif  result ==11:
            result ="Castor-seed"
        elif  result == 12:
            result ="Cotton-lint"
        elif result == 13:
            result="Maize"
        elif result ==14:
            result ="Potato"
        elif  result == 15:
            result = "Rice"
        elif result  == 16:
            result ="Sesamum"
        elif result ==17:
            result ="Sugarcane"
        elif   result == 18:
            result ="Pulses-total"
        elif  result == 19:
            result="Rice"
        elif   result == 20:
            result ="Sesamum"
        elif  result == 21:
            result ="Sugarcane"
        elif  result == 22:
            result ="Other-Cereals-Millets"
        elif  result == 23:
            result ="Guar-seed"
        elif result == 24:
            result ="Onion"
        elif result == 25:
            result ="Garlic"
        else:
            result ="wheat"

    return render_template('pi.html', re=result)



if __name__ == "__main__":
    print("Starting Python Flask Server")
    load_saved_artifacts()
    app.run(debug=True)
