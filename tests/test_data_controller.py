import unittest
from types import SimpleNamespace

from controllers.DataController import DataController


class UploadFilenameTests(unittest.TestCase):
    def setUp(self):
        self.controller = DataController.__new__(DataController)
        self.controller.app_settings = SimpleNamespace(
            FILE_ALLOWED_TYPES=["text/plain"],
            FILE_MAX_SIZE=1,
        )
        self.controller.size_scale = 1048576

    def test_preserves_extension_and_replaces_spaces(self):
        self.assertEqual(
            self.controller.get_clean_file_name(" quarterly report 2026.pdf "),
            "quarterly_report_2026.pdf",
        )

    def test_removes_path_separators_and_special_characters(self):
        self.assertEqual(
            self.controller.get_clean_file_name("../private/report?.pdf"),
            "privatereport.pdf",
        )

    def test_uses_fallback_for_empty_or_only_punctuation_names(self):
        self.assertEqual(self.controller.get_clean_file_name("   ...///"), "uploaded_file")

    def test_unknown_upload_size_is_allowed_for_streaming_input(self):
        is_valid, _ = self.controller.validate_uploaded_file(
            SimpleNamespace(content_type="text/plain", size=None)
        )

        self.assertTrue(is_valid)

    def test_known_oversized_upload_is_rejected(self):
        is_valid, _ = self.controller.validate_uploaded_file(
            SimpleNamespace(content_type="text/plain", size=2 * 1048576)
        )

        self.assertFalse(is_valid)

    def test_unsupported_content_type_is_rejected(self):
        is_valid, _ = self.controller.validate_uploaded_file(
            SimpleNamespace(content_type="application/octet-stream", size=10)
        )

        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()
