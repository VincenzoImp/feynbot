import unittest
from unittest.mock import patch

from backend.src.ir_pipeline.tools.inspire import InspireOSFullTextSearchTool
from scripts.utils import get_inspire_os_client


class InspireTLSVerificationTest(unittest.TestCase):
    @patch("backend.src.ir_pipeline.tools.inspire.OpenSearch")
    def test_runtime_client_verifies_certificates(self, open_search):
        InspireOSFullTextSearchTool()

        host = open_search.call_args.kwargs["hosts"][0]
        assert host["use_ssl"]
        assert host["verify_certs"]

    @patch("scripts.utils.OpenSearch")
    def test_script_client_verifies_certificates(self, open_search):
        get_inspire_os_client()

        host = open_search.call_args.kwargs["hosts"][0]
        assert host["use_ssl"]
        assert host["verify_certs"]


if __name__ == "__main__":
    unittest.main()
