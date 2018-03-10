import sys


def main():
    if __package__ == '':
        import os.path
        path = os.path.dirname(os.path.dirname(__file__))
        sys.path[0:0] = [path]
    from . import cli
    sys.exit(cli.atcodertools())


if __name__ == "__main__":
    sys.exit(main())
