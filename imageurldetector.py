import json
import urllib
import urllib.request


class ImageUrlDetector(object):
    blogName = ''
    startPosition = 0
    proxyAddress = ''
    pictureUrlList = []

    def __init__(self, blogname, startposition, proxyaddress):
        self.blogName = blogname
        self.startPosition = startposition
        self.proxyAddress = proxyaddress

    def detect(self):
        # url to start with
        blogname = self.blogName.strip()
        baseurl = 'http://api.tumblr.com/v2/blog/' + blogname + '.tumblr.com/info'

        if self.proxyAddress:
            proxy_support = urllib.request.ProxyHandler({'http': self.proxyAddress})
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)

        inforequest = urllib.request.Request(baseurl)
        inforesponse = urllib.request.urlopen(inforequest)
        inforesstring = inforesponse.read().decode('utf8')
        bloginfo = json.loads(inforesstring)
        blogtitle = bloginfo['response']['blog']['title']
        blogpostscount = bloginfo['response']['blog']['posts']
        print('Blog (' + blogtitle + ') has ' + str(blogpostscount) + ' posts.')
        offset = self.startPosition
        while True:
            posturl = 'http://api.tumblr.com/v2/blog/' + blogname + '.tumblr.com/posts/photo?offset=' + str(offset)
            postrequest = urllib.request.Request(posturl)
            postresponse = urllib.request.urlopen(postrequest)
            postresstring = postresponse.read().decode('utf8')
            postdata = json.loads(postresstring)
            posts = postdata['response']['posts']
            partpostscount = len(posts)
            print('Detecting posts from ' + str(offset) + ' to ' + str(offset + partpostscount))
            for post in posts:
                photodatas = post['photos']
                for photo in photodatas:
                    imageurl = photo['original_size']['url']
                    self.pictureUrlList.append(imageurl)
                    # print(imageurl)
                # imageurl = photodata['original_size']['url']
                # self.pictureUrlList.append(imageurl)
            offset += 20
            if(partpostscount < 20):
                break
        # print('Find ' + str(len(self.pictureUrlList)) + ' images.')

    def getimageurls(self):
        return self.pictureUrlList
