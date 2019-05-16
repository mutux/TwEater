# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import urllib
import time


class TuEater:
    @staticmethod
    def eatUsers(digester, names, bpargs):
        users = []
        cnt = 0
        for name in names:
            if len(name.strip()) == 0 or name.strip().startswith("# "):
                continue
            user = TuEater.ripUser(name)
            if user is not None:
                users.append(user)
            time.sleep(0.3)
            if len(users) >= 20:
                print ' batch:', cnt, len(users) * (cnt + 1), name,
                cnt += 1
                digester(users, bpargs)
                del users[:]

    @staticmethod
    def ripUser(name):
        u_url = "https://twitter.com/" + name
        doc = None
        try:
            doc = pq(url=u_url, opener=lambda url, **kw: urllib.urlopen(url).read())
        except Exception as e:
            print str(e)
        if doc is None:
            return None
        user = {}
        user["name"] = name.encode('utf-8')
        des_str = doc("p.ProfileHeaderCard-bio.u-dir").text()
        loc_str = doc("div.ProfileHeaderCard-location").text()
        url_str = doc("div.ProfileHeaderCard-url").text()
        join_str = doc("span.ProfileHeaderCard-joinDateText").attr("title")
        bir_str = doc("div.ProfileHeaderCard-birthdate").text()
        if des_str is None:
            des_str = ''
        if loc_str is None:
            loc_str = ''
        if url_str is None:
            url_str = ''
        if join_str is None:
            join_str = ''
        if bir_str is None:
            bir_str = ''
        user["description"] = des_str.encode('utf-8')
        user["location"] = loc_str.encode('utf-8')
        user["url"] = url_str.encode('utf-8')
        user["join"] = join_str.encode('utf-8')
        user["birth"] = bir_str.encode('utf-8')
        return user
