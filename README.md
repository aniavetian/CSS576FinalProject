# CSS576FinalProject

## Requirements
This project is dependent upon the user having sendmail and libmilter dependencies installed. 
See: https://github.com/sdgathman/pymilter  
See: https://pythonhosted.org/milter/
Python milter extension: https://pypi.python.org/pypi/pymilter/ Python: http://www.python.org Sendmail: http://www.sendmail.org

### Python and Sendmail Requirements
- The email support requires python 2.4.
- Python must be configured with thread support. This is because pymilter uses sendmail's libmilter which requires thread support.
- You must compile sendmail with libmilter enabled. In versions of sendmail prior to 8.12 libmilter is marked FFR (For Future Release) and is not installed by default. Sendmail 8.12 still does not enable libmilter by default. You must explicitly select the "MILTER" option when compiling.
- When compiling Python milter against sendmail versions earlier than 8.13, you must set MAX_ML_REPLY to 1 in setup.py. There is no way to tell from the libmilter includes that smfi_setmlreply is not supported.
- Python milter has been tested against sendmail-8.11 through sendmail-8.13.
- Python milter must be compiled for the specific version of sendmail it will run with. (Since the result is dynamically loaded, there could conceivably be multiple versions available and selected at startup - but that will have to wait.) This situation may only exist for sendmail versions prior to 8.12. The protocol seems designed for backward compatibility - and 8.12 is the first official milter release.

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
