from statistics.analyzer import Analyzer
from classification.classifier import Classifier


file_path = 'C:\\Users\Roman\\Documents\\lab02\\statistics\\default_data.csv'

analyzer = Analyzer(file_path)

analyzer.execute()

statistics_dictionary = analyzer.read_csv_table('statistics.csv')
freq_statistics = analyzer.read_csv_table('statistics_dictionary.csv')
statistics_unnormal = analyzer.read_csv_table('statistics_dictionary_unnormal_probability.csv')
classifier = Classifier(statistics_dictionary, statistics_unnormal, freq_statistics).calc_normal_probability()


