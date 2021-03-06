#!/usr/bin/env python3

import random

from bottle import route, run, HTTPResponse
from sources.Exceptions import NoResultException, SourceNotFound
from fetcher import fetchFirstMeaning

from sources import Factory

@route('/')
def main():
    return HTTPResponse(status=200, body="Hey there, this is a cool site (still in beta) that makes it easy to find meanings. Just go to <a href='//dafuq.is/afk'>dafuq.is/afk</a> to know about what <b>afk</b> is. You can also choose sources: We currently use urbandictionary and wordnik. Try: <a href='//dafuq.is/kewl/ud'>dafuq.is/kewl/ud</a> or <a href='//dafuq.is/vernacular/wordnik'> dafuq.is/vernacular/wordnik</a>. <br><br>I might serve some ads from <a href='https://basicattentiontoken.org/'>https://basicattentiontoken.org/</a>. You know for the domain and hosting and whatnot. <br><br> By the way, want to take this to new level? Join <a href='//github.com/dafuq-is'>our github organization</a> and give us some love.")

@route('/<word>')
def getMeaning(word):
    _prioritizedSources = Factory.getAllSources()

    # randomize (for now)
    # The idea is to create a prioritized list based on the word
    # A smart system that selects the likeliness of people looking for a specific source
    # when they think of the word.
    # e.g., when someone says fudge, they might be more like to find that its a replacement of f***
    # rather than looking for a candy.
    #
    # We will categorize the sources based on what kind of meaning it provides (literal, pop culture, meme, etc)
    # ...and find association of the particular word or phrase with these categories
    #
    # Each source within a category will be separately ranked
    # One source can be in more than one category with different ranks
    random.shuffle(_prioritizedSources)

    try:
        meaning = fetchFirstMeaning(_prioritizedSources, word)
    except NoResultException:
        return HTTPResponse(status=404, body="Dafuq! <b>" + word +  "</b> is not known to any of our sources")

    return HTTPResponse(status=200, body=meaning['meaning'] + '.<br><br>as defined by: <b>' + meaning['source'] + '</b>')


@route('/<word>/<service>')
def choose(word, service):
    try:
        meaning = Factory.getSource(service).getMeaning(word)
    except NoResultException:
        return HTTPResponse(status=404, body="Dafuq! <b>" + service + "</b> does not know about <b>" + word + "</b>! ")
    except SourceNotFound:
        supported = ", ".join(Factory.getAllSources())
        return HTTPResponse(status=404, body="Dafuq! <b>" + service + "</b> is not supported. Use: <i>" + supported + "</i>!")


    return HTTPResponse(status=200, body=meaning)


run(host='0.0.0.0', port=8080, debug=True)
