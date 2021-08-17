import csv

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("http://segseguranca.com.br/base.asp?verif=ABCDEFGHI2.83321334405622POIUYT1.09861228866811&link=consulta_produto&validade=passei&tipo=descricao&valor=")

pages_number = len(driver.find_elements_by_class_name("indicePagina")) + 1

driver.find_element_by_id("areaLoginCliente").click()
driver.find_element_by_id("usuario").send_keys("0071454")
driver.find_element_by_id("senha").send_keys("3401")
driver.find_element_by_id("btLogin").click()

with open("products.txt", "w+") as products_file:
    csv_writer = csv.writer(products_file, delimiter=";")

    for page_index in range(pages_number):
        driver.get(f"http://segseguranca.com.br/base.asp?currentPage={page_index + 1}&verif=ABCDEFGHI2.83321334405622POIUYT1.09861228866811&link=consulta_produto&validade=passei&tipo=descricao&valor=")

        for product in driver.find_elements_by_class_name("cabecalhoTabelaFundoColor"):
            try:
                code = product.find_element_by_class_name("cabecalhoTabelaInfoProduto").text.split("\n")[0].split()[1]
                price = product.find_element_by_class_name("tabelaPrecoProdutoItem").text.split("\n")[0].split()[1]

                csv_writer.writerow([code, price])

            except NoSuchElementException:
                pass

driver.quit()
