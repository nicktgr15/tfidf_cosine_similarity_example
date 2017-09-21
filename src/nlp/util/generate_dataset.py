from urllib.request import urlopen
import json
from nlp import QA_DATASET_CSV
from nlp.model.q import q_to_line, q

DATASET_URL = "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json"


def generate_dataset():
    with open(QA_DATASET_CSV, 'w', encoding='utf-8') as f:
        with urlopen(DATASET_URL) as url:
            j = json.loads(url.read().decode())
            for d in j['data']:
                for p in d['paragraphs']:
                    for qas in p['qas']:
                        f.write(q_to_line(
                            q(question=qas['question']))
                        )

if __name__ == '__main__':
    generate_dataset()