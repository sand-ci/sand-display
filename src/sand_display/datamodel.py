
import json
import time

class CachedData():

    def __init__(self, config):
        self._config = config
        self._expiry = 0
        self._data = {}

    def GetSources(self):
        self._CheckData()
        return self._data

    def _CheckData(self):
        if time.time() > self._expiry:
            try:
                with open(self._config['DATA_FILE'], "r") as fp:
                    self._data = json.load(fp)
            except:
                self._expiry = time.time() + 1
