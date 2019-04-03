import re
from xml.dom.minidom import Document
from enum import Enum, unique


@unique
class Attr(Enum):
    id = 'id'
    date = 'date'
    source = 'source'
    url = 'url'
    content = 'content'
    text = 'text'
    parse = 'parse'


class PetrXmlConverter:
    def __init__(self, input_path, output_path=''):
        self.input_path = input_path
        if output_path == '':
            self.output_path = 'xml/' + input_path.split('/')[-1].split('.')[0] + '.xml'
        else:
            self.output_path = output_path
        self.events = []

    def generate_events(self):
        """
        This method should be overridden depending on the input format of input files.
        """
        with open(self.input_path, 'r') as source:
            for line in source.readlines():
                properties = line.split('\t')
                event = {
                    Attr.id: properties[0],
                    Attr.date: properties[4].split(' ')[0].replace('-', ''),
                    Attr.source: properties[6],
                    Attr.url: properties[9]
                }
                content = re.sub(r'\s', '', properties[8])
                parse = self.parse(content)
                print('parsed event {0}'.format(event[Attr.id]))
                event[Attr.content] = self.sep_sentence(parse)
                self.events.append(event)

    def parse(self, text):
        return ''

    def sep_sentence(self, parse):
        stack = []
        sentences = []
        for i in range(len(parse)):
            if parse[i] == '(':
                stack.append(i)
            elif parse[i] == ')':
                if len(stack) == 3 and parse[stack[-1]+1] != 'P':
                    parse_sent = parse[stack[2]:i + 1]
                    text_sent = re.sub(r'\([A-Z]+\s', '', parse_sent).replace(')', '')
                    sentences.append({
                        Attr.text: re.sub(r'\s', '', text_sent),
                        Attr.parse: parse_sent.replace(' ', '')
                    })
                stack.pop()
        return sentences

    def generate_xml(self):
        xml_doc = Document()
        # <Sentences> element
        xml_root = xml_doc.createElement('Sentences')

        for event in self.events:
            # check keys
            keys_check = [key in event.keys() for key in [Attr.id, Attr.date, Attr.source, Attr.content]]
            keys_check.sort()
            if not keys_check[0]:
                print('\033[1;31m'+'Event without proper keys. Please check event format.\n{}'.format(event)+'\033[0m')
                continue

            for sent_i in range(len(event[Attr.content])):

                # <Text> element
                xml_text = xml_doc.createElement('Text')
                text_text = xml_doc.createTextNode('\n' + event[Attr.content][sent_i][Attr.text] + '\n')
                xml_text.appendChild(text_text)

                # <Parse> element
                xml_parse = xml_doc.createElement("Parse")
                parse_text = xml_doc.createTextNode('\n' + event[Attr.content][sent_i][Attr.parse] + '\n')
                xml_parse.appendChild(parse_text)

                # <Sentence> element
                xml_sentence = xml_doc.createElement('Sentence')
                xml_sentence.setAttribute('id', event[Attr.id] + '_' + str(sent_i + 1))
                xml_sentence.setAttribute('sentence', 'True')
                xml_sentence.setAttribute('source', event[Attr.source])
                xml_sentence.setAttribute('date', event[Attr.date])
                xml_sentence.appendChild(xml_text)
                xml_sentence.appendChild(xml_parse)

                xml_root.appendChild(xml_sentence)

        xml_doc.appendChild(xml_root)

        with open(self.output_path, 'w+') as output_file:
            xml_doc.writexml(output_file, newl='\n', encoding='utf-8')

    def print_events(self):
        for event in self.events:
            print('*********************************************************')
            print('event id:', event[Attr.id])
            print('event date:', event[Attr.date])
            print('event source:', event[Attr.source])
            print('event url:', event[Attr.url])
            print('event sentences:')
            for sentence in event[Attr.content]:
                print(sentence[Attr.text])
                print(sentence[Attr.parse])

    def run(self):
        self.generate_events()
        self.generate_xml()

