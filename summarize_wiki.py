import sys
import bz2
import time

sys.path.append('/home/fede/tprofesional/gensim')
from gensim.corpora.wikicorpus import extract_pages, filter_wiki
from gensim.summarization import summarize
from timeout import TimeoutError, timeout

# The location of the Wikipedia dump.
wiki_fname = "/media/sdb2/enwiki2/enwiki-latest-pages-articles.xml.bz2"


@timeout(10*60)
def summarize_timeout(text):
    summarize(filter_wiki(text))


def summarize_wiki():
    ignore_namespaces = 'Wikipedia Category File Portal Template MediaWiki User Help Book Draft'.split()

    t1 = time.time()
    successful = 0
    failed = 0
    timedout = 0
    
    extracted_pages = extract_pages(bz2.BZ2File(wiki_fname), ('0',))
    for title, text, pageid in extracted_pages:
        if any(title.startswith(ignore + ':') for ignore in ignore_namespaces):
            continue
            
        try:
            summarize_timeout(text)
            successful += 1
        except TimeoutError:
            print "Timeout summarizing article", title, "with id", pageid
            timedout += 1
        except RuntimeError:
            failed += 1
        
        if (successful + failed) % 1000 == 0:
            print "Article", successful + failed, "summarized."
         
        time.sleep(1)

    t2 = time.time()

    print "Successful summaries:", successful
    print "Failed summaries:", failed
    print "Timeout summaries:", timedout

    print "t1:", t1
    print "t2", t2
    print "dt", t2 - t1


summarize_wiki()
