import requests_html
import sys
import os
from datetime import datetime

if __name__ == "__main__":
    print("Handy Scrapper Tool")

    website_url =  sys.argv[1] if len(sys.argv) > 1 else None
    if website_url:
        print("SITE - ", website_url)
    else:
        print("Please pass the website url to scrap.")
        exit()
    
    from requests_html import HTMLSession
    session = HTMLSession()
    r = session.get(website_url)

    grab_urls  = list(r.html.links)
    grab_urls.sort()
    file_ext = None
    while True:
        print(" >>> Type 'quit' to cancel")
        pattern = input("Do you want to analyze URL pattern to fetch: ")
        if pattern.strip().lower() == "quit":
            break
        file_ext = pattern
        download_urls = list()
        for _ in grab_urls:
            if pattern in _:
                download_urls.append(_)

        if len(download_urls):
            print("Grabbed URLS - ", download_urls)
    
    yes_no = input("Do you want to download media(Y/N): ")
    if yes_no.strip().lower() == "n":
        exit()
    else:
        if not len(download_urls):
            print("No download URLs found")
            exit()
        else:
            current_path =  os.path.dirname(os.path.abspath(__file__))
            download_path = os.path.join(current_path, 
            "files_" + str(datetime.now().isoformat()).replace(".", "_").replace("-", "_").replace(":", "_"))

            print(download_path)
            os.mkdir(download_path)

            for idx, _media_url in enumerate(download_urls):
                print("[*] {}".format(_media_url))

                X = session.get(_media_url)
                open(os.path.join(download_path, str(idx) + file_ext), "wb").write(X.content)
    

    print("----****------")


    


