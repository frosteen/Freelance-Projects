import urllib.request
from lxml import html
import json
import pdfkit

SEED_URL = "https://www.indiabix.com/electronics-and-communication-engineering/digital-electronics/"


class Crawler:
    def __init__(self, seed_url):
        self.seed_url = seed_url

    def get_html_page(self, url):
        try:
            proxies = {"http": "http://myproxy.example.com:1234"}
            response = urllib.request.urlopen(url)
        except Exception as e:
            print(str(e))
            return "FetchError"
        return response.read()

    def get_html_dom(self, url):
        html_doc = self.get_html_page(url)
        html_dom = html.fromstring(html_doc)
        return html_dom

    def get_all_category_urls(self):
        category_url_pool = list()
        ##First category url is missed out in the list, since it has no anchor tag, so appending seed category url too.
        category_url_pool.append(self.seed_url)
        dom = self.get_html_dom(self.seed_url)
        category_nodes = dom.xpath(
            "//div[@class='div-top-left' and ./h3[contains(.,'Exercise :: ')]]/div[contains(@class,'div-scroll')]//li/a/@href"
        )
        for category_node in category_nodes:
            category_url_pool.append("https://www.indiabix.com" + category_node)
        return category_url_pool

    def get_all_pagination_urls(self, url):
        pagination_url_pool = list()
        pagination_url_pool.append(url)
        category_dom = self.get_html_dom(url)
        pagination_partial_urls = category_dom.xpath(
            "//div[@class='mx-pager-container']/p/a[./span[contains(@class,'mx-pager-no')]]/@href"
        )
        for pagination_partial_url in pagination_partial_urls:
            pagination_url_pool.append(
                "https://www.indiabix.com" + pagination_partial_url
            )
        # print(pagination_url_pool)
        return pagination_url_pool

    def get_data_from_final_url(self, url):
        print(url)
        final_data_pool = list()
        page_dom = self.get_html_dom(url)
        question_nodes = page_dom.xpath(
            "//div[@class='bix-div-container']/table[contains(@class,'bix-tbl-container')]"
        )
        for question_node in question_nodes:
            processing_data = dict()

            # Question number
            question_number = question_node.xpath(
                ".//td[contains(@class,'bix-td-qno')]/text()"
            )[0]
            processing_data["question_number"] = question_number

            # Question
            question = question_node.xpath(".//td[contains(@class,'bix-td-qtxt')]")
            WORD = ""
            for x in question:
                WORD = WORD + html.tostring(x).decode("utf-8").replace(
                    "/_files/", "https://www.indiabix.com/_files/"
                )
            processing_data["question"] = WORD

            # Answer
            answer_option = question_node.xpath(
                ".//div[contains(@class,'bix-div-answer')]//span[contains(@class,'jq-hdnakqb')]"
            )[0]
            processing_data["answer"] = html.tostring(answer_option).decode("utf-8")

            # Explanation
            answer_explanation = question_node.xpath(
                ".//div[contains(@class,'bix-div-answer')]//div[contains(@class,'bix-ans-description')]"
            )
            WORD = ""
            for x in answer_explanation:
                WORD = WORD + html.tostring(x).decode("utf-8").replace(
                    "/_files/", "https://www.indiabix.com/_files/"
                )
            processing_data["explanation"] = WORD

            # Options
            option_nodes = question_node.xpath(
                ".//td[contains(@class,'bix-td-miscell')]/table[contains(@class,'bix-tbl-options')]//tr/td[contains(@class,'bix-td-option')][2]"
            )
            processing_data["options"] = list()
            for option_node in option_nodes:
                option = (
                    html.tostring(option_node)
                    .decode("utf-8")
                    .replace("/_files/", "https://www.indiabix.com/_files/")
                )
                processing_data["options"].append(option)

            # Append final data
            final_data_pool.append(processing_data)

        # Save to JSON data
        with open("./resources/questions_data.json", "a") as myfile:
            for data in final_data_pool:
                myfile.write(json.dumps(data) + ",\n")


if __name__ == "__main__":
    c = Crawler(SEED_URL)
    cat_urls = c.get_all_category_urls()
    with open("./resources/questions_data.json", "a") as myfile:
        myfile.write("[")
    for cat_url in cat_urls:
        pag_urls = c.get_all_pagination_urls(cat_url)
        for pag_url in pag_urls:
            c.get_data_from_final_url(pag_url)
    filedata = ""
    print("Modifying...")
    with open("./resources/questions_data.json", "r") as myfile:
        filedata = myfile.read()
    filedata = filedata[:-1]
    with open("./resources/questions_data.json", "w") as myfile:
        myfile.write(filedata)
        myfile.write("]")
    print("Done.")
