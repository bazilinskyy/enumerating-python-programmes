#!/usr/bin/env python
# -*- coding: utf-8 -*- 

'''
Created on Oct 6, 2013

@author: Pavlo Bazilinskyy <PAVLO.BAZILINSKYY.2013@nuim.ie>
'''

import __builtin__
from itertools import product
import time


# start where it left off, bug with all false, output just programs
########## CONFIGURATION ##########
OUTPUT_FOUND_NOTIFICATION = False
OUTPUT_SYNTAX_CHECK_ERRORS = False
OUTPUT_FOUND_PROGRAMS = True
OUTPUT_HASH_PLACEHOLDER = False
OUTPUT_TIMESTAMPS = False
OUTPUT_STATS_ON_TIMESTAMPS = False
OUTPUT_PROGRAM_CANDIDATES = False
OUTPUT_STATS_ON_LEN_OF_PROGRAMS = False
STARTING_LETTER = 'a'
FINISHING_LETTER = 'z'
USE_UPPERCASE = True
MAX_LENGTH_PROGRAM = -1  # -1 indicates that a program will run in an infinite loop,
                                        # incrementing length of generated program candidates in each iteration.
OUTPUT_TO_FILE = True 
FILE_NAME = "found_programs.txt"  # Name of the file for outputting found programs
####################################

########### CONFIGURATION ##########
numberTries = 0  # Count number of tries
programsFound = 0  # Count a number of programs found
####################################

# Generate alphabet consisting of all letters of English alphabet, digits, special symbols.
def getAlphabet(startLetter='a', finishLetter='z', digits=True, symbols=True):
    alphabet = ''.join(getLettersInRange(startLetter, finishLetter))
    if digits:  # Add digits to the alphabet.
        alphabet += "0123456789"
    if symbols:  # Add all the special characters.
        alphabet += "+-=%&|^#.,;:(){}[]!*/\?~_ \t\n"
    if USE_UPPERCASE:  # Also add uppercase letters, if required.
        alphabet += ''.join(getLettersInRange(startLetter.upper(), finishLetter.upper()))
    return alphabet

# Receive letters in range [startLetter,finishLetter] as a generator.
def getLettersInRange(startLetter='a', finishLetter='z'):
    for number in xrange(ord(startLetter), ord(finishLetter) + 1):
        yield chr(number)

# Tries to compile programCandidate. If compilation is unsuccessful, an  exception is raised.        
def tryCompile(programCandidate):
    __builtin__.compile(programCandidate, "test_script.py", 'exec')
        
# Print output to the console
def printFoundProgram(program):
    if OUTPUT_HASH_PLACEHOLDER:
        print "\n\n######################################################################################################"
    if OUTPUT_FOUND_NOTIFICATION:
        print "Program number", programsFound, "was found. It is", len(program), "characters long. Total number of tries so far:", numberTries
    if OUTPUT_HASH_PLACEHOLDER:
        print "######################################################################################################"
    if OUTPUT_FOUND_PROGRAMS:
        print "Ж", program

# Append output to the file
def appendToFile(programCandidate):
    try:
        f = file(FILE_NAME, "a")
        f.write("Ж ")
        f.write(str(programsFound))
        f.write(": ")
        f.write(programCandidate)
        f.write("\n")
        f.close()
    except IOError as (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)

# Main function
if __name__ == '__main__':
    print "Enumerating Python programs by Pavlo Bazilinskyy <PAVLO.BAZILINSKYY.2013@nuim.ie>"
    # Output language of combinations of all possible symbols that can be inputed from a keyboard in lexicographical order (Sigma*).
    alphabet = getAlphabet()  # Input language
    if OUTPUT_TIMESTAMPS:
        start_time = time.time()
    numCharGenerate = 1  # Words of which length to generate inn the current itteration of the loop.
    print "Program has started work... Output will come soon.\n"
    
    # Clear file for output
    if OUTPUT_TO_FILE:
        open(FILE_NAME, 'w').close()
    
    if OUTPUT_STATS_ON_LEN_OF_PROGRAMS:
        foundProgramsByLength = dict()  # Create dictionary for storing numbers of programs of different langth found.
    
    # Main loop. It can be exited if MAX_LENGTH_PROGRAM is defined.
    while True:
        if OUTPUT_STATS_ON_LEN_OF_PROGRAMS:
            foundProgramsByLength[str(numCharGenerate)] = 0  # Initialise entry correspponding to current length in the dictionary.
            # Generate all possible words of size numCharGenerate in lexicographical order. 
        for programCandidate in product(getAlphabet(startLetter=STARTING_LETTER, finishLetter=FINISHING_LETTER), repeat=numCharGenerate): 
            numberTries += 1
            programCandidate = """""".join(programCandidate)
            if OUTPUT_PROGRAM_CANDIDATES:
                print "\nNEXT PROGRAM CANDIDATE:\n", programCandidate
            
            #===================================================================
            # These two lines can be uncommented to check that the program can work with repeating symbols and it can be used
            # as an argument for proving that the language is created in a lexicographical order.
            #===================================================================
            #if (programCandidate == """1\t1"""):
            #    print "FOUND: ", programCandidate
            
            try:
                tryCompile(programCandidate)  # Compile to see if a program candidate can be seen as a Python program.
                programsFound += 1
                printFoundProgram(programCandidate)  # Print out found program
                if OUTPUT_TO_FILE:  # Output found program to the file
                    appendToFile(programCandidate)
                if OUTPUT_STATS_ON_LEN_OF_PROGRAMS:
                    foundProgramsByLength[str(numCharGenerate)] += 1  # Increment a number of programs found for current length
            except SyntaxError, v:  # Program candidate failed to be compiled. Hence, it is not a valid Python program.
                if OUTPUT_SYNTAX_CHECK_ERRORS:
                    print "Syntax error:", v, " in program: ", programCandidate
            if OUTPUT_TIMESTAMPS and numberTries % 1000000 == 0:  # Output timestamp after analysing every 1000000 candidates.
                print "\n%.0f seconds elapsed." % (time.time() - start_time)
                if OUTPUT_STATS_ON_TIMESTAMPS:
                    print "Programs found                :", programsFound
                    print "Program candidates generated  :", numberTries
                if OUTPUT_STATS_ON_LEN_OF_PROGRAMS:
                    print "Numbers of programs of different length found:", foundProgramsByLength
                
        if (MAX_LENGTH_PROGRAM != -1 and numCharGenerate >= MAX_LENGTH_PROGRAM):
            break
        numCharGenerate += 1
    
    # Output some statistics
    print "A total number of possible Python programs found:", programsFound
    print "A total number of program candidates generated  :", numberTries
        
        
