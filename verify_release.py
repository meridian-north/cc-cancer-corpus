#!/usr/bin/env python3
"""Check public release bytes against an unsigned SHA-256 manifest, offline.

--write updates only the manifest for the explicit reviewed inventory. Neither mode
scans for new files, signs a release, validates clinical claims or contacts a server.
"""
import argparse
import hashlib
from pathlib import Path, PurePosixPath
import re
import sys
import subprocess

INVENTORY = "PUBLIC_RELEASE_FILES.txt"
MANIFEST = "MANIFEST_SHA256.txt"


def safe_file(root, name):
    parts = PurePosixPath(name)
    if (not name or parts.is_absolute() or "\\" in name or any(p in ("", ".", "..") for p in name.split("/"))
            or any(c.isspace() for c in name) or parts.as_posix() != name):
        raise ValueError("unsafe release path: %r" % name)
    path = root
    for part in parts.parts:
        path = path / part
        if path.is_symlink():
            raise ValueError("symlink not permitted: %s" % name)
    if not path.is_file():
        raise ValueError("missing release file: %s" % name)
    return path


def inventory(root):
    names = safe_file(root, INVENTORY).read_text(encoding="utf-8").splitlines()
    if not names or len(names) != len(set(names)) or names != sorted(names):
        raise ValueError("inventory must be nonempty, unique and sorted")
    if MANIFEST in names:
        raise ValueError("manifest cannot hash itself")
    for name in names:
        safe_file(root, name)
    return names


def expected_manifest(root):
    return "".join(hashlib.sha256(safe_file(root, name).read_bytes()).hexdigest() + "  " + name + "\n"
                   for name in inventory(root))


def verify(root):
    names = inventory(root)
    contents = safe_file(root, MANIFEST).read_text(encoding="utf-8")
    lines = contents.splitlines()
    listed = []
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            raise ValueError("invalid manifest line")
        listed.append(match[2])
    if listed != names:
        raise ValueError("manifest paths differ from the reviewed inventory")
    if contents != expected_manifest(root):
        raise ValueError("release bytes differ from manifest; review the changes before regenerating")
    return len(names)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--tracked", action="store_true", help="Also require every Git-tracked file (except the manifest) in the inventory.")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.write:
            destination = root / MANIFEST
            if destination.is_symlink():
                raise ValueError("manifest cannot be a symlink")
            content = expected_manifest(root)
            destination.write_text(content, encoding="utf-8")
        count = verify(root)
        if args.tracked:
            tracked = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], check=True, capture_output=True).stdout.decode("utf-8").split("\0")
            if sorted(name for name in tracked if name and name != MANIFEST) != inventory(root):
                raise ValueError("Git-tracked public files differ from inventory")
    except (OSError, UnicodeError, ValueError, subprocess.CalledProcessError) as exc:
        print("RELEASE_CHECK_FAILED: %s" % exc, file=sys.stderr)
        return 1
    print("LOCAL_RELEASE_BYTES_MATCH: %d files. Unsigned manifest; issuer and scientific claims not authenticated." % count)
    return 0

if __name__ == "__main__":
    sys.exit(main())
