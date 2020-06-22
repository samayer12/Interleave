import unittest
from src import interleave


class MyTestCase(unittest.TestCase):
    def test_opens_PDF(self):
        self.assertEqual('1. First Entry\n\n'
                         '2. Second Entry\n\n'
                         '3. Third Entry\n\n\f', interleave.convert_pdf_to_txt('../test/PDFs/Simple.pdf'))

if __name__ == '__main__':
    unittest.main()
