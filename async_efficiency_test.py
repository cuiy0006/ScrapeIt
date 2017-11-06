import time
import aiohttp
import asyncio
import os
jobs = ['https://images.pexels.com/photos/46710/pexels-photo-46710.jpeg', 'https://images.pexels.com/photos/248797/pexels-photo-248797.jpeg', 'https://images.pexels.com/photos/219998/pexels-photo-219998.jpeg', 'https://images.pexels.com/photos/351127/pexels-photo-351127.jpeg', 'https://images.pexels.com/photos/189848/pexels-photo-189848.jpeg', 'https://images.pexels.com/photos/221361/pexels-photo-221361.jpeg', 'https://images.pexels.com/photos/302804/pexels-photo-302804.jpeg', 'https://images.pexels.com/photos/33044/sunflower-sun-summer-yellow.jpg', 'https://images.pexels.com/photos/386025/pexels-photo-386025.jpeg', 'https://images.pexels.com/photos/165213/pexels-photo-165213.jpeg', 'https://images.pexels.com/photos/131723/pexels-photo-131723.jpeg', 'https://images.pexels.com/photos/343720/pexels-photo-343720.jpeg', 'https://images.pexels.com/photos/247292/pexels-photo-247292.jpeg', 'https://images.pexels.com/photos/358904/pexels-photo-358904.jpeg', 'https://images.pexels.com/photos/17727/pexels-photo.jpg', 'https://images.pexels.com/photos/325807/pexels-photo-325807.jpeg', 'https://images.pexels.com/photos/457881/pexels-photo-457881.jpeg', 'https://images.pexels.com/photos/298246/pexels-photo-298246.jpeg', 'https://images.pexels.com/photos/373524/pexels-photo-373524.jpeg', 'https://images.pexels.com/photos/215/road-sky-clouds-cloudy.jpg', 'https://images.pexels.com/photos/191741/pexels-photo-191741.jpeg', 'https://images.pexels.com/photos/109275/pexels-photo-109275.jpeg', 'https://images.pexels.com/photos/35545/watermelon-summer-little-girl-eating-watermelon-food.jpg', 'https://images.pexels.com/photos/88212/pexels-photo-88212.jpeg', 'https://images.pexels.com/photos/296879/pexels-photo-296879.jpeg', 'https://images.pexels.com/photos/274060/pexels-photo-274060.jpeg', 'https://images.pexels.com/photos/136050/pexels-photo-136050.jpeg', 'https://images.pexels.com/photos/449627/pexels-photo-449627.jpeg', 'https://images.pexels.com/photos/34066/pexels-photo.jpg', 'https://images.pexels.com/photos/264109/pexels-photo-264109.jpeg', 'https://images.pexels.com/photos/235615/pexels-photo-235615.jpeg', 'https://images.pexels.com/photos/164287/pexels-photo-164287.jpeg', 'https://images.pexels.com/photos/158361/kinzig-shore-trees-mirroring-black-forest-158361.jpeg', 'https://images.pexels.com/photos/302023/pexels-photo-302023.jpeg', 'https://images.pexels.com/photos/106144/rubber-duck-bath-duck-toys-costume-106144.jpeg', 'https://images.pexels.com/photos/225203/pexels-photo-225203.jpeg', 'https://images.pexels.com/photos/9537/sea-beach-sand-sun.jpg', 'https://images.pexels.com/photos/307008/pexels-photo-307008.jpeg', 'https://images.pexels.com/photos/296282/pexels-photo-296282.jpeg', 'https://images.pexels.com/photos/187919/pexels-photo-187919.jpeg', 'https://images.pexels.com/photos/186980/pexels-photo-186980.jpeg', 'https://images.pexels.com/photos/302549/pexels-photo-302549.jpeg', 'https://images.pexels.com/photos/169193/pexels-photo-169193.jpeg', 'https://images.pexels.com/photos/365341/pexels-photo-365341.jpeg', 'https://images.pexels.com/photos/320316/pexels-photo-320316.jpeg', 'https://images.pexels.com/photos/361081/pexels-photo-361081.jpeg', 'https://images.pexels.com/photos/414105/pexels-photo-414105.jpeg', 'https://images.pexels.com/photos/158316/kinzig-fischer-bach-black-forest-water-158316.jpeg', 'https://images.pexels.com/photos/234054/pexels-photo-234054.jpeg', 'https://images.pexels.com/photos/51548/pexels-photo-51548.jpeg', 'https://images.pexels.com/photos/176395/pexels-photo-176395.jpeg', 'https://images.pexels.com/photos/262325/pexels-photo-262325.jpeg', 'https://images.pexels.com/photos/54459/summer-sunflower-flowers-sky-54459.jpeg', 'https://images.pexels.com/photos/386009/pexels-photo-386009.jpeg', 'https://images.pexels.com/photos/51397/legs-window-car-dirt-road-51397.jpeg', 'https://images.pexels.com/photos/413195/pexels-photo-413195.jpeg', 'https://images.pexels.com/photos/111085/pexels-photo-111085.jpeg', 'https://images.pexels.com/photos/355328/pexels-photo-355328.jpeg', 'https://images.pexels.com/photos/365668/pexels-photo-365668.jpeg', 'https://images.pexels.com/photos/5360/sea-sunny-person-beach.jpg', 'https://images.pexels.com/photos/286763/pexels-photo-286763.jpeg', 'https://images.pexels.com/photos/279574/pexels-photo-279574.jpeg', 'https://images.pexels.com/photos/257832/pexels-photo-257832.jpeg', 'https://images.pexels.com/photos/9568/summer-sun-yellow-photography.jpg', 'https://images.pexels.com/photos/265960/pexels-photo-265960.jpeg', 'https://images.pexels.com/photos/61129/pexels-photo-61129.jpeg', 'https://images.pexels.com/photos/371633/pexels-photo-371633.jpeg', 'https://images.pexels.com/photos/158471/ibis-bird-red-animals-158471.jpeg', 'https://images.pexels.com/photos/326055/pexels-photo-326055.jpeg', 'https://images.pexels.com/photos/307006/pexels-photo-307006.jpeg', 'https://images.pexels.com/photos/356977/pexels-photo-356977.jpeg', 'https://images.pexels.com/photos/268533/pexels-photo-268533.jpeg', 'https://images.pexels.com/photos/141784/pexels-photo-141784.jpeg', 'https://images.pexels.com/photos/267151/pexels-photo-267151.jpeg', 'https://images.pexels.com/photos/414586/pexels-photo-414586.jpeg', 'https://images.pexels.com/photos/237593/pexels-photo-237593.jpeg', 'https://images.pexels.com/photos/35847/summer-still-life-daisies-yellow.jpg', 'https://images.pexels.com/photos/58592/pexels-photo-58592.jpeg', 'https://images.pexels.com/photos/158756/flowers-plants-korea-nature-158756.jpeg', 'https://images.pexels.com/photos/130879/pexels-photo-130879.jpeg', 'https://images.pexels.com/photos/158821/mineral-water-lime-ice-mint-158821.jpeg', 'https://images.pexels.com/photos/414320/pexels-photo-414320.jpeg', 'https://images.pexels.com/photos/289825/pexels-photo-289825.jpeg', 'https://images.pexels.com/photos/311458/pexels-photo-311458.jpeg', 'https://images.pexels.com/photos/421759/pexels-photo-421759.jpeg', 'https://images.pexels.com/photos/210012/pexels-photo-210012.jpeg', 'https://images.pexels.com/photos/160699/girl-dandelion-yellow-flowers-160699.jpeg', 'https://images.pexels.com/photos/248812/pexels-photo-248812.jpeg', 'https://images.pexels.com/photos/221433/pexels-photo-221433.jpeg', 'https://images.pexels.com/photos/33227/sunrise-phu-quoc-island-ocean.jpg', 'https://images.pexels.com/photos/175717/pexels-photo-175717.jpeg', 'https://images.pexels.com/photos/235648/pexels-photo-235648.jpeg', 'https://images.pexels.com/photos/369495/pexels-photo-369495.jpeg', 'https://images.pexels.com/photos/67286/apple-blossom-tree-branch-spring-67286.jpeg', 'https://images.pexels.com/photos/279415/pexels-photo-279415.jpeg', 'https://images.pexels.com/photos/125457/pexels-photo-125457.jpeg', 'https://images.pexels.com/photos/5331/beach-vacation-people-sand.jpg', 'https://images.pexels.com/photos/413960/pexels-photo-413960.jpeg', 'https://images.pexels.com/photos/213807/pexels-photo-213807.jpeg', 'https://images.pexels.com/photos/61136/pexels-photo-61136.jpeg', 'https://images.pexels.com/photos/21423/forest-park-walk-trail-21423.jpg', 'https://images.pexels.com/photos/249210/pexels-photo-249210.jpeg', 'https://images.pexels.com/photos/462024/pexels-photo-462024.jpeg', 'https://images.pexels.com/photos/261403/pexels-photo-261403.jpeg', 'https://images.pexels.com/photos/160097/pexels-photo-160097.jpeg']
jb = ['https://www.github.com', 'https://www.yahoo.com', 'https://www.cnn.com', 'https://www.google.com', 'https://www.baidu.com']

