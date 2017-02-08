'''
'''

from Bio import SeqIO
from Bio import SeqUtils
import click
import operator
import sys
import utils

bases = ['A', 'T', 'C', 'G', 'N', '-']

class SeqSummary:
    bases = ['A', 'T', 'C', 'G', 'N']
    def __init__(self, seqrec, sep = '|'):
        self.sep = sep
        self.s = seqrec.upper() # makes sure comparison is always in upper case
    def __str__(self):
        out = self.sep.join(map(str,[self.id, \
            self.length, \
            '{:.3}'.format(self.geecee), \
            self.A,
            self.T,
            self.C,
            self.G,
            self.N,
            self.dash]))
        return out
    def summarise(self):
        self.__dict__['id'] = self.s.id
        self.__dict__['length'] = len(self.s)
        self.__dict__['geecee'] = SeqUtils.GC(self.s.seq)
        self.__dict__['counts'] = {}
        for b in self.bases:
            self.__dict__[b] = self.s.seq.count(b)
        self.__dict__['dash'] = self.s.seq.count('-')
    def generate_chunks(self, n_chunks):
        self.chunks = {}
        self.chunks['counts'] = utils.split_seq(self.s, n_chunks, self.length)
    def chunk_percent(self, feature):
        self.chunks[feature] = utils.chunk_percent(self.chunks['counts'], feature)
    def print_blocks(self, feature):
        blocks = utils.percent_to_blocks(self.chunks[feature], thresholds = [0.5, 0.9, 0.95])
        print(self.id + ' ' + blocks)

class SummaryGroup:
    def __init__(self, sort, sep, by = 'geecee', desc = False):
        self.sort = sort
        self.by = by
        self.desc = desc
        self.sep = sep
        self.sequences = []
    def add(self, seqrec):
        tmp = SeqSummary(seqrec, self.sep)
        tmp.summarise()
        print('Parsed {}'.format(tmp.id), file = sys.stderr)
        if not self.sort:
            print(tmp)
        self.sequences.append(tmp)
    def arrange(self):
        self.sequences = sorted(self.sequences, key = operator.attrgetter(self.by), reverse = self.desc)
    def summarise(self):
        n_seq = len(self.sequences)
        mean_len = sum([s.length for s in self.sequences])/float(n_seq)
        mean_geecee = sum([s.geecee for s in self.sequences])/float(n_seq)
        mean_A = sum([s.A for s in self.sequences])/float(n_seq)
        mean_T = sum([s.T for s in self.sequences])/float(n_seq)
        mean_C = sum([s.C for s in self.sequences])/float(n_seq)
        mean_G = sum([s.G for s in self.sequences])/float(n_seq)
        mean_N = sum([s.N for s in self.sequences])/float(n_seq)
        mean_dash = sum([s.dash for s in self.sequences])/float(n_seq)
        print('N={} | mean length = {} | mean GC = {:.3}\nmean A = {:.3} | mean T = {:.3} | mean C = {:.3} | mean G = {:.3} | mean N = {:.3} | mean - = {:.3}'.format(n_seq, mean_len, mean_geecee, mean_A, mean_T, mean_C, mean_G, mean_N, mean_dash), file = sys.stderr)
    def chunk_stats(self, n_chunks = 10, feature = 'geecee'):
        for s in self.sequences:
            s.generate_chunks(n_chunks)
            s.chunk_percent(feature)
    def get_blocks(self, feature):
        for s in self.sequences:
            s.print_blocks(feature = feature)

def print_header(sep = '|'):
    header = sep.join(['ID','LENGTH', 'GEECEE', 'A', 'T', 'C', 'G', 'N', '-' ])
    print(header)

def parse_sep(sep):
    '''
    If passing a \t Python interprets it as \\t
    '''
    if sep == '\\t':
        sep = '\t'
    return sep

@click.command()
@click.option('-d', '--delim', default=',', show_default = True, metavar = '<char>', help = 'Set separator character.')
@click.option('-s', '--sort', is_flag = True)
@click.option('--by', default = 'geecee', show_default = True, type = click.Choice(['geecee', 'length', 'N', 'dash', 'A', 'T', 'C', 'G']), help = 'Sort by column.')
@click.option('--desc', is_flag = True, help = 'Sort by descending order.')
@click.option('--feature', default = 'dash', type = click.Choice(['geecee', 'length', 'N', 'dash', 'A', 'T', 'C', 'G']), help = 'calculate chunk percent' )
@click.option('-c', '--chunks', default = 10, help = "Number of roughly equally sized non-overlapping chunks to calculate percent of features")
@click.argument('filename')
def main(filename, delim, sort, by, desc, feature, chunks):
    '''
    \b
    This script will take FILENAME (FASTA formatted file), and produce summary stats for each sequence in the file.
    '''
    seqs = SeqIO.parse(filename, format  = 'fasta')
    sep = parse_sep(delim)
    print_header(sep)
    group = SummaryGroup(sort, sep, by, desc)
    for s in seqs:
        group.add(s)
    if sort:
        group.arrange()
        for s in group.sequences:
            print(s)
    group.summarise()
    group.chunk_stats(n_chunks = chunks, feature = feature)
    group.get_blocks(feature)

if __name__ == '__main__':
    main()
