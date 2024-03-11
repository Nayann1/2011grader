import re
import ourfunctions
import json

def calc_powset(bol):
    with open('powset.n', 'r') as file:
        content = file.read()
    curjson = {"rPages":[],"rExercises":[{"eTopic":None,"eQuestion":[],"eActions":[{"tag":"Check"}],"eHidden":[{"tag":"FValueS","fvName":"tag","fvValS":"ExerciseType"},{"tag":"FValue","fvName":"exId","fvVal":0},{"tag":"FValueS","fvName":"exTag","fvValS":"Powset"}],"eBroughtBy":[]}],"rSplash":None,"rSes":"","rCurrentPage":None,"rLogin":None,"rEcho":None,"rProgress":None,"rDone":False}
    # {"tag":"FText","contents":"Write the powerset 𝒫"},{"tag":"FText","contents":" in roster notation"},{"tag":"FFieldMath","contents":"roster"}
    vars = {}
    vars['random_unique'] = ourfunctions.random_unique
    def mj(txt,val):
        newjson = ourfunctions.make_json(txt,val,curjson)
        return newjson
    vars['write_to_exercise'] = mj
    if bol == 1:
        vars['get_response'] = ourfunctions.get_response
    


    exec(content, None, vars)

    print(curjson)
    return curjson
calc_powset(1)

