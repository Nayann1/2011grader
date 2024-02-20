from flask import Flask, render_template, request
import json
import re
import powset
app = Flask(__name__)


@app.route('/')

def index():
    return render_template('single.html')

@app.route('/~sjc/cs30/cs30.cgi', methods=['POST'])
def serve_app():
    form_data = request.form
    ex_value = form_data.get('ex')
    final_json = powset.calc_powset()
    z = json.loads(final_json)
    print(z)
    if (ex_value):
        new_content = z["rExercises"][0]['eQuestion'][1]['contents']
        pattern = r'\d+'
        numbers = re.findall(pattern, new_content)
        print(numbers)

        temp = '\\left\\{\\left\\{\\right\\}, \\left\\{x\\right\\}, \\left\\{y\\right\\}, \\left\\{x, y\\right\\}\\right\\}'
        for c in temp:
            if c == 'x':
                temp = temp.replace(c, numbers[0])
            if c == 'y':
                temp = temp.replace(c, numbers[1])

        print(temp)        
        json_data = json.loads(ex_value)
        
        roster_value = json_data['cValue']['roster']
        #print(roster_value)
        mydata = {'rPages': [], 'rExercises': [], 'rSplash': {'tag': 'SplashPR', 'contents': {'prOutcome': 'POIncorrect', 'prFeedback': [{'tag': 'FText', 'contents': 'In roster notation, '}, {'tag': 'FText', 'contents': 'the powerset 𝒫'}, {'tag': 'FMath', 'contents': new_content}, {'tag': 'FText', 'contents': ' is  '}, {'tag': 'FMath', 'contents': temp}, {'tag': 'FText', 'contents': 'Your answer was '}, {'tag': 'FMath', 'contents': str(roster_value)}], 'prTimeToRead': 9}}, 'rSes': '', 'rCurrentPage': None, 'rLogin': None, 'rEcho': None, 'rProgress': None, 'rDone': False}
        
        return json.dumps(mydata)
        #print(form_data)
        #print(ex_value)
        #json_data = json.loads(ex_value)
    
    return final_json
    #roster_value = json_data['cValue']['roster']
    #
    #


    #x = '{"rPages":[],"rExercises":[{"eTopic":"Powerset operations","eQuestion":[{"tag":"FText","contents":"Write the powerset 𝒫"},{"tag":"FMath","contents":"(\\\\left\\\\{9,6\\\\right\\\\})"},{"tag":"FText","contents":" in roster notation"},{"tag":"FFieldMath","contents":"roster"}],"eActions":[{"tag":"Check"}],"eHidden":[{"tag":"FValueS","fvName":"tag","fvValS":"ExerciseType"},{"tag":"FValue","fvName":"exId","fvVal":0},{"tag":"FValueS","fvName":"exTag","fvValS":"Powset"}],"eBroughtBy":[]}],"rSplash":null,"rSes":"","rCurrentPage":null,"rLogin":null,"rEcho":null,"rProgress":null,"rDone":false}'


   

    return '{"rPages":[],"rExercises":[{"eTopic":"Powerset operations","eQuestion":[{"tag":"FText","contents":"Write the powerset 𝒫"},{"tag":"FMath","contents":"(\\\\left\\\\{9,6\\\\right\\\\})"},{"tag":"FText","contents":" in roster notation"},{"tag":"FFieldMath","contents":"roster"}],"eActions":[{"tag":"Check"}],"eHidden":[{"tag":"FValueS","fvName":"tag","fvValS":"ExerciseType"},{"tag":"FValue","fvName":"exId","fvVal":0},{"tag":"FValueS","fvName":"exTag","fvValS":"Powset"}],"eBroughtBy":[]}],"rSplash":null,"rSes":"","rCurrentPage":null,"rLogin":null,"rEcho":null,"rProgress":null,"rDone":false}'
    




if __name__ == "__main__":
    app.run(debug=True)


    #return  '{"rPages":[{"pId":"Powset","pName":"L1.1 - Powerset operations"},{"pId":"SetOps","pName":"L1.2 - More set operations"},{"pId":"IncExcCardinalities","pName":"L1.3 - Inclusion exclusion principle"},{"pId":"multiplicitiesRelations","pName":"L2.1 - Multiplicities of relations"},{"pId":"LogicWrongStep","pName":"L3.2 - Logic: rewriting expressions (identify wrong steps)"},{"pId":"SetConversion","pName":"? - Conversion to set-builder notation"},{"pId":"ProbBasic","pName":"L11? - Basic Probability"},{"pId":"ProbaCompute","pName":"L14 - Probability : compute expression"},{"pId":"ProbExpect","pName":"L13? - Expected Value"},{"pId":"Cardinality","pName":"L12 - Cardinality of Expression"},{"pId":"GraphsGiveSet","pName":"L17 - Graph basics 1"},{"pId":"ModN","pName":"L25 - Modulo: True or False"},{"pId":"Roster","pName":"Optional - Roster notation"},{"pId":"LogicProofOrder","pName":"L3.2 - Logic: rewriting expressions"},{"pId":"LogicRewriting","pName":"L3.1 - Logic Rewriting"}],"rExercises":[],"rSplash":null,"rSes":"","rCurrentPage":null,"rLogin":"Single user mode","rEcho":null,"rProgress":null,"rDone":false}'
    #return '{"rPages":[],"rExercises":[],"rSplash":{"tag":"SplashPR","contents":{"prOutcome":"POIncorrect","prFeedback":[{"tag":"FText","contents":"In roster notation, "},{"tag":"FText","contents":"the powerset 𝒫"},{"tag":"FMath","contents":"(\\left\\{0,1\\right\\})"},{"tag":"FText","contents":" is "},{"tag":"FMath","contents":"\\left\\{\\left\\{\\right\\}, \\left\\{0\\right\\}, \\left\\{1\\right\\}, \\left\\{0, 1\\right\\}\\right\\}"},{"tag":"FText","contents":"Your answer was "},{"tag":"FMath","contents":""}],"prTimeToRead":9}},"rSes":"","rCurrentPage":null,"rLogin":null,"rEcho":null,"rProgress":null,"rDone":false}'
