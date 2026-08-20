import unittest

from controllers.DataController import DataController


class UploadFilenameTests(unittest.TestCase):
    def setUp(self):
        self.controller = DataController.__new__(DataController)

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


if __name__ == "__main__":
    unittest.main()
