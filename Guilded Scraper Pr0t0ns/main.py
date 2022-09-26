
import requests
import json
import random
import string
import threading
scraped_names = []
proxies = []
class Guilded_scrape:
    @staticmethod
    def gen_username():
        username_query = ''
        for i in range(random.randint(2, 5)):
            letter = random.choice(string.ascii_lowercase)
            username_query += letter
        return username_query
    @staticmethod
    def scrape(downloaded_pfps, only_scrape_pfp):
        try:
            proxy = random.choice(proxies)
            username_query = Guilded_scrape.gen_username()
            url = f'https://www.guilded.gg/api/search?query={username_query}&entityType=user&maxResultsPerType={random.randint(15, 20)}&excludedEntityIds=4WanoWwm'
            data = requests.get(url, proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'}).json()
            for user in data['results']['users']:
                uid = user['id']
                username = user['name']
                pfp = user['profilePicture']
                data = open("scraped/user_ids.txt", 'r+').read()
                if uid in data:
                    return Guilded_scrape.scrape(downloaded_pfps, only_scrape_pfp)
                if pfp != None:
                    f = open("scraped/pfp_links.txt", "a+")
                    f.write(f"{pfp}\n")
                    f.close()
                    if downloaded_pfps:
                        image_bytes = requests.get(pfp).content
                        if "webp" in pfp:
                            extension = 'webp'
                        elif "png" in pfp:
                            extension = 'png'
                        else:
                            input(pfp)
                        dir_name = f'scraped/pfps/{uid}{random.randint(1, 100000)}.{extension}'
                        try:
                            open(dir_name, 'wb').write(image_bytes)
                        except Exception as error:
                            return Guilded_scrape.scrape(downloaded_pfps, only_scrape_pfp)
                    print(f"[+]: Scraped PFP, Username & User id from user --> ({username})")
                else:
                    print(f"[+]: Scraped Username & User ID from user --> ({username})")
                if only_scrape_pfp == True and pfp == None:
                    pass
                else:
                    f = open("scraped/user_ids.txt", "a+")
                    f.write(f"{uid}\n")
                    f.close()  
                    if len(username) > 10 or len(username) <= 2:
                        pass
                    else:
                        if username in scraped_names:
                            pass
                        else:
                            scraped_names.append(username)
                            f = open("scraped/usernames.txt", "a+")
                            f.write(f"{username}\n")
                            f.close()
            return Guilded_scrape.scrape(downloaded_pfps, only_scrape_pfp)
        except Exception as err:
            return Guilded_scrape.scrape(downloaded_pfps, only_scrape_pfp)
    
if __name__ == "__main__":
    with open("config.json") as conf:
        conf = str(conf.read())
        data = json.loads(conf)
        downloaded_pfp_images = data['Download_pfps']
        only_scrape_pfp = data['Only_scrape_Accounts_with_pfp']
        del data
    with open("scraped/proxies.txt") as data:
        data = data.readlines()
        for proxy in data:
            proxy = proxy.replace('\n', "")
            proxies.append(proxy)
    for i in range(int(input("Enter thread amt: "))):
        threading.Thread(target=Guilded_scrape.scrape, args=[downloaded_pfp_images, only_scrape_pfp]).start()
    