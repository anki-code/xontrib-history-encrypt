<p align="center">
History backend that encrypt the xonsh shell commands history file<br> to prevent extracting sensitive data from the commands history <br>(keys, passwords, hosts, names).
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

## Encryption type

You can set the encryption type before loading the xontrib:

* `$XONSH_HISTORY_ENCRYPT_TYPE = 'base64'` (default) - command's text encoding but without encryption. It can save from 
thoughtless full file system scanning for keywords (i.e. password, key) as well as the reading by not experienced user 
who trying to read history file. 

* More strong solutions are in the future. Feel free to help.

## Known issues

### Work in progress

The xontrib now is in proof of concept stage and you can faced with speed issues or another. 
Your thought and PRs are appreciated.

### The history will be not saved in case of xonsh crash

The current implementation of history management is simple and when xonsh crash the history will be lost too. 
Use `history flush` command to force writing to the disk before experiments.

## Credits

* This package is the part of [ergopack](https://github.com/anki-code/xontrib-ergopack) - the pack of ergonomic xontribs.
* This package was created with [xontrib cookiecutter template](https://github.com/xonsh/xontrib-cookiecutter).
