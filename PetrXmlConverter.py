from xml.dom.minidom import Document


class PetrXmlConverter:
    def __init__(self, input_path, output_path=''):
        self.input_path = input_path
        if output_path == '':
            self.output_path = 'output/' + input_path.split('/')[-1].split('.')[0] + '.xml'
        else:
            self.output_path = output_path
        self.events = []

    def generate_events(self):
        """
        This method should be overridden depending on the input format of input files.
        """
        with open(self.input_path, 'r') as source:
            for line in source.readlines():
                attrs = line.split('\t')
                content = attrs[8]\
                    .replace('。', '。\n')\
                    .replace('。\n”', '。”\n')\
                    .replace('\u3000', '')\
                    .replace(' ', '')\
                    .strip(' \n')
                event = {
                    'id': attrs[0],
                    'date': attrs[4].split(' ')[0].replace('-', ''),
                    'source': attrs[6],
                    'url': attrs[9],
                    'content': content.split('\n'),
                    'parse': []
                }
                for sent in event['content']:
                    parse = self.parse(sent)
                    event['parse'].append(parse)
                self.events.append(event)

    def parse(self, text):
        return ''

    def generate_xml(self):
        xml_doc = Document()
        # <Sentences> element
        xml_root = xml_doc.createElement('Sentences')

        for event in self.events:
            # check keys
            keys_check = [key in event.keys() for key in ['date', 'id', 'source', 'content', 'parse']]
            keys_check.sort()
            if not keys_check[0]:
                print('\033[1;31m'+'Event without proper keys. Please check event format.\n{}'.format(event)+'\033[0m')
                continue

            for sent_i in range(len(event['content'])):

                # <Text> element
                xml_text = xml_doc.createElement('Text')
                text_text = xml_doc.createTextNode('\n' + event['content'][sent_i] + '\n')
                xml_text.appendChild(text_text)

                # <Parse> element
                xml_parse = xml_doc.createElement("Parse")
                parse_text = xml_doc.createTextNode('\n' + event['parse'][sent_i] + '\n')
                xml_parse.appendChild(parse_text)

                # <Sentence> element
                xml_sentence = xml_doc.createElement('Sentence')
                xml_sentence.setAttribute('id', event['id'] + '_' + str(sent_i + 1))
                xml_sentence.setAttribute('sentence', 'True')
                xml_sentence.setAttribute('source', event['source'])
                xml_sentence.setAttribute('date', event['date'])
                xml_sentence.appendChild(xml_text)
                xml_sentence.appendChild(xml_parse)

                xml_root.appendChild(xml_sentence)
                print('parsed event {0}_{1}'.format(event.get('id'), sent_i+1))

        xml_doc.appendChild(xml_root)

        with open(self.output_path, 'w+') as output_file:
            xml_doc.writexml(output_file, newl='\n', encoding='utf-8')

    def run(self):
        self.generate_events()
        self.generate_xml()
