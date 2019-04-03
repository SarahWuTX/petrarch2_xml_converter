import glob
import logging
from stanfordcorenlp import StanfordCoreNLP
from PetrXmlConverter import PetrXmlConverter


class FromCorenlpConverter(PetrXmlConverter):
    def __init__(self, input_path, output_path='', corenlp_path='', port=8000, memory='4g', lang='zh', timeout=1500,
                 quiet=True, logging_level=logging.WARNING):
        super().__init__(input_path, output_path)

        self.corenlp_path = corenlp_path
        if self.corenlp_path == '' and not self.find_corenlp():
            raise IOError('Could not find stanford corenlp.')
        self.nlp = StanfordCoreNLP(self.corenlp_path, port, memory, lang, timeout, quiet, logging_level)

        print('\033[1;32m'+'Starting up StanfordCoreNLP...'+'\033[0m')

    def __del__(self):
        self.nlp.close()
        print('\033[1;32m'+'Corenlp closed!'+'\033[0m')

    def parse(self, text):
        return self.nlp.parse(text)

    def find_corenlp(self):
        corenlp_paths = glob.glob("stanford-corenlp-full-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]")
        if len(corenlp_paths) == 0:
            return False
        else:
            corenlp_paths.sort()
            self.corenlp_path = corenlp_paths[-1]
            return True
