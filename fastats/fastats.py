'''
'''

from Bio import SeqIO
from Bio import SeqUtils
import click

bases = ['A', 'T', 'C', 'G', 'N', '-']

class SeqSummary:
    bases = ['A', 'T', 'C', 'G', 'N', '-']
    def __init__(self, seqrec, sep = '|'):
        self.__dict__ = {}
        self.sep = sep
        self.s = seqrec.upper() # makes sure comparison is always in upper case
    def __str__(self):
        out = self.sep.join(map(str,[self.id, \
            self.length, \
            '{:.3}'.format(self.geecee), \
            self.counts['A'],
            self.counts['T'],
            self.counts['C'],
            self.counts['G'],
            self.counts['N'],
            self.counts['-']]))
        return out
    def summarise(self):
        self.__dict__['id'] = self.s.id
        self.__dict__['length'] = len(self.s)
        self.__dict__['geecee'] = SeqUtils.GC(self.s.seq)
        self.__dict__['counts'] = {}
        for b in self.bases:
            self.__dict__['counts'][b] = self.s.seq.count(b)

class SummaryGroup:
    def __init__(self, by, desc = False):
        self.by = by
        self.desc = desc
        self.__dict__ = {}


def print_header(sep = '|'):
    header = sep.join(['ID','LENGTH', 'GEECEE', 'A', 'T', 'C', 'G', 'N', '-' ])
    print(header)

def calc_summary(seqrec, sep):
    seq = SeqSummary(seqrec, sep)
    seq.summarise()
    print(seq)

def parse_sep(sep):
    '''
    If passing a \t Python interprets it as \\t
    '''
    if sep == '\\t':
        sep = '\t'
    return sep

@click.command()
@click.option('-d', '--delim', default='|', show_default = True, metavar = '<char>', help = 'Set separator character.')
@click.option('-s', '--sort', is_flag = True)
@click.option('--by', default = 'geecee', show_default = True, type = click.Choice(['geecee', 'length', 'N', '-', 'A', 'T', 'C', 'G']), help = 'Sort by column.')
@click.option('--desc', is_flag = True, help = 'Sort by descending order.')
@click.argument('filename')
def main(filename, delim, sort, by, desc):
    '''

    '''
    seqs = SeqIO.parse(filename, format  = 'fasta')
    sep = parse_sep(delim)
    for s in seqs:
        calc_summary(s, sep)

if __name__ == '__main__':
    main()
