import sys
import argparse

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

def get_args(argv=None):
    parser = argparse.ArgumentParser(description="AWBW tool")
    return parser.parse_args(argv)

def main(args):
    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main(get_args()))
