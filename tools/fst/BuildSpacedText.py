#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Leonel Figueiredo de Alencar
# leonel.de.alencar@ufc.br

# Usage: python BuildSpacedText.py infile.pairs [foma]

# where the input file is in the Foma's flookup output. 
# The spaced text output is either the default xfst's format or foma's format.
# format. This module can be use to recompile a unrestricted transducer
# into a restricted one (Alencar et al. 2014). The exact procedure for this reduction of complexity
# is described in the following paper:

# Alencar, Leonel F. de et al. JMorpher: A Finite-State Morphological Parser in Java for Android. In: Baptista, Jorge et al. (Eds.). Computational Processing of the Portuguese Language. 11th International Conference, PROPOR 2014. São Carlos/SP, Brazil, October 6-8, 2014. Proceedings. Cham; Heidelberg: Springer, 2014, p. 59-69. 
# (Series: Lecture Notes in Computer Science, Vol. 8775. Subseries: Lecture Notes in Artificial Intelligence) 
# ISBN 978-3-319-09760-2
# http://www.springer.com/computer/ai/book/978-3-319-09760-2?detailsPage=chapter


import re
import os
import sys
from CreateInflectionTagsForParticiples import includeGenderAndNumberTags
# separators
FORMAT={"foma":"\n", "xfst":"\n\n"}
SEPARATOR="+"
SEP_REGEX=r"[+]"
WORDPARSESEP=r"\s+"
# This can be used to parse MWEs with one or more white spaces inside
#WORDPARSESEP=r"\t"
SUFFIX="stxt"

def convert_from_up_format(infile):
	"""
	Converts from input format into output format.
	The first is generated by Foma's up command, the
	former by Foma's flookup utility.
	input format
	====================
	fabricar+V+PRF+1+PL
	fabricámos
	fabular+V+PRF+1+PL
	fabulámos
	fabulizar+V+PRF+1+PL
	fabulizámos

	output format
	===================
	fabricámos	fabricar+V+PRF+1+PL

	fabulámos	fabular+V+PRF+1+PL

	fabulizámos	fabulizar+V+PRF+1+PL

	faccionámos	faccionar+V+PRF+1+PL

	"""
	lines=[line.decode("utf-8").strip() for line in open(infile,"rU").readlines() if line.strip() != ""]
	i=0
	j=1
	c=len(lines)
	f=open("%s.pairs" % infile, "w")
	while (j < c):
		f.write("%s\t%s\n\n" % (lines[j].encode("utf-8"),lines[i].encode("utf-8")))
		i=i+2
		j=j+2

def extract_parts(entry,sep_regex=SEP_REGEX):
	"""Separates word form from analysis string, which is parsed into
	its constitutive elements.
	Output is a list with two elements, the second of which is a list, for example:
	>>> BuildSpacedText.extract_parts("fabricámos	fabricar+V+PRF+1+PL")
	('fabric\xc3\xa1mos', ['fabricar', 'V', 'PRF', '1', 'PL'])
	
	"""
	word,parse=re.split(WORDPARSESEP,entry)
	parts=re.split(sep_regex,parse)
	# To include gender and number tags for past participles (not necessary in DELAF-PB version 2)
	# includeGenderAndNumberTags(word,parts)
	return word,parts

def build_spaced_text_entry(entry):
	"""Builds a string in Foma's spaced-text format from the output of
	the extract_parts function.
	"""
	elements = extract_parts(entry)
	form = elements[0]
	parts = elements[1]
	lemma=" ".join(list(parts[0]))
	features=["%s%s" % (SEPARATOR,feature) for feature in parts[1:]]
	return "%s %s\n%s" % (lemma," ".join(features)," ".join(list(form)))
	
def ignore_line(line):
	return len(line.strip()) > 0 and not line.strip().startswith("#")

def extract_entries(infile):
	return [line.strip().decode("utf-8") for line in open(infile,"rU").readlines() if ignore_line(line)]

def write_entries(entries,outfile,format="xfst"):
	f=open(outfile,"w")
	for entry in entries:
		out=build_spaced_text_entry(entry)
		separator=FORMAT.get(format)
		if out:
			f.write("%s%s" % (out.encode("utf-8"),separator))
	f.close()

def convert(infile,format="xfst"):
	"""
	Converts from input format into Foma's spaced-text format:
	input format
	===================
	fabricámos	fabricar+V+PRF+1+PL

	fabulámos	fabular+V+PRF+1+PL

	fabulizámos	fabulizar+V+PRF+1+PL

	faccionámos	faccionar+V+PRF+1+PL

	foma's spaced-text format
	===================
	f a b r i c a r +V +PRF +1 +PL
	f a b r i c á m o s
	f a b u l a r +V +PRF +1 +PL
	f a b u l á m o s
	f a b u l i z a r +V +PRF +1 +PL
	f a b u l i z á m o s
	f a c c i o n a r +V +PRF +1 +PL
	f a c c i o n á m o s

	xsft's spaced-text format (blank line between pairs)
	===================
	f a b r i c a r +V +PRF +1 +PL
	f a b r i c á m o s

	f a b u l a r +V +PRF +1 +PL
	f a b u l á m o s

	"""
	outfile="%s.%s" % (infile, SUFFIX)
	entries=extract_entries(infile)
	write_entries(entries,outfile,format)

def test():
	user=os.path.expanduser("~")
	root=os.path.join(user,"Dropbox/recursos/unitex_pb/lexc/fst03")
	source="teste.pairs.txt" # TODO: this should be teste.up
	output="%s.converted" % source # TODO: this should be teste.up.pairs
	convert_from_up_format(os.path.join(root,source))
	convert(os.path.join(root,output))

def main(): 
    # default format xfst
    if len(sys.argv) == 2:
        convert(sys.argv[1])
    else:
        convert(sys.argv[1],sys.argv[2])

if __name__ == '__main__':
	main()
