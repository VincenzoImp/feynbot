import re
import unittest

from backend.src.ir_pipeline.utils.inspire_formatter import format_refs
from langchain_core.documents import Document


class FormatReferencesTest(unittest.TestCase):
    def test_reference_numbers_match_citation_positions(self):
        docs = [
            Document(
                page_content="first chunk",
                metadata={"control_number": 10},
            ),
            Document(
                page_content="second chunk",
                metadata={"control_number": 10},
            ),
            Document(
                page_content="third chunk",
                metadata={"control_number": 20},
            ),
        ]

        formatted_answer, citations = format_refs(
            "First claim [1]. Second claim [2]. Third claim [3].",
            docs,
        )

        assert [
            citations[int(ref) - 1].control_number
            for ref in re.findall(r"\[(\d+)\]", formatted_answer)
        ] == [10, 10, 20]
        assert formatted_answer == "First claim [1]. Second claim [2]. Third claim [3]."
        assert [
            (citation.doc_id, citation.control_number, citation.snippet)
            for citation in citations
        ] == [
            (1, 10, "first chunk"),
            (2, 10, "second chunk"),
            (3, 20, "third chunk"),
        ]


if __name__ == "__main__":
    unittest.main()
