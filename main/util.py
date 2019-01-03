import platform
import hashlib


def get_name(file):
    """
    get name of file from its filepath
    :param file:
    :return: name
    """
    plt = platform.system()
    if plt == 'Windows':
        file_list = file.split('\\')
        return file_list[len(file_list) - 1]
    elif plt == 'Linux':
        file_list = file.split('/')
        return file_list[len(file_list) - 1]
    elif plt == 'Darwin':
        file_list = file.split('/')
        return file_list[len(file_list) - 1]


def scale(rmin, rmax, val, tmin=0.0, tmax=10.0):
    """
    scale a value from list to a specific range
    :param rmin: min of list
    :param rmax: max of list
    :param val: current value from list
    :param tmin: target min
    :param tmax: target max
    :return: target value scaled
    """
    if rmin == rmax:
        return 0
    return ((val - rmin) / (rmax - rmin)) * (tmax - tmin) + tmin


def sha256sum(filename):
    """
    Calculate sha of a file
    :param filename:
    :return:
    """
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()
