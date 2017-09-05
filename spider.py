import h5py
from utils import *

class spider:
    '''
    爬虫类
    '''
    done_list = []      #数组，为所有已经爬完的用户名或唯一id
    done_img_list = []  #数组，为所有已经爬完的用户的头像路径
    wait_list = {}  #为所有等待作为种子的用户名和图片uri
    file_name = "train_set.hdf5"

    def __init__(self):
        self.init_spider()

    def init_spider(self):
        self.init_lists()

    # 从h5py文件中读取数据
    def init_lists(self):
        try:
            with h5py.File(self.file_name, "r") as file:
                # 如果保存的时候该数据为空，则不会创建这个dataset
                try:
                    self.done_list = list(file['done_list'])
                    wait_user = list(file['wait_user'])
                    wait_img = list(file['wait_img'])
                    for i in range(len(wait_user)):
                        self.wait_list[wait_user[i].decode()] = wait_img[i].decode()
                except Exception as error:
                    pass
        except Exception as error:
            warn_msg("x")

    #保存结果
    def save_result(self):
        file = None
        # img_array保存本轮所有的图片矩阵
        img_array = np.zeros((34*34*3, 1))
        # 在矩阵右侧添加所有图片的矩阵，规格均为(nx, 1)，所以按照列添加axis = 1
        for ele in self.done_img_list:
            if ele == None:
                continue
            img_array = np.c_[img_array, uri2matrix(ele)]
            # img_array = np.insert(img_array, img_array.shape[1], values=uri2matrix(ele), axis=0)
            log(img_array)
        #合并所有的已完成图片矩阵
        try:
            with h5py.File(self.file_name, "r") as file:
                if 'done_img' in file:
                    img_array = np.c_[np.array(file['done_img']), img_array]
        except Exception as err:
            warn_msg("No such File :  " + self.file_name)


        with h5py.File(self.file_name, "w") as file:
            try:
                del file["done_list"]
                del file["wait_user"]
                del file["wait_img"]
                del file["done_img"]
            except Exception as err:
                pass
            file.create_dataset("done_list", data=np.bytes_(self.done_list))
            prompt("done_list" + "保存完毕")
            file.create_dataset("wait_user", data=np.bytes_(list(self.wait_list.keys())))
            prompt("done_list" + "保存完毕")
            file.create_dataset("wait_img", data=np.bytes_(list(self.wait_list.items())))
            prompt("done_list" + "保存完毕")
            file.create_dataset("done_img", data=img_array, dtype="i")
            prompt("done_list" + "保存完毕")





class spider_Factory:
    pass