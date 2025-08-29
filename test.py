import unittest
import tempfile
import os
from utils import serialize_payload, load_candidates, load_keys

class TestUtils(unittest.TestCase):
    def test_serialize_payload_with_times(self):
        payload = {
            "start_time": 1234567890,
            "end_time": 1234567999,
            "other": "test"
        }
        result = serialize_payload(payload)
        self.assertIsInstance(result, bytes)
        self.assertIn(b'"start_time": "1234567890"', result)
        self.assertIn(b'"end_time": "1234567999"', result)
        self.assertIn(b'"other": "test"', result)

    def test_load_candidates(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp.write("Alice\nBob\nCharlie\n")
            tmp_path = tmp.name

        try:
            candidates = load_candidates(tmp_path)
            self.assertEqual(candidates, {1: "Alice", 2: "Bob", 3: "Charlie"})
        finally:
            os.remove(tmp_path)

    def test_load_candidates_empty(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            candidates = load_candidates(tmp_path)
            self.assertEqual(candidates, {})
        finally:
            os.remove(tmp_path)

    def test_load_keys(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp.write("firstkey\nsecondkey\nthirdkey\n")
            tmp_path = tmp.name

        try:
            keys = load_keys(tmp_path)
            self.assertEqual(keys, ["firstkey", "secondkey", "thirdkey"])
        finally:
            os.remove(tmp_path)

if __name__ == "__main__":
    unittest.main()