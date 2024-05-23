import random
import json
import proofgen
import os
from fractions import Fraction

def random_unique(minmax, n=2):
    unique_values = random.sample(range(minmax[0], minmax[1] + 1), n)
   
    return unique_values

def get_files(folder_path):
    start = {"rPages":[],"rExercises":[],"rSplash":None,"rSes":"","rCurrentPage":None,"rLogin":"Single user mode","rEcho":None,"rProgress":None,"rDone":False}
    count = 1
    for filename in os.listdir(folder_path):
        new_problem = {}
        q_name = filename.split('.')[0]
        new_problem["pId"] = q_name
        p_name = 'L' + str(count) + ' - ' + str(q_name)
        new_problem["pName"] = p_name
        start["rPages"].append(new_problem)
        count += 1
    return json.dumps(start)
get_files(r'C:\Users\nayan\OneDrive\Desktop\4970Project\2011grader\n_files')


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

def add_to_question(js, curr_json):
    curr_json["rExercises"][0]["eQuestion"].append(js)
    return curr_json

def form_json(tags, vals):
    res = {}
    for i in range(len(tags)):
        res[tags[i]] = vals[i]
    return res

def form_logic_step(step):
    return form_json(["tag", "fIndentation", "fContent"], ["FIndented", 1, [form_json(["tag", "contents"], ["FMath", step])]])

def create_steps(steps):


    clusters = []
    for step in steps:
        st = [form_json(["tag", "contents"], ["FMath", "="]), form_json(["tag", "contents"], ["FText", str(step.explanation)]), form_logic_step(str(step.rhs))] 
        clusters.append(st)
    fin = form_json(["tag", "fvName", "fClusters"], ["FReorder", "proof", clusters])   
    return fin 

def check_proof_answer(orig, shuffled, ans):
    for i in range(len(orig)):
        if shuffled[ans[i]] != orig[i]:
            return False
    return True

def get_correct_proof(orig, shuffled):
    res = []
    for i in range(len(orig)):
        res.append(shuffled.index(orig[i]))
    return res


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



def get_acc_tim(vf, d):
    vf2 = vf * vf
    twod = d * 2
    a = vf2 / twod
    t = vf / a
    return round(a, 2), round(t, 2)

def get_prop(d, h):
    if h == 0 or h == 2:
        return round((d-1)/24,2)
    else:
        return round((2*(d-1))/24,2)
    
def fraction_to_decimal(fraction_str):
    
    cleaned_str = fraction_str.replace('\\frac{', '').replace('}', '')
    
    
    # Split the cleaned string into numerator and denominator
    try:
        numerator, denominator = cleaned_str.split('{')
    except:
        return 1
    
    numerator = int(numerator)
    denominator = int(denominator)
    
    decimal_value = round(numerator / denominator,2)
    
    return str(decimal_value)

    



