from link_finder import LinkFinder
from domain import *
from general import *
import Library.Connection as CustomConnection
import os


class Spider:
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    web_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        super().__init__()
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.web_file = os.path.join(Spider.project_name,'www')
        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(page_url)
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()
            Spider.add_to_web_tree(page_url)

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        try:
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(CustomConnection.URL(page_url))
        except:
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url not in Spider.queue) and (url not in Spider.crawled) and (Spider.domain_name == get_domain_name(url)):
                Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

    @staticmethod
    def add_to_web_tree(path):
        try:
            print(path)
            page_html = CustomConnection.URL(path)
            path = path.split(Spider.domain_name,1)[1][1:]
            path = Spider.web_file+"/"+ path
            print(path)
            if '/' in path:
                path = path.split('/')
                file = path.pop(-1)
                path = os.sep.join(path)
                file_path = os.path.join(path, file)
            else:
                file_path = path

            if not os.path.exists(path):
                os.makedirs(path)
            if not os.path.isfile(file_path):
                write_file(file_path, page_html)
        except:
            print("Path is not working correct")
            raise

if __name__ == "__main__":
    s = Spider("j", 'http://www.jeddah.gov.sa/index.php', 'jeddah.gov.sa')
    s.add_to_web_tree('http://www.jeddah.gov.sa/Amanah/index.php')
