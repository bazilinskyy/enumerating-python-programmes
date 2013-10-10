 #!/usr/bin/env python3
# -*- coding: utf-8 -*- 

'''
Created on Oct 6, 2013

@author: Pavlo Bazilinskyy <PAVLO.BAZILINSKYY.2013@nuim.ie>
'''

import builtins
from itertools import product
import time
import os.path

########## CONFIGURATION ##########
OUTPUT_FOUND_NOTIFICATION           = False
OUTPUT_SYNTAX_CHECK_ERRORS          = False
OUTPUT_FOUND_PROGRAMS               = True
OUTPUT_PROGRAM_CANDIDATES           = False
OUTPUT_TIMESTAMPS                   = True
OUTPUT_STATS_ON_TIMESTAMPS          = True
OUTPUT_STATS_ON_LEN_OF_PROGRAMS     = True
SHOW_STATS_AFTER                    = 1000000
STARTING_LETTER                     = 'a'
FINISHING_LETTER                    = 'z'
USE_UPPERCASE                       = True
MAX_LENGTH_PROGRAM                  = -1    # -1 indicates that a program will run in an infinite loop,
                                            # incrementing length of generated program candidates in each iteration.
OUTPUT_TO_FILE                      = True 
FILE_NAME                           = "found_programs.txt"  # Name of the file for outputting found programs
####################################

########### CONFIGURATION ##########
numberTries = 0                 # Count number of tries
programsFound = 0               # Count a number of programs found
numCharGenerate = 1             # Start processing strings of this length. Updated when a file is loaded.
foundProgramsByLength = dict()  # Dictionary of numbers of found programs in the current session, sorted by length
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
    alphabet = ''.join(sorted(alphabet))
    return alphabet

# Receive letters in range [startLetter,finishLetter] as a generator.
def getLettersInRange(startLetter='a', finishLetter='z'):
    for number in range(ord(startLetter), ord(finishLetter) + 1):
        yield chr(number)

# Tries to compile programCandidate. If compilation is unsuccessful, an  exception is raised.        
def tryCompile(programCandidate):
    builtins.compile(programCandidate, "test_script.py", 'exec')
        
# Print output to the console
def printFoundProgram(program):
    if OUTPUT_FOUND_NOTIFICATION:
        print("\n--- Program number", programsFound, "was found. It is", len(program), "characters long. Total number of tries so far:", numberTries)
    if OUTPUT_FOUND_PROGRAMS:
        print("Ж", program)

# Append output to the file
def appendToFile(programCandidate):
    try:
        f = open(FILE_NAME, "a")
        f.write("Ж ")
        f.write(str(programsFound))
        f.write("/")
        f.write(str(numberTries))
        f.write(": ")
        f.write(programCandidate)
        f.write("\n")
        f.close()
    except IOError as xxx_todo_changeme:
        (errno, strerror) = xxx_todo_changeme.args
        print("I/O error({0}): {1}".format(errno, strerror))
        
# Load last session from the file and continue from there
def loadFromFile():
    global programsFound
    global numCharGenerate
    global numberTries
    
    # Check if file exists:
    try:
        open(FILE_NAME)
        # Now check if is not empty
        if (os.path.getsize(FILE_NAME) <= 0):
            raise IOError
    except IOError:
        return False # Return False if there is no file to load
    
    # First retrieve the last line in the file to find where program was stopped.
    lastString = returnLastLineTextFile(FILE_NAME)
    
    # Find occurrence of the first digit with a regex
    import re
    m = re.search(b"\d", lastString)
    if m:
        programsFound = int(lastString[m.start() : lastString.find(b'/')])   # Redefine a number of found programs based on the value in the last line of the file
        numCharGenerate = len(lastString[lastString.find(b':') : ]) - 3      # Set length of the string to work with to the value from the file
        numberTries = findNumberOfTriesBeforeGivenLength(FILE_NAME, numCharGenerate) # Update a number of attempts based on the last string of (last processed length of string - 1)
        return lastString[lastString.find(b'/') + 1 :  lastString.find(b':')] # Return number of the last try
    else:
        return False
    
