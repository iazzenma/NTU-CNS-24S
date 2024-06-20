Before executing the codes, please make sure you have the following packages:
pwn, math, itertools, sys, base64, Crypto.Util.number, gmpy2, binascii, hashlib, HashTools

python3 code5.py [Username]
    for Username = bob: solve the rail-fence cipher with a online tool, and then manually enter the action 2 and the passphrase. 
    for Username = eve: check the file eve.txt, find the line containing only meaningful words, and then manually enter the action 3 and the passphrase. 
    for Username = admin: check the file admin.txt, find the line containing only meaningful words, which is the flag.

python3 code[6c,7a,7b].py
python3 code8.py: because of the relative path problem, be sure to run this code with current working directory being b11902008/code.  

credit: https://docs.xanhacks.xyz/crypto/rsa/08-hastad-broadcast-attack/
6b.py used several functions from the code in the above website