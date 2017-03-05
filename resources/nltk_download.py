import argparse
import nltk
import ssl

parser = argparse.ArgumentParser(description='Downloads and install NLTK data')
parser.add_argument('-d', '-D', '--dir', metavar='<PATH>', type=str, help='Install directory')
args = parser.parse_args()

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

download_dir = None
if args.dir:
    download_dir = args.dir

nltk.download(info_or_id='stopwords', download_dir=download_dir)
nltk.download(info_or_id='punkt', download_dir=download_dir)