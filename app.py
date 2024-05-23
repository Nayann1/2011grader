from flask import Flask, render_template, request
import json
import re
import sys
import powset
import ourfunctions
import proofgen
import random
from proofgen import Variable
from proofgen import Expression
app = Flask(__name__)


global_qtype = None

@app.route('/')
def index():
    return render_template('single.html')

@app.route('/get_animal')
def get_qtype(data):
    try:
        return data.split('?')[1].split('&')[0]
    except IndexError:
        return 'Question type not set'

stored = {}
nextExerciseNr = 0

@app.route('/~sjc/cs30/cs30.cgi', methods=['POST'])
def serve_app():
    global stored, nextExerciseNr
    form_data = request.form
    question = get_qtype(form_data['s'])
    #print(question)
    ex_value = form_data.get('ex')
    q_string = question + '.n'

    with open(q_string, 'r') as file:
        content = file.read()
    if (ex_value):
        json_data = json.loads(ex_value)
        #print(json_data)
        vars,lineno = stored[json_data['exId']]

        roster_value = json_data['cValue']['roster']
        #print(roster_value)
        mydata = {'rPages': [], 'rExercises': [], 'rSplash': {'tag': 'SplashPR', 'contents': {'prOutcome': 'POIncorrect', 'prFeedback': [], 'prTimeToRead': 9}}, 'rSes': '', 'rCurrentPage': None, 'rLogin': None, 'rEcho': None, 'rProgress': None, 'rDone': False}
        def get_response():
            if roster_value != None:
                return roster_value
            else:
                return json_data['cValue']['proof']
        def fb(txt,val):
           
            res2 = ourfunctions.add_to_feedback(txt, val, mydata) 
            return res2
        def respond(bool):
            if bool:
                mydata['rSplash']['contents']['prOutcome'] = 'POCorrect'
            return 
        vars['get_response'] = get_response
        vars['add_to_feedback'] = fb
        vars['get_set'] = ourfunctions.get_set
        vars['get_set2'] = ourfunctions.get_set2
        vars['new_get_set'] = ourfunctions.new_get_set
        vars['new_get_set2'] = ourfunctions.new_get_set2
        vars['respond'] = respond
        vars['check_proof_answer'] = ourfunctions.check_proof_answer
        content = '\n'.join(content.split('\n')[lineno:])
        #print('executing '+str(content))
        exec(content,None,vars)
        return json.dumps(mydata)
    else:
        #curjson = {"rPages":[],"rExercises":[{"eTopic": None,"eQuestion":[],"eActions":[{"tag":"Check"}],"eHidden":[{"tag":"FValueS","fvName":"tag","fvValS":"ExerciseType"},{"tag":"FValue","fvName":"exId","fvVal":0},{"tag":"FValueS","fvName":"exTag","fvValS":"Powset"}],"eBroughtBy":[]}],"rSplash":None,"rSes":"","rCurrentPage":None,"rLogin":None,"rEcho":None,"rProgress":None,"rDone":False}
        curjson = {"rPages":[],"rExercises":[{"eTopic":"Logic: rewriting expressions","eQuestion":[],"eActions":[{"tag":"Check"}],"eHidden":[{"tag":"FValueS","fvName":"tag","fvValS":"ExerciseType"},{"tag":"FValue","fvName":"exId","fvVal":0},{"tag":"FValueS","fvName":"exTag","fvValS":"LogicProofOrder"}],"eBroughtBy":["Tyler","Fei"]}],"rSplash":None,"rSes":"","rCurrentPage":None,"rLogin":None,"rEcho":None,"rProgress":None,"rDone":False}
        
        # {"tag":"FText","contents":"Write the powerset 𝒫"},{"tag":"FText","contents":" in roster notation"},{"tag":"FFieldMath","contents":"roster"}
        vars = {}
        vars['random_unique'] = ourfunctions.random_unique
        vars['gen_sets'] = ourfunctions.gen_sets
        vars['generate_proof'] = proofgen.generate_proof
        vars['stringRule'] = proofgen.stringRule
        vars['vee'] = proofgen.vee
        vars['lnot'] = proofgen.lnot
        vars['wedge'] = proofgen.wedge
        vars['Variable'] = Variable
        vars['Expression'] = Expression
        vars['form_json'] = ourfunctions.form_json
        vars['form_logic_step'] = ourfunctions.form_logic_step
        vars['create_steps'] = ourfunctions.create_steps
        def mj(txt,val):
            #print('mjcalled')
            res = ourfunctions.make_json(txt,val,curjson)
            return res
        
        def aj(js):
            res = ourfunctions.add_to_question(js,curjson)
            
            return res


        def tp(t):
            re = ourfunctions.topic(t, curjson)
            return re

        vars['write_to_exercise'] = mj
        vars['topic'] = tp
        vars['add_to_question'] = aj
        
        try:
            
            exec(content, None, vars)
            #
            # print("HERE")
            
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


    #return  '{"rPages":[{"pId":"Powset","pName":"L1.1 - Powerset operations"},{"pId":"SetOps","pName":"L1.2 - More set operations"},{"pId":"IncExcCardinalities","pName":"L1.3 - Inclusion exclusion principle"},{"pId":"multiplicitiesRelations","pName":"L2.1 - Multiplicities of relations"},{"pId":"LogicWrongStep","pName":"L3.2 - Logic: rewriting expressions (identify wrong steps)"},{"pId":"SetConversion","pName":"? - Conversion to set-builder notation"},{"pId":"ProbBasic","pName":"L11? - Basic Probability"},{"pId":"ProbaCompute","pName":"L14 - Probability : compute expression"},{"pId":"ProbExpect","pName":"L13? - Expected Value"},{"pId":"Cardinality","pName":"L12 - Cardinality of Expression"},{"pId":"GraphsGiveSet","pName":"L17 - Graph basics 1"},{"pId":"ModN","pName":"L25 - Modulo: True or False"},{"pId":"Roster","pName":"Optional - Roster notation"},{"pId":"LogicProofOrder","pName":"L3.2 - Logic: rewriting expressions"},{"pId":"LogicRewriting","pName":"L3.1 - Logic Rewriting"}],"rExercises":[],"rSplash":null,"rSes":"","rCurrentPage":null,"rLogin":"Single user mode","rEcho":null,"rProgress":null,"rDone":false}'
    #return '{"rPages":[],"rExercises":[],"rSplash":{"tag":"SplashPR","contents":{"prOutcome":"POIncorrect","prFeedback":[{"tag":"FText","contents":"In roster notation, "},{"tag":"FText","contents":"the powerset 𝒫"},{"tag":"FMath","contents":"(\\left\\{0,1\\right\\})"},{"tag":"FText","contents":" is "},{"tag":"FMath","contents":"\\left\\{\\left\\{\\right\\}, \\left\\{0\\right\\}, \\left\\{1\\right\\}, \\left\\{0, 1\\right\\}\\right\\}"},{"tag":"FText","contents":"Your answer was "},{"tag":"FMath","contents":""}],"prTimeToRead":9}},"rSes":"","rCurrentPage":null,"rLogin":null,"rEcho":null,"rProgress":null,"rDone":false}'
