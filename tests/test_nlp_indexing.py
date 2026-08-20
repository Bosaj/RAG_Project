import unittest

from helpers.indexing import reset_requested_for_page


class IndexResetTests(unittest.TestCase):
    def test_reset_is_requested_for_first_page(self):
        self.assertEqual(reset_requested_for_page(reset_requested=1, page_no=1), 1)

    def test_reset_is_not_repeated_for_later_pages(self):
        self.assertEqual(reset_requested_for_page(reset_requested=1, page_no=2), 0)
        self.assertEqual(reset_requested_for_page(reset_requested=1, page_no=10), 0)

    def test_reset_stays_disabled_when_not_requested(self):
        self.assertEqual(reset_requested_for_page(reset_requested=0, page_no=1), 0)


if __name__ == "__main__":
    unittest.main()
