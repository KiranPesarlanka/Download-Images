import sys
import shutil
import requests

from tqdm import tqdm
from basescript import BaseScript

class Downloader(BaseScript):
    DESC = 'Download Images'

    def __init__(self):
        super(Downloader, self).__init__()

    def define_args(self, parser):
	parser.add_argument('-u', '--url', help='Provide API URL')
        parser.add_argument('-p', '--path', help='Provide directory Absoulte Path to download')

    def save_image(self, url):
        _url = "_".join(url.split('/')[-2:])
        file_name = self.args.path + _url
        try:
            r = requests.get(url, stream = True)
            with open(file_name,'wb') as f:
                shutil.copyfileobj(r.raw, f)
        except Exception as err:
            print("FAILED---"+url)
            print(err)

    def extract_api(self):
        try:
            response = requests.get(self.args.url)
        except Exception as error:
            print(error)
            print("Unable to reach API")
            sys.exit()

        urls = []
        j_response = response.json()
        if "list" in j_response:
            elements = j_response["list"]
            for element in elements:
                urls.append(element.get("item_data", {}).get("image_url", ""))

        urls = filter(None, urls)
        self.log.info("Total images to download:" + str(len(urls)))
        for url in tqdm(urls):
            self.save_image(url)


    def run(self):

        self.log.info("Started Downloading")
        self.args.path = self.args.path if self.args.path.endswith("/") else self.args.path+"/"
        self.extract_api()
        self.log.info("Downloading Completed!")

if __name__ == '__main__':
    Downloader().start()
