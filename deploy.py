from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy


app = Flask(__name__)

@app.route('/my_prediction', methods=["GET"])
def prediction_api():
    try:
        carat_value=float(request.args.get('carat'))
        length_value=float(request.args.get('Length'))
        color_value=request.args.get('Color')
        clarity_value=request.args.get('Clarity')
                       
        prediction_from_api=FunctionGeneratePrediction(
                                                    inp_carat=carat_value, 
                                                    inp_Length=length_value, 
                                                    inp_color=color_value,
                                                    inp_clarity=clarity_value                                                     inp_carat=carat_value, 

                                                        )

        return (prediction_from_api,color_value)
    
    except Exception as e:
        return('Something is not right!:'+str(e))


import os
if __name__ =="__main__":
    
    app.run(host='127.0.0.1', port=8080, threaded=True, debug=True, use_reloader=False)