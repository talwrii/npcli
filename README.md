# Npcli
Interact with Python's numpy package from the command line. Useful as part of pipelines.

# Attribution

Influenced by and liberally taking ideas from from Wes Turner's [pyline](https://github.com/westurner/pyline) utility.

# Motivation

Command line pipelines are wonderful things. Some nice properties include:

* Complete searchable history of everything you have run
* Being able to use commands you already know instead of libraries that may not exist
* Being able to compose disparate commands through string input and output
* Completion

However the command line is sometimes slightly... lacking. Particularly when it comes to
things like maths. There are ad-hoc, single purpose commands that can help, things like
`feedgnuplot` or `sum` or similar, but they will always only solve one problem.

Here we try to solve a general class of problems by welding python (any numpy)
to the command line so that anything you can do in python can be done
in a way that easily interacts with a the command line.

# Examples

```
# The squares of the numbers 1 to 100
seq 100 | npcli 'd**2'

# Work out the mean of some random numebrs
npcli 'np.random.random(10000)' -m numpy.random | npcli 'np.mean(d)'

# Plot a graph
seq 100 | npcli -nK 'pylab.plot(d); pylab.show()'

# Produce a histogram of when most lines in syslog are printed
sudo cat /var/log/syslog | cut -d " "  -f 1-4 | xargs -L 1 -I A date -d  A  +%s | npcli 'd % 86400' | npcli 'd // 3600 * 3600' | uniq -c  | npcli -Kn 'pylab.plot(d[:,1], d[:,0]); pylab.show()'

# Generate some random data
npcli -K 'random(100)'

# Summarize the last 100 days of GOOG's share price
curl "http://real-chart.finance.yahoo.com/table.csv?s=GOOG" | head -n 100 | npcli  -I pandas  'd["Close"].describe()' -D

# Chain together operations
seq 10 | npcli  'd' -e 'd*2' -e 'd + 4' -e 'd * 3' -e 'd - 12'  -e 'd / 6'

# Multiple data sources
npcli --name one <(seq 100) --name two <(seq 201 300) 'one + two'

```

# Just open a file for goodness sake

It is very easy to do more on the command line that you should.
Most programming languages are Turing-Complete and everything that is done
here can be done in a python file with subprocesses. Above a certain size one-liners
become unwieldy

The cost of doing this is that you actually have to go to the effort of opening file,
and doing these sort of things in files can take a lot of typing.

You also lose the simplicity of the "modify", "press enter", "see if it works" cycle
that the command line gives you.

# Usage

```
usage: make-readme.py [-h] [--expr EXPR] [--code] [--debug]
                      [--input-format INPUT_FORMAT] [--kitchen-sink]
                      [--name NAME NAME]
                      [--output-format OUTPUT_FORMAT | --raw | --repr | --no-result]
                      [--module MODULE] [-f data_source]
                      expr [data_sources [data_sources ...]]

Interact with numpy from the command line

positional arguments:
  expr                  Expression involving d, a numpy array
  data_sources          Files to read data from. Stored in d1, d2 etc

optional arguments:
  -h, --help            show this help message and exit
  --expr EXPR, -e EXPR  Expression involving d, a numpy array. Multipe
                        expressions get chained
  --code                Produce python code rather than running
  --debug               Print debug output
  --input-format INPUT_FORMAT, -I INPUT_FORMAT
                        Dtype of the data read in. "lines" for a list of
                        lines. "str" for a string. "csv" for csv, "pandas" for
                        a pandas csv
  --kitchen-sink, -K    Import a lot of useful things into the execution scope
  --name NAME NAME, -N NAME NAME
                        A named data source
  --output-format OUTPUT_FORMAT, -O OUTPUT_FORMAT
                        Output as a flat numpy array with this format. "str"
                        for a string
  --raw                 Result is a string that should be written to standard
                        out
  --repr, -D            Output a repr of the result. Often used for _D_ebug
  --no-result, -n       Discard result
  --module MODULE, -m MODULE
                        Result is a string that should be written to standard
                        out
  -f data_source

```

# Alternatives and prior work

* *xargs*
* *awk*
* *perl command line invocation*
* *pyline*
* *pyp*
* *Rio* - A similar tool in R (that gives you access to the marverlously succinct ggplot!)

# Caveats

`npcli` uses `argparse`.
`argparse` appears to be not be able to deal with repeated flags (`-e 1 -e second`) and repeated optional position args (i.e. data sources), it may error out when given valid input.
This can be circumvented by using the `-f` flag in preference to positional arguments.
However, we still allow positional arguments in the interest of discoverability.
I'm open to this being a bad decision.

# Contributing

There are unit tests: you can run them with

```
python setup.py test
```

This run the tests with `tox` for a quicker test run use:

```
nosetests test
```
