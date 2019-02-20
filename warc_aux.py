from warcio.archiveiterator import ArchiveIterator

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

