import os
import csv
import scrapy
from bs4 import BeautifulSoup

class MySpider(scrapy.Spider):
    name = 'urbanoutfitters_upwork'
    start_urls = ['https://www.urbanoutfitters.com/products_sitemap.xml']
    custom_settings = {
        'USER_AGENT': 'Chrome/79.0.3945.88',  # Cambia a Safari
        'DOWNLOAD_DELAY': 3,  # Añade un retraso de 3 segundos entre las solicitudes
    }

    def get_links(self, xml):
        """ Get the links from the page """
        format_links = []
        soup = BeautifulSoup(xml, features='xml')
        links = soup.find_all('loc')
        for link in links:
            link = link.text
            format_links.append(link)
        return format_links

    def start_requests(self):
        print("Starting the requests")
        # Leer el archivo XML
        with open(os.path.expanduser('~/Scrapy_projects/products_sitemap.xml'), 'r') as file:
            data = file.read()

        # Extraer las URLs del archivo XML
        urls = self.get_links(data)
        print(f"URLs: {urls}")
        # Leer el archivo CSV de proxies
        with open(os.path.expanduser('~/Scrapy_projects/Proxy.csv'), 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Construir la URL del proxy
                proxy_url = f"http://{row['IP Address']}:{row['Port Number']}"
                print(proxy_url)
                # Hacer una solicitud para cada URL
                for url in urls:
                    yield scrapy.Request(
                        url,
                        callback=self.parse_product,
                        meta={'proxy': proxy_url},
                        headers={'User-Agent': 'Chrome/58.0.3029.110'}
                    )

    def parse_product(self, response):
        # Aquí puedes implementar la lógica para extraer los datos de los productos
        nombre = response.xpath('/html/body/div[1]/div[1]/div[2]/main/div/div[3]/div[2]/div[1]/h1/text()').get()
        precio_normal = response.xpath('/html/body/div[1]/div[1]/div[2]/main/div/div[3]/div[2]/div[4]/p/span[2]/text()').get()
        precio_rebajado = response.xpath('/html/body/div[1]/div[1]/div[2]/main/div/div[3]/div[2]/div[4]/p/span[1]/text()').get()
        imagenes = response.xpath('/html/body/div[1]/div[1]/div[2]/main/div/div[3]/div[1]/div/div//img/@src').getall()

        yield {
            'nombre': nombre,
            'precio_normal': precio_normal,
            'precio_rebajado': precio_rebajado,
            'imagenes': imagenes,
        }