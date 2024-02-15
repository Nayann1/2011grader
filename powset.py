import re
import ourfunctions
import json

def calc_powset():
    with open('powset.n', 'r') as file:
        vars = {}
        vars['random_unique'] = ourfunctions.random_unique
        

        for line in file:
            assignment = re.match(r'(\w+)\s*=\s*(.+)', line)

            returnstmt = re.match(r'return\s*(.+)', line)
            pattern = re.compile(r'make_json\("([^"]+)",\s*([^)]+)\)')


            if assignment:
                
                variable, value = (assignment.groups())
                evaluated_value = eval(value, {}, vars)
                
                vars[variable] = evaluated_value
            elif pattern and "value" in vars:
                c = '{"rPages":[],"rExercises":[{"eTopic":"Powerset operations","eQuestion":[{"tag":"FText","contents":"Write the powerset 𝒫"},{"tag":"FText","contents":" in roster notation"},{"tag":"FFieldMath","contents":"roster"}],"eActions":[{"tag":"Check"}],"eHidden":[{"tag":"FValueS","fvName":"tag","fvValS":"ExerciseType"},{"tag":"FValue","fvName":"exId","fvVal":0},{"tag":"FValueS","fvName":"exTag","fvValS":"Powset"}],"eBroughtBy":[]}],"rSplash":null,"rSes":"","rCurrentPage":null,"rLogin":null,"rEcho":null,"rProgress":null,"rDone":false}'

                vars['j'] = ourfunctions.make_json("FText", vars['value'], c)

            elif returnstmt:
                value, = (returnstmt.groups())
                vals = (str(eval(value, {}, vars)))
                
        print(vars['j'])
        return vars['j']
calc_powset()