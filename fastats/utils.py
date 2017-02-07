'''
Some utils
'''

import numpy as np
import collections

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

block = '\u2588'

def split_seq(seqrec, n_chunks, s_len):
    '''
    Split a sequence record into roughly equal sized non-overlapping chunks
    Then count how many of each individual features exist in each chunk
    '''
    # create a list of locations to split the sequence at
    # remove the first and last positions of the list, as these
    # generate zero-length chunks
    locs = np.linspace(0, s_len, n_chunks, dtype = 'int64')[1:-1]
    #create a np.array from the sequence
    seq_array = np.array(list(seqrec.seq))
    seq_chunks = np.split(seq_array, locs)
    seq_chunks = [collections.Counter(chunk) for chunk in seq_chunks]
    return(seq_chunks)

def chunk_percent(seq_chunk, feature = 'dash'):
    '''
    Calculate the proportion of each chunk that is of a certain feature (e.g., A, T, C, G, or GC)
    '''
    if feature == 'dash':
        stats = [chunk['-']/sum(chunk.values()) for chunk in seq_chunk]
    elif feature == 'geecee':
        stats = [(chunk['G'] + chunk['C'])/sum(chunk.values()) for chunk in seq_chunk]
    elif feature.upper() in ['A', 'T', 'C', 'G']:
        stats = [chunk[feature]/sum(chunk.values()) for chunk in seq_chunk]
    else:
        print("WARNING: Not sure about generating stats on feature {}. Will try anyway!".format(feature), file = sys.stderr)
        stats = [chunk[feature]/sum(chunk.values()) for chunk in seq_chunk]
    return stats

def percent_to_blocks(stats, thresholds = [0.5, 0.9, 0.95]):
    out = ''
    for s in stats:
        if s < thresholds[0]:
            out += bcolors.FAIL + block + bcolors.ENDC
        elif s >= thresholds[0] and s < thresholds[1]:
            out += bcolors.WARNING + block + bcolors.ENDC
        else:
            out += bcolors.OKBLUE + block + bcolors.ENDC
    return out
