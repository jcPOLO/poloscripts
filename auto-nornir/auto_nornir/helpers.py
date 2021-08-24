import ipaddress
import os
import errno
import logging
import sys
from typing import List, Union


dir_path = os.path.dirname(os.path.realpath(__file__))


def is_ip(string: str) -> bool:
    try:
        ipaddress.ip_address(string)
        return True
    except ValueError:
        return False


def check_directory(path: str):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def is_int(v: any) -> bool:
    v = str(v).strip()
    return v == '0' or (v if v.find('..') > -1 else v.lstrip('-+').rstrip('0').rstrip('.')).isdigit()


def get_platforms(path='templates') -> list:
    if not os.path.exists(os.path.dirname(path)):
        try:
            return os.listdir(path)
        except Exception as e:
            raise e


def configure_logging(logger, debug=''):
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    fh = logging.FileHandler(f'{dir_path}/auto-nornir.log')
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    # ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


class HumanBytes:
    ''' 
    USAGE
        print(HumanBytes.format(2251799813685247)) # 2 pebibytes
        print(HumanBytes.format(2000000000000000, True)) # 2 petabytes
        print(HumanBytes.format(1099511627776)) # 1 tebibyte
        print(HumanBytes.format(1000000000000, True)) # 1 terabyte
        print(HumanBytes.format(1000000000, True)) # 1 gigabyte
        print(HumanBytes.format(4318498233, precision=3)) # 4.022 gibibytes
        print(HumanBytes.format(4318498233, True, 3)) # 4.318 gigabytes
        print(HumanBytes.format(-4318498233, precision=2)) # -4.02 gibibytes
    '''
    METRIC_LABELS: List[str] = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    BINARY_LABELS: List[str] = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    PRECISION_OFFSETS: List[float] = [0.5, 0.05, 0.005, 0.0005] # PREDEFINED FOR SPEED.
    PRECISION_FORMATS: List[str] = ["{}{:.0f} {}", "{}{:.1f} {}", "{}{:.2f} {}", "{}{:.3f} {}"] # PREDEFINED FOR SPEED.

    @staticmethod
    def format(num: Union[int, float], metric: bool=False, precision: int=1) -> str:
        """
        Human-readable formatting of bytes, using binary (powers of 1024)
        or metric (powers of 1000) representation.
        """

        assert isinstance(num, (int, float)), "num must be an int or float"
        assert isinstance(metric, bool), "metric must be a bool"
        assert isinstance(precision, int) and precision >= 0 and precision <= 3, "precision must be an int (range 0-3)"

        unit_labels = HumanBytes.METRIC_LABELS if metric else HumanBytes.BINARY_LABELS
        last_label = unit_labels[-1]
        unit_step = 1000 if metric else 1024
        unit_step_thresh = unit_step - HumanBytes.PRECISION_OFFSETS[precision]

        is_negative = num < 0
        if is_negative: # Faster than ternary assignment or always running abs().
            num = abs(num)

        for unit in unit_labels:
            if num < unit_step_thresh:
                # VERY IMPORTANT:
                # Only accepts the CURRENT unit if we're BELOW the threshold where
                # float rounding behavior would place us into the NEXT unit: F.ex.
                # when rounding a float to 1 decimal, any number ">= 1023.95" will
                # be rounded to "1024.0". Obviously we don't want ugly output such
                # as "1024.0 KiB", since the proper term for that is "1.0 MiB".
                break
            if unit != last_label:
                # We only shrink the number if we HAVEN'T reached the last unit.
                # NOTE: These looped divisions accumulate floating point rounding
                # errors, but each new division pushes the rounding errors further
                # and further down in the decimals, so it doesn't matter at all.
                num /= unit_step       

        return HumanBytes.PRECISION_FORMATS[precision].format("-" if is_negative else "", num, unit)

