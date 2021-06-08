from google.cloud import storage
import pickle

def load_races2data():
    bucket_name = "artifacts.f1-betting-313907.appspot.com"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob('races2data.pickle')
    races2data = pickle.load(blob.open('rb'))
    return races2data


def save_races2data(races2data):
    bucket_name = "artifacts.f1-betting-313907.appspot.com"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob('races2data.pickle')
    with blob.open('wb') as f:
        pickle.dump(races2data, f)