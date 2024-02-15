import re
import ourfunctions
import json

def calc_powset():
    with open('powset.n', 'r') as file:
        content = file.read()
    c = '{"rPages":[],"rExercises":[{"eTopic":"Powerset operations","eQuestion":[{"tag":"FText","contents":"Write the powerset 𝒫"},{"tag":"FText","contents":" in roster notation"},{"tag":"FFieldMath","contents":"roster"}],"eActions":[{"tag":"Check"}],"eHidden":[{"tag":"FValueS","fvName":"tag","fvValS":"ExerciseType"},{"tag":"FValue","fvName":"exId","fvVal":0},{"tag":"FValueS","fvName":"exTag","fvValS":"Powset"}],"eBroughtBy":[]}],"rSplash":null,"rSes":"","rCurrentPage":null,"rLogin":null,"rEcho":null,"rProgress":null,"rDone":false}'
    vars = {}
    vars['random_unique'] = ourfunctions.random_unique
    def mj(txt,val):
        vars['j'] = ourfunctions.make_json(txt,val,c)
        return
    vars['make_json'] = mj
    exec(content, None, vars)
    print(vars['j'])
    return vars['j']
calc_powset()