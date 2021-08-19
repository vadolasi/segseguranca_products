import csv

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

with open("config.txt") as config_file:
    url, login, password = config_file.readlines()

driver.get(url)

pages_number = len(driver.find_elements_by_class_name("indicePagina")) + 1

driver.find_element_by_id("areaLoginCliente").click()
driver.find_element_by_id("usuario").send_keys(login)
driver.find_element_by_id("senha").send_keys(password)
driver.find_element_by_id("btLogin").click()

with open("products.txt", "w+") as products_file:
    csv_writer = csv.writer(products_file, delimiter=";")

    for page_index in range(pages_number):
        driver.get(f"{url}&currentPage={page_index + 1}")

        for product in driver.find_elements_by_class_name("cabecalhoTabelaFundoColor"):
            try:
                code = product.find_element_by_class_name("cabecalhoTabelaInfoProduto").text.split("\n")[0].split()[1]
                price = product.find_element_by_class_name("tabelaPrecoProdutoItem").text.split("\n")[0].split()[1]

                csv_writer.writerow([code, price])

            except NoSuchElementException:
                pass

driver.quit()
