from nlp.entity_extractor import EntityExtractor

extractor = EntityExtractor()

text = """
We propose a Transformer based OCR model evaluated on ICDAR.
The model achieves 98.7% Accuracy for Multilingual OCR.
"""

print("Methods :", extractor.extract_methods(text))
print("Datasets:", extractor.extract_datasets(text))
print("Metrics :", extractor.extract_metrics(text))
print("Problems:", extractor.extract_problems(text))