<p align="center">
History backend that encrypt the xonsh shell commands history file<br> to prevent leaking sensitive data from the commands history <br>(keys, passwords, hosts, names).
</p>

<p align="center">  
If you like the idea click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=History%20backend%20for%20xonsh%20shell%20that%20encrypt%20the%20history.&url=https://github.com/anki-code/xontrib-history-encrypt" target="_blank">tweet now</a>.
</p>


## Installation

To install use pip:

```bash
xpip install xontrib-history-encrypt
# or: xpip install -U git+https://github.com/anki-code/xontrib-history-encrypt
```

## Usage: supported encryption

### Base64 (default)

Base64 is not the real encrypter and implemented as fast way to encode history file and for education reasons.
It can save you from the massive scanning the file system for keywords (i.e. password, key) 
as well as reading the history file by not experienced user. But it can be decoded in five minutes by the professional.

```python
# Add to xonsh RC file
$XONSH_HISTORY_ENCRYPTOR = 'base64'
xontrib load history_encrypt
```

### Fernet 

The implementation of [Fernet](https://cryptography.io/en/latest/fernet.html) (AES CBC + HMAC) that was strongly 
recommended on [stackoverflow](https://stackoverflow.com/a/55147077). On first start it generates a key that you 
should save in secure place. Than you can use this key to decrypt the history.

```python
# Add to xonsh RC file
$XONSH_HISTORY_ENCRYPTOR = 'fernet'
xontrib load history_encrypt
```

### Custom 

```python
from xontrib.history_encrypt.fernet import *

$XONSH_HISTORY_ENCRYPTOR = {
  'key': fernet_key,
  'enc': lambda data, key: fernet_encrypt(data.encode(), key).decode(),
  'dec': lambda data, key: fernet_decrypt(data.encode(), key).decode()  
}
xontrib load history_encrypt
```

## What should I know?

### How to check the backend is working

```bash
history info
# backend: xontrib-history-encrypt
# sessionid: 374eedc9-fc94-4d27-9ab7-ebd5a5c87d12
# filename: /home/user/.local/share/xonsh/xonsh-history-encrypt.txt
# commands: 1
```

### Some points about the backend

* At start the backend read and decrypt all commands and this could take time. Basically we assume that you will use the xontrib on your servers and haven't so big history.

* The commands are stored in the memory and flush to the disk at the exit from the shell. If the shell has crash there is no flushing to the disk and commands will be lost. Use `history flush` command if you plan to run something experimental.

* The backend has minimal history management support in comparing with json or sqlite backends and you can find the lack of features.

If you want to improve something from the list PRs are welcome!

## Credits

* This package is the part of [ergopack](https://github.com/anki-code/xontrib-ergopack) - the pack of ergonomic xontribs.
* This package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).
