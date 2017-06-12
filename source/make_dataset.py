import json
import random
import gizeh
import scipy.misc as misc
from collections import OrderedDict

from captions import *
from questions import *

def circle(color, position):
    return gizeh.circle(20, fill=color, xy=position, stroke_width=2)
    

def square(color, position):
    return gizeh.square(40, fill=color, xy=position, stroke_width=2)
    

def star(color, position):
    real_position = [position[0]+0, position[1]+1]
    return gizeh.star(nbranches=5, fill=color, xy=real_position,
                      radius=20, ratio=0.5, angle=0.95, stroke_width=2)


def triangle(color, position):
    real_position = [position[0]+0, position[1]+7]
    return gizeh.regular_polygon(25, fill=color, xy=real_position,
                                 n=3, angle=0.53, stroke_width=2)

colors = {
    "red":    (1, 0, 0),
    "green":  (0, 1, 0),
    "blue":   (0, 0, 1),
    "ornage": (1, 0.6, 0),
    "gray":   (0.5, 0.5, 0.5),
    "yellow": (1, 1, 0)
}
shapes = {
    "circle": circle,
    "square": square,
    "triangle": triangle,
    "star": star,
}
    
num_dataset = 10000
num_questions = 10
num_captions = 10


def create_board():
    padding = 25
    board = [["bg" for i in range(3)] for j in range(3)]
    surface = gizeh.Surface(width=256, height=256, bg_color=(0.8, 0.8, 0.8))

    for color_key, color in colors.items():
        shape_key, shape = random.choice(list(shapes.items()))
        empty_indices = [(i, j) for i in range(len(board)) \
                                for j in range(len(board[0])) if board[i][j] == "bg"]
        random_index = random.choice(empty_indices)
    
        noise_pos = random.randint(0, 30)
        draw_pos = [random_index[1]*(256-padding)/3 + padding+noise_pos, 
                    random_index[0]*(256-padding)/3 + padding+noise_pos]
        shape(color, draw_pos).draw(surface)
    
        board[random_index[0]][random_index[1]] = [draw_pos, " ".join([color_key, shape_key])]

    return board, surface


def create_questions(board):
    non_rel_fns = [question_shape, question_position, question_count]
    rel_fns = [question_rel_closet, question_rel_furthest, question_rel_count]
    
    n = 0
    non_rel_questions, non_rel_answers = list(), list()
    q_board = [(board[i][j][0], board[i][j][1], [0]*6, (i, j)) \
               for i in range(3) for j in range(3) if board[i][j] != "bg"]
    q_shape = {"square":0, "circle":0, "star":0, "triangle":0}

    while True:
        fn = random.choice(non_rel_fns)
        try:
            if fn.__name__ == "question_count":
                question, answer = fn(q_board, q_shape)
            else:
                question, answer = fn(q_board)
            non_rel_questions.append(question)
            non_rel_answers.append(answer)
        except BaseException as e:
            continue
        n += 1
        if n >= num_questions: break
    
    n = 0
    rel_questions, rel_answers = list(), list()
    q_board = [(board[i][j][0], board[i][j][1], [0]*6, (i, j)) \
               for i in range(3) for j in range(3) if board[i][j] != "bg"]
    q_shape = {"square":0, "circle":0, "star":0, "triangle":0}
    
    while True:
        fn = random.choice(rel_fns)
        try:
            question, answer = fn(q_board)
            rel_questions.append(question)
            rel_answers.append(answer)
        except BaseException as e:
            continue
        n += 1
        if n >= num_questions: break

    return non_rel_questions, non_rel_answers, rel_questions, rel_answers


def create_captions(board):
    non_rel_fns = [caption_shape, caption_position, caption_count]
    rel_fns = [caption_rel_closet, caption_rel_furthest, caption_rel_count]
    
    n = 0
    non_rel_captions = list()
    q_board = [(board[i][j][0], board[i][j][1], [0]*6, (i, j)) \
               for i in range(3) for j in range(3) if board[i][j] != "bg"]
    q_shape = {"square":0, "circle":0, "star":0, "triangle":0}

    while True:
        fn = random.choice(non_rel_fns)
        try:
            if fn.__name__ == "caption_count":
                non_rel_captions.append(fn(q_board, q_shape))
            else:
                non_rel_captions.append(fn(q_board))
        except BaseException as e:
            continue
        n += 1
        if n >= num_captions: break

    n = 0
    rel_captions = list()
    q_board = [(board[i][j][0], board[i][j][1], [0]*6, (i, j)) \
               for i in range(3) for j in range(3) if board[i][j] != "bg"]
    q_shape = {"square":0, "circle":0, "star":0, "triangle":0}
    
    while True:
        fn = random.choice(rel_fns)
        try:
            rel_captions.append(fn(q_board))
        except BaseException as e:
            continue
        n += 1
        if n >= num_captions: break

    return non_rel_captions, rel_captions

def main():
    dataset = list()
    for i in range(num_dataset):
        if i % 500 == 0: print(i)
        board, surface = create_board()
        non_rel_q, non_rel_a, rel_q, rel_a = create_questions(board)
        non_rel_c, rel_c = create_captions(board)

        im_path = "images/image_{}.png".format(i)
        surface.write_to_png(im_path)
        
        data = OrderedDict()
        data["image"] = im_path
        data["non_rel_q"]   = non_rel_q
        data["non_rel_ans"] = non_rel_a
        data["rel_q"]   = rel_q
        data["rel_ans"] = rel_a
        data["non_rel_cap"] = non_rel_c
        data["rel_cap"]     = rel_c
        dataset.append(data)

    with open("dataset.json", "w") as _file:
        json.dump(dataset, _file, indent=4)
    

if __name__ == "__main__":
    main()
