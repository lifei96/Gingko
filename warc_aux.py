from warcio.archiveiterator import ArchiveIterator
import boto3
import botocore
import csv

def getSetOfSites(filename):
    result = set()
    with open(filename, 'rb') as f:
        for record in ArchiveIterator(f):
            if record.rec_type == 'response':
                headers = record.__dict__['http_headers'].headers
                content_type = ""
                for h in headers:
                    if h[0] == 'Content-Type':
                        content_type = h[1]
                        break
                if not content_type.startswith("text/html"):
                    continue
                rec_headers = record.__dict__['rec_headers'].headers
                for h in rec_headers:
                    if h[0] == 'WARC-Target-URI':
                        if h[1].startswith("http://") or h[1].startswith("https://"):
                            result.add(h[1][ : h[1].find('/', len('https://'))])
                        break
    return result

def downloadSegment(remote_path, save_path):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket("commoncrawl")
    bucket.download_file(remote_path, save_path)

def loadSiteList(csv_path):
    result = list()
    with open(csv_path) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            result.append(row[0].lower())
    return result

def matchSite(cite_list, a_url):
    # return the matching site in the list (if found)
    # return None otherwise
    a_url = a_url.lower()
    for c in cite_list:
        if c in a_url:
            return c
    return None

def storeInSQL():
    # TBD
    pass

def handleOneSegment(warc_file_path):
    # TBD
    pass
