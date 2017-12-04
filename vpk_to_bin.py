'''Combine VPK files into a single .bin file for use with the e-Reader.
If it works at all, its behavior is not well-understood.'''
import os
import glob
import warnings
import time
#import pdb
import bitstring
# for "notes" with chunk numbers
CARD_ID_DELIMITER = '_'
# this depends on the type of card you're using.
# Animal Crossing has 2 VPKs + 1 header = 3 chunks.
# could determine chunks per card programatically;
# it is probably even stored within the card itself
# see https://caitsith2.com/ereader/ereader%20card%20info.txt
# (but I don't think the answer is spelled out there)
CHUNKS_PER_CARD = 3
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/cards'
IN_DIR = dir + '/vpk/'
OUT_DIR = dir + '/bin/'

filenames = os.listdir(IN_DIR)
groups = set()
for file in filenames:
    card_id = file.partition(CARD_ID_DELIMITER)[0]
    groups.add(card_id)
# awaiting refactor but probably no longer needed
# bad_groups = set()
for group in groups:
    card_glob = glob.glob(IN_DIR + group + "*")
    # print(card_glob)
    if len(card_glob) < CHUNKS_PER_CARD:
        length_warn = "less than" + \
            str(CHUNKS_PER_CARD) + \
            " files/folders with similar names found; check the vpk folder."
    if len(card_glob) > CHUNKS_PER_CARD:
        length_warn = "more than" + \
            str(CHUNKS_PER_CARD) + \
            " files/folders with similar names found; check the vpk folder."
    if len(card_glob) != CHUNKS_PER_CARD:
        warnings.warn(length_warn)
        # there's probably a way to do the next 3 lines
        # within one for loop instead of 2
        # bad_groups.add(group)
        # like this?
        groups.discard(group)
# for bad_group in bad_groups:
#    groups.discard(bad_group)
# print(groups)
# current way of handling this messes up glob if you
# have a number of folders equal to CHUNKS_PER_CARD that
# match the wildcard rules for glob().
# ex. 3 folders named "old" "old 2" "old tests".
# can glob be set to ignore folders?
for group in groups:
    # pdb.set_trace()
    print(group)
    header_num = 0
    # there should only be one match for each call to glob() in the next line;
    # thus we extract the first/only match
    head_path = glob.glob(IN_DIR + group + "_" + str(header_num) + "*")[0]
    print(head_path)
    # https://pythonhosted.org/bitstring/creation.html#from-a-file
    # this will become the final card,
    # but the following line only adds the header to it
    card = bitstring.BitArray(filename=head_path)
    #card = bitstring.BitArray(00)
    print("head len: ", hex(card.len))
    # match group names with individual integers,
    # attempting to sort them from smallest to largest number
    # (glob does not sort items; hence the roundabout way of using glob twice)
    for num in range(1, CHUNKS_PER_CARD):
        chunk_path = glob.glob(IN_DIR + group + "_" + str(num) + "*")[0]
        print(glob.glob(IN_DIR + group + "_" + str(num) + "*"))
        print(chunk_path)
        # maybe some ".endswith" code here could remove folders?
        chunk = bitstring.Bits(filename=chunk_path)
        # length is a bit unintuitive -- it's the numeric length of
        # representing the bytes as hex characters.
        # iirc, divide by 2 and convert to hex to
        # get the typical hex-editor length.
        # beware, you might be debugging (hex length) errors
        # related to the next few lines for a while
        print("chunk lenth: ", chunk.length)
        # print(chunk.hex)
        card.append(chunk)
        # card.append(card)
        print("fl cl: ", card.length, " ", hex(card.length),
              " ", int(str(card.length), 16) / 2)
    # pad to the length of a proper e-Reader card .bin file.
    # obviously the length is different for short dotcodes, not yet handled.
    # not verified from any kind of documentation or reverse-engineering!
    # May break things! Further testing needed!
    proper_length = 0x81c
    # 0x840? proper_length used to be 0x81c, and it worked through some fluke.
    # I think it may work as long as the data isn't truncated and it is
    # bit-aligned to end on a multiple of 16 bytes
    # (like the last column in a hex editor).
    print("prop len: ", proper_length, hex(proper_length))
    pad_length = int(proper_length - (card.length / 8))
    print("card l: ", card.length, " ", hex(card.length))
    print("pad l: ", pad_length, "\n")
    # VBA doesn't like our cards! Let's add one non-zero byte if
    # it's not proper_length long already. 0x01 and 0xAA both
    # seem to work for example.
    # life is confusing. maybe this next block isn't needed.
    # makes more of an issue if the length is 0x840 and not 0x81c? what?
    # if pad_length >= 1:
    #    print("asdf")
    #    card.append(b"\00") #should be 0x01 not 0x00
    #    pad_length = pad_length - 1
    #    print("pl: ", pad_length, "\n")
    # b"\00" multiplies differently than 0x00!
    # the latter cancels out to 0, which is not what we want.
    print(b"\00" * pad_length)
    # other byte sequences might work; I think official cards pad
    # bytes in sequence: for example, E0, E1, ..., FE, FF, 00, 01, ...
    card.append(b"\00" * pad_length)

    # https://stackoverflow.com/questions/10607688/how-to-create-a-file-name-with-the-current-date-time-in-python
    timestr = time.strftime("%Y%m%d-%H%M%S")
    out_name = OUT_DIR + group + '_' + timestr + ".bin"
    open(out_name, 'wb').write(card.tobytes())
    # the final note I have from working on this (unfinished) script:
    # the sizes from the bitarray() etc functions are actually correct,
    # so what is the issue? the pad_length calcuation? negatives?
