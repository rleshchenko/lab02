import nltk, csv, codecs

nltk.download('punkt')
from nltk.tokenize import word_tokenize
from io import StringIO


class Analyzer:
    file_path = ''

    def __init__(self, file_path):
        self.file_path = file_path

    def execute(self):
        csv_table = self.read_csv_table()
        tokenized_array = self.tokenize_column_text(csv_table)
        frequency_statistics = self.count_word_frequence(tokenized_array)
        frequency_statistics_per_topic = self.count_word_frequence_per_topic(tokenized_array)
        unnormal_probability = self.calc_unnormal_probability(frequency_statistics_per_topic)

        return self.save_statistics_to_file(
            frequency_statistics,
            frequency_statistics_per_topic,
            unnormal_probability
        )

    def read_csv_table(self, file_path=''):
        columns = []
        if file_path != '':
            self.file_path = file_path

        with open(self.file_path, "rb") as f:
            contents = f.read().decode("UTF-8")
            buff = StringIO(contents)
            reader = csv.reader(buff)
            for row in reader:
                if columns:
                    for i, value in enumerate(row):
                        columns[i].append(value)
                else:
                    # first row
                    columns = [[value] for value in row]

        as_dict = {c[0]: c[1:] for c in columns}

        return as_dict

    def tokenize_column_text(self, csv_table):
        result = {}
        columns = list(csv_table.keys())
        for column in columns:
            result[column] = []
            for line in csv_table[column]:
                result[column].append(word_tokenize(line))

        return result

    def count_word_frequence(self, tokenized_array):
        word_sets = tokenized_array
        result = {}
        for word_set in word_sets:
            for line in word_sets[word_set]:
                for word in line:
                    if len(word) == 1:
                        continue
                    count = self.count_word_in_wordsets(word, word_sets)
                    if count != 0:
                        result[word] = count

        return result

    def count_word_in_wordsets(self, word, word_sets):
        count = 0
        for word_set in word_sets:
            for line in word_sets[word_set]:
                count += line.count(word)

        return count

    def count_word_frequence_per_topic(self, tokenized_array):
        result = {}
        for topic in tokenized_array:
            for line in tokenized_array[topic]:
                for word in line:
                    if len(word) == 1:
                        continue
                    result[word] = self.count_word_in_topics(word, tokenized_array)

        return result

    def count_word_in_topics(self, word, tokenized_array):
        result = {}
        for topic in tokenized_array:
            count = 0
            for line in tokenized_array[topic]:
                count += line.count(word)

            result[topic] = count

        return result

    def calc_unnormal_probability(self, dictionary):
        result = {}
        for word in dictionary:
            result[word] = {}
            for item in dictionary[word]:
                target = dictionary[word][item]
                result[word][item] = target * (1 / 3)

        return result

    def save_statistics_to_file(
            self,
            frequency_statistics,
            frequency_statistics_per_topic,
            unnormal_probability
    ):
        word, columns = frequency_statistics_per_topic.popitem()
        csv_columns = ['Word'] + list(columns.keys())
        with open('statistics.csv', 'w', encoding='UTF-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, csv_columns)
            writer.writeheader()
            for data in frequency_statistics_per_topic:
                tempDict = {'Word': data}
                tempDict.update(frequency_statistics_per_topic[data])
                values = list(tempDict.values())
                tempDict = dict(zip(csv_columns, values))
                writer.writerow(tempDict)

        with open('statistics_dictionary.csv', 'w', encoding='UTF-8', newline='') as csv_file:
            csv_columns = ['Word', 'Frequency']
            writer = csv.DictWriter(csv_file, csv_columns)
            writer.writeheader()
            for data in frequency_statistics:
                tempDict = {'Word': data, 'Frequency': frequency_statistics[data]}
                writer.writerow(tempDict)

        with open('statistics_dictionary_unnormal_probability.csv', 'w', encoding='UTF-8', newline='') as csv_file:
            word, columns = unnormal_probability.popitem()
            csv_columns = ['Word'] + list(columns.keys())
            writer = csv.DictWriter(csv_file, csv_columns)
            writer.writeheader()
            for data in unnormal_probability:
                tempDict = {'Word': data}
                tempDict.update(unnormal_probability[data])
                values = list(tempDict.values())
                tempDict = dict(zip(csv_columns, values))
                writer.writerow(tempDict)
        return
