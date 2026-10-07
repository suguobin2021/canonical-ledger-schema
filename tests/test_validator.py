import unittest
from canonical_ledger_schema import ValidationError, validate_ledger

def trade(**changes):
    row={"trade_id":"T1","instrument":"SYNTH-USD","side":"long","status":"settled","signal_time":"2026-01-01T00:05:00Z","entry_time":"2026-01-01T00:10:00Z","exit_time":"2026-01-01T01:00:00Z","entry_price":100.0,"exit_price":104.0,"gross_return":0.04,"cost_return":0.001,"net_return":0.039}
    row.update(changes)
    return row

class Tests(unittest.TestCase):
    def doc(self, *rows): return {"schema_version":"0.1.0","trades":list(rows)}
    def test_valid(self): validate_ledger(self.doc(trade()))
    def test_entry_before_signal(self):
        with self.assertRaises(ValidationError): validate_ledger(self.doc(trade(entry_time="2026-01-01T00:00:00Z")))
    def test_settled_requires_exit(self):
        with self.assertRaises(ValidationError): validate_ledger(self.doc(trade(exit_time=None)))
    def test_exit_before_entry(self):
        with self.assertRaises(ValidationError): validate_ledger(self.doc(trade(exit_time="2026-01-01T00:06:00Z")))
    def test_duplicate_id(self):
        with self.assertRaises(ValidationError): validate_ledger(self.doc(trade(),trade()))
    def test_negative_cost(self):
        with self.assertRaises(ValidationError): validate_ledger(self.doc(trade(cost_return=-0.001)))
    def test_return_identity(self):
        with self.assertRaises(ValidationError): validate_ledger(self.doc(trade(net_return=0.04)))
    def test_naive_timestamp(self):
        with self.assertRaises(ValidationError): validate_ledger(self.doc(trade(signal_time="2026-01-01T00:05:00")))

if __name__ == "__main__": unittest.main()
