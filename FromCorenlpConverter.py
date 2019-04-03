import logging
from stanfordcorenlp import StanfordCoreNLP
from PetrXmlConverter import PetrXmlConverter


class FromCorenlpConverter(PetrXmlConverter):
    def __init__(self, input_path, corenlp_path, output_path='', port=None, memory='4g', lang='zh', timeout=1500,
                 quiet=True, logging_level=logging.WARNING):
        super().__init__(input_path, output_path)
        self.nlp = StanfordCoreNLP(corenlp_path, port, memory, lang, timeout, quiet, logging_level)
        print('\033[1;32m'+'Start up StanfordCoreNLP...'+'\033[0m')

    def __del__(self):
        self.nlp.close()
        print('Corenlp closed!')

    def parse(self, text):
        return self.nlp.parse(text)
