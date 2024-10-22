#!/usr/bin/env python3

import errno
import logging
import os
import stat
import sys
import threading

from fuse import FUSE, Operations

from cache import Cache

# Configure logging
logging.basicConfig(level=logging.INFO)


class BlogFS(Operations):
    def __init__(self):
        self.cache = Cache()
        self.files = self.cache.get_posts()
        self.fd = 0
        self.rwlock = threading.Lock()

    def readdir(self, path, fh):
        logging.info(f"readdir: {path}")
        dirents = ['.', '..']
        if path == '/':
            dirents.extend(self.files.keys())
        return dirents

    def getattr(self, path, fh=None):
        logging.info(f"getattr: {path}")
        if path == '/':
            return dict(
                st_mode=(stat.S_IFDIR | 0o755), st_nlink=2
            )
        elif path[1:] in self.files:
            post = self.files[path[1:]]
            attrs = dict(
                st_mode=(stat.S_IFREG | 0o444),
                st_nlink=1,
                st_size=len(post['content'].encode('utf-8')),
                st_ctime=post['created_at'] / 1000,
                st_mtime=post['updated_at'] / 1000,
                st_atime=post['updated_at'] / 1000,
            )
            return attrs
        else:
            raise FileNotFoundError(errno.ENOENT)

    def open(self, path, flags):
        logging.info(f"open: {path}")
        if path[1:] not in self.files:
            raise FileNotFoundError(errno.ENOENT)
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if flags & accmode != os.O_RDONLY:
            raise PermissionError(errno.EACCES)
        return 0

    def read(self, path, size, offset, fh):
        logging.info(f"read: {path}, size: {size}, offset: {offset}")
        post = self.files.get(path[1:])
        if post is None:
            raise FileNotFoundError(errno.ENOENT)
        content = post['content'].encode('utf-8')
        return content[offset : offset + size]


def main(mountpoint):
    FUSE(BlogFS(), mountpoint, nothreads=True, foreground=True)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <mountpoint>")
        sys.exit(1)
    mountpoint = sys.argv[1]
    main(mountpoint)

