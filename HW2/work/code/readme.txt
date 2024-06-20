The following list how you should use the executables for each problem.
Make sure that your working directory is `code\`.
Make sure that all the packages are installed. The packages I used are: pwntools, pycryptodome.
SageMath should also be installed. 

5.(b) `python code5b.py`
5.(d) First obtain the private key with `sage code5d_ph.sage`, and then decrypt with `code5d_decrypt.py`.
6.(a) `python code6a.py`
6.(b) `python code6b.py`
6.(c) `python code6c.py`
6.(d) It is a bit complicated for this one. Please execute the files as following:
- Extract the domain name with `python code6d_domain.py`
- Scan for the port with `python code6d_portsacn.py`
- Connect to the service multiple times with `python code6d_get_data.py`
- Solve the ECDLP's with `sage code6d_ecdlp.sage`
- Finally, decode and clean up with `python code6d_decode.py`