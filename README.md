# CSS576FinalProject

## Requirements
This project is dependent upon the user having sendmail and libmilter dependencies installed. 
See: https://github.com/sdgathman/pymilter
Python milter extension: https://pypi.python.org/pypi/pymilter/ Python: http://www.python.org Sendmail: http://www.sendmail.org

## Setup
See the sendmail README for all dependencies including sendmail, libmilter, pymilter.

1. Build and install Sendmail, enabling libmilter (see libmilter/README).  
2. Build and install Python, enabling threading.  
3. Install this module: python setup.py --help  
4. Add these two lines to sendmail.cf[a]:  
``` 
O InputMailFilters=pythonfilter
Xpythonfilter,        S=local:/home/username/pythonsock
```  
5. Run the main.py filter milter with: python main.py  
Note: that milters should almost certainly not run as root.
