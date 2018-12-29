from main.db import Db
from main.datastructure.feature import Feature
from main.datastructure.distance import Distance
from main.extractor import Extractor
from main.hash import sha256sum
from main.scale import scale
import os

database_name = 'db.sqlite'
audio_folder_name = 'audio_resources'
root_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
db_file = os.path.join(root_dir_path, database_name)
audio_path = os.path.join(root_dir_path, audio_folder_name)


def initialize_extreme_dist_table_and_update_it():
    db = Db(storage_file=db_file)
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


def test_update_factor():
    db = Db(storage_file=db_file)
    hash2 = '9e0035d3ef4d0f06bfa161f328e6bb78a5e20e291b46463722dddf2eee62b1ab'
    hash1 = 'e4d5bb5509746f7ed8feb98ea41fa797a30ebf6dda68507b094bb4d3b4ae7c89'
    dist = Distance(hash1=hash1, hash2=hash2, mfcc_dist=1.1, chroma_cens_dist=1.1, chroma_stft_dist=1.0, mel_dist=1.0,
                    tonnetz_dist=1.0, rhythm_dist=1.0)
    print(db.update_factors(dist))


def check_hashes_present():
    db = Db(storage_file=db_file)
    hash1 = '9e0035d3ef4d0f06bfa161f328e6bb78a5e20e291b46463722dddf2eee62b1ab'
    hash2 = 'e4d5bb5509746f7ed8feb98ea41fa797a30ebf6dda68507b094bb4d3b4ae7c89'
    print(db.is_hashes_present(hash1, hash2))


def get_extreme_distance():
    db = Db(storage_file=db_file)
    asd = db.get_extreme_distances()
    print(asd)


def init_extreme_table(db):
    max = 1.7976931348623157e+308
    min_feature = Feature(mfcc=max, chroma_cens=max, chroma_stft=max, mel=max, tonnetz=max, rhythm=max)
    max_feature = Feature(mfcc=0.0, chroma_cens=0.0, chroma_stft=0.0, mel=0.0, tonnetz=0.0, rhythm=0.0)
    return db.set_initial_extreme_distance(min_feature=min_feature, max_feature=max_feature)


def get_features():
    ex = Extractor()
    db = Db(storage_file=db_file)
    print('Creating tables if not present...')
    if not db.create_tables():
        return
    print('Initializing extreme distance tables...')
    if not init_extreme_table(db):
        return

    # todo: loop over the directory
    list_of_files = os.listdir(audio_path)
    list_of_files_processed = []
    i = 0
    while i < len(list_of_files):
        ifile = list_of_files[i]
        # todo: get two audios
        if ifile not in list_of_files_processed:
            list_of_files_processed.append(ifile)
            ifeature = ex.get_all_features(os.path.join(audio_path, ifile))
            j = i + 1
            while j < len(list_of_files):
                jfile = list_of_files[j]

                ifile_sha = sha256sum(os.path.join(audio_path, ifile))
                jfile_sha = sha256sum(os.path.join(audio_path, jfile))
                # todo: check if their hash is already present in the distance table
                if db.is_hashes_present(ifile_sha, jfile_sha):
                    print(ifile, ' and ', jfile, ' already present in database')
                    j += 1
                    continue
                else:
                    # todo: if not, calculate features and distances and save to db
                    jfeature = ex.get_all_features(os.path.join(audio_path, jfile))
                    dist = ex.get_distance(ifeature, jfeature)
                    db.save_feature_distances(dist)

                    # should compute its factors here but will do for all together in the end

                    # todo: check if the distances of features is the min or max
                    ext_dist = db.get_extreme_distances()
                    # todo: if true, then update the extreme_distance_table
                    if dist.mfcc_dist > ext_dist[0][2]:
                        db.update_max_distance('mfcc', dist.mfcc_dist)
                    if dist.mfcc_dist < ext_dist[0][1]:
                        db.update_min_distance('mfcc', dist.mfcc_dist)

                    if dist.chroma_cens_dist > ext_dist[1][2]:
                        db.update_max_distance('chroma_cens', dist.chroma_cens_dist)
                    if dist.chroma_cens_dist < ext_dist[1][1]:
                        db.update_min_distance('chroma_cens', dist.chroma_cens_dist)

                    if dist.chroma_stft_dist > ext_dist[2][2]:
                        db.update_max_distance('chroma_stft', dist.chroma_stft_dist)
                    if dist.chroma_stft_dist < ext_dist[2][1]:
                        db.update_min_distance('chroma_stft', dist.chroma_stft_dist)

                    if dist.mel_dist > ext_dist[3][2]:
                        db.update_max_distance('mel', dist.mel_dist)
                    if dist.mel_dist < ext_dist[3][1]:
                        db.update_min_distance('mel', dist.mel_dist)

                    if dist.tonnetz_dist > ext_dist[4][2]:
                        db.update_max_distance('tonnetz', dist.tonnetz_dist)
                    if dist.tonnetz_dist < ext_dist[4][1]:
                        db.update_min_distance('tonnetz', dist.tonnetz_dist)

                    if dist.rhythm_dist > ext_dist[5][2]:
                        db.update_max_distance('rhythm', dist.rhythm_dist)
                    if dist.rhythm_dist < ext_dist[5][1]:
                        db.update_min_distance('rhythm', dist.rhythm_dist)
                j += 1
        i += 1


def calculate_factors():
    print('Calcuating factors....')
    db = Db(storage_file=db_file)
    distances = db.get_complete_distance_table()
    extremes = db.get_extreme_distances()
    for dist in distances:
        # check if previously its value is 0.0, here only checking if mfcc = 0
        if dist[3] == 0.0:
            # todo: calculate the new factor value based on the new extreme values
            mfcc_factor = scale(rmin=extremes[0][1], rmax=extremes[0][2], val=dist[2])
            chroma_cens_factor = scale(rmin=extremes[1][1], rmax=extremes[1][2], val=dist[4])
            chroma_stft_factor = scale(rmin=extremes[2][1], rmax=extremes[2][2], val=dist[6])
            mel_factor = scale(rmin=extremes[3][1], rmax=extremes[3][2], val=dist[8])
            tonnetz_factor = scale(rmin=extremes[4][1], rmax=extremes[4][2], val=dist[10])
            rhythm_factor = scale(rmin=extremes[5][1], rmax=extremes[5][2], val=dist[12])
            new_dist_factor = Distance(hash1=dist[0], hash2=dist[1], mfcc_dist=mfcc_factor,
                                       chroma_cens_dist=chroma_cens_factor, chroma_stft_dist=chroma_stft_factor,
                                       mel_dist=mel_factor, tonnetz_dist=tonnetz_factor, rhythm_dist=rhythm_factor)
            # todo: and update that feature value in all the rows in feature table
            db.update_factors(new_dist_factor)


def print_factors():
    db = Db(storage_file=db_file)
    factors = db.get_all_factors()
    t = 0
    min = 0
    max = 0
    list = []
    for fact in factors:
        sum = fact[2] + fact[3] + fact[4] + fact[5] + fact[6] + fact[7]
        if t == 0:
            min = sum
            max = sum
            t += 1
        else:
            if sum < min:
                min = sum
            elif sum > max:
                max = sum

    for fact in factors:
        sum = fact[2] + fact[3] + fact[4] + fact[5] + fact[6] + fact[7]
        print(fact[0], ' and ', fact[1], ' ==> ', scale(min, max, sum))


if __name__ == '__main__':
    get_features()
    calculate_factors()
    print_factors()
