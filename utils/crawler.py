from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler
import logging

"""
这是一个爬虫程序，使用icrawler模块对Google、Bing、Baidu等浏览器上有关锂电池的图片进行爬取并汇总到utils/data/raw文件夹下。
说明:
    1. 这一程序只能爬取到所需要的原数据集，但是不能保证数据集样本的互异性和有效性，还需要进行数据清洗和汇总
    2. 我们将主要聚焦于圆柱形（如18650）、方形电池和软包电池这三种常用电池的图片进行采集和标注
"""

class GoogleCrawler:
    def __init__(self, storage_path="data/raw/google"):
        # 设定google爬虫的保存路径
        self.google_storage = {"root_dir":storage_path}
        # 创建一个google icrawler对象
        self.google_crawler = GoogleImageCrawler(parser_threads=4,
                                            downloader_threads=4,
                                            storage=self.google_storage,
                                            )

    def crawl(self, keywords, max_num=10):
        # 对指定的关键词进行爬取
        for keyword in keywords:
            self.google_crawler.crawl(keyword=keyword,
                                 max_num=max_num,
                                 min_size=(500, 500),
                                 file_idx_offset="auto")

        print("Google浏览器中的图片爬取完毕")

class BingCrawler:
    def __init__(self, storage_path="data/raw/bing"):
        # 设定bing爬虫的保存路径
        self.bing_storage = {"root_dir": storage_path}
        # 创建一个bing icrawler对象
        self.bing_crawler = BingImageCrawler(parser_threads=4,
                                        downloader_threads=4,
                                        storage=self.bing_storage,
                                        )

    def crawl(self, keywords, max_num=10):
        # 对指定关键词进行爬取
        for keyword in keywords:
            self.bing_crawler.crawl(keyword=keyword,
                               max_num=max_num,
                               min_size=(500, 500),
                               file_idx_offset="auto")

        print("Bing浏览器中的图片爬取完毕")


class BaiduCrawler:
    def __init__(self, storage_path="data/raw/baidu"):
        # 设定baidu爬虫的保存路径
        self.baidu_storage = {"root_dir": storage_path}
        # 创建一个baidu icrawler对象
        self.baidu_crawler = BaiduImageCrawler(parser_threads=4,
                                             downloader_threads=4,
                                             storage=self.baidu_storage,
                                             )

    def crawl(self, keywords, max_num=10):
        # 对指定关键词进行爬取
        for keyword in keywords:
            self.baidu_crawler.crawl(keyword=keyword,
                                    max_num=max_num,
                                    min_size=(500, 500),
                                    file_idx_offset="auto")

        print("Baidu浏览器中的图片爬取完毕")

if __name__ == '__main__':
    # 指定所要爬取的图片的关键词
    target_keywords = ["li battery",
                ]

    # 设置爬虫输出日志的目标文件路径，将日志信息输出到logs/crawler.log文件中，不在控制台上显示
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/crawler.log'),  # 指定日志文件路径
        ]
    )

    # 创建爬虫对象并进行爬取
    google_crawler = GoogleCrawler()
    google_crawler.crawl(keywords=target_keywords, max_num=5)
    bing_crawler = BingCrawler()
    bing_crawler.crawl(keywords=target_keywords, max_num=5)
    baidu_crawler = BaiduCrawler()
    baidu_crawler.crawl(keywords=target_keywords, max_num=5)




