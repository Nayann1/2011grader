import random
import json
def random_unique(minmax, n=2):
    unique_values = random.sample(range(minmax[0], minmax[1] + 1), n)
   
    return unique_values



def create_answer(val):
    num_values = random.choice([1, 2, 3])
    selected_values = random.sample(val, num_values)
    return selected_values

def make_json(updated_tag,values, curr_json):
    if (type(values) == list):
        result = '{' + ', '.join(map(str, values)) + '}'
        contents_str = r"\left\{res\right\}"
        contents_str = contents_str.replace("res", result)
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

def new_get_set(set1, set2):
    res1 =  ', '.join(map(str, set1))
    res2 = ', '.join(map(str, set2))
    z = r"\left\{set1\right\} \cap \left\{set2\right\}"
    result_string = z.replace("set1", res1).replace("set2", res2)
    return result_string

def new_get_set2(st):
    res1 =  ','.join(map(str, st))
    z= r"\left\{res\right\}"
    result_string = z.replace("res", res1)
    return result_string


def respond(b):
    if b:
        print("CORRECT")
    else:
        print("INCORRECT")



def topic(topic, js):
    #curjson = {"rPages":[],"rExercises":[{"eTopic": None,"eQuestion":[],"eActions":[{"tag":"Check"}],"eHidden":[{"tag":"FValueS","fvName":"tag","fvValS":"ExerciseType"},{"tag":"FValue","fvName":"exId","fvVal":0},{"tag":"FValueS","fvName":"exTag","fvValS":"Powset"}],"eBroughtBy":[]}],"rSplash":None,"rSes":"","rCurrentPage":None,"rLogin":None,"rEcho":None,"rProgress":None,"rDone":False}
    js['rExercises'][0]['eTopic'] = topic
    return js



def gen_sets(mn, mx, size1, size2):
    length = min(size1, size2)
    array = [i+1 for i in range(length)]

    num_values = random.choice(array)
    unique_values = set()
    while len(unique_values) < size1:
        unique_values.add(random.randint(mn, mx))
    value1 = list(unique_values)

    answ = set()
    unique_values2 = set()
    
    while len(answ) < num_values:
        answ.add(random.choice(value1))

    ans = list(answ)
    while len(answ) < size2:
        answ.add(random.randint(mn, mx))
    value2 = list(answ)
    #print(value1, value2, ans, num_values)
    return value1, value2, ans



