import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpRequest
from django.shortcuts import render_to_response
import objhandler

from knajpa.models.articles import Article
from knajpa.utils  import InvalidRequestError
from knajpa.handlers.articles  import ArticleHandler


def index(request):
    return render_to_response('index.html')

def admin_pages(request):
    return render_to_response('admin-knajpa.html')



def articles(request):
    article_handler = ArticleHandler
    #article_handler.initialize(request,response)
    return article_handler.response
