#!/bin/bash
#
# file: enron_naive_bayes.sh
#
#
# description: primitive implementation of naive bayes for the enron
#   email data set. downloads a sample file from the enron data set,
#   uncompresses it, and then does one-word naive bayes estimation.
#
#
# usage: ./enron_naive_bayes.sh <word>
#
#     e.g. ./enron_naive_bayes.sh money
#
#   (be sure to make the script executable with "chmod +x")
#
# requires: the wget utility to fetch the enron1.tar.gz data file.
#   replace wget (below) with "curl -O" if curl is preferred, or the
#   file can be manually downloaded to the working directory
#
# author: jake hofman (gmail: jhofman)
#

# how to use the code
if [ $# -eq 1 ]
    then
    word=$1
else
    echo "usage: enron_naive_bayes.sh <word>"
    echo
    echo "e.g. ./enron_naive_bayes.sh money"
    exit
fi

# if the file doesn't exist, download the .tar.gz
if ! [ -e enron1.tar.gz ]
    then
    echo "retrieving data ... "
    wget 'http://www.aueb.gr/users/ion/data/enron-spam/preprocessed/enron1.tar.gz'
fi

# if the directory doesn't exist, uncompress the .tar.gz
if ! [ -d enron1 ]
    then
    echo "uncompressing data ... "
    tar zxf enron1.tar.gz
fi

# change into enron1
cd enron1

# get counts of total spam, ham, and overall msgs
Nspam=`ls -l spam/*.txt | wc -l`
Nham=`ls -l ham/*.txt | wc -l`
Ntot=$Nspam+$Nham

echo $Nspam spam examples
echo $Nham ham examples

# get counts containing word in spam and ham classes
Nword_spam=`grep -il $word spam/*.txt | wc -l`
Nword_ham=`grep -il $word ham/*.txt | wc -l`

echo $Nword_spam "spam examples containing $word"
echo $Nword_ham "ham examples containing $word"

# calculate probabilities using bash calculator "bc"
#
# note: floating point arithmetic is a bit awkward in bash, done with
# bc, the "bash calculator". as pointed out after class, one can use
# zshell (zsh) which natively supports floating point operations.
#
Pspam=`echo "scale=4; $Nspam / ($Nspam+$Nham)" | bc`
Pham=`echo "scale=4; 1-$Pspam" | bc`
echo "P(spam) =" $Pspam
echo "P(ham) =" $Pham

Pword_spam=`echo "scale=4; $Nword_spam / $Nspam" | bc`
Pword_ham=`echo "scale=4; $Nword_ham / $Nham" | bc`
echo "P($word|spam) =" $Pword_spam
echo "P($word|ham) =" $Pword_ham

Pspam_word=`echo "scale=4; $Pword_spam*$Pspam" | bc`
Pham_word=`echo "scale=4; $Pword_ham*$Pham" | bc`
Pword=`echo "scale=4; $Pspam_word+$Pham_word" | bc`
Pspam_word=`echo "scale=4; $Pspam_word / $Pword" | bc`
echo "P(spam|$word) =" $Pspam_word

# return to original directory
cd ..