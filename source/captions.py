import math
import random

non_relational = {
    "shape": ["Object with <color> have the <shape> shape."],
    "pos"  : ["Object with <color> is on the <pos>."],
    "count": ["There are <count> <shape> shape objects."]
}

relational = {
    "closet":   ["Object with <color> is closet to the <shape> object.",
                 "Object with <color> is closet to the <color> object."],
    "furthest": ["Object with <color> is furthest to the <shape> object.",
                 "Object with <color> is furthest to the <color> object."],
    "count":    ["There are <count> objects have the shape of the <color> object."]
}

def caption_shape(q_board):
    available = [(elem[0], elem[1]) for elem in q_board if elem[2][0] == 0]
    obj = random.choice(available)
    
    caption = non_relational["shape"][0]
    caption = caption.replace("<color>", obj[1].split()[0])
    caption = caption.replace("<shape>", obj[1].split()[1])
    
    for i, e in enumerate(q_board):
        if obj[0] == e[0]:
            q_board[i][2][0] = 1
            
    return caption


def caption_position(q_board):
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
    
    caption = non_relational["pos"][0]
    caption = caption.replace("<color>", obj[1].split()[0])
    caption = caption.replace("<pos>", " ".join(obj_loc))
    
    for i, e in enumerate(q_board):
        if obj[0] == e[0]:
            q_board[i][2][1] = 1
            
    return caption


# TODO: need to check duplicated or not
def caption_count(q_board, q_shape):
    available = [(elem[0], elem[1]) for elem in q_board if elem[2][2] == 0]
    
    counter = {"square": 0,"circle": 0,"star": 0,"triangle": 0}
    for elem in available:
        shape = elem[1].split()[1]
        counter[shape] += 1
    
    choice = random.choice([sp[0] for sp in q_shape.items() if sp[1] == 0])
    choice_count = counter[choice]
    
    caption = non_relational["count"][0]
    caption = caption.replace("<shape>", choice)
    caption = caption.replace("<count>", str(choice_count))
    
    q_shape[choice] = 1
            
    return caption


def caption_rel_closet(q_board):
    available = [(elem[0], elem[1]) for elem in q_board if elem[2][3] == 0]
    obj = random.choice(available)
    maybe_neighbor = [(elem[0], elem[1]) for elem in q_board if elem != obj]
    
    min_dis, min_obj = math.inf, None
    for elem in maybe_neighbor:
        distance = math.sqrt((obj[0][0]-elem[0][0])**2 + (obj[0][1]-elem[0][1])**2)
        if distance == 0: continue
            
        if min_dis > distance:
            min_dis = distance
            min_obj = elem
    
    idx = random.randrange(2)
    caption = relational["closet"][idx]
    caption = caption.replace("<color>", obj[1].split()[0], 1)
    
    if idx == 0:
        caption = caption.replace("<shape>", min_obj[1].split()[1], 1)
    else:
        caption = caption.replace("<color>", min_obj[1].split()[0], 1)
        
    for i, e in enumerate(q_board):
        if obj[0] == e[0]:
            q_board[i][2][3] = 1
    
    return caption
    
    
def caption_rel_furthest(q_board):
    available = [(elem[0], elem[1]) for elem in q_board if elem[2][4] == 0]
    obj = random.choice(available)
    maybe_neighbor = [(elem[0], elem[1]) for elem in q_board if elem != obj]
    
    max_dis, max_obj = 0, None
    for elem in maybe_neighbor:
        distance = math.sqrt((obj[0][0]-elem[0][0])**2 + (obj[0][1]-elem[0][1])**2)
        if distance == 0: continue
            
        if max_dis < distance:
            max_dis = distance
            max_obj = elem
    
    idx = random.randrange(2)
    caption = relational["furthest"][idx]
    caption = caption.replace("<color>", obj[1].split()[0], 1)
    
    if idx == 0:
        caption = caption.replace("<shape>", max_obj[1].split()[1], 1)
    else:
        caption = caption.replace("<color>", max_obj[1].split()[0], 1)
        
    for i, e in enumerate(q_board):
        if obj[0] == e[0]:
            q_board[i][2][4] = 1
    
    return caption
    
    
def caption_rel_count(q_board):
    available = [(elem[0], elem[1]) for elem in q_board if elem[2][5] == 0]
    obj = random.choice(available)
    
    counter = {"square": 0,"circle": 0,"star": 0,"triangle": 0}
    for elem in available:
        shape = elem[1].split()[1]
        counter[shape] += 1
        
    caption = relational["count"][0]
    caption = caption.replace("<color>", obj[1].split()[0])
    caption = caption.replace("<count>", str(counter[obj[1].split()[1]]))
        
    for i, e in enumerate(q_board):
        if obj[0] == e[0]:
            q_board[i][2][5] = 1

    return caption