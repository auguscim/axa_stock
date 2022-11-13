import json
import unittest
from aum_server import AUMServer


class AumServerTest(unittest.TestCase):
    def test_create_payload(self):
        server = AUMServer()
        payload = server.create_payload()
        payload_dict = json.loads(payload)
        sum = 0
        print(type(payload_dict))
        for k in payload_dict:
            sum += payload_dict[k]
        self.assertEqual(sum, 100)



if __name__ == "__main__":
    unittest.main()

