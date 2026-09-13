import unittest

from backend.src.ir_pipeline.utils.inspire_formatter import format_refs
from langchain_core.documents import Document


class FormatReferencesTest(unittest.TestCase):
    def test_ignores_references_outside_the_document_range(self):
        docs = [
            Document(page_content="first chunk", metadata={"control_number": 10}),
            Document(page_content="second chunk", metadata={"control_number": 20}),
        ]

        for invalid_reference in (0, 3):
            with self.subTest(reference=invalid_reference):
                formatted_answer, citations = format_refs(
                    f"Invalid [{invalid_reference}]. Valid [2].",
                    docs,
                )

                assert formatted_answer == f"Invalid [{invalid_reference}]. Valid [1]."
                assert len(citations) == 1
                assert citations[0].control_number == 20


if __name__ == "__main__":
    unittest.main()
