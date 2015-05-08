import sys
import bz2
import time

sys.path.append('/home/fede/tprofesional/gensim')
from gensim.corpora.wikicorpus import extract_pages, filter_wiki
from gensim.summarization import summarize

wiki_fname = "/media/sdb2/enwiki2/enwiki-latest-pages-articles.xml.bz2"


def summarize_wiki():
    ignore_namespaces = 'Wikipedia Category File Portal Template MediaWiki User Help Book Draft'.split()

    t1 = time.time()
    successful = 0
    failed = 0

    for title, text, pageid in extract_pages(bz2.BZ2File(wiki_fname), ('0',)):
        if any(title.startswith(ignore + ':') for ignore in ignore_namespaces):
            continue

        try:
            summarize(filter_wiki(text))
            successful += 1
        except:
            failed += 1

    t2 = time.time()

    print "Successful summaries:", successful
    print "Failed summaries:", failed

    print "t1:", t1
    print "t2", t2
    print "dt", t2 - t1


summarize_wiki()
