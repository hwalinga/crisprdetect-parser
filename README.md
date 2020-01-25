# CRISPRDetect Parser

In this repo you can find a parser that extracts the spacers and the metadata
from a CRISPRDetect output file.

# Usage

You can use the program as such: (NB. Here I use the extension `.crisprdetect`. You can have a different extension.):

```sh
$ python crisprdetectparser.py -s spacers genome1.crisprdetect genome2.crisprdetect > metadata.tsv
```

This will process all the arrays in genome1 and genome2. Puts the spacers in the
spacers folder and will output to metadata.tsv.

If you have a lot files, use wildcards:

```sh
$ python crisprdetectparser.py -s spacers *.crisprdetect{,.fp} > metadata.tsv
```

If you really have a lot of files, use `xargs`. 

```sh
$ find . -name '*.crisprdetect' -o -name '*.crisprdetect.fp' | xargs python crisprdetectparser.py -s spacers > metadata.tsv
```

# More help

For more detailed instructions on the command-line arguments:

```sh
$ python crisprdetectparser.py --help
```

----

```
usage: CRISPRDetect parser [-h] [--spacers-directory [SPACERS_DIRECTORY]]
                           [--out OUT] [--sep SEP]
                           [--crisprdetect-extension CRISPRDETECT_EXTENSION]
                           [--spacers-extension SPACERS_EXTENSION] [--header]
                           [--force]
                           [files [files ...]]

Run this progrom on CRISPRDetect output files to extract the spacers and the
metadate about the CRISPR arrays. The program can process the CRISPR array
files with sufficient quality score, but also the array files with a score
below the required quality score (with the .fp extension).

positional arguments:
  files                 All the crisprdetect(with or without .fp) output
                        files.

optional arguments:
  -h, --help            show this help message and exit
  --spacers-directory [SPACERS_DIRECTORY]
                        Create spacers folder. Creates a folder with fasta
                        files that contain the spacer sequences for each
                        genome. Leave out if you don't want to extract the
                        spacers.
  --out OUT             Output file, if left out, this will be stdout. If file
                        already exist it will append.
  --sep SEP             Seperator in the metadata file. (Default: tab)
  --crisprdetect-extension CRISPRDETECT_EXTENSION
                        Extension of crisperdetect files that is cut off for
                        genome name. (Default: crisprdetect)
  --spacers-extension SPACERS_EXTENSION
                        Extension string of the spacers fasta file. (Default:
                        spacers.fna)
  --header              Output file with a header: genome contig array_id
                        begin end orientation number_of_spacers array_family
                        quality_score repeat_sequence
  --force               Overwrite existing files.
```

# Install CRISPRDetect

Get the most recent version of CRISPRDetect from http://crispr.otago.ac.nz/CRISPRDetect/CRISPRDetect_help.html

This program only works on a unix system (OSX, Linux, BSD). 

You could install dependencies using brew (https://brew.sh/):

```sh
$ brew install blast emboss cd-hit viennarna clustal-w 
```

However, the program already bundles pre-compiled versions of these dependencies, so you can also add these to your PATH. (The only one you have to install yourself is blast.)

NB. The perl program uses an external grep command a few times. If you have 
genome names that can be interpreted as regex, this will create incorrect output. 
Therefore it is best if the external grep command uses the -F flag. You can change that 
in the program using:

```sh
$ sed -i 's/grep/grep -F/g' CRISPRDetect.pl
$ sed -i 's/grep -w '\''\$a/grep -wF '\''\$a/g; s/grep '\''\$a/grep -F '\''\$a/g' CD_MODULES/CRISPRDETECT_SUBS_1.pm 
```

Instead of trying to download CRISPRDetect from the above link (which can be
tricky sometimes as the server is in New Zealand), you can also get the program
from this repo. It is located in the `CRISPRDetect_2.4_grep_patched` folder
and also has the grep patch applied to it. 
