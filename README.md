# fastats
Generate quick FASTA stats

# Use case
You have a multi-FASTA file, and you wish to have some summary stats for each
sequence in file.

# How to install it
The easiest way of installing `fastats` is using `pip`:

`pip install git+https://github.com/andersgs/fastats.git`

Use the `--user` option to install locally:

`pip install --user git+https://github.com/andersgs/fastats.git`

Use the `--install-option` to install the script in a particular location:

`pip install --install-option="--install-scripts=$HOME/bin" --user git+https://github.com/andersgs/fastats.git`

Once installed type the following:

`fastats --help`

## Dependencies

* [Click](http://click.pocoo.org/5/)
* [BioPython](http://biopython.org)

# Options
* `-s/--sort`: sort the output by a particular column
* `--by`: specify column to sort on (default: `geecee`)
* `--desc`: sort by descending mode
* `-d/--delim`: change column delimter (default: `|`)

# Output

## To stdout
A header, followed by one line per sequence in the FASTA file with:

* *ID*: sequence ID
* *Length*: sequence length
* *GeeCee*: Percent GC
* *A, T, C, G*: Count of canonical bases
* *N*: Count of Ns
* *-*: Count of gaps

## To stderr
* One line per sequence confirming it was successfully parsed.
* A summary line containing total number of sequenced parsed, mean length, and mean GC
* A summary line containing the mean count of A, T, C, G, N, and -

# Examples

## Simplest form
    fastats in.fasta

## Sort by GC content
    fastats --sort --by geecee in.fasta

## Change to TAB delimited output
    fastats --delim '\t' in.fasta
