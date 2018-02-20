class FrequencyTable:
    def __init__(self):
        self.table = {}
        self.totals = {}
        self.total = 0

    def add(self, key1, key2):
        add_to_table(self.table, key1, key2)

        if key1 in self.totals:
            self.totals[key1] += 1.
        else:
            self.totals[key1] = 1.

        self.total += 1

    def get_prob(self, key1, key2):
        if key1 in self.table and key2 in self.table[key1]:
            return (self.table[key1][key2] / self.totals[key1]) * 100000 # underflow hack fix
        else:
            return 0

    def get_unigram_prob(self, key1):
        if key1 in self.table:
            return sum(self.table[key1].values()) / self.total * 100000
        else:
            return 0


def add_to_table(table, first_key, second_key):
    if first_key in table:
        t2 = table[first_key]

        if second_key in t2:
            t2[second_key] += 1
        else:
            t2[second_key] = 1
    else:
        table[first_key] = { second_key: 1 }
