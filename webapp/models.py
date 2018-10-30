import datetime
import json
from datetime import date

from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
    """用户"""
    uid = models.IntegerField("用户编号", blank=False, null=False)
    account = models.CharField("用户名", max_length=30, blank=True, null=False)
    passwd = models.CharField("密码", max_length=20, blank=True, null=True)
    history = models.CharField("浏览历史", max_length=100, blank=True, null=True)

    def __str__(self):
        return self.uid

    # class Meta:
    #     db_table = 'user'
    #     verbose_name = '用户信息'
    #     verbose_name_plural = verbose_name


class Author(models.Model):
    """"作者"""
    aid = models.IntegerField("作者编号", blank=False, null=False)
    author_name = models.IntegerField("作者姓名", blank=True, null=False)
    author_from = models.CharField("作者单位", max_length=300, blank=True, null=False)
    author_introduction = models.BooleanField("作者介绍")

    def __str__(self):
        return self.aid


class Paper(models.Model):
    """论文"""
    pid = models.IntegerField("论文编号", blank=False, null=False)
    paper_title = models.CharField("论文题目", max_length=300, blank=True, null=False)
    paper_abstract = models.BooleanField("论文摘要")
    paper_pubDate = models.DateField("出版日期")

    def __str__(self):
        return self.pid


class Keyword(models.Model):
    """关键词"""
    kid = models.IntegerField("关键字编号", blank=False, null=False)
    keyword = models.CharField("关键字", max_length=300, blank=True, null=False)

    def __str__(self):
        return self.kid


class AtoP(models.Model):
    """Author to Paper"""
    aTop_id = models.IntegerField("aTop编码", blank=False, null=False)
    aTop_author = models.ForeignKey(Author, verbose_name="作者", related_name="aTop_author", null=True, blank=True)
    aTop_paper = models.ForeignKey(Paper, verbose_name="论文", related_name="aTop_paper", null=True, blank=True)

    def __str__(self):
        return self.aTop_id


class PtoP(models.Model):
    """Paper to Paper"""
    pTop_id = models.IntegerField("pTop编码", blank=False, null=False)
    pTop_paper = models.ForeignKey(Paper, verbose_name="论文", related_name="pTop_paper", null=True, blank=True)
    pTop_reference = models.ForeignKey(Paper, verbose_name="参考文献", related_name="pTop_reference", null=True, blank=True)

    def __str__(self):
        return self.pTop_id


class KtoP(models.Model):
    """"Keyword to Paper"""
    kTop_id = models.IntegerField("kTop编码", blank=False, null=False)
    kTop_keyword = models.ForeignKey(Keyword, verbose_name="关键字", related_name="kTop_keyword", null=True, blank=True)
    kTop_paper = models.ForeignKey(Paper, verbose_name="论文", related_name="kTop_paper", null=True, blank=True)

    def __str__(self):
        return self.kTop_id
#
#
#
#
#     def trunk_tree_list(self):
#         per_list = [self]
#
#         def underling(users):
#             back = []
#             for u in users:
#                 unders = u.children.all()
#                 back.extend(unders)
#             if back:
#                 per_list.extend(back)
#                 return underling(back)
#             else:
#                 return
#
#         underling([self])
#         return per_list
#
#     def pack_data(self):
#         """
#         数据打包
#         """
#         def get_value(s, field):
#             return getattr(s, field.name) or ''
#
#         data = []
#         [data.append((f.name, get_value(self, f))) for f in self._meta.fields]
#         data.append(("depart", self.depart.name if self.depart else "----"))
#         data.append(("parent", self.parent.cname if self.parent else "----"))
#         data.append(("user_rank_name", self.user_rank_name(self.rank)))
#         data.append(("user_type_name", self.user_type_name(self.utype)))
#
#         return dict(data)
