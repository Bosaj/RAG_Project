import asyncio
import unittest

from pydantic import ValidationError

from routes.base import health_check
from routes.schemes.data import ProcessRequest
from routes.schemes.nlp import PushRequest, SearchRequest


class RequestSchemaTests(unittest.TestCase):
    def test_process_request_defaults(self):
        request = ProcessRequest(file_id="document-1")

        self.assertEqual(request.file_id, "document-1")
        self.assertEqual(request.chunk_size, 100)
        self.assertEqual(request.overlap_size, 20)
        self.assertEqual(request.do_reset, 0)

    def test_process_request_accepts_explicit_processing_options(self):
        request = ProcessRequest(
            file_id="document-1",
            chunk_size=256,
            overlap_size=32,
            do_reset=1,
        )

        self.assertEqual(request.chunk_size, 256)
        self.assertEqual(request.overlap_size, 32)
        self.assertEqual(request.do_reset, 1)

    def test_push_request_defaults_to_preserving_existing_index(self):
        self.assertEqual(PushRequest().do_reset, 0)

        with self.assertRaises(ValidationError):
            PushRequest(do_reset=2)

    def test_search_request_requires_text_and_defaults_limit(self):
        request = SearchRequest(text="What is RAG?")

        self.assertEqual(request.text, "What is RAG?")
        self.assertEqual(request.limit, 5)

        with self.assertRaises(ValidationError):
            SearchRequest()

        with self.assertRaises(ValidationError):
            SearchRequest(text="", limit=0)

        with self.assertRaises(ValidationError):
            SearchRequest(text="question", limit=101)

    def test_health_check_returns_liveness_response(self):
        self.assertEqual(asyncio.run(health_check()), {"status": "ok"})

    def test_process_request_rejects_invalid_chunking_options(self):
        with self.assertRaises(ValidationError):
            ProcessRequest(chunk_size=0)

        with self.assertRaises(ValidationError):
            ProcessRequest(chunk_size=20, overlap_size=20)

        with self.assertRaises(ValidationError):
            ProcessRequest(do_reset=2)


if __name__ == "__main__":
    unittest.main()
