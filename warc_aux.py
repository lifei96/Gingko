from warcio.archiveiterator import ArchiveIterator
import os
import boto3
import botocore
import csv
import pymysql
import pymysql.cursors
import random

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

def matchSite(site_list, a_url):
    # return the matching site in the list (if found)
    # return None otherwise
    a_url = a_url.lower()
    for c in site_list:
        if c.lower() in a_url:
            return c
    return None

def storeInSQL(connection, site, http_headers, rec_headers, is_fake, raw_html):
    """CREATE TABLE `web_pages`(
        `site` TEXT,
        `is_fake` INT,
        `http_headers` MEDIUMTEXT,
        `rec_headers` MEDIUMTEXT,
        `html` MEDIUMTEXT
    );
    """
    print(site)
    with connection.cursor() as cursor:
        sql = "INSERT INTO `web_pages` VALUES (%s, %s, %s, %s, %s)"
        http_headers_str = str(http_headers)
        rec_headers_str = str(rec_headers)
        cursor.execute(sql, (site, is_fake, http_headers_str, rec_headers_str, raw_html))
    connection.commit()

def storeInSQL2(connection, site, http_headers, rec_headers, raw_html):
    """CREATE TABLE `web_pages2`(
        `site` TEXT,
        `http_headers` MEDIUMTEXT,
        `rec_headers` MEDIUMTEXT,
        `html` MEDIUMTEXT
    );
    """
    with connection.cursor() as cursor:
        sql = "INSERT INTO `web_pages2` VALUES (%s, %s, %s, %s)"
        http_headers_str = str(http_headers)
        rec_headers_str = str(rec_headers)
        cursor.execute(sql, (site, http_headers_str, rec_headers_str, raw_html))
    connection.commit()

def handleOneSegment(warc_file_path, site_list, is_fake=1):
    connection = pymysql.connect(host='localhost',
                                 port=8889,
                                 user='root',
                                 password='root',
                                 db='gingko',
                                 cursorclass=pymysql.cursors.DictCursor)
    with open(warc_file_path, 'rb') as f:
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
                html = record.content_stream().read().decode("cp437")
                rec_headers = record.__dict__['rec_headers'].headers
                for h in rec_headers:
                    if h[0] == 'WARC-Target-URI':
                        if h[1].startswith("http://") or h[1].startswith("https://"):
                            site = matchSite(site_list, h[1])
                            if site:
                                storeInSQL(connection, site, headers, rec_headers, is_fake, html)
    connection.close()

def handleOneMonth(paths_filepath, site_list, is_fake=1):
    f = open(paths_filepath)
    lines = f.readlines()
    f.close()
    for line in lines:
        l = line[:-1]
        print(l)
        downloadSegment(remote_path=l, save_path="./current.warc.gz")
        print("(downloaded)")
        handleOneSegment("./current.warc.gz", site_list, is_fake)
        os.remove("./current.warc.gz")

site_dict = dict()

def get_site_dict():
    global site_dict
    return site_dict

def download_out_of_list_pages(paths_filepath, site_list):
    global site_dict
    f = open(paths_filepath)
    lines = f.readlines()
    f.close()
    random.shuffle(lines)
    for line in lines[:5]:
        l = line[:-1]
        print(l)
        downloadSegment(remote_path=l, save_path="./current.warc.gz")
        print("(downloaded)")
        #
        connection = pymysql.connect(host='localhost',
                                     port=3306,
                                     user='root',
                                     password='root',
                                     db='gingko',
                                     cursorclass=pymysql.cursors.DictCursor)
        with open("./current.warc.gz", 'rb') as f:
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
                    html = record.content_stream().read().decode("cp437")
                    rec_headers = record.__dict__['rec_headers'].headers
                    url = ""
                    site = None
                    for h in rec_headers:
                        if h[0] == 'WARC-Target-URI':
                            if h[1].startswith("http://") or h[1].startswith("https://"):
                                site = matchSite(site_list, h[1])
                                url = h[1]
                                break
                    if site == None:
                        if url.find('/', 9) < 0:
                            continue
                        site = url[:url.find('/', 9)]
                        if site not in site_dict:
                            site_dict[site] = 0
                        if site_dict[site] >= 5:
                            continue
                        site_dict[site] += 1
                        storeInSQL2(connection, site, headers, rec_headers, html)
        connection.close()
        #
        os.remove("./current.warc.gz")
