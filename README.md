# zhihu_spider
## Author : Lee-jiazh
## Environment : python 3.5
we can get zhihu avatars and information by the zhihu spider.

The `spider.py` can load a hdf5 file to get last data. So `__init__` get them into the memory.

This project allows you generate more spiders to adjust your website.For example, you can develop the weibo spider by adding a class called `weibo_spider` and so on.


### Table of Contents.

* [Read this first](#read-this-first)
* [Spider Runs](#run-spider)
* [Zhihu spider details](#zhihu-detail)
* [Save your data by h5py](#save-data)
* [What else?](#what-else)

## <span id="read-this-first">Read this first</span>
- This project is develped for the primer, you can use it to get all websites, because you can get the skills. In the end, I will give you a blog url.

- Just do this.

---
## <span id="run-spider">Spider Runs</span>
- Fist of all, we don't need to think which website to crawl, just think the process deeply.

- We need a seed as our program start. And we need a list to save the website that we have `completed` the work, just call it *done_list*. Another list is used to keep the `waiting` list, because one user can contains lots of users' information, but we can process it one by one, when an element in waiting list completed, it will be in done_list, so we call it `wait_list`.

- We need to save this running results, therefore load the dataset by running.

- After crawling, save current results. 

## <span id="zhihu-detail">Zhihu spider details</span>
### Task : Get plenty of users' information and `avatars`. 

- We adopts the measure: find the users' followers and keep on the program.So we search for a user who have lots of followers,like *vczh*... 

- We found that zhihu uses `ajax` to load the users' information, so we get thet ajax url by network `XHR`, the url is *https://www.zhihu.com/api/v4/members/excited-vczh/followers?offset=0&limit=20*. If you click it, you will find it can't open, so I found a problem, we need put `authorization` into the *headers*, its value is `oauth c3cef7c66a1843f8b3a9e6a1e3160e20` or yours, I don't know what it means, but it really works.

- Next step is much easier, parse the `json` to the python dictionary, by the function `eval()`. Warning: the data is *false*, but  *False* in python.

- Iteration.

## <span id="save-data">Save your data by h5py</span>
- Hdf5 is used to save numpy array, so you should be able to apply numpy.
- The avatars are all images, if we store them by file system, it will occupy lots of storage, h5py could compress them well. And we convert them to numpy arraies, it will be convenient to use them develop image processing programs.
- The problem is how to convert image array in the memory, you can see the codes in `utils.py`. 
- The another problem is storing `string`(i.e. *variable length in UTF-8 encoding`(python3)`*)
---

## <span id="what-else">What else?</span>
- You can develop a weibo_spider, and you will not think about how to store them and how to initialize your system. You only need to code you `run` function.
- Spider is so easy.

- My blog is [Wind_white Blog](http://blog.csdn.net/wind_white)