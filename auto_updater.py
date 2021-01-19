import requests
from bs4 import BeautifulSoup


class HostsAutoUpdater(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def get_ips(self, urls):
        urls_ipaddr = []
        for url in urls:
            segs = url.split('.')
            domain = '.'.join(segs[-2:])
            url_ip = 'https://{}.ipaddress.com/{}'.format(domain, url)
            urls_ipaddr.append(url_ip)
        ips = {}
        for i, url in enumerate(urls_ipaddr):
            print('Get {} ...'.format(url))
            r = requests.get(url)
            if r.status_code == 200:
                # print('get {} return content: {}'.format(url, r.content))
                bs = BeautifulSoup(r.content, 'html.parser')
                links = bs.find_all('a')
                # print('links: {}'.format(links))
                for link in links:
                    href = link.get('href')
                    if href.find('https://www.ipaddress.com/ipv4/') >= 0:
                        ip = link.text
                        ips[urls[i]] = ip
            else:
                print('Error')
        print(ips)
        return ips

    def update_hosts(self, fn, pairs):
        print('new pairs: {}'.format(pairs))
        with open(fn, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if not line.startswith('#'):
                    segs = line.strip().split()
                    if len(segs) > 1:
                        # there may be more than one url in a line
                        ip = segs[0]
                        url = ' '.join(segs[1:])
                        print('{}: {}'.format(url, ip))
                        # keep old ones
                        if pairs.get(url) is None:
                            pairs[url] = ip
        print('whole pairs: {}'.format(pairs))
        with open(fn, 'w') as f:
            for k in pairs.keys():
                f.write('{}\t{}\n'.format(pairs[k], k))
        print('Finished writing file {}'.format(fn))


def main():
    urls = [
        "github.githubassets.com",
        "camo.githubusercontent.com",
        "github.map.fastly.net",
        "github.global.ssl.fastly.net",
        "github.com",
        "api.github.com",
        "raw.githubusercontent.com",
        "user-images.githubusercontent.com",
        "favicons.githubusercontent.com"
    ]
    hau = HostsAutoUpdater()
    pairs = hau.get_ips(urls)
    fn = '/etc/hosts'
    hau.update_hosts(fn, pairs)


if __name__ == '__main__':
    main()
