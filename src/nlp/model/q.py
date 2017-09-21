from collections import namedtuple

q = namedtuple('Q', 'question')


def line_to_q(line):
    return q(question=line.rstrip("\n"))


def q_to_line(q):
    return "%s\n" % q.question


def csv_to_qs(csv_file):
    with open(csv_file, encoding='utf-8') as f:
        qs = f.readlines()
        qs = [line_to_q(l) for l in qs]
        return qs
