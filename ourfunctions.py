import random
import json
def random_unique(minmax, n=2):
    unique_values = random.sample(range(minmax[0], minmax[1] + 1), n)
   
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

def get_response(j):
    print(j)
    return 5

def add_to_feedback(updated_tag,values, curr_json):
    if (type(values) == int):
        contents_str = str(values)
    else:
        contents_str = values
    data_dict = {"tag": updated_tag, "contents": f"{contents_str}"}
    curr_json['rSplash']['contents']['prFeedback'].append(data_dict)
    return curr_json

def get_set(v1, v2):
    z = r"\left\{\left\{\right\},\left\{value[0]\right\},\left\{value[1]\right\},\left\{value[0],value[1]\right\}\right\}"
    result_string = z.replace("value[0]", str(v1)).replace("value[1]", str(v2))
    return result_string

def get_set2(v1, v2):
    z = r"(\left\{value[0],value[1]\right\})"
    result_string = z.replace("value[0]", str(v1)).replace("value[1]", str(v2))
    return result_string

def respond(b):
    if b:
        print("CORRECT")
    else:
        print("INCORRECT")




