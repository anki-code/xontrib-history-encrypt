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

## Usage

```bash
xontrib load history_encrypt
# Now your commands will be managed by xontrib-history-encrypt.

history info
# backend: xontrib-history-encrypt
# sessionid: 374eedc9-fc94-4d27-9ab7-ebd5a5c87d12
# filename: /home/user/.local/share/xonsh/xonsh-history-encrypt.txt
# commands: 1
```

## Supported encryption

You can set the encryption type before loading the xontrib:

* `$XONSH_HISTORY_ENCRYPTOR = 'base64'` (default) - command's text encoding but without encryption. 
  It can save from the massive scanning the file system for keywords (i.e. password, key) as well as reading the history file by not experienced user. 
  And yes, it can be decoded in five minutes.

To more strong encryption use custom encryption like in the demo below.

## Custom encryption demo 

Here is the implementation of [Fernet](https://cryptography.io/en/latest/fernet.html) (AES CBC + HMAC) that was strongly 
recommended on [stackoverflow](https://stackoverflow.com/a/55147077). It will be the part of this xontrib in the future.

Add this to the RC file i.e. `/tmp/rc`:

```python
from cryptography.fernet import Fernet

def fernet_key():
    print('[xontrib-history-encrypt] Enter the key or press enter to create new: ', end='')
    key = input()
    if not key.strip():
      key = Fernet.generate_key()
      print('[xontrib-history-encrypt] Save the key and use it next time: ', key.decode())
    return key 

def fernet_encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def fernet_decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

$XONSH_HISTORY_ENCRYPTOR = {
  'key': fernet_key,
  'enc': lambda data, key: fernet_encrypt(data.encode(), key).decode(),
  'dec': lambda data, key: fernet_decrypt(data.encode(), key).decode()  
}
xontrib load history_encrypt
```
Then run the xonsh shell:
```python
bash
xonsh --rc /tmp/rc
# [xontrib-history-encrypt] Enter the key or press enter to create new: <Enter>
# [xontrib-history-encrypt] Save the key and use it next time: q_eaCZ01bt_9lUQPZIhE6WvOeKUq0S2L4A7crxCZrCU=
echo 1
# 1
echo 2
# 2
exit

xonsh --rc /tmp/rc
# [xontrib-history-encrypt] Enter the key or press enter to create new: q_eaCZ01bt_9lUQPZIhE6WvOeKUq0S2L4A7crxCZrCU=
# History loaded!
```

## Known issues

### The history will be not saved in case of xonsh crash

The current implementation of history management is simple and when xonsh crash the history will be lost too. 
Use `history flush` command to force writing to the disk before experiments.

## Credits

* This package is the part of [ergopack](https://github.com/anki-code/xontrib-ergopack) - the pack of ergonomic xontribs.
* This package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).
