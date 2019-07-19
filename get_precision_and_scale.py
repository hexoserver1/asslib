def get_precision_and_scale(n, max_digits=14):
    """
                precision, scale = get_precision_and_scale(n)

                where
                    n is a floating point number
                    precision is the precision of n
                    scale is the scale of n

                Gets precision and scale values of a given floating point number (n)

                Thanks to Mark Ransom - https://stackoverflow.com/users/5987/mark-ransom

                title - get_precision_and_scale vr - 1.1 author - Mark Ransom date - 20100610

                mods - 1.1 Corrections to code styling and added optional max_digits argument (20190717fakas)
        """
    from math import log10

    int_part = int(abs(n))
    magnitude = 1 if int_part == 0 else int(log10(int_part)) + 1
    if magnitude >= max_digits:
        return magnitude, 0
    frac_part = abs(n) - int_part
    multiplier = 10 ** (max_digits - magnitude)
    frac_digits = multiplier + int(multiplier * frac_part + 0.5)
    while frac_digits % 10 == 0:
        frac_digits /= 10
    scale = int(log10(frac_digits))
    return magnitude + scale, scale


def unix_to_adyf(unix_time, milli=False):
    # Convert a Unix  timestamp or a numpy array of Unix timestamps to
    # ADYFAA01 (Day number and day fraction since 1760-01-01 00:00)

    if milli:
        # If timestamp is in milliseconds rather than seconds
        unix_time /= 1000

    adyf_time = (unix_time - 18144000) / 86400
    return adyf_time
