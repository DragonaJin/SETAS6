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

    return_dict["papers"] = papers
    return_dict["names"] = names
    return_dict["made"] = zip(papers, names)
    return render(request, template_name, return_dict)


def searchAuthor(request, template_name):
    return_dict = {}
    if request.method != "POST":
        return render(request, template_name, return_dict)
    author_name = request.POST.get("author_name")
    print(author_name)
    authors = Author.objects.get(author_name=author_name)
    return_dict["author"] = authors
    return render(request, template_name, return_dict)


def authorContent(request, template_name, authorId):
    print(authorId)
    return_dict = {}
    author = Author.objects.get(id=authorId)
    return_dict["author"] = author
    his_papers = AtoP.objects.filter(aTop_author_id=authorId)
    his_papers = his_papers.order_by('aTop_paper__paper_pubDate')

    partners = {}
    names = []
    collaborate = []
    years = {}
    for paper in his_papers:
        print(paper.aTop_paper.paper_pubDate.year)
        if paper.aTop_paper.paper_pubDate.year not in years.keys():
            years[paper.aTop_paper.paper_pubDate.year] = 1
        else:
            years[paper.aTop_paper.paper_pubDate.year] += 1
        his_partners = AtoP.objects.filter(aTop_paper_id=paper.aTop_paper_id)
        for his_partner in his_partners:
            pName = Author.objects.get(id=his_partner.aTop_author_id)

            if pName.author_name in partners.keys():
                partners[pName.author_name] += 1
            else:
                if author.author_name != pName.author_name:
                    names.append(pName.author_name)
                partners[pName.author_name] = 1
    print(years)
    year = list(years.keys())
    num = list(years.values())
    print(year)
    print(num)
    return_dict["year"] = json.dumps(year)
    return_dict["num"] = json.dumps(num)
    print(partners)
    print(len(names))
    achievements = partners[author.author_name]
    for name, value in partners.items():
        if name == author.author_name:
            continue
        print(name)
        collaborate.append(value)
    print(names)
    print(collaborate)
    return_dict['achievements'] = achievements
    return_dict['names'] = json.dumps(names)
    return_dict['collaborate'] = json.dumps(collaborate)
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
