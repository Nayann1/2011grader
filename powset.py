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
            if assignment:
                
                variable, value = (assignment.groups())
                evaluated_value = eval(value, {}, vars)
                
                vars[variable] = evaluated_value
            elif returnstmt:
                value, = (returnstmt.groups())
                vals = (str(eval(value, {}, vars)))
                
        data = {
            "tag":"FMath",
            "contents":f"(\\left\\{{{vars['value'][0]},{vars['value'][1]}\\right\\}})"
        }
        json_data = json.dumps(data)
        return json_data
