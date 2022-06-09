# Training data cleaner

## The problem

Translation memories are an excellent source of training data for machine translation (MT) models.

However, they may contain data that is not suitable for use in training, such as untranslated sentences, empty cells, cells containing multiple sentences, and so on. Moreover, training data files created by merging several TMs may contain duplicate rows and multiple translations for single source texts, which may also need to be removed in order to ensure optimal training outcomes. (Google Cloud, 2022)

## The solution

Data cleaning is the process of removing and editing rows in the training data file in order to improve the overall quality of the data as much as possible in the time available. The task requires knowledge of both source and target languages, so it should be carried out by linguists. For large datasets of 100,000 rows or more, it is not feasible for linguists to inspect every row, so programmatic methods must be used to identify issues with the data and address them in batches. This tool aims to put these methods into the hands of linguists without a programming background to enable efficient and effective data cleaning.

## Using this tool

https://training-data-cleaner.herokuapp.com/

(More documentation to follow, but it should be possible to understand the basic functionality using the sample datasets below for now.)

### Sample datasets

The following sample datasets are provided in this repo for use when trying out the tool:

| Dataset  | Description | 
| ------------- | ------------- |
| [EN-ES TED Talks sample](app/test_data/ted_es_en_short.xlsx)  | A sample of 20,000 rows from the TED2013 v1.1 dataset for EN-ES from [Orpus](https://opus.nlpl.eu/index.php), with duplicate rows added and some cell content deleted to demonstrate all of the checks currently implemented in the tool with minimal loading time. |
| [EN-ES TED Talks all](app/test_data/ted_es_en.xlsx)  | All 156,698 rows of the TED2013 v1.1 dataset for EN-ES [Orpus](https://opus.nlpl.eu/index.php), to demonstrate the tool's relevance to real-life datasets. Some views may take some time to load. Loading animations, etc. will be added in a future version so please be patient for now! |

## References

Google Cloud (2022) *AutoML Translation beginner's guide*. https://cloud.google.com/translate/automl/docs/beginners-guide (Accessed: 4 Jun 2022).
