from __future__ import annotations

import argparse
import sys
from typing import Sequence

import password_cracker.core as core
import password_cracker.db as db


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="password-cracker",
        description="Simple password timing attack demo and user manager.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List stored users")

    add_parser = subparsers.add_parser("add", help="Add or update a user password")
    add_parser.add_argument("user", help="Username to add or update")
    add_parser.add_argument("password", help="Password to store")

    check_parser = subparsers.add_parser("check", help="Verify a password guess")
    check_parser.add_argument("user", help="Username to verify")
    check_parser.add_argument("guess", help="Password guess")
    check_parser.add_argument("--constant-time", action="store_true", help="Use constant-time comparison for verification")

    estimate_parser = subparsers.add_parser("estimate", help="Estimate a password length using timing")
    estimate_parser.add_argument("user", help="Username to estimate")
    estimate_parser.add_argument("--max-len", type=int, default=32, help="Maximum length to test")
    estimate_parser.add_argument("--trials", type=int, default=1000, help="Number of timing trials per length")
    estimate_parser.add_argument("--verbose", action="store_true", help="Show confidence scores while cracking")

    crack_parser = subparsers.add_parser("crack", help="Attempt to recover a password using timing differences")
    crack_parser.add_argument("user", help="Username to crack")
    crack_parser.add_argument("--length", type=int, help="Password length if already known")
    crack_parser.add_argument("--trials", type=int, default=1000, help="Measurements per trial")
    crack_parser.add_argument("--verbose", action="store_true", help="Show progress while cracking")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "list":
        users = db.list_users()
        print("Users:")
        for user in users:
            print(f"- {user}")
        return 0

    if args.command == "add":
        db.set_password(args.user, args.password)
        db.save_password_database()
        print(f"Saved password for user {args.user!r}.")
        return 0

    if args.command == "check":
        checker = db.check_password_constant_time if args.constant_time else db.check_password
        result = checker(args.user, args.guess)
        print("Match" if result else "No match")
        return 0 if result else 1

    if args.command == "estimate":
        length = core.estimate_password_length(
            args.user,
            max_len=args.max_len,
            trials=args.trials,
            verbose=args.verbose,
        )
        print(f"Estimated password length for {args.user!r}: {length}")
        return 0

    if args.command == "crack":
        length = args.length
        if length is None:
            length = core.estimate_password_length(args.user, verbose=args.verbose, trials=args.trials)
            print(f"Estimated length: {length}")

        try:
            password = core.crack_password(args.user, length, trials=args.trials, verbose=args.verbose)
        except KeyboardInterrupt:
            print("\nPassword crack interrupted by user.")
            if not args.verbose:
                print("Run with --verbose to see progress while cracking.")
            return 1
        
        print(f"Recovered password for {args.user!r}: {password}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
