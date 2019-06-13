# -*- coding: utf-8 -*-
import scrapy
import json
from zhihuuser.items import UserItem

#   爬取知乎vczh用户的所有关注和所有粉丝信息,并且爬取每个关注用户和粉丝用户的关注和粉丝。。  完成层层递归爬取
class ZhihuSpider(scrapy.Spider):
    #   指定spider名称
    name = "zhihu"
    #   指定爬取范围域
    allowed_domains = ["www.zhihu.com"]
    #   指定爬取用户的url_token
    start_user = 'excited-vczh'
    #   构造一个用户信息url
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    #   构造用户关注列表
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    #   构造用户粉丝列表
    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'


    def start_requests(self):
        #   爬取初始用户的基本信息
        yield scrapy.Request(url=self.user_url.format(user=self.start_user,include=self.user_query),callback=self.parse_user)
        #   爬取初始用户的关注列表信息
        yield scrapy.Request(url=self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0,limit=20),callback=self.parse_follows)
        #   爬取初始用户的粉丝列表信息
        yield scrapy.Request(url=self.followers_url.format(user=self.start_user,include=self.followers_query,offset=0,limit=20),callback=self.parse_followers)


    def parse_user(self, response):
        #   爬取用户的基本信息
        result = json.loads(response.text)
        item = UserItem()
        # 遍历item中的所有字段
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        print(item)
        yield item

    def parse_follows(self,response):
        #   爬取关注者信息
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                #   遍历用户的关注列表，将关注者的url_token拼接为一个用户url,回调函数parse_user
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.parse_user)

        #   判断paging在results中并且is_end为false ， is_end 代表是否又下一页
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            #   获取下一页url
            next_page = results.get('paging').get('next')
            #   发送下一页请求，回调本身
            yield scrapy.Request(url=next_page,callback=self.parse_follows)

        print(results)


    def parse_followers(self,response):
        #   获取用户的粉丝列表信息
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                #   遍历用户的粉丝列表，将粉丝的url_token拼接为一个用户url,回调函数parse_user
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.parse_user)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            #   获取下一页url
            next_page = results.get('paging').get('next')
            #   发送下一页请求，回调本身
            yield scrapy.Request(url=next_page, callback=self.parse_followers)

        print(results)