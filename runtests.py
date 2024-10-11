import os
import sys
import subprocess
import argparse

def cli_params():
    """CLI tools"""
    parser = argparse.ArgumentParser(description="Run tests")
    parser.add_argument(
        'test_module', nargs='?', default='tests', help='Target a specific test module'
    )
    parser.add_argument(
        "-f", "--flags",
        dest="flags",
        nargs='*',
        default=[],
        help="flags to be passed to pytest e.g. -vv",
    )
    return parser.parse_args()


def run_tests(test_module, flags):
    repo_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_root)
    cmd = [sys.executable, "-m", "pytest"] \
        + flags \
        + [test_module]
    result = subprocess.run(cmd, check=False)
    sys.exit(result.returncode)    

def main():
    args = cli_params()
    flags = args.flags
    flags = ['-' + i for i in args.flags]
    run_tests(args.test_module, flags)


if __name__ == "__main__":
    main()
