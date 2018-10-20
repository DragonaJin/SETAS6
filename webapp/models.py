import datetime
import json
from django.db import models
from django.contrib.auth.models import User, UserManager, Group
from django.utils.translation import ugettext_lazy as _

# class User(User):
#     """用户"""
#     uid = models.IntegerField("级别", blank=False, null=False)
#     username = models.CharField("用户名", max_length=20, blank=True, null=False)
#     passwd = models.CharField("密码", max_length=20, blank=True, null=True)
#     history = models.CharField("浏览历史", max_length=100, blank=True, null=True)
#
#
#     objects = UserManager()
#
#
#
#     def __str__(self):
#         return self.cname or self.username
#
#     class Meta:
#         verbose_name = "用户"
#         verbose_name_plural = verbose_name
#         permissions = (
#             ("salesman", "销售角色"),
#             ("customer_service", "客服角色"),
#             ("lawyer", "法务角色"),
#             ("treasurer", "财务角色"),
#         )
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