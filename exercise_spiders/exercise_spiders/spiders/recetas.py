import scrapy

class RecetasSpider(scrapy.Spider):
    name = "recetas"
    allowed_domains = ["www.recetasgratis.net"]
    start_urls = ["https://www.recetasgratis.net"]

    def parse(self, response):
        # Buscar todos los enlaces que contienen 'receta' en su href
        receta_links = response.css('a[href*="receta"]::attr(href)').getall()
        for link in receta_links:
            yield response.follow(link, self.parse_receta)

    def parse_receta(self, response):
        # Este método se llama para cada página de receta
        # Aquí puedes extraer los datos de la receta

        ingredientes = response.css('.ingredientes li label::text').getall()
        pasos = response.css('.apartado p::text').getall()
        # Esto te dará una lista de todos los textos dentro de los divs con un id que es 'anchor' seguido de un número
        # Puedes hacer lo que necesites con estos datos, por ejemplo, puedes imprimirlos:
        for ingrediente, paso in zip(ingredientes, pasos):
            yield {'ingrediente': ingrediente, 'paso': paso, 'url': response.url}