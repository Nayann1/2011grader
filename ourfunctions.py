import random
import json
def random_unique(minmax, n=2):
    unique_values = random.sample(range(minmax[0], minmax[1] + 1), 2)
   
    return unique_values

def make_json(updated_tag,values, curr_json):
    if (type(values) == list):
        contents_str = f"(\\left\\{{{values[0]},{values[1]}\\right\\}})"
    else:
        contents_str = values
    
    data_dict = {"tag": updated_tag, "contents": f"{contents_str}"}
    
    # math_string = json.dumps(data_dict)
    
    
    # math_data = json.loads(math_string)
    # curr_data = json.loads(curr_json)
    
    # contents_value = math_data["contents"]

    curr_json["rExercises"][0]["eQuestion"].append(data_dict)
    
    return curr_json

def get_response(cn):
    return cn


