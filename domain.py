from urllib.parse import urlparse


# Get domain name (example.com)
def get_domain_name(url, lvl=4):
    try:
        results = get_sub_domain_name(url).split('.')
        domain =''
        for i in range(lvl):
            domain += results[i-lvl] + ('.' if i != (lvl-1) else '')
        return domain
    except:
        return ''


# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
