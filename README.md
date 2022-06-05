# Training data cleaner

## The problem

Translation memories are an excellent source of training data for machine translation (MT) models.

However, they may contain data that is not suitable for use in training, such as untranslated sentences, empty cells, cells containing multiple sentences, and so on. Moreover, training data files created by merging several TMs may contain duplicate rows and multiple translations for single source texts, which may also need to be removed in order to ensure optimal training outcomes. (Google Cloud, 2022)

## The solution

Data cleaning is the process of removing rows and editing data to produce the highest quality data possible in the time available. The task requires knowledge of both source and target languages, so it should be carried out by linguists. For large datasets of 100,000 rows or more, it is not feasible for linguists to inspect every row, so programatic methods must be used to identify issues with the data. This tool aims to put these methods in the hands of linguists without technical backgrounds to allow for efficient and effective data cleaning.

## Using this tool

(coming soon)

## References

Google Cloud (2022) *AutoML Translation beginner's guide*. https://cloud.google.com/translate/automl/docs/beginners-guide (Accessed: 4 Jun 2022).