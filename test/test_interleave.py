import unittest
from src import interleave


class PDFTests(unittest.TestCase):
    def test_opens_PDF(self):
        self.assertEqual('1. First Entry\n\n'
                         '2. Second Entry\n\n'
                         '3. Third Entry\n\n\f', interleave.convert_pdf_to_txt('./test/PDFs/Simple.pdf'))

if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)
