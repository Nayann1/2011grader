import random
import json
def random_unique(minmax, n=2):
    unique_values = random.sample(range(minmax[0], minmax[1] + 1), 2)
   
    return unique_values

def make_json(updated_tag,values, curr_json):
    contents_str = f"(\\left\\{{{values[0]},{values[1]}\\right\\}})"
    
    data_dict = {"tag": updated_tag, "contents": f"{contents_str}"}
    math_string = json.dumps(data_dict)
    
    
    math_data = json.loads(math_string)
    curr_data = json.loads(curr_json)
    
    contents_value = math_data["contents"]

    
    curr_data["rExercises"][0]["eQuestion"].insert(1, {"tag": "FMath", "contents": contents_value})
    updated_json = json.dumps(curr_data)
    return updated_json


