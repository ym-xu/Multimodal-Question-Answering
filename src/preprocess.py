# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
# 
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import sys
import json
import parser
from pathlib import Path
import numpy as np
import util
import datasets
import random
import os

def select_examples_NQ(data, index, passages, passages_index):
    selected_data = []
    for i, k in enumerate(index):
        ctxs = [
                {
                    'id': idx,
                    'title': passages[idx][1],
                    'text': passages[idx][0],
                }
                for idx in passages_index[str(i)]
            ]
        dico = {
            'question': data[k]['question'],
            'answers': data[k]['answer'],
            'ctxs': ctxs,
        }
        selected_data.append(dico)

    return selected_data

def get_struture_PopQA(data):
    data_ = []
    for sample in data:
        ctxs = [{
            'id' : "",
            'title' : "",
            'text' : ""
        } for passage in sample['ctxs']]
        
        dico = {
            'question' : sample['question'],
            'answers' : sample['answers'],
            'ctxs' : ctxs,
            'prop' : sample['prop'],
            'prop_id' : sample['prop_id'],
            'subj' : sample['subj'],
            'subj_id' : sample['subj_id'],
            'obj_id' : sample['obj_id'],
            's_pop' : sample['s_pop'],
            'o_pop' : sample['o_pop']
        }
        data_.append(dico)
    
    return data_

def get_struture_EQ(data):
    data_ = []
    for sample in data:
        ctxs = [{
            'id' : "",
            'title' : "",
            'text' : ""
        } for i in range(10)]
        
        dico = {
            'question' : sample['question'],
            'answers' : sample['answers'],
            'ctxs' : ctxs,
        }
        data_.append(dico)
    
    return data_
    

if __name__ == "__main__":
    dir_path = Path(sys.argv[1])
    save_dir = Path(sys.argv[2])

    passages = util.load_passages(save_dir/'psgs_w100.tsv')
    passages = {p[0]: (p[1], p[2]) for p in passages}

    #load NQ question idx
    # print("process NQ")
    # NQ_idx = {}
    # NQ_passages = {}
    # for split in ['train', 'dev', 'test']:
    #     with open(dir_path/('NQ.' + split + '.idx.json'), 'r') as fin:
    #         NQ_idx[split] = json.load(fin)
    #     with open(dir_path/'nq_passages' /  (split + '.json'), 'r') as fin:
    #         NQ_passages[split] = json.load(fin)


    # originaltrain, originaldev = [], []
    # with open(dir_path/'NQ-open.dev.jsonl') as fin:
    #     for k, example in enumerate(fin):
    #         example = json.loads(example)
    #         originaldev.append(example)
    
    # with open(dir_path/'NQ-open.train.jsonl') as fin:
    #     for k, example in enumerate(fin):
    #         example = json.loads(example)
    #         originaltrain.append(example)

    # NQ_train = select_examples_NQ(originaltrain, NQ_idx['train'], passages, NQ_passages['train'])
    # NQ_dev = select_examples_NQ(originaltrain, NQ_idx['dev'], passages, NQ_passages['dev'])
    # NQ_test = select_examples_NQ(originaldev, NQ_idx['test'], passages, NQ_passages['test'])

    # NQ_save_path = save_dir / 'NQ'
    # NQ_save_path.mkdir(parents=True, exist_ok=True)

    # with open(NQ_save_path/'train.json', 'w') as fout:
    #     json.dump(NQ_train, fout, indent=4)
    # with open(NQ_save_path/'dev.json', 'w') as fout:
    #     json.dump(NQ_dev, fout, indent=4)
    # with open(NQ_save_path/'test.json', 'w') as fout:
    #     json.dump(NQ_test, fout, indent=4)
        
    #load PopQA
    print("process PopQA")
    popqa = datasets.load_dataset("akariasai/PopQA")["test"]
    allsample = []
    
    for p in popqa:
        set_ = {}
        set_['question'] = p['question']
        set_['answer'] = eval(p['possible_answers'])
        set_['prop'] = p['prop']
        set_['prop'] = p['prop_id']
        set_['subj'] = p['subj']
        set_['subj_id'] = p['subj_id']
        set_['obj_id'] = p['obj_id']
        set_['s_pop'] = p['s_pop']
        set_['o_pop'] = p['o_pop']
        allsample.append(set_)
        
    random.shuffle(allsample)
    train_size = int(0.7 * len(allsample))
    test_size = int(0.2 * len(allsample))
    dev_size = len(allsample) - train_size - test_size
    traindata = allsample[:train_size]
    testdata = allsample[train_size:train_size+test_size]
    devdata = allsample[train_size+test_size:]
    
    PopQA_train = get_struture_PopQA(traindata)
    PopQA_test = get_struture_PopQA(testdata)
    PopQA_dev = get_struture_PopQA(devdata)
    
    PopQA_save_path = save_dir / 'PopQA'
    PopQA_save_path.mkdir(parents=True, exist_ok=True)
    
    with open(PopQA_save_path/'train.json', 'w') as fout:
        json.dump(PopQA_train, fout, indent=4)
    with open(PopQA_save_path/'dev.json', 'w') as fout:
        json.dump(PopQA_dev, fout, indent=4)
    with open(PopQA_save_path/'test.json', 'w') as fout:
        json.dump(PopQA_test, fout, indent=4)
        
    #load EQ
    print("process EQ")
    eq_save_path = dir_path / 'dataset'
    print(eq_save_path)
    devdata = util.read_data(eq_save_path, 'dev')
    testdata = util.read_data(eq_save_path, 'test')
    traindata = util.read_data(eq_save_path, 'train')
    
    EQ_train = get_struture_EQ(traindata)
    EQ_test = get_struture_EQ(testdata)
    EQ_dev = get_struture_EQ(devdata)
    
    EQ_save_path = save_dir / 'EQ'
    EQ_save_path.mkdir(parents=True, exist_ok=True)
    
    with open(EQ_save_path/'train.json', 'w') as fout:
        json.dump(EQ_train, fout, indent=4)
    with open(EQ_save_path/'dev.json', 'w') as fout:
        json.dump(EQ_dev, fout, indent=4)
    with open(EQ_save_path/'test.json', 'w') as fout:
        json.dump(EQ_test, fout, indent=4)

            
    

