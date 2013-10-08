'''
Created on Oct 6, 2013

@author: Pavlo Bazilinskyy <PAVLO.BAZILINSKYY.2013@nuim.ie>
'''

import itertools
import __builtin__
import time


###### CONFIGURATION  #############
SHOW_SYNTAX_CHECK_ERRORS    = False
OUTPUT_FOUND_PROGRAMS       = False
OUTPUT_TIMESTAMPS           = True                      

###################################

numberTries = 0 # Count number of tries
programsFound = 0 # Count a number of programs found

# Generate alphabet consisting of all letters of English alphabet, digits, special symbols 
def getAlphabet(startLetter='a', finishLetter='g', digits=True, symbols=True):
    alphabet = ''.join(getLettersInRange(startLetter, finishLetter))
    if digits:
        alphabet += "0123456789"
    if symbols:
        alphabet += "+-=%&|^#.,(){}[]!*/\?~_"
    return alphabet
        
def getLettersInRange(startLetter='a', finishLetter='z'):
    for number in xrange(ord(startLetter), ord(finishLetter)+1):
        yield chr(number)

# Tries to compile programCandidate. If compilation is unsuccessful, an  exception is raised.        
def tryCompile(programCandidate):
    __builtin__.compile(programCandidate, "test_script.py", 'exec')
        
def printFoundProgram(program):
     # Print content of the file
    if OUTPUT_FOUND_PROGRAMS:
        print "\n\n######################################################################################################"
    print "Program number ", programsFound, " was found. It is  ", len(program), " characters long. Total number of tries so far: ", numberTries
    if OUTPUT_FOUND_PROGRAMS:
        print "######################################################################################################"
        print program

if __name__ == '__main__':
    # Output language of combinations of all possible symbols that can be inputed from a keyboard in lexicographical order (Sigma*).
    alphabet = getAlphabet()  # Input language
    if OUTPUT_TIMESTAMPS:
        start_time = time.time()
    for i in range (1, len(getAlphabet())):
        for programCandidate in itertools.permutations(alphabet, i):
            numberTries += 1
            programCandidate = """""".join(programCandidate)
            #programCandidate = """4^_"""
            try:
                tryCompile(programCandidate) # Compile to see if a program candidate can be seen as a Python program.
                programsFound += 1
                printFoundProgram(programCandidate) # Print out found program
            except Exception, v: # Program candidate failed to be compiled. Hence, it is not a valid Python program.
                if SHOW_SYNTAX_CHECK_ERRORS:
                    print "Syntax error:", v, " in program: ", programCandidate
            if OUTPUT_TIMESTAMPS and numberTries % 1000000 == 0: # Output timestamp after analysing every 1000000 candidates.
                print "%.0f seconds elapsed." % (time.time() - start_time)
            
    print numberTries # Output a total number of tries. Not likely to ever be executed.