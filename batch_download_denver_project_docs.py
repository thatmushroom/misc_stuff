import bs4
import requests
import urllib
import time
import os

class denvergov_project_scraper(object):
    def __init__(self):
        self.valid_prefix = '2021-' # Cut down on scraping old stuff by default
        # Config
        self.project_list_site_url = 'https://www.denvergov.org/api/streets/row/projects'
        self.download_base_url = 'https://www.denvergov.org/media/denverapps/planreview/'
        self.sleep_timer_config = 5 # 
        self.project_list_list = [] # Overall list
        self.project_file_list = [] # Project-specific, to be overwritten 

    def reset_project_file_list(self):
        self.project_file_list = []
    
    def get_project_list(self):
        project_list_site = requests.get(self.project_list_site_url)
        self.project_list_list = project_list_site.json()


# Step 2: Get a specific project's file  
    def get_project_file_list(self, project_name):
        site_specific_file_list_site = requests.get(self.project_list_site_url,{'project': project_name})
        # site_specific_file_list_site is a list of dicts. Can extract the filename from 'Title'
        for project_document in site_specific_file_list_site.json():
            self.project_file_list.append(project_document['Title'])
        



    def get_project_files(self, project_name):
        # make folder if it doesn't exist
        if not os.path.isdir(project_name):
            os.mkdir(project_name)

        # Grab files
        for project_filename in self.project_file_list:
            # Construct download URL
            download_url = self.download_base_url + urllib.parse.quote(project_name) + '/' + urllib.parse.quote(project_filename)
            # Download
            print(download_url)
            try:
                urllib.request.urlretrieve(download_url, os.path.join(project_name, project_filename))
            except:
                print('file not found-ish')
            # Don't spam the denvergov site - sleep a little bit
            time.sleep(self.sleep_timer_config)


    # Step N: Enumerate all files 

    # TODO: Preserve list of what has been downloaded, don't re-download.

if __name__ == "__main__":
    scraper = denvergov_project_scraper()
    scraper.get_project_list()

    ### Filter the list - insert custom config here ###
    # Trim project list based on prefix
    print(len(scraper.project_list_list))
    if scraper.valid_prefix is not None:
        scraper.project_list_list[:] = [project for project in scraper.project_list_list if (project.startswith(scraper.valid_prefix))]
    print(len(scraper.project_list_list))
    
    # Test one file
    scraper.get_project_file_list(scraper.project_list_list[0])
    scraper.get_project_files(scraper.project_list_list[0])
    scraper.reset_project_file_list()
    # Code for iterating across the whole list
    # for project in scraper.project_list_list:
    #     scraper.get_project_file_list(project)
    #     scraper.get_project_files(project)
    #     scraper.reset_project_file_list


    