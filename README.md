# scrapy-zhihu

案例描述：

  使用scrapy框架爬取知乎用户信息。首先从一个大v用户（确保用户不是0关注0粉丝）开始，获取大v用户的基本信息以及大v用户的所有粉丝和所有关注，然后遍历粉丝列表和关注列表，循环实现爬取每个用户的基本信息。整个案例采用递归思路实现
  
推荐环境：
  
  python 3.5+<br>
  scrapy 1.6<br>
  pymongo 3.7.2

思路分析：

  ![image](https://github.com/limou09/scrapy-zhihu/blob/master/1.png)<br>
  我们从一个关注的人开始,获取这个关注的人的信息并储存下来,然后获取这个关注的人的的关注的人和粉丝,再去获取关注人的人的信息并存储循环往复下去就实现了从一个人开始层层抓取下去.
  
基本使用

   scrapy crawl zhihu
   
