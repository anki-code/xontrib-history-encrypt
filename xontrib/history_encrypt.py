import os
import uuid
import builtins
from base64 import b64decode, b64encode

try:
    import ujson as json
except ImportError:
    import json  # type: ignore

from xonsh.history.base import History

_crypters = {
    'base64': {
        'key': None,
        'enc': lambda data, key=None: b64encode(data.encode()).decode(),
        'dec': lambda data, key=None: b64decode(data).decode()
    }
}

class XontribHistoryEncrypt(History):

    def __init__(self, filename=None, sessionid=None, **kwargs):

        encryptor = __xonsh__.env.get('XONSH_HISTORY_ENCRYPTOR', 'base64')
        if type(encryptor) is dict:
            self.key = encryptor['key']
            self.enc = encryptor['enc']
            self.dec = encryptor['dec']
        elif type(encryptor) is str:
            self.key = _crypters[encryptor]['key']
            self.enc = _crypters[encryptor]['enc']
            self.dec = _crypters[encryptor]['dec']

        self.key = self.key() if callable(self.key) else self.key

        self.lock = False
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
        if os.path.exists(self.filename):
            data = []
            first_line = True
            with open(self.filename, 'r') as file:
                for line in file:
                    if first_line:
                        try:
                            crypt_mark = self.dec(line, self.key)
                            assert crypt_mark.isdigit()
                        except:
                            printx("{YELLOW}The crypted history file is not matching with crypto algorithm.")
                            printx(f"File: {self.filename}")
                            printx(f"Change the encryption algorithm or (re)move the history file.{{RESET}}")
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


__xonsh__.env['XONSH_HISTORY_BACKEND'] = XontribHistoryEncrypt
