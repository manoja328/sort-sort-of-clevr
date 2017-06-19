import os
import sys
import json
import random
import cPickle as pickle

skipthought_path = "path/to/skipthought/directory/"
dataset_dir = "path/to/dataset/directory/"

os.chdir(skipthought_path)
sys.path.insert(0, skipthought_path)
import skipthoughts

model = skipthoughts.load_model()
encoder = skipthoughts.Encoder(model)

with open(os.path.join(dataset_dir, "dataset.json")) as _file:
    dataset = json.load(_file)

new_data = list()
for data in dataset:
    im_path = os.path.join(dataset_dir, data["path"])
    text = data["non_rel_question"] + data["rel_question"] +
           data["non_rel_caption"] + data["rel_caption"]
    enc_vec = encoder.encode(text, verbose=False)

    datum = {
        "path": im_path,
        "non_rel_question": enc_vec[:10, 2400:], # use only biskip
        "rel_question": enc_vec[10:20, 2400:],
        "non_rel_caption": enc_vec[20:30, 2400:],
        "rel_caption": enc_vec[30:, 2400:],
        "non_rel_answer": data["non_rel_ans"],
        "rel_answer": data["rel_answer"]
    }
    new_data.append(datum)

pickle.dump(new_data, open(os.path.join(dataset_dir, "dataset.pkl"), "wb"))
