from django.db import models


class UserProfile(models.Model):
    """用户"""
    username = models.CharField("用户名", max_length=30, blank=True, null=False, unique=True)
    password = models.CharField("密码", max_length=20, blank=True, null=True)
    history = models.CharField("浏览历史", max_length=512, blank=True, null=True)

    def __str__(self):
        return self.username


class Author(models.Model):
    """"作者"""
    author_name = models.CharField("作者姓名", max_length=128, blank=True, null=False, unique=True)
    author_from = models.CharField("作者单位", max_length=300, blank=True, null=False)
    author_introduction = models.CharField("作者介绍", max_length=4096)

    def __str__(self):
        return self.id


class Paper(models.Model):
    """论文"""
    pid = models.CharField("论文编号", max_length=64, blank=False, null=False, unique=True, primary_key=True)
    paper_title = models.CharField("论文题目", max_length=300, blank=True, null=False)
    paper_abstract = models.CharField("论文摘要", max_length=2048)
    paper_pubDate = models.DateField("出版日期")
    doi_number = models.CharField("doi编号", max_length=32, blank=True, null=False, unique=True)

    def __str__(self):
        return self.pid


class AtoP(models.Model):
    """Author to Paper"""
    aTop_author = models.ForeignKey(Author, verbose_name="作者", related_name="aTop_author", null=False, blank=True)
    aTop_paper = models.ForeignKey(Paper, verbose_name="论文", related_name="aTop_paper", null=False, blank=True)

    def __str__(self):
        return self.id


# class PtoP(models.Model):
#     """Paper to Paper"""
#     pTop_paper = models.ForeignKey(Paper, verbose_name="论文", related_name="pTop_paper", null=False, blank=True)
#     pTop_reference = models.ForeignKey(Paper, verbose_name="参考文献", related_name="pTop_reference", null=False, blank=True)
#
#     def __str__(self):
#         return self.id


class KtoP(models.Model):
    """"Keyword to Paper"""
    kTop_keyword = models.CharField("关键字",max_length=256, null=False, blank=True)
    kTop_paper = models.ForeignKey(Paper, verbose_name="论文", related_name="kTop_paper", null=False, blank=True)

    def __str__(self):
        return self.id


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
