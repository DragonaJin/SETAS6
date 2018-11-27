import json

from django.http import Http404
from django.shortcuts import render
from webapp.models import *
from webapp.shortcuts.ajax import *
from django.http import HttpResponseRedirect

def index(request, template_name):

    return_dict = {}
    key = ""
    paperList = []
    nameList = []
    try:
        key = UserProfile.objects.get(username=request.session['username']).history
    except Exception as e:
        print(e)
        key = ""
        papers = Paper.objects.all().order_by('-paper_pubDate')[0:9]
        for paper in papers:
            authors = AtoP.objects.filter(aTop_paper_id=paper.pid)
            name = ''
            for author in authors:
                name += Author.objects.get(id=author.aTop_author_id).author_name
                name += ';'
                # print(Author.objects.get(id=author.aTop_author_id).author_name)
            nameList.append(name)
        return_dict["papers"] = papers
        return_dict["name"] = nameList
        return_dict["made"] = zip(papers, nameList)

        return render(request, template_name, return_dict)






    if key:
        keyList = KtoP.objects.filter(kTop_keyword__icontains=key).values("kTop_paper_id").distinct()[0:9]

        for key in keyList:
            paper = Paper.objects.get(pid=key["kTop_paper_id"])
            print(key["kTop_paper_id"])
            paperList.append(paper)
            authors = AtoP.objects.filter(aTop_paper_id=key["kTop_paper_id"])
            name = ''
            for author in authors:
                name += Author.objects.get(id=author.aTop_author_id).author_name
                name += ';'
                # print(Author.objects.get(id=author.aTop_author_id).author_name)
            nameList.append(name)
            print(name)
        return_dict["papers"] = paperList
        return_dict["name"] = nameList
        return_dict["made"] = zip(paperList, nameList)

        # for paper, author in zip(keyList, paperList):
        #     return
    else:
        print("hello")
        papers = Paper.objects.all().order_by('-paper_pubDate')[0:9]
        for paper in papers:
            authors = AtoP.objects.filter(aTop_paper_id=paper.pid)
            name = ''
            for author in authors:
                name += Author.objects.get(id=author.aTop_author_id).author_name
                name += ';'
                # print(Author.objects.get(id=author.aTop_author_id).author_name)
            nameList.append(name)
        return_dict["papers"] = papers
        return_dict["name"] = nameList
        return_dict["made"] = zip(papers, nameList)
    return render(request, template_name, return_dict)


def goto(request, template_name):

    return render(request, template_name)


def detail(request, template_name, paperId):
    print(paperId)

    paperInfo = Paper.objects.get(pid=paperId)
    print(paperInfo.paper_title)
    keyList = KtoP.objects.filter(kTop_paper_id=paperId)
    aIdList = AtoP.objects.filter(aTop_paper_id=paperId)
    authorList = []
    for aid in aIdList:
        author = Author.objects.get(id=aid.aTop_author_id)
        authorList.append(author)
    """打开详情页时，如果是已注册用户的话，那么就登个记 """
    try:
        if(request.session['username']):
            account = request.session['username']
            userInfo = UserProfile.objects.get(username=account)
            for key in keyList:
                userInfo.history = key.kTop_keyword
                break
            userInfo.save()
    except Exception as e:
        print(e)


    return_dict = {"paperInfo" : paperInfo}
    return_dict["keyList"] = keyList
    return_dict["authorList"] = authorList
    return render(request, template_name, return_dict)


def search(request, template_name):
    return_dict = {}
    if request.method != "POST":
        return render(request, template_name, return_dict)
    search_type = request.POST.get("search_type")
    search_content = request.POST.get("search_content")
    if search_type == "title":
        papers = Paper.objects.filter(paper_title=search_content)

    elif search_type == "author":
        author = Author.objects.get(author_name=search_content)
        atops = AtoP.objects.filter(aTop_author=author)
        l = [i.aTop_paper_id for i in atops]
        papers = Paper.objects.filter(pid__in=l)
    else:
        papers = Paper.objects.filter(kTop_paper__kTop_keyword=search_content)
    names = []
    for paper in papers:
        author_list = AtoP.objects.filter(aTop_paper=paper)
        authors = ''
        for a in author_list:
            authors += a.aTop_author.author_name
            authors += ";"
        names.append(authors)

    return_dict["papers"]=papers
    return_dict["names"] = names
    return_dict["made"] = zip(papers, names)
    return render(request, template_name, return_dict)



def login(request):
    account = request.POST.get("log_account")
    passwd = request.POST.get("log_passwd")
    try:
        user = UserProfile.objects.get(username=account)
    except Exception:
        return ajax_error("客户不存在！")
    if user.password != passwd:
        return ajax_error("密码错误！")
    else:
        request.session['username'] = account
        return ajax_success()


def register(request):
    account = request.POST.get("re_account")
    passwd = request.POST.get("re_passwd")
    user = UserProfile.objects.filter(username=account)
    if user:
        return ajax_error("客户已存在！")
    else:
        user = UserProfile(username=account, password=passwd)
        user.save()
        request.session['username'] = account
        return ajax_success()
def quit(request):
    del request.session['username']
    return HttpResponseRedirect("/index/")
