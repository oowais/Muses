import os

from db import Db
from extractor import Extractor

database_name = 'db.sqlite'
audio_folder_name = 'audio_resources'
root_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
db_file = os.path.join(root_dir_path, database_name)
audio_path = os.path.join(root_dir_path, audio_folder_name)


def get_features_and_save_to_db_test():
    name1 = 'metal0.mp3'
    name2 = 'metal1.mp3'
    file1 = '../audio_resources/' + name1
    file2 = '../audio_resources/' + name2

    ex = Extractor()

    feature1 = ex.get_all_features(file1)
    feature2 = ex.get_all_features(file2)

    dist = ex.get_distance(feature1, feature2)

    db = Db(storage_file=db_file)
    # print('deleting tables: ', db.delete_tables())
    print('creating tables: ', db.create_tables())
    print('Saving into db: ', db.save_feature_distances(dist_obj=dist))


def test_get_hash_from_db():
    db = Db(storage_file=db_file)
    hash1 = '9e0035d3ef4d0f06bfa161f328e6bb78a5e20e291b46463722dddf2eee62b1ab'
    hash2 = 'e4d5bb5509746f7ed8feb98ea41fa797a30ebf6dda68507b094bb4d3b4ae7c89'
    dist = db.get_distance(hash2, hash1)
    print(dist)


def check_hashes_present():
    db = Db(storage_file=db_file)
    hash1 = '9e0035d3ef4d0f06bfa161f328e6bb78a5e20e291b46463722dddf2eee62b1ab'
    hash2 = 'e4d5bb5509746f7ed8feb98ea41fa797a30ebf6dda68507b094bb4d3b4ae7c89'
    print(db.is_hashes_present(hash1, hash2))


if __name__ == '__main__':
    pass
