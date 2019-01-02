def scale(rmin, rmax, val, tmin=0.0, tmax=10.0):
    if rmin == rmax:
        return 1
    return ((val - rmin) / (rmax - rmin)) * (tmax - tmin) + tmin
