from os.path import splitext, basename
import urllib
from urllib.parse import urlparse
import urllib.request
from urllib.request import urlretrieve
import sys


class ImageUrlDownloader(object):
    imageurl = ''
    outdir = ''
    filename = ''

    def __init__(self, url, outdir, filename):
        self.imageurl = url
        self.outdir = outdir
        disassembled = urlparse(url)
        file, file_ext = splitext(basename(disassembled.path))
        if not filename:
            self.filename = file + file_ext
        else:
            self.filename = filename + file_ext

    def download(self):
        filepath = self.outdir + self.filename
        urlretrieve(self.imageurl, filepath, self.reporthook)

    def reporthook(self, blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            s = "\r%5.1f%% %*d / %d" % (
                percent, len(str(totalsize)), readsofar, totalsize)
            sys.stderr.write(s)
            if readsofar >= totalsize: # near the end
                sys.stderr.write("\n")
        else: # total size is unknown
            sys.stderr.write("read %d\n" % (readsofar,))
