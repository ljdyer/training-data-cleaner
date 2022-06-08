# Training data cleaner

## The problem

Translation memories are an excellent source of training data for machine translation (MT) models.

However, they may contain data that is not suitable for use in training, such as untranslated sentences, empty cells, cells containing multiple sentences, and so on. Moreover, training data files created by merging several TMs may contain duplicate rows and multiple translations for single source texts, which may also need to be removed in order to ensure optimal training outcomes. (Google Cloud, 2022)

## The solution

Data cleaning is the process of removing and editing rows in the training data file in order to improve the overall quality of the data as much as possible in the time available. The task requires knowledge of both source and target languages, so it should be carried out by linguists. For large datasets of 100,000 rows or more, it is not feasible for linguists to inspect every row, so programmatic methods must be used to identify issues with the data and address them in batches. This tool aims to put these methods into the hands of linguists without a programming background to enable efficient and effective data cleaning.

## Using this tool

https://training-data-cleaner.herokuapp.com/

Test dataset: [here](app/test_data/data.xlsx)

## References

Google Cloud (2022) *AutoML Translation beginner's guide*. https://cloud.google.com/translate/automl/docs/beginners-guide (Accessed: 4 Jun 2022).
