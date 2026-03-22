#!/usr/bin/env python

"""CLI tool for managing AI Daily Brief subscribers.

Provides simple commands to add, remove, and list subscriber email
addresses stored in the JSON file used by the service.
"""

import argparse
from subscriptions import add_subscriber, remove_subscriber, load_subscribers


def main():
    parser = argparse.ArgumentParser(description="Manage AI Daily Brief subscribers")
    subparsers = parser.add_subparsers(dest="command")

    # add command
    add_parser = subparsers.add_parser("add", help="Add a subscriber email")
    add_parser.add_argument("email", help="Email address to add")

    # remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a subscriber email")
    remove_parser.add_argument("email", help="Email address to remove")

    # list command
    subparsers.add_parser("list", help="List all subscriber emails")

    args = parser.parse_args()

    if args.command == "add":
        add_subscriber(args.email)
        print(f"added subscriber: {args.email}")
    elif args.command == "remove":
        remove_subscriber(args.email)
        print(f"removed subscriber: {args.email}")
    elif args.command == "list":
        subs = load_subscribers()
        print("current subscribers:")
        for s in subs:
            print(f" - {s}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
