#!/bin/bash

# getting help
man command

# directory listings and navigation
ls
ls -alh
cd
cd dir
cd ..

# displaying and combining files
cat file
more file
less file
cat file1 file2


# streams: redirection of standard input/output
program < input
program > output
program1 | program2

# special characters: *, ?, $
# quoting/escaping: ', "

# basic searching and line count
grep pattern file
wc file
wc -l file