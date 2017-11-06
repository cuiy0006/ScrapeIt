from NASA_scraper import get_NASA_gallery_pic
from pexel_scraper import get_pexels_summer_pic
from easenet_music_scraper import get_163Album_pic
import time


if __name__ == '__main__':
    start = time.time()
    get_NASA_gallery_pic() #https://www.nasa.gov/multimedia/imagegallery/iotd.html
    get_pexels_summer_pic() #https://www.pexels.com/search/summer/
    get_163Album_pic() #http://music.163.com/#/artist/album?id=101988&limit=10000&offset=0
    print(time.time()-start)