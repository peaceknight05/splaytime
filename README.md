# splaytime
Python 3 interpreter for the esolong (esoteric language) [Splaytime](https://esolangs.org/wiki/Splaytime).

## Installation

None. Simply have Python 3 installed on your computer and run init.py

## Syntax

`python int.py [-h] [-w] [-v] [-d] [-i INPUT] [-o OUTPUT] file`

`file`: File to interpret.

`-h`, `--help`: Shows the help message.

`-w`, `--show-warnings`: Show warnings (default: False)

`-v`, `--verbose: For debugging`; outputs every instruction that is done. (default: False)

`-d`, `--display-tree`: For debugging; outputs the splay tree at the end. (default: False)

`-i INPUT`, `--input INPUT`: Uses a file as an input source instead of stdin. (default: None)
                      
`-o OUTPUT`, `--output OUTPUT`: Outputs to a file instead of stdout. (default: None)
