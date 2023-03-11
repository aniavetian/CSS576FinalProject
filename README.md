# CSS576FinalProject

## Requirements
This project is dependent upon the user having sendmail and libmilter dependencies installed. 
See: https://github.com/sdgathman/pymilter
Python milter extension: https://pypi.python.org/pypi/pymilter/ Python: http://www.python.org Sendmail: http://www.sendmail.org

## Setup
To use this with sendmail, add the following to sendmail.cf:  
O InputMailFilters=pythonfilter  
Xpythonfilter,        S=local: #local socket name#  
See the sendmail README for libmilter.
