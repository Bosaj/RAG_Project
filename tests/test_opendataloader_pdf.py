"""
Tests for OpenDataLoader-PDF and Unlimited-OCR module
"""

import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from helpers.opendataloader_pdf import OpenDataLoaderPDF, DocumentBlock


class TestOpenDataLoaderPDF(unittest.TestCase):
    def setUp(self):
        self.loader = OpenDataLoaderPDF(ocr_enabled=True)

    def test_extract_headers_and_paragraphs(self):
        mock_stream = """
# MOROCCAN OFFICIAL GAZETTE
--- Page 1 ---
BULLETIN OFFICIEL DU ROYAUME DU MAROC
This bulletin covers recent legal and ministerial announcements.

| Article | Domain | Status |
| 10 | Commercial Code | Active |
| 11 | Maritime Code | Amended |

Further text follows on the next paragraph.
"""
        doc = self.loader.extract_from_text_stream(mock_stream, "bo_7200.pdf")
        self.assertEqual(doc.filename, "bo_7200.pdf")
        self.assertGreater(len(doc.blocks), 2)

        types = [b.block_type for b in doc.blocks]
        self.assertIn("header", types)
        self.assertIn("paragraph", types)
        self.assertIn("table", types)

        # Check table extraction
        table_block = next(b for b in doc.blocks if b.block_type == "table")
        self.assertIn("Commercial Code", table_block.text)
        self.assertEqual(table_block.metadata.get("row_count"), 3)


if __name__ == "__main__":
    unittest.main()
