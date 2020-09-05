import sys, getopt
import requests
import json
import os

def get_url_list(uid):
    vlist = []
    url = f"https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp"
    data = json.loads(requests.get(url).text)
    if data["code"] == 0:
        count = data["data"]["page"]["count"]
        page_count = int(count/30) + 1
        for page in range(page_count):
            pn = page + 1
            url = f"https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn={pn}&keyword=&order=pubdate&jsonp=jsonp"
            page_vdict = json.loads(requests.get(url).text)["data"]["list"]["vlist"]
            for vdict in page_vdict:
                vlist.append(vdict["bvid"])
        
    return vlist

def write_vlist(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'u:', ['uid='])
    except:
        print('run.py -u <uid>')
        sys.exit(2)
    else:
        for opt, arg in opts:
            if opt == '-u':
                vlist = get_url_list(arg)
                urls = ""
                for v in vlist:
                    urls += f"https://www.bilibili.com/video/{v}\n"
                with open("video_list.txt", 'w+') as f:
                    f.write(urls)

if __name__ == "__main__":
    write_vlist(sys.argv)
    print(os.popen("annie -p -F video_list.txt").read())