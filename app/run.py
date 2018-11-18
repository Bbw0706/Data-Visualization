import scrapy
from scrapy.crawler import CrawlerProcess
from collections import Counter
import sta
import os
from os import path
import numpy as np
import wordcloud
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
import random

class DetikScrap(scrapy.Spider):
    'Terjawabnya Misteri Diam Si Kancil di Malam Pembantaian, detik.com, "https://news.detik.com/berita/d-4304003/terjawabnya-misteri-diam-si-kancil-di-malam-pembantaian"'
    name = "Detik"
    start_urls = [
        'https://news.detik.com/berita/d-4304003/terjawabnya-misteri-diam-si-kancil-di-malam-pembantaian',
    ]

    def grey_color_func(self, word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(0, 0%%, %d%%)" % random.randint(150, 250)

    def transform_format(self, val):
        for i in val :
            if i == 0 :
                return 255
            else :
                return i
        return val

    def parse(self, response):
        a = []
        b = []
        c = ''
        for quote in response.css('.detail_text'):
            for i in quote.css('p::text').extract():
                a.append(i)

        for i in a :
            c += i

        d = sta(c)

        data = Counter(d)
        e = data.most_common()

        f = ()
        g = list(f)
        for i in e:
            g.append(i)

        h = tuple(g)

        j = dict(h)

        mask = np.array(Image.open(path.join(path.dirname(__file__), "py.png")))
        transformed_mask = np.ndarray((mask.shape[0], mask.shape[1]), np.int32)

        for i in range(len(mask)):
            transformed_mask[i] = list(map(self.transform_format, mask[i]))

        cloud = wordcloud.WordCloud(background_color="#000",
                            width=1000, height=800,
                            mask=transformed_mask,
                            collocations=False
                          ).generate_from_frequencies(j)

        image_colors = wordcloud.ImageColorGenerator(mask)

        plt.figure()
        # plot words
        plt.imshow(cloud.recolor(color_func=image_colors), interpolation="bilinear")
        # remove axes
        plt.axis("off")
        # show the result
        plt.show()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(DetikScrap)
process.start()