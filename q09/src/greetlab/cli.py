import argparse


def main():
    p = argparse.ArgumentParser(prog="sdt-greet")
    p.add_argument("--name", required=True, help="要问候的名字")
    a = p.parse_args()
    print(f"Hello, {a.name}!")
