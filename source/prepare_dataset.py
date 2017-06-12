import os
import sys
import json
import random
import cPickle as pickle

skipthought_path = "/home/nmhkahn/Works/skip-thoughts/"
os.chdir(skipthought_path)
sys.path.insert(0, skipthought_path)

import skipthoughts

model = skipthoughts.load_model()
encoder = skipthoughts.Encoder(model)

dataset_dir = "/home/nmhkahn/Datasets/sort-sort-of-clevr/"
with open(os.path.join(dataset_dir, "dataset.json")) as _file:
    dataset = json.load(_file)

new_data = list()
for data in dataset:
    im_path = os.path.join(dataset_dir, data["image"])
    text = data["non_rel_q"] + data["rel_q"] + data["non_rel_cap"] + data["rel_cap"]
    enc_vec = encoder.encode(text, verbose=False)

    datum = {
        "path": im_path,
        "non_rel_q": enc_vec[:10, 2400:], # use only biskip
        "rel_q": enc_vec[10:20, 2400:],
        "non_rel_cap": enc_vec[20:30, 2400:],
        "rel_cap": enc_vec[30:, 2400:],
        "non_rel_ans": data["non_rel_ans"],
        "rel_ans": data["rel_ans"]
    }
    new_data.append(datum)

pickle.dump(new_data, open(os.path.join(dataset_dir, "dataset.pkl"), "wb"))
