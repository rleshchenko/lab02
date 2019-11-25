import csv

class Classifier:
    dictionary = {}
    def __init__(self, statistic_dictionary, statistic_unnormal, freq_statistic):
        self.statistic_dictionary = statistic_dictionary
        self.statistic_unnormal = statistic_unnormal
        self.freq_statistic = freq_statistic

    def calc_normal_probability(self):
        result = {}
        columns = ['Наука\n','Інтернет\n', 'Космос']
        for column in self.statistic_dictionary:
            for index in range(len(self.statistic_dictionary[column])):
                word = self.statistic_dictionary['Word'][index]
                result[word] = {}
                for column in columns:
                    result[word][column] = self.calc_normal_probability_per_column(column, index)

        self.save_to_file(result)


    def calc_normal_probability_per_column(self, column_name, index):
        p_word_freq = float(self.freq_statistic['Frequency'][index])
        p_word_unnormal = float(self.statistic_unnormal[column_name][index])
        p_class = 0.33

        normal_probability = (p_word_freq * p_word_unnormal + p_class) / (p_word_freq + 1)

        return normal_probability

    def save_to_file(self, dictionary):
        csv_columns = ['Word', 'Наука\n','Інтернет\n', 'Космос']
        with open('statistics_normalized.csv', 'w', encoding='UTF-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, csv_columns)
            writer.writeheader()
            for data in dictionary:
                tempDict = {'Word': data}
                tempDict.update(dictionary[data])
                values = list(tempDict.values())
                tempDict = dict(zip(csv_columns, values))
                writer.writerow(tempDict)
