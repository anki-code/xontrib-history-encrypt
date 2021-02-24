import os
import uuid
import builtins
from base64 import b64decode, b64encode

try:
    import ujson as json
except ImportError:
    import json  # type: ignore

from xonsh.history.base import History

class XontribHistoryEncrypt(History):

    def __init__(self, filename=None, sessionid=None, **kwargs):

        crypt = __xonsh__.env.get('XONSH_HISTORY_ENCRYPT_TYPE', 'base64')
        if type(crypt) is list:
            self.encrypter, self.decrypter = crypt
        else:
            self.encrypter = lambda data: b64encode(data.encode()).decode()
            self.decrypter = lambda data: b64decode(data)

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
            with open(self.filename, 'r') as file:
                for line in file:
                    data.append(json.loads(self.decrypter(line)))
            return reversed(data) if newest_first else data
        return []

    def all_items(self, newest_first=False):
        return self.items(newest_first)

    def flush(self, **kwargs):
        with open(self.filename, 'a') as file:
            for data in self.buffer:
                if 'out' in data:
                    del data['out']
                file.write(self.encrypter(json.dumps(data)) + os.linesep)
        self.buffer = []

    def info(self):
        data = {}
        data["backend"] = "xontrib-history-encrypt"
        data["sessionid"] = str(self.sessionid)
        data["filename"] = self.filename
        data["commands"] = len(self.buffer)
        return data


__xonsh__.env['XONSH_HISTORY_BACKEND'] = XontribHistoryEncrypt
