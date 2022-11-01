# BK_Precision1696
Python controller for BK Precision 1696 for ETA experiments  
The goal is to control voltage, current, and time for a 5-step program.  BK Precision offers some help at https://github.com/BKPrecisionCorp/1696B_Series   The series is similar but not identical; although the library of functions should be useful.  Be cautious, there are some typos in the BK library and the move to Python 3 seems to have caused syntax changes.
## To do:  
- detect appropriate COM  
- report COM port number (can we use the getComm from 1696lib?)  
- report COM port baud, etc  
- save programmed values to a text file  
- load programmed values from a text file  
