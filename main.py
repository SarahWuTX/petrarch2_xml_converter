from FromCorenlpConverter import FromCorenlpConverter
from FromWebConverter import FromWebConverter


def corenlp_test():
    input_path = 'input/news.txt'
    output_path = 'xml/news.xml'
    corenlp_path = 'stanford-corenlp-full-2018-10-05'  # path of corenlp package
    port = 8000
    FromCorenlpConverter(input_path, output_path, corenlp_path, port).run()


def web_test():
    input_path = 'input/news.txt'
    output_path = 'xml/news.xml'
    FromWebConverter(input_path, output_path).run()


if __name__ == "__main__":
    corenlp_test()
    # web_test()


