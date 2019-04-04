import json
import random
import gizeh
from collections import OrderedDict
from tqdm import tqdm
import os
from collections import defaultdict

def circle(color, position):
    return gizeh.circle(r=15, fill=color, xy=position, stroke_width=2)

colors = {
    "red":    (1, 0, 0),
}
shapes = {
    "circle": circle,
}

colors_idx = {
    "red":    1,
}
shapes_idx = {
    "circle": 1,
}

Ndataset = 10000
Neach = 1000

ans_distribution = defaultdict(int)

def create_board(Nobjects):
    
    W, H = 224 , 224
    Nrows = 3
    Ncols = 4
    Nobjects_min = 1
    Nobjects_max = 10
    padding = 20
    board = [["bg" for _ in range(Ncols)] for _ in range(Nrows)]
    surface = gizeh.Surface(width=W, height=H, bg_color=(0.8, 0.8, 0.8))    
    #Nobjects = random.randint(Nobjects_min,Nobjects_max)
    
#    if ans_distribution[Nobjects] > Neach:
#        return None
#    
#    ans_distribution[Nobjects] +=1
    for _ in range(Nobjects):
        shape_key, shape = random.choice(list(shapes.items()))
        color_key, color = random.choice(list(colors.items()))
        empty_indices = [(i, j) for i in range(Nrows) \
                                for j in range(Ncols) if board[i][j] == "bg"]

        random_index = random.choice(empty_indices)
        noise_x = random.randint( padding,  W//Ncols - padding)
        noise_y = random.randint( padding,  H//Nrows - padding)
        
        draw_pos = [random_index[1] * W//Ncols + noise_x,
                    random_index[0] * H//Nrows + noise_y]
        shape(color, draw_pos).draw(surface)
        board[random_index[0]][random_index[1]] = [draw_pos, " ".join([color_key, shape_key])]

    return board, surface , Nobjects

#%%

if __name__ == "__main__":
    dataset = list()
    
    if not os.path.exists('images'):
        os.mkdir('images')
    
    counter = 0
    for n in tqdm(range(1,11)):
        for _ in tqdm(range(Neach)):
            board, surface,Nobjects = create_board(n)
    
            #        # convert board data into vector [color, shape]
            #        board_vec = [[[] for _ in range(3)] for _ in range(3)]
            #        for i in range(3):
            #            for j in range(3):
            #                board_vec[i][j] += [0]*2
            #                if board[i][j] == "bg":
            #                    continue
            #
            #                color, shape = board[i][j][1].split()
            #                board_vec[i][j][0] = colors_idx[color]
            #                board_vec[i][j][1] = shapes_idx[shape]
            
            
            im_path = "images/image_{}.png".format(counter)
            surface.write_to_png(im_path)
    
            data = OrderedDict()
            data["ans"] = Nobjects
            data["path"] = im_path
            #data["board"] = board_vec
            dataset.append(data)
            counter +=1

    with open("dataset.json", "w") as _file:
        json.dump(dataset, _file)

    import matplotlib.pyplot as plt
    from collections import Counter
    answers = [ ent['ans'] for ent in dataset]
    cnt = Counter(answers)
    print (cnt)
    cntkeys = sorted(cnt)
    cntvals = [ cnt[ii] for ii in cntkeys]
    plt.plot(cntkeys,cntvals)
    plt.ylim([0,1200])
    plt.show()