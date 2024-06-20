import os

INVALID_COMMAND = 'INVALID COMMAND'
ROOT_PATH = f'{__file__}/../..'
SSD_FILE_PATH = f'{ROOT_PATH}/virtual_ssd_pkg/ssd.py'
RESULT_FILE_PATH = f'{ROOT_PATH}/result.txt'
HELP_MESSAGE = """============================== Command Guide ==============================
1) write [LBA] [value]
: write [value] to [LBA].
: [LBA] should be an integer between 0 and 99.
: [value] should be in hexadecimal format between 0x00000000 and 0xFFFFFFFF.
2) read [LBA]
: read the value written to [LBA].
3) fullwrite [value]
: write [value] to all LBA(0~99).
: [value] should be in hexadecimal format between 0x00000000 and 0xFFFFFFFF.
4) fullread
: read the all LBA(0~99) values.
5) exit
: quit the shell.
6) help
: see the command guide."""
MIN_LBA = 0
MAX_LBA = 99
MAX_NUM_LBA = 100
MIN_ERASE_SIZE = 1
MAX_ERASE_SIZE = 100
MAX_SIZE_PER_COMMAND = 10
COMMAND_DIR_PATH = os.path.join(os.path.dirname(f'{__file__}'), 'commands')