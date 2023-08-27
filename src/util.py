
import os
import errno
import torch
import sys
import logging
import json
from pathlib import Path
import torch.distributed as dist
import csv
import os
import glob

logger = logging.getLogger(__name__)

def load_passages(path):
    if not os.path.exists(path):
        logger.info(f'{path} does not exist')
        return
    logger.info(f'Loading passages from: {path}')
    passages = []
    with open(path) as fin:
        reader = csv.reader(fin, delimiter='\t')
        for k, row in enumerate(reader):
            if not row[0] == 'id':
                try:
                    passages.append((row[0], row[1], row[2]))
                except:
                    logger.warning(f'The following input line has not been correctly loaded: {row}')
    return passages

def read_data(eq_save_path, dir_):
    json_data = []
    json_pattern = os.path.join(eq_save_path/dir_, '*.json')

    json_files = glob.glob(json_pattern)

    for f in json_files:
        filename = os.path.basename(f)

        with open(f, 'r') as file:
            json_data += json.load(file)
    return json_data