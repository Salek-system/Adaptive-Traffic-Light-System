import enum
import logging

# setting the logger
for handler in logging.root.handlers[:]:  # make sure all handlers are removed
    logging.root.removeHandler(handler)
logging.root.setLevel(logging.DEBUG)
logging_format = logging.Formatter('%(asctime)s: %(levelname)s [%(name)s:%(funcName)s:%(lineno)d] - %(message)s')
h = logging.StreamHandler()
h.setFormatter(logging_format)
logging.root.addHandler(h)


class RoadsNames(enum.Enum):
    H1 = [0, 1, 5, 6]  #
    H2 = [7, 8, 9, 10]
    V1 = [16, 15, 14]
    V2 = [2, 3, 4]
    V3 = [13, 12, 11]


#        V1      V2      V3
#        |       |       |
# H1 ----------------------------->
#        |       |       |
# H2 <-----------------------------
#        |       |       |
#        V
