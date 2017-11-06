import requests, os, time

class BeautifulPicture():
    def __init__(self, headers, folder_path):
        self.headers = headers
        self.folder_path = folder_path
        self.mkdir(folder_path)
        self._session = None

    def mkdir(self, path):
        ''' create directory if not exists
        Args:
            path (string): directory path
        Retruns:
            None
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

        Returns:
            bool: exception not occurs True, otherwise False
        '''
        try:
            #open mode: b->binary mode, w->overwrite, (default)r->read, a->append
            #begin = time.time()
            img = requests.get(url, self.headers)
            #x1 = time.time()

            with open(self.folder_path + '\\' + name, 'wb') as f: 
                f.write(img.content)
                #x2 = time.time()
                print(name, 'saved successfully!')
            return True
        except:
            print('*******FAIL******', name, '  ', url)
            return False
    