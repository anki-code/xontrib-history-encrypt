import os
import sys
import uuid
import builtins

try:
    import ujson as json
except ImportError:
    import json  # type: ignore

from xonsh.history.base import History

class XontribHistoryEncrypt(History):

    def __init__(self, filename=None, sessionid=None, **kwargs):
        self.debug = __xonsh__.env.get('XONSH_HISTORY_ENCRYPT_DEBUG', False)
        self.lock = False

        self.tqdm = lambda a: a
        if self.debug:
            try:
                from tqdm import tqdm
                self.tqdm = tqdm
            except:
                pass

        encryptor = __xonsh__.env.get('XONSH_HISTORY_ENCRYPTOR', 'base64')
        if type(encryptor) is dict:
            self.key = encryptor['key']
            self.enc = encryptor['enc']
            self.dec = encryptor['dec']
        elif type(encryptor) is str:
            if encryptor == 'disabled':
                self.key = None
                self.enc = lambda data, key=None: data
                self.dec = lambda data, key=None: data
            elif encryptor == 'base64':
                from xontrib.history_encrypt.base64 import base64_encode, base64_decode
                self.key = None
                self.enc = lambda data, key=None: base64_encode(data.encode()).decode()
                self.dec = lambda data, key=None: base64_decode(data.encode()).decode()
            elif encryptor == 'fernet':
                from xontrib.history_encrypt.fernet import fernet_key, fernet_encrypt, fernet_decrypt
                self.key = fernet_key
                self.enc = lambda data, key: fernet_encrypt(data.encode(), key).decode()
                self.dec = lambda data, key: fernet_decrypt(data.encode(), key).decode()
            else:
                printx(f"{{RED}}[xontrib-history-encrypt] Wrong encryptor name '{encryptor}'! History will not be loaded and saved.{{RESET}}")
                self.lock = True
        else:
            printx('{RED}[xontrib-history-encrypt] Wrong encryptor type! History will not be loaded and saved.{RESET}')
            self.lock = True

        if not self.lock:
            self.key = self.key() if callable(self.key) else self.key

        self.sessionid = uuid.uuid4() if sessionid is None else sessionid
        self.buffer = []
        self.gc = None

        if filename is None:
            data_dir = builtins.__xonsh__.env.get("XONSH_DATA_DIR")
            data_dir = os.path.expanduser(data_dir)
            filename_env = __xonsh__.env.get('XONSH_HISTORY_ENCRYPT_FILE', os.path.join(data_dir, 'xontrib-history-encrypt-data.txt'))
            self.filename = filename_env
        else:
            self.filename = filename

        self.inps = None
        self.rtns = None
        self.tss = None
        self.outs = None
        self.last_cmd_rtn = None
        self.last_cmd_out = None
        self.hist_size = None
        self.hist_units = None
        self.remember_history = True

    def append(self, data):
        self.buffer.append(data)

    def items(self, newest_first=False):
        if self.lock:
            return []

        if os.path.exists(self.filename):
            data = []
            first_line = True
            with self.tqdm(open(self.filename, 'r')) as file:
                for line in file:
                    line = line.rstrip()
                    if first_line:
                        try:
                            crypt_mark = self.dec(line, self.key)
                            assert crypt_mark.isdigit()
                        except:
                            printx("{YELLOW}The crypted history file is not matching with crypto algorithm or the key.{RESET}")
                            printx(f"{{YELLOW}}Change the encryption algorithm or the key or remove the history file.{{RESET}}")
                            printx(f"{{YELLOW}}History file: {self.filename}{{RESET}}")
                            printx(f"{{RED}}History has not loaded and will not be saved!{{RESET}}")
                            self.lock = True
                            return []
                        first_line = False
                        continue
                    data.append(json.loads(self.dec(line, self.key)))
            return reversed(data) if newest_first else data
        return []

    def all_items(self, newest_first=False):
        return self.items(newest_first)

    def flush(self, **kwargs):
        if self.lock:
            return

        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                from datetime import datetime
                file.write(self.enc(datetime.now().strftime("%Y%m%d%H%M%S"), self.key) + os.linesep)

            try:
                os.chmod(self.filename, 0o600)
            except Exception as e:
                if self.debug:
                    print(f'Exception while setting permissions to {self.filename}: {e}', file=sys.stderr)
                pass

        with open(self.filename, 'a') as file:
            for data in self.buffer:
                if 'out' in data:
                    del data['out']
                file.write(self.enc(json.dumps(data), self.key) + os.linesep)
        self.buffer = []

    def info(self):
        data = {}
        data["backend"] = "xontrib-history-encrypt"
        if self.lock:
            data["locked"] = "YES! Current session history will not be saved."
        data["sessionid"] = str(self.sessionid)
        data["filename"] = self.filename
        data["commands"] = len(self.buffer)
        return data



encryptor = __xonsh__.env.get('XONSH_HISTORY_ENCRYPTOR', 'base64')

if encryptor == 'dummy':
    from xonsh.history.dummy import DummyHistory
    __xonsh__.env['XONSH_HISTORY_BACKEND'] = DummyHistory
else:
    __xonsh__.env['XONSH_HISTORY_BACKEND'] = XontribHistoryEncrypt
