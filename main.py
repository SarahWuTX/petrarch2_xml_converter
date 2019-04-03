import glob

from FromCorenlpConverter import FromCorenlpConverter
from FromWebConverter import FromWebConverter


def find_corenlp():
    corenlp_paths = glob.glob("stanford-corenlp-full-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]")
    if len(corenlp_paths) == 0:
        return None
    else:
        corenlp_paths.sort()
        return corenlp_paths[-1]


def corenlp_test():
    input_path = 'input/news.txt'
    output_path = 'output/news.xml'
    corenlp_path = 'stanford-corenlp-full-2018-10-05'  # path of corenlp package
    port = 8000
    FromCorenlpConverter(input_path, corenlp_path, output_path, port).run()


def web_test():
    input_path = 'input/news.txt'
    output_path = 'output/news.xml'
    FromWebConverter(input_path, output_path).run()


if __name__ == "__main__":
    corenlp_test()
    # web_test()


