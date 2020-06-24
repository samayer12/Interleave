import unittest
from src import interleave


class PDFTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample_text = '1. First Entry\n\n2. Second Entry\n\n3. Third Entry\n\n\f'

    def test_opens_PDF(self):
        self.assertEqual('1. First Entry\n\n'
                         '2. Second Entry\n\n'
                         '3. Third Entry\n\n\f', interleave.convert_pdf_to_txt('./test/PDFs/Simple.pdf'))

    def test_splits_sentences(self):
        self.assertEqual(['1. First Entry', '2. Second Entry', '3. Third Entry', '\f'],
                         interleave.get_sentences(self.sample_text))

    def test_zip_sentences_to_tuple(self):
        list1 = self.sample_text
        list2 = self.sample_text

        self.assertEqual([('1. First Entry', '1. First Entry'),
                         ('2. Second Entry', '2. Second Entry'),
                         ('3. Third Entry', '3. Third Entry'),
                         ('\f', '\f')],
                         interleave.zip_sentences(interleave.get_sentences(list1),
                                                  interleave.get_sentences(list2)))

if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)
