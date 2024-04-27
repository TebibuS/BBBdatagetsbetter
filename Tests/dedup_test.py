import sys
sys.path.append('C:\BBBdatagetsbetter')
from BBB_Library import data_deduplication as dedup

result = dedup.deduplication('C:\BBBdatagetsbetter\Data\cleaned_and_normalized_data_all.csv',4.5)