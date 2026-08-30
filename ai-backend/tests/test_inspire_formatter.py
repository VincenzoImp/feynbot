import unittest

from backend.src.ir_pipeline.utils.inspire_formatter import format_refs
from langchain_core.documents import Document


class FormatReferencesTest(unittest.TestCase):
    def test_assigns_distinct_ids_to_chunks_from_the_same_paper(self):
        docs = [
            Document(
                page_content="first chunk",
                metadata={"control_number": 10},
            ),
            Document(
                page_content="second chunk",
                metadata={"control_number": 10},
            ),
        ]

        formatted_answer, citations = format_refs(
            "First claim [1]. Second claim [2].",
            docs,
        )

        assert formatted_answer == "First claim [1]. Second claim [2]."
        assert [
            (citation.doc_id, citation.control_number, citation.snippet)
            for citation in citations
        ] == [
            (1, 10, "first chunk"),
            (2, 10, "second chunk"),
        ]

    def test_ignores_references_outside_the_document_range(self):
        docs = [
            Document(page_content="first chunk", metadata={"control_number": 10}),
            Document(page_content="second chunk", metadata={"control_number": 20}),
        ]

        formatted_answer, citations = format_refs(
            "Invalid [0] and [3]. Valid [2].",
            docs,
        )

        assert formatted_answer == "Invalid [0] and [3]. Valid [1]."
        assert len(citations) == 1
        assert citations[0].control_number == 20


if __name__ == "__main__":
    unittest.main()