# Find out a number of tries attempted before reaching the first string of given length
def findNumberOfTriesBeforeGivenLength(f, length):
    with open(f, 'r') as inF:
        for line in inF:
            if (len(line[line.find(':') : ]) - 3) == length: # Find the first string with a program candidate of given length
                return int(line[line.find('/') + 1 :  line.find(':')]) - 1
    return False
                
    
# Return the last line from a text file.
# From http://stackoverflow.com/questions/3346430/most-efficient-way-to-get-first-and-last-line-of-file-python
def returnLastLineTextFile(f):
    with open(f, 'rb') as fh:
        offs = -100
        while True:
            fh.seek(offs, 2)
            lines = fh.readlines()
            if len(lines)>1:
                last = lines[-1]
                break
            offs *= 2
        return last
    
# Main function
if __name__ == '__main__':
    print("--- Enumerating python programs by Pavlo Bazilinskyy <PAVLO.BAZILINSKYY.2013@nuim.ie>")
    # Output language of combinations of all possible symbols that can be inputed from a keyboard in lexicographical order (Sigma*).
    alphabet = getAlphabet()  # Input language
    if OUTPUT_TIMESTAMPS:
        start_time = time.time()
    print("--- Program has started work... Output will come soon.\n")
    
    # Try to load from the file from the previous session
    # If file with previous session was found, simple run while loop for that many times without trying to compile
    numberTriesLoaded = int(loadFromFile()) # Retrieve the last session
    if (numberTriesLoaded):
        print("--- Last saved session loaded successfully.")
    else:
        # Clear file for output
        if OUTPUT_TO_FILE:
            open(FILE_NAME, 'w').close()
    
    # Main loop. It can be exited if MAX_LENGTH_PROGRAM is defined.
    while True:
        if OUTPUT_STATS_ON_LEN_OF_PROGRAMS:
            foundProgramsByLength[str(numCharGenerate)] = 0  # Initialise entry corresponding to current length in the dictionary.
            # Generate all possible words of size numCharGenerate in lexicographical order. 
        for programCandidate in product(getAlphabet(startLetter=STARTING_LETTER, finishLetter=FINISHING_LETTER), repeat=numCharGenerate): 
            numberTries += 1
            # Check if there is any need to compile (this program candidate has not been processed in previous sessions
            if (numberTries <= numberTriesLoaded and numberTriesLoaded != -1):
                continue
            
            # Otherwise process the program candidate
            programCandidate = """""".join(programCandidate) # Make a string representing next program candidate
            if OUTPUT_PROGRAM_CANDIDATES:
                print("\nNEXT PROGRAM CANDIDATE:\n", programCandidate)
            
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
            except SyntaxError as v:  # Program candidate failed to be compiled. Hence, it is not a valid Python program.
                if OUTPUT_SYNTAX_CHECK_ERRORS:
                    print("Syntax error:", v, " in program: ", programCandidate)
            if OUTPUT_TIMESTAMPS and numberTries % SHOW_STATS_AFTER == 0:  # Output timestamp after analysing every 1000000 candidates.
                print("\n--- %.0f seconds elapsed." % (time.time() - start_time))
                if OUTPUT_STATS_ON_TIMESTAMPS:
                    print("--- Programs found                :", programsFound)
                    print("--- Program candidates generated  :", numberTries)
                if OUTPUT_STATS_ON_LEN_OF_PROGRAMS:
                    print("--- Numbers of programs of different length found in this session:", foundProgramsByLength)
                
        if (MAX_LENGTH_PROGRAM != -1 and numCharGenerate >= MAX_LENGTH_PROGRAM):
            break
        numCharGenerate += 1
    
    # Output some statistics
    print("A total number of possible Python programs found:", programsFound)
    print("A total number of program candidates generated  :", numberTries)
        
        
