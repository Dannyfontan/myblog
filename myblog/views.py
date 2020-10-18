from django.shortcuts import redirect

def testpage(request):
    return redirect("article:article_list")
