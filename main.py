from fastapi import FastAPI
from fastapi.params import Body
import requests
################################################
app = FastAPI()
#### to run the code >>>   'https://dexcom-api.herokuapp.com/api/Dexcom_classification' ###
def get_result(student_id,reading, trend):
    
    if ((reading >= 80) and (reading <= 140)):
        return {"Student_id": student_id,"value":reading,"trend":trend,"Classification": 3}
        
        
    elif ((reading < 80) and (trend in ["Flat", "Double up", "Single up", "Forty_five up"])):
        return {"Student_id": student_id,"value":reading,"trend":trend, "Classification": 2,'alert':"yellow"}
        
    elif ((reading < 80) and (trend in ["Double down", "Single down", "Forty_five down"])):
        return {"Student_id": student_id,"value":reading,"trend":trend,"Classification": 1,'alert':"red"}
        
    elif ((reading > 140) and (trend in ["Double up", "Single up", "Forty_five up"])):
        return {"Student_id": student_id,"value":reading,"trend":trend, "Classification": 5,'alert':"red"}
        
    elif ((reading > 140) and (trend in ["Flat", "Double down", "Single down", "Forty_five down"])):
        return {"Student_id": student_id,"value":reading,"trend":trend, "Classification": 4,'alert':"yellow"}
       
        
  
@app.get("/api/Dexcom_classification")
async def root():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    x = requests.get('http://dexcom.invasso.com/api/dexcom/simulation', headers=headers)
    y = x.json()

    trend_name = y['trend']
    reading_value =  y['sensor_treading_value']
    student_id = y['student_id']
    
    ### Special Cases ###
    if (('range' in y) and (reading_value >= int(y['range']['from'])) and (reading_value <= int(y['range']['to']))):
        studentRange = y['range']
        return {"Student_id": student_id,"Student_Range":studentRange,"value":reading_value,"trend":trend_name,"Classification": 3}

    else:
        return get_result(student_id,reading_value, trend_name)
        
        


    
