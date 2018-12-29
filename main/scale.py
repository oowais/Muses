def scale(rmin, rmax, val, tmin=0.0, tmax=10.0):
    return ((val - rmin) / (rmax - rmin)) * (tmax - tmin) + tmin
