#!/usr/bin/env python3
from __future__ import annotations

import os
import re

from pwn import context, log, remote, u64

FLAG_REGEX = re.compile(r"gctf{.*}")


def main() -> int:
    context.log_level = "error"

    HOST = "target"
    PORT = 1337

    rem_con = remote(HOST, PORT)

    # derive the key
    context.update(arch="amd64", endian="big")
    key = hex(((0x5443474D489DFDD3 + 12345678) ^ u64(b"HACKERS!")) >> 5)

    rem_con.recvuntil(b"Please input your key")
    rem_con.sendline(key.encode())

    output = rem_con.recvuntil(b"}").decode()
    flag = FLAG_REGEX.findall(output)

    if flag:
        print(f"Flag:\n\n{flag[0]}")
    else:
        log.error("Flag not found")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
