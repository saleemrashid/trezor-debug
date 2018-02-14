#!/usr/bin/env python3
import io
import os
import re
import sys
import tokenize


REGEX_INTTYPE = re.compile("^u?int(8|16|32|64)_t$")
REGEX_SUFFIX = re.compile("^u?l?l?$", re.IGNORECASE)


def process_replacement_tokens(g):
    tokens = list(reversed(list(g)))

    while tokens:
        tok = tokens.pop()

        if tok[0] == tokenize.OP and tok[1] == "(":
            inner = tokens.pop()

            if inner[0] == tokenize.NAME and REGEX_INTTYPE.match(inner[1]):
                end = tokens.pop()

                if end[0] == tokenize.OP and end[1] == ")":
                    continue
                else:
                    tokens.append(end)
                    tokens.append(inner)
            else:
                tokens.append(inner)
        elif tok[0] == tokenize.NUMBER:
            suffix = tokens.pop()
            if suffix[0] == tokenize.NAME and REGEX_SUFFIX.match(suffix[1]):
                pass
            else:
                tokens.append(suffix)

        yield tok


def process_replacement(replacement):
    source = replacement.encode()

    g = tokenize.tokenize(io.BytesIO(source).readline)
    source = tokenize.untokenize(process_replacement_tokens(g))

    return source.decode()


def process(fsrc, fdst):
    allowed_header = False

    for line in fsrc:
        line = line.rstrip("\n")

        # Line markers
        if line.startswith("# "):
            filename = line.split()[2].strip("\"")
            folder, _, _ = filename.partition(os.path.sep)
            allowed_header = (folder == "libopencm3")

        # Macro definitions
        elif line.startswith("#define "):
            if not allowed_header:
                continue

            try:
                directive, identifier, replacement = line.split(None, 2)
            except ValueError:
                continue

            if identifier.startswith("_") or identifier.startswith("MMIO"):
                continue

            replacement = process_replacement(replacement)

            if "(" in identifier:
                fdst.write("def {}:\n".format(identifier))
                fdst.write("    return {}\n".format(replacement))
            else:
                fdst.write("{} = {}\n".format(identifier, replacement))


if __name__ == "__main__":
    process(sys.stdin, sys.stdout)
