from tika import parser                 # to initiate tika server
import time
import re

def get_text(file, sleep=0, counter=0):
    if counter == 2:        # so we stop the recursive function
        pass
    # grab the raw text using parser.from_file()
    raw = parser.from_file(file)
    status = raw['status']          # returns the status code from tika server
    # if things go well, return the raw text
    if status == 200:
        print(f"'{file}' successfully opened!")
        return raw['content']
    # if things don't go well, pause for five seconds and try again
    # we might not need this code, but it's useful for other server calls
    else:
        print(f'! ! ! ! error code {status} ! ! ! !')
        print(f'! ! ! ! trying again ! ! ! !')
        time.sleep(5)
        counter += 1
        # repeats grab_text up to twice
        return get_text(file, counter=counter)

# https://stackoverflow.com/questions/44333462/

def make_paragraphs(document, sleep=0):

    clean = re.sub(r'([\.\?\!])\n\n([A-Z])', r'\1PPAARRAAGGRRAAPPHH\2', document)
    clean = re.sub(r'\n\n\n\n([a-z]+)', r'PPAARRAAGGRRAAPPHH', clean)
#     clean = re.sub('(\d+)\n\n', r'\1PPAARRAAGGRRAAPPHHJJOOIINN', clean)
    clean = re.sub(r'([A-Za-z]+)\-\n\n', 'PPAARRAAGGRRAAPPHH', clean)
    clean = re.sub(r'\s\n\n', 'PPAARRAAGGRRAAPPHH', clean)
    clean = re.sub(r'\n\n\n\n', 'PPAARRAAGGRRAAPPHH', clean)
    clean = re.sub(r'\n\n', ' ', clean)
    clean = re.sub(r'\-\n', '', clean)
    clean = re.sub(r'\n', ' ', clean)
    clean = re.sub(r'\t', ' ', clean)
    clean = re.sub(r'\s\s', ' ', clean)
    clean = re.sub(r'\-([a-zA-Z]+)', r'\1', clean)
    clean = re.sub(r'\ue060', 'INFINITY', clean)
#     clean = re.sub('([A-Za-z]+)JJOOIINNPPAARRAAGGRRAAPPHH(.+)PPAARRAAGGRRAAPPHHJJOOIINN([a-z]+)', r'\1\3', clean)
    clean = re.split('PPAARRAAGGRRAAPPHH', clean)
    time.sleep(sleep)
    return clean