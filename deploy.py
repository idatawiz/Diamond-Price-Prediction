from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy


# Data import and Prediction

def FunctionPredictResult(InputData):
    import pandas as pd
    Num_Inputs=InputData.shape[0]
    
    DataForML=pd.read_pickle('DataForML.pkl')
    InputData=InputData.append(DataForML)
    
    InputData['color'].replace({  'J':1, 
                                  'I':2,
                                  'H':3,
                                  'G':4,
                                  'F':5,
                                  'E':6,
                                  'D':7
                                 }, inplace=True)
    
    InputData['clarity'].replace({'I1':1,
                                  'SI1':2,
                                  'SI2':3,
                                  'VS1':4,
                                  'VS2':5,
                                  'VVS1':6,
                                  'VVS2':7,
                                  'IF':8
                                 }, inplace=True)
    
    
    InputData=pd.get_dummies(InputData)
            
    Predictors=['carat','Length', 'color' , 'clarity']
    
    # Generating the input values to the model
    X=InputData[Predictors].values[0:Num_Inputs]
    
    X=PredictorScalerFit.transform(X)
    
    
    import pickle
    with open('Final_XGB_Model.pkl', 'rb') as fileReadStream:
        PredictionModel=pickle.load(fileReadStream)
        # Don't forget to close the filestream!
        fileReadStream.close()
            
    # Genprice Predictions
    Prediction=PredictionModel.predict(X)
    PredictionResult=pd.DataFrame(Prediction, columns=['Prediction'])
    return(PredictionResult)


# Generate Prediction API function

def FunctionGeneratePrediction(inp_carat, inp_Length, inp_color,inp_clarity):
    SampleInputData=pd.DataFrame(
     data=[[inp_carat, inp_Length, inp_color,inp_clarity]],
     columns=['carat','Length', 'color' , 'clarity'])
    Predictions=FunctionPredictResult(InputData= SampleInputData)
    
    return(Predictions.to_json())


app = Flask(__name__)

@app.route('/my_prediction', methods=["GET"])
def prediction_api():
    try:
        carat_value=float(request.args.get('carat'))
        length_value=float(request.args.get('Length'))
        color_value=request.args.get('Color')
        clarity_value=request.args.get('Clarity')
                       
        prediction_from_api=FunctionGeneratePrediction(inp_carat=carat_value,inp_Length=length_value,inp_color=color_value,
                                                    inp_clarity=clarity_value)

        return (prediction_from_api,color_value)
    
    except Exception as e:
        return('Something is not right!:'+str(e))


import os
if __name__ =="__main__":
    
    app.run(debug=True)