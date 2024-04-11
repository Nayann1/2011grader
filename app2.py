from flask import Flask, render_template, request
import json
import re
import sys
import powset

import ourfunctions
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('single.html')

stored = {}
nextExerciseNr = 0

@app.route('/~sjc/cs30/cs30.cgi', methods=['POST'])
def serve_app():
    
    global stored, nextExerciseNr
    form_data = request.form
    ex_value = form_data.get('ex')
    
    with open('moreset.n', 'r') as file:
        content = file.read()
    if (ex_value):
        json_data = json.loads(ex_value)
        vars,lineno = stored[json_data['exId']]
        #print('stored data:'+str(stored[0][0]))
        # new_content = final_json["rExercises"][0]['eQuestion'][1]['contents']
        # print(new_content)
        # pattern = r'\d+'
        # numbers = re.findall(pattern, new_content)
        

        


        #{"cAction":{"tag":"Check"},"tag":"ExerciseType","exId":0,"exTag":"Powset","cValue":{"roster":"99"}}
        roster_value = json_data['cValue']['roster']
        #print(roster_value)
        mydata = {'rPages': [], 'rExercises': [], 'rSplash': {'tag': 'SplashPR', 'contents': {'prOutcome': 'POIncorrect', 'prFeedback': [], 'prTimeToRead': 9}}, 'rSes': '', 'rCurrentPage': None, 'rLogin': None, 'rEcho': None, 'rProgress': None, 'rDone': False}
        def get_response():
            return roster_value
        def fb(txt,val):
           
            res2 = ourfunctions.add_to_feedback(txt, val, mydata) 
            return res2
        def respond(bool):
            if bool:
                mydata['rSplash']['contents']['prOutcome'] = 'POCorrect'
            return
        vars['get_response'] = get_response
        vars['add_to_feedback'] = fb
        vars['new_get_set'] = ourfunctions.new_get_set
        vars['new_get_set2'] = ourfunctions.new_get_set2
        vars['respond'] = respond
        content = '\n'.join(content.split('\n')[lineno:])
        #print('executing '+str(content))
        exec(content,None,vars)
        return json.dumps(mydata)
    else:
        curjson = {"rPages":[],"rExercises":[{"eTopic": None,"eQuestion":[],"eActions":[{"tag":"Check"}],"eHidden":[{"tag":"FValueS","fvName":"tag","fvValS":"ExerciseType"},{"tag":"FValue","fvName":"exId","fvVal":0},{"tag":"FValueS","fvName":"exTag","fvValS":"Powset"}],"eBroughtBy":[]}],"rSplash":None,"rSes":"","rCurrentPage":None,"rLogin":None,"rEcho":None,"rProgress":None,"rDone":False}
        # {"tag":"FText","contents":"Write the powerset 𝒫"},{"tag":"FText","contents":" in roster notation"},{"tag":"FFieldMath","contents":"roster"}
        vars = {}
        # vars['random_unique'] = ourfunctions.random_unique
        # vars['create_answer'] = ourfunctions.create_answer
        vars['gen_sets'] = ourfunctions.gen_sets
        def mj(txt,val):
            #print('mjcalled')
            res = ourfunctions.make_json(txt,val,curjson)
            return res
        
        def tp(t):
            re = ourfunctions.topic(t, curjson)
            return re

        vars['write_to_exercise'] = mj
        vars['topic'] = tp
        try:
            exec(content, None, vars)
        except NameError as e:
             exc_type, exc_value, exc_traceback = sys.exc_info()
             line = exc_traceback.tb_next.tb_lineno-1
             #print(f'line no {line}')
        curjson["rExercises"][0]['eHidden'] += [{'tag': 'FValue', 'fvName': 'exId', 'fvVal': nextExerciseNr}]
        
        stored[nextExerciseNr] = (vars, line)
        nextExerciseNr += 1
        newjson=curjson
       
    return json.dumps(newjson)
    #roster_value = json_data['cValue']['roster']
    #
    #


    #x = '{"rPages":[],"rExercises":[{"eTopic":"Powerset operations","eQuestion":[{"tag":"FText","contents":"Write the powerset 𝒫"},{"tag":"FMath","contents":"(\\\\left\\\\{9,6\\\\right\\\\})"},{"tag":"FText","contents":" in roster notation"},{"tag":"FFieldMath","contents":"roster"}],"eActions":[{"tag":"Check"}],"eHidden":[{"tag":"FValueS","fvName":"tag","fvValS":"ExerciseType"},{"tag":"FValue","fvName":"exId","fvVal":0},{"tag":"FValueS","fvName":"exTag","fvValS":"Powset"}],"eBroughtBy":[]}],"rSplash":null,"rSes":"","rCurrentPage":null,"rLogin":null,"rEcho":null,"rProgress":null,"rDone":false}'


   

    return '{"rPages":[],"rExercises":[{"eTopic":"Powerset operations","eQuestion":[{"tag":"FText","contents":"Write the powerset 𝒫"},{"tag":"FMath","contents":"(\\\\left\\\\{9,6\\\\right\\\\})"},{"tag":"FText","contents":" in roster notation"},{"tag":"FFieldMath","contents":"roster"}],"eActions":[{"tag":"Check"}],"eHidden":[{"tag":"FValueS","fvName":"tag","fvValS":"ExerciseType"},{"tag":"FValue","fvName":"exId","fvVal":0},{"tag":"FValueS","fvName":"exTag","fvValS":"Powset"}],"eBroughtBy":[]}],"rSplash":null,"rSes":"","rCurrentPage":null,"rLogin":null,"rEcho":null,"rProgress":null,"rDone":false}'
    




if __name__ == "__main__":
    app.run(debug=True)

