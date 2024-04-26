import data_deduplication as dedup
"""
data = dedup.load_data('C:\BBBdatagetsbetter\Data\cleaned_and_normalized_data_all.csv')
links = dedup.data_indexer(data)
features = dedup.compute_features(data,links)
matches = dedup.compute_matches(features, 4.5)
final_matches = dedup.get_matches(data,matches)
print(final_matches)
"""
result = dedup.deduplication('C:\BBBdatagetsbetter\Data\cleaned_and_normalized_data_all.csv',4.5)   