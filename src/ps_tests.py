from elasticsearch_dsl import Search, Q
from elasticsearch import Elasticsearch
import datetime
import requests


host = "192.170.227.31"
username = "dweitzel"
password = "6ZOiEmp6J7"

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return int(round((dt - epoch).total_seconds() * 1000.0))


class PSData:
    def __init__(self, username, password, host="192.170.227.31", index="ps_*"):
        self.client = Elasticsearch(hosts="{}:{}@{}".format(username, password, host), timeout=60)
        self.index = index


    def GetNumtests(self, endpoint=None):
        """
        Gather the number of tests run over a day, month (30 days), and year
        returns: {"day": count, "month": count, "year", count}
        """
        to_return = {}
        to_return['day'] = self._GetCountPeriod(1, endpoint)
        to_return['month'] = self._GetCountPeriod(30, endpoint)
        to_return['year'] = self._GetCountPeriod(365, endpoint)
        return to_return

    def _GetCountPeriod(self, days=1, endpoint=None):
        s = Search(using=self.client, index=self.index)
        to_date = datetime.datetime.now()
        from_date = datetime.datetime.now() - datetime.timedelta(days=days)
        if endpoint:
            q = Q("multi_match", query=endpoint, fields=['src_host', 'dest_host'])
            s = s.query(q)
        s = s.filter('range', **{'timestamp': {'from': unix_time_millis(from_date), 'to': unix_time_millis(to_date) }})
        return s.count()


def test_index(index):
    psdata = PSData(username, password, index=index)
    return psdata.GetNumtests()

results = {}
results = {
    'latency': test_index("ps_owd*"),
    'packet_loss': test_index("ps_packet_loss*"),
    'retransmits': test_index("ps_retransmits*"),
    'throughput': test_index("ps_throughput*"),
    'traceroute': test_index("ps_trace*")
}

results['total'] = {
    'day': results['latency']['day'] + results['throughput']['day'] + results['traceroute']['day'],
    'month': results['latency']['month'] + results['throughput']['month'] + results['traceroute']['month'],
    'year': results['latency']['year'] + results['throughput']['year'] + results['traceroute']['year']
}

api_key = ""
with open('api_key', 'r') as api_key_file:
    api_key = api_key_file.read().strip()

headers = {'Authorization': 'Bearer {}'.format(api_key)}
res = requests.post("https://display.sand-ci.org/upload_psstats", json=results, headers=headers)
if res.ok:
    print("Got ok from send")