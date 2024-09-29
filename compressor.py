import gzip
import shutil

def compress_file(original_file, compressed_file):
    with open(original_file, 'rb') as f_in:
        with gzip.open(compressed_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# Specify the original joblib file and the target gzip file
original_file = 'random_forest_model.joblib'
compressed_file = 'random_forest_model.joblib.gz'

# Compress the file
compress_file(original_file, compressed_file)
