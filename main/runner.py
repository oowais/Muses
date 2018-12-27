from main.db import Db
from main.datastructure.feature import Feature
from main.datastructure.distance import Distance
from main.extractor import Extractor
import os


database_name = 'db.sqlite'


def initialize_extreme_dist_table_and_update_it():
    db = Db(storage_file=os.path.abspath(os.path.join(os.path.dirname(__file__), '../' + database_name)))
    min_feature = Feature(mfcc=0.0, chroma_cens=0.0, chroma_stft=0.0, mel=0.0, tonnetz=0.0, rhythm=0.0)
    max_feature = Feature(mfcc=0.0, chroma_cens=0.0, chroma_stft=0.0, mel=0.0, tonnetz=0.0, rhythm=0.0)
    db.set_initial_extreme_distance(min_feature=min_feature, max_feature=max_feature)
    db.update_extreme_distance('rhythm', 3.53334, 22.5226)


def get_features_and_save_to_db_test():
    name1 = 'metal0.mp3'
    name2 = 'metal1.mp3'
    file1 = '../audio_resources/' + name1
    file2 = '../audio_resources/' + name2

    ex = Extractor()

    feature1 = ex.get_all_features(file1)
    feature2 = ex.get_all_features(file2)

    dist = ex.get_distance(feature1, feature2)

    db = Db(storage_file=os.path.abspath(os.path.join(os.path.dirname(__file__), '../' + database_name)))
    print('deleting tables: ', db.delete_tables())
    print('creating tables: ', db.create_tables())
    print('Saving into db: ', db.save_feature_distances(dist_obj=dist))


def test_get_hash_from_db():
    db = Db(storage_file=os.path.abspath(os.path.join(os.path.dirname(__file__), '../' + database_name)))
    hash1 = '9e0035d3ef4d0f06bfa161f328e6bb78a5e20e291b46463722dddf2eee62b1ab'
    hash2 = 'e4d5bb5509746f7ed8feb98ea41fa797a30ebf6dda68507b094bb4d3b4ae7c89'
    dist = db.get_distance(hash2, hash1)
    print(dist)


def main():
    # todo: loop over the directory
    # todo: get two audios
    # todo: check if their hash is already present in the distance table
    # todo: if not, calculate features and distances and save to db
    # todo: check if the distances of features is the min or max
    # todo: if true, then update the extreme_distance_table
    # todo: calculate the new factor value based on the new extreme values
    # todo: and update that feature value in all the rows in feature table
    pass


if __name__ == '__main__':
    pass

