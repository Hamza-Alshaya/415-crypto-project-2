# Program information:

### How to run:
1. From the parent directory, run the Certificate authority server first.

`$ python cryptography/ca.py`

2. On a different terminal, run the Alice instance from the same parent directory.

`$ python alice.py`

2. On a third terminal, run the Bob instance from the same parent directory.

`$ python bob.py`

### Libraries and dependencies:
- flask         **(for running the CA http server)**
- pycryptodome  **(used for generating large prime numbers and for performance evaluation)**
- hashlib (included with python)    **(used for evaluating hash performance)**       

### Tested environment(s)/package(s) version(s)
- Windows 11 + MSYS2, running MINGW64_NT-10.0-22631: 3.5.4-0bc1222b.x86_64 2024-09-04 18:28 UTC x86_64 Msys
- Python                3.11.9
- pycryptodome          3.21.0
- Flask                 3.0.2


***The scripts were also tested on a Linux ARM machine running a Debian GUI OS with Python3. The packages were installed via the Operating system's package manager, "apt".***
