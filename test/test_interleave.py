import unittest
from src import interleave
from unittest.mock import patch


class PDFTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.short_text = '1. First Entry\n\n22. Second Entry\n\n321. Third Entry\n\n\f'

        cls.multiline_text = '1. First Entry. This is a really long entry. It spans multiple lines. Very long. ' \
                             'So tall. Can you \n\nbelieve how many words are here?\n\n' \
                             '2. Second Entry. This is an even longer entry! ' \
                             'This one spans three lines. Ha, and you thought the \n\nlast guy was verbose. ' \
                             'Wait until I tell you a story my great-great grandfather once told me. Four\n\n' \
                             'score and seven years ago...\n\n' \
                             '3. Third Entry\n\n\f'

        cls.multipage_text = '1. First Entry. \n\n' \
                             '2. Second Entry. This paragraphs spans multiple pages. Words enable the document to \n\n' \
                             'automatically handle a page-break. This paragraph splits to the next page and continues ' \
                             'with a \n\n\fnormal word.\n\n' \
                             '3. Third Entry. This paragraphs spans multiple pages. Words enable the document to ' \
                             'automatically \n\nhandle a page-break. This paragraph splits to the next page and continues ' \
                             'with a number so it is \n\n\f1234 words.\n\n\f'

        cls.split_simple_text = ['1. First Entry', '22. Second Entry', '321. Third Entry']

        cls.split_multiline_text = ['1. First Entry. This is a really long entry. It spans multiple lines. Very long. '
                                    'So tall. Can you believe how many words are here?',
                                    '2. Second Entry. This is an even longer entry! This one spans three lines. '
                                    'Ha, and you thought the last guy was verbose. '
                                    'Wait until I tell you a story my great-great grandfather once told me. '
                                    'Four score and seven years ago...',
                                    '3. Third Entry']

        cls.split_multipage_text = ['1. First Entry. ',
                                    '2. Second Entry. This paragraphs spans multiple pages. Words enable the document '
                                    'to automatically handle a page-break. This paragraph splits to the next page and '
                                    'continues with a normal word.',
                                    '3. Third Entry. This paragraphs spans multiple pages. Words enable the document '
                                    'to automatically handle a page-break. This paragraph splits to the next page and '
                                    'continues with a number so it is 1234 words.']


        cls.processed_text = [('1. First Entry', '1. First Entry'),
                              ('22. Second Entry', '22. Second Entry'),
                              ('321. Third Entry', '321. Third Entry')]

    def test_opens_PDF(self):
        self.assertEqual(self.short_text, interleave.convert_pdf_to_txt('./test/PDFs/Simple.pdf'))

    def test_opens_multiline_PDF(self):
        self.assertEqual(self.multiline_text, interleave.convert_pdf_to_txt('./test/PDFs/Multiline.pdf'))

    def test_opens_multipage_PDF(self):
        self.assertEqual(self.multipage_text, interleave.convert_pdf_to_txt('./test/PDFs/Multipage.pdf'))

    def test_splits_short_sentences(self):
        self.assertEqual(self.split_simple_text,
                         interleave.get_sentences(self.short_text))

    def test_splits_multiline_sentences(self):
        self.assertEqual(self.split_multiline_text,
                         interleave.get_sentences(self.multiline_text))

    def test_splits_multipage_paragraphs(self):
        self.assertEqual(self.split_multipage_text,
                         interleave.get_sentences(self.multipage_text))

    def test_zip_sentences_to_tuple(self):
        list1 = self.short_text
        list2 = self.short_text

        self.assertEqual(self.processed_text,
                         interleave.zip_sentences(interleave.get_sentences(list1),
                                                  interleave.get_sentences(list2)))

    @patch('builtins.open')
    @patch('src.interleave.writer', autospec=True)
    def test_writes_csv(self, mock_writer, mock_open):
        interleave.create_csv(self.processed_text)
        self.assertEqual(1, mock_open.call_count)
        self.assertEqual(2, mock_writer.call_count)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)
