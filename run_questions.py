from flask import Flask, render_template, request, jsonify, redirect
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

def get_qtype(data):
    try:
        return data.split('?')[1].split('&')[0]
    except IndexError:
        return data

stored = {}
nextExerciseNr = 0
total_score = 0



@app.route('/~sjc/cs30/cs30.cgi', methods=['POST'])
def serve_app():
    global stored, nextExerciseNr, total_score
    form_data = request.form
    question = get_qtype(form_data['s'])
    ex_value = form_data.get('ex')
    q_string = question + '.n'
    file_path = r'n_files'

    if q_string == '.n':
        result = ourfunctions.get_files(file_path)
        return result
    
    with open(f"{file_path}\\{q_string}", 'r') as file:
        content = file.read()
    if (ex_value):
        json_data = json.loads(ex_value)
        vars,lineno = stored[json_data['exId']]

        mydata = {'rPages': [], 'rExercises': [], 'rSplash': {'tag': 'SplashPR', 'contents': {'prOutcome': 'POIncorrect', 'prFeedback': [], 'prTimeToRead': 9}}, 'rSes': '', 'rCurrentPage': None, 'rLogin': None, 'rEcho': None, 'rProgress': None, 'rDone': False}
        def get_response():
            try:
                return json_data['cValue']['roster']
            except:
                return json_data['cValue']['proof']
        def get_total_score():
            return total_score
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
        vars['get_acc_tim'] = ourfunctions.get_acc_tim
        vars['get_prop'] = ourfunctions.get_prop
        vars['fraction_to_decimal'] = ourfunctions.fraction_to_decimal
        vars['respond'] = respond
        vars['check_proof_answer'] = ourfunctions.check_proof_answer
        vars['get_correct_proof'] = ourfunctions.get_correct_proof
        vars['get_total_score'] = get_total_score
        content = '\n'.join(content.split('\n')[lineno:])

        exec(content,None,vars)
        if mydata['rSplash']['contents']['prOutcome'] == 'POCorrect':
            total_score += 1
        return json.dumps(mydata)
    else:
        curjson = {"rPages":[],"rExercises":[{"eTopic":"Logic: rewriting expressions","eQuestion":[],"eActions":[{"tag":"Check"}],"eHidden":[{"tag":"FValueS","fvName":"tag","fvValS":"ExerciseType"},{"tag":"FValue","fvName":"exId","fvVal":0},{"tag":"FValueS","fvName":"exTag","fvValS":"LogicProofOrder"}],"eBroughtBy":["Tyler","Fei"]}],"rSplash":None,"rSes":"","rCurrentPage":None,"rLogin":None,"rEcho":question,"rProgress":None,"rDone":False}
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
            
        except NameError as e:
             exc_type, exc_value, exc_traceback = sys.exc_info()
             line = exc_traceback.tb_next.tb_lineno-1

        curjson["rExercises"][0]['eHidden'] += [{'tag': 'FValue', 'fvName': 'exId', 'fvVal': nextExerciseNr}]
        
        stored[nextExerciseNr] = (vars, line)
        nextExerciseNr += 1
        newjson=curjson
        
       
    return json.dumps(newjson)

if __name__ == "__main__":
    app.run(debug=True)

