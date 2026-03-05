# GCP Loader
from typing import Dict, List
from google.cloud import storage

# Provide helper functions to list prefixes (subfolders) and read objects

def list_prefixes(bucket_name: str, delimiter: str = '/') -> List[str]:
    # List unique top-level prefixes (subfolder names) in the given bucket.
    client = storage.Client()
    iterator = client.list_blobs(bucket_name, delimiter=delimiter)
    return sorted(list(iterator.prefixes))

def load_documents_from_gcp(bucket_name: str, prefix: str = '') -> Dict[str, str]:
    # Load all text-based files from the given bucket and prefix. Supported: .txt files.
    docs: Dict[str, str] = {}
    client = storage.Client()
    if prefix and not prefix.endswith('/'):
        prefix += '/'
    blobs = client.list_blobs(bucket_name, prefix=prefix)
    for blob in blobs:
        name = blob.name
        if name.endswith('/'):
            continue
        if name.lower().endswith('.txt'):
            try:
                docs[name] = blob.download_as_text()
            except Exception as e:
                print(f'Failed to read {name}: {e}')
    return docs