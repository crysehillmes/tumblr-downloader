import argparse
import os
from imageurldetector import ImageUrlDetector
from imagedownloader import ImageUrlDownloader

parser = argparse.ArgumentParser(description="A simple download tool for tumblr blog.")
group = parser.add_mutually_exclusive_group()
group.add_argument("-b", "--blog")
parser.add_argument("-o", '--outdir')
parser.add_argument("-s", '--start', type=int)
parser.add_argument("-s", '--end', type=int)
parser.add_argument("-p", '--proxy')
args = parser.parse_args()

blog = args.blog
start = args.start
if not start:
    start = 0
proxy = args.proxy
outdir = args.outdir
if not outdir.endswith('/'):
    outdir += '/'
detector = ImageUrlDetector(blog, start, proxy)
detector.detect()
piclist = detector.getimageurls()
piccount = len(piclist)
print('Image Count: ' + str(piccount))
if not os.path.exists(outdir):
    os.makedirs(outdir)
for index, picurl in enumerate(piclist):
    print('Downloading [' + str(index + 1) + ' / ' + str(piccount) + ']')
    downloader = ImageUrlDownloader(picurl, outdir, str(index))
    downloader.download()
