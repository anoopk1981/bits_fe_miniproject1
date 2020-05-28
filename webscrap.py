import scrapy
import re
import pandas as pd


class DmartSpider(scrapy.Spider):
    name = 'vegetables'
    allowed_domains = ['www.dmart.in/vegetables']
    start_urls = ['http://www.dmart.in/vegetables']

    def parse(self, response):
        category = response.xpath("//a[@class='nonrwd_only_bc']/text()").get() # Get the category - In this case it is Vegetables
        category = re.sub(r'\s', '', category)  #Remove the unwanted characters
        category = re.sub("[\(\[].*?[\)\]]", "", category) #Remove text inside brackets along with the brackets itself
        items = response.xpath("//h4//a/text()").getall()  #Get the items

        for idx, item in enumerate(items):
                item = re.sub("[\(\[].*?[\)\]]", "", item)  #Remove text inside brackets along with the brackets itself
                item = item.replace("Fresh", "") #Remove the work Fresh
                item = item.strip()
                items[idx] = item
        tuple_list =  [tuple(item.split(":")) for item in items] #Convert the item list into a tuple
        item, quantity = zip(*tuple_list) #Separate the tuple into two lists - one to store the item name and next one to store the quantity

        cost = response.xpath("//p[@class='product-listing--discounted-price ']/text()").getall()  #Get the cost
        cost = list(dict.fromkeys(cost))  #Remove word 'Dmart' as it is duplicated
        cost.remove('DMart ') #Remove the final occurence of the word

        categories = [category for _ in range(len(cost))] #Create a list to store the category value. The length will be the length of the cost list or item list or quantity list

        df = pd.DataFrame(columns=['Category', 'Item','Quantity','Cost'])  #Create data frame
        df['Category'] = categories
        df['Item'] = item
        df['Quantity'] = quantity
        df['Cost'] = cost

        yield df.to_csv("data.csv", sep=",")  #Write to a csv file

