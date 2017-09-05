import spider
import re
from utils import *
class zhihu_spider(spider.spider):

    # 获取一个用户的头像，大小为68*68pixel
    def get_avatar(self, user_id):
        uri = "https://www.zhihu.com/people/" + user_id + "/answers"
        request = url_request.Request(uri)
        html = url_request.urlopen(request).read().decode()
        return None

    def convert_uri(self, user, offset, limit):
        return ('https://www.zhihu.com/api/v4/members/' + str(user) + '/followers' + '?offset=' + str(offset) + '&limit=' + str(limit))

    # 返回user和头像的uri
    def get_next_user(self):
        if len(self.wait_list) == 0:
            return None, None
        else:
            ele= self.wait_list.popitem()   # pop a tuple (key, value)
            return ele[0], ele[1]

    #处理json数据，主要功能为加入datalist。
    def process_data(self, data):
        if data == None:
            return False
        for ele in data['data']:
            self.append_wait_list(ele['url_token'], ele['avatar_url'])

        # 处理json数据，判断这个用户是否所有被关注者都被爬完了
        if data['paging']['is_end'] == True:
            #加入done_list中
            return False

    # 把爬取结果放入done_list中，去重
    def append_done_list(self, seed, seedimg):
        if seed not in self.done_list:
            self.done_list.append(seed)
            self.done_img_list.append(seedimg)

    def append_wait_list(self, uri, img_uri):
        if uri not in self.wait_list and uri not in self.done_list:
            self.wait_list[uri] = img_uri

    # 爬虫运行
    def run(self, seed, iteration = 1000):
        seed_img = self.get_avatar(seed)   #把种子的头像爬下来，并放入done_list中

        limit = 20
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", 'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'}
        #迭代iteration个用户
        for i in range(iteration):
            offset = 0
            log(seed)
            while True:
                if(seed.encode() in self.done_list):
                    seed, seed_img = self.get_next_user()
                    break

                log('iteration: ' + str(i) + '  limit: ' + str(limit) + '  offset: ' + str(offset))
                data = run_uri(self.convert_uri(seed, offset, limit), headers=headers)

                #获取了20条数据，处理，如果都处理完毕，则该用户完成
                status = self.process_data(data)
                if status == False:
                    self.append_done_list(seed, seed_img)
                    seed, seed_img = self.get_next_user()
                    break
                offset += 20
            if seed == None:
                break
        self.save_result()

        
if __name__ == "__main__":
    spider = zhihu_spider()
    spider.run(seed="excited-vczh")


