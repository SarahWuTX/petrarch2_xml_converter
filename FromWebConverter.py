import requests
from pyquery import PyQuery as pq
from PetrXmlConverter import PetrXmlConverter


class FromWebConverter(PetrXmlConverter):

    def parse(self, text):
        url = 'http://nlp.stanford.edu:8080/parser/index.jsp'
        data = {
            'query': text,
            'parserSelect': 'Chinese'
        }
        response = requests.post(url, data)
        doc = pq(response.content)
        parse = doc('#parse').text()
        return parse

