# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import json
import logging
import os
import numpy as np
import torch

import model.fid.util

from model.fid.evaluation import calculate_matches

logger = logging.getLogger(__name__)

def validate(data, workers_num):
    match_stats = calculate_matches(data, workers_num)
    top_k_hits = match_stats.top_k_hits

    logger.info('Validation results: top k documents hits %s', top_k_hits)
    top_k_hits = [v / len(data) for v in top_k_hits]
    logger.info('Validation results: top k documents hits accuracy %s', top_k_hits)
    return match_stats.questions_doc_hits

def eval_pop(opt):
    R5 = []
    R20 = []
    R100 = []
    R150 = []
    R200 = []
    logger = model.fid.util.init_logger(is_main=True)
    with open(opt.l_dir, "r") as f:
        poplevels = json.load(f)
    with open(opt.data, 'r') as fin:
        data = json.load(fin)
    for l in range(opt.levels):
        data_ = []
        for en in data:
            max_ = opt.levels + 1
            #for i in en['answers']:
            #    if i in poplevels.keys():
            #        if poplevels[i] < max_:
            #            max_ = poplevels[i]
            #if max_ == l:
            #    data_.append(en)
            if len(en[opt.type]) == 0:
                continue
            if en[opt.type] in poplevels.keys():
                if poplevels[en[opt.type]] == l:
                    data_.append(en)
        answers = [ex[opt.type] for ex in data_]
        match_stats = calculate_matches(data_, args.validation_workers)
        top_k_hits = match_stats.top_k_hits
        top_k_hits = [v / len(data_) for v in top_k_hits]
        R5.append(top_k_hits[4])
        R20.append(top_k_hits[19])
        R100.append(top_k_hits[99])
        R150.append(top_k_hits[149])
        R200.append(top_k_hits[199])
        #questions_doc_hits = validate(data_, args.validation_workers)
    logger.info('Validation results: top 5 documents in 10 levels hits accuracy %s', R5)
    logger.info(R20)
    logger.info(R100)
    logger.info(R150)
    logger.info(R200)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--data', required=True, type=str, default=None)
    parser.add_argument('--validation_workers', type=int, default=16,
                        help="Number of parallel processes to validate results")
    parser.add_argument('--pop', required=False, type=str, default=None)
    parser.add_argument('--l_dir', required=True, type=str, default=None)
    parser.add_argument('--levels', required=True, type=int, default=None)
    parser.add_argument('--type', required=True, type=str, default=None)

    args = parser.parse_args()
    eval_pop(args)