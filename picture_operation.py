import requests, os

class BeautifulPicture():
    def __init__(self, headers, folder_path):
        self.headers = headers
        self.folder_path = folder_path
        self.mkdir(folder_path)

    def mkdir(self, path):
        ''' create directory if not exists
        Args:
            path (string): directory path
        '''
        path = path.strip()
        isExist = os.path.exists(path)
        if not isExist:
            print('create new path', path)
            os.makedirs(path)
            print('created!')
        else:
            print(path, 'already exists!')
    
    def save_img(self, url, name):
        '''save image
        Args:
            url (string): image's url
            name (string): image's name
        '''
        try:
            img = requests.get(url, headers=self.headers)
            #open mode: b->binary mode, w->overwrite, (default)r->read, a->append
            with open(self.folder_path + '\\' + name, 'wb') as f: 
                f.write(img.content)
                print(name, 'saved successfully!')
            return True
        except:
            return False
    

