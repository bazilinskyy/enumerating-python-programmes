'''
Created on Oct 6, 2013

@author: Pavlo Bazilinskyy <PAVLO.BAZILINSKYY.2013@nuim.ie>
'''

import py_compile_no_pyc

if __name__ == '__main__':
    
    while True:
        try:
            py_compile_no_pyc.compile('test_script.py', doraise=True)
            print "OK"
        except py_compile_no_pyc.PyCompileError:
            print "NOT OK"