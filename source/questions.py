import math
import random

non_relational = {
    "q_shape": ["What is the shape of the <color> object?"],
    "q_pos"  : ["Is the <color> object on the <pos>?", 
                "Where is <color> object?"],
    "q_count": ["How many <shape> objects are there?"]
}

relational = {
    "q_closet":   ["What is the shape of the object that is closet to the <color> object?",
                   "What is the color of the object that is colset to the <color> object?"],
    "q_furthest": ["What is the shape of the object that is furthest to the <color> object?",
                   "What is the color of the object that is furthest to the <color> object?"],
    "q_count":    ["How many objects have the shape of the <color> object?"]
}


def question_shape(q_board):
    available = [(elem[0], elem[1]) for elem in q_board if elem[2][0] == 0]
    obj = random.choice(available)
    
    question = non_relational["q_shape"][0]
    question = question.replace("<color>", obj[1].split()[0])
    answer = obj[1].split()[1]
    
    for i, e in enumerate(q_board):
        if obj[0] == e[0]:
            q_board[i][2][0] = 1
            
    return question, answer


def question_position(q_board):
    available = [(elem[0], elem[1], elem[3]) for elem in q_board if elem[2][1] == 0]
    obj = random.choice(available)
    
    obj_loc = list()
    if obj[2] == (1, 1):
        obj_loc.append("center")
    
    if obj[2][1] == 0:
        obj_loc.append("left")
    elif obj[2][1] == 2:
        obj_loc.append("right")
        
    if obj[2][0] == 0:
        obj_loc.append("top")
    elif obj[2][0] == 2:
        obj_loc.append("bottom")
    
    q_idx = random.randrange(2)
    question = non_relational["q_pos"][q_idx]
    question = question.replace("<color>", obj[1].split()[0])
    
    if q_idx == 0:
        q_loc = random.choice(["left", "right", "top", "bottom", "center"])
        question = question.replace("<pos>", q_loc)
        if q_loc in obj_loc:
            answer = "yes"
        else:
            answer = "no"
    else:
        answer = " ".join(obj_loc)
    
    for i, e in enumerate(q_board):
        if obj[0] == e[0]:
            q_board[i][2][1] = 1
            
    return question, answer


# TODO: need to check duplicated or not
def question_count(q_board, q_shape):
    available = [(elem[0], elem[1]) for elem in q_board if elem[2][2] == 0]
    question = non_relational["q_count"][0]
    
    counter = {"square": 0,"circle": 0,"star": 0,"triangle": 0}
    for elem in available:
        shape = elem[1].split()[1]
        counter[shape] += 1
    
    choice = random.choice([sp[0] for sp in q_shape.items() if sp[1] == 0])
    choice_count = counter[choice]
    question = question.replace("<shape>", choice)
    answer = str(choice_count)
    
    q_shape[choice] = 1
            
    return question, answer


def question_rel_closet(q_board):
    available = [(elem[0], elem[1]) for elem in q_board if elem[2][3] == 0]
    obj = random.choice(available)
    maybe_neighbor = [(elem[0], elem[1]) for elem in q_board if elem != obj]
    
    q_idx = random.randrange(2)
    question = relational["q_closet"][q_idx]
    
    min_dis, min_obj = math.inf, None
    for elem in maybe_neighbor:
        distance = math.sqrt((obj[0][0]-elem[0][0])**2 + (obj[0][1]-elem[0][1])**2)
        if distance == 0: continue
            
        if min_dis > distance:
            min_dis = distance
            min_obj = elem
    
    question = question.replace("<color>", obj[1].split()[0])
    
    if q_idx == 0:
        answer = min_obj[1].split()[1]
    else:
        answer = min_obj[1].split()[0]
        
    for i, e in enumerate(q_board):
        if obj[0] == e[0]:
            q_board[i][2][3] = 1
    
    return question, answer
    
    
def question_rel_furthest(q_board):
    available = [(elem[0], elem[1]) for elem in q_board if elem[2][4] == 0]
    obj = random.choice(available)
    maybe_neighbor = [(elem[0], elem[1]) for elem in q_board if elem != obj]
    
    q_idx = random.randrange(2)
    question = relational["q_furthest"][q_idx]
    
    max_dis, max_obj = 0, None
    for elem in maybe_neighbor:
        distance = math.sqrt((obj[0][0]-elem[0][0])**2 + (obj[0][1]-elem[0][1])**2)
        if distance == 0: continue
            
        if max_dis < distance:
            max_dis = distance
            max_obj = elem
    
    question = question.replace("<color>", obj[1].split()[0])
    
    if q_idx == 0:
        answer = max_obj[1].split()[1]
    else:
        answer = max_obj[1].split()[0]
        
    for i, e in enumerate(q_board):
        if obj[0] == e[0]:
            q_board[i][2][4] = 1
    
    return question, answer
    
    
def question_rel_count(q_board):
    available = [(elem[0], elem[1]) for elem in q_board if elem[2][5] == 0]
    obj = random.choice(available)
    
    question = relational["q_count"][0]
    question = question.replace("<color>", obj[1].split()[0])
    
    counter = {"square": 0,"circle": 0,"star": 0,"triangle": 0}
    for elem in available:
        shape = elem[1].split()[1]
        counter[shape] += 1
        
    answer = str(counter[obj[1].split()[1]])

    for i, e in enumerate(q_board):
        if obj[0] == e[0]:
            q_board[i][2][5] = 1

    return question, answer