async def main(loop):
      #async with aiohttp.ClientSession(loop=loop) as session:
        for img_uri in jobs:
            print('start')
            img_name = img_uri.split('/')[-1]
            headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            #async with session.get(img_uri, headers=headers) as response:
            await asyncio.sleep(1)#response.read()
            print('end')

async def save_img(url, name, loop):
        try:
            print('start')
            headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            async with aiohttp.ClientSession(loop=loop) as session:
              async with session.get(url, headers=headers) as response:
                  img = await response.read()
            print('end')
            return True
        except Exception as e:
            print('*******FAIL******', name, '  ', url)
            return False

if __name__ == '__main__':
    asyncio.set_event_loop(asyncio.new_event_loop())
    begin = time.time()
    loop = asyncio.get_event_loop()
    tasks = [save_img(job, job.split('/')[-1], loop) for job in jobs]
    loop.run_until_complete(asyncio.wait(tasks))

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main(loop)) 

    print(time.time()-begin)

# import threading
# import asyncio

# @asyncio.coroutine
# def hello():
#     print('Hello world! (%s)' % threading.currentThread())
#     yield from asyncio.sleep(1)
#     print('Hello again! (%s)' % threading.currentThread())

# loop = asyncio.get_event_loop()
# tasks = [hello(), hello()]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()