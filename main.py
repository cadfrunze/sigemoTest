from selenium import webdriver, common
from selenium.webdriver.remote.webelement import WebElement
from raport import gen_raport
import time
import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import random


class Testing:
    TARGET: str = "https://www.sigemo.ro/"
    USER: str = os.getenv("user_sigemo")
    PASS: str = os.getenv("pass_sigemo")

    # settings
    ch_options = webdriver.ChromeOptions()
    driver: webdriver = webdriver.Chrome(options=ch_options)
    ch_options.add_experimental_option("detach", True)
    driver.maximize_window()
    asteapta: WebDriverWait = WebDriverWait(driver, 20)

    # setup driver inainte de exec. fiecarui ttest_case

    def setup_method(self):
        # inainte de exec. fiecarei test_case, tzuca-l tata!
        self.driver.get(self.TARGET)
        try:
            self.asteapta.until(ec.element_to_be_clickable((By.CLASS_NAME, "cc-btn.cc-dismiss")))
        except common.exceptions.TimeoutException:
            pass
        else:
            self.driver.find_element(By.CLASS_NAME, "cc-btn.cc-dismiss").click()

    # test_case_1
    @pytest.mark.test
    def test_search1(self) -> None:
        """test_case_1"""
        expected_rez: str = "Niciun produs nu îndeplineşte criteriile de căutare."
        self.driver.find_element(By.NAME, "search").clear()
        time.sleep(3)
        self.driver.find_element(By.NAME, "search").send_keys("")
        self.asteapta.until(ec.element_to_be_clickable((By.CLASS_NAME, "search-button")))
        self.driver.find_element(By.CLASS_NAME, "search-button").click()

        rezultate = self.asteapta.until(ec.presence_of_element_located((By.CLASS_NAME, "main-products-wrapper")))
        rezultate_list: list = rezultate.text.split("\n")
        # print(rezultate_list)
        if expected_rez in rezultate_list:
            indexul: int = rezultate_list.index(expected_rez)
            try:
                assert expected_rez == rezultate_list[indexul]
                rezultat_final = "trecut".upper()
            except AssertionError:
                rezultat_final = "respins".upper()
        else:
            rezultat_final = "respins".upper()
        print(rezultat_final)
        time.sleep(5)
        gen_raport(self.test_search1.__doc__, rezultat_final)

    # test_case_2
    @pytest.mark.test
    def test_search2(self) -> None:
        """test_case_2"""
        rezultat_final: str = ""
        # expected_rez: str = "Niciun produs nu îndeplineşte criteriile de căutare."
        self.driver.find_element(By.NAME, "search").clear()
        time.sleep(3)
        self.driver.find_element(By.NAME, "search").send_keys("hankook")
        self.asteapta.until(ec.element_to_be_clickable((By.CLASS_NAME, "search-button")))
        self.driver.find_element(By.CLASS_NAME, "search-button").click()
        # self.driver.find_element(By.CLASS_NAME, "search-button").click()

        anunturi: list = self.asteapta.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "detalii-produs")))

        for element in anunturi:
            if "hankook" in element.text.lower():

                new_list: list = element.text.lower().split(" ")
                indexul: int = new_list.index("hankook")

                try:
                    assert "hankook" == new_list[indexul]
                    rezultat_final: str = "trecut".upper()
                except AssertionError:
                    rezultat_final = "respins".upper()
                finally:
                    break
        else:
            pass
            # aici poate sa nu fie pe stoc:)
        print(rezultat_final)
        time.sleep(5)
        gen_raport(self.test_search2.__doc__, rezultat_final)

    # test_case_3
    @pytest.mark.test
    def test_login1(self) -> None:
        """test_case_3"""

        rezult_expect: str = "Eroare: Datele de autentificare sunt greşite!"
        self.asteapta.until(ec.element_to_be_clickable((By.CLASS_NAME, "menu-item.main-menu-item.main-menu-item-1.multi"
                                                                       "-level.dropdown.drop-menu")))
        self.driver.find_element(By.CLASS_NAME, "menu-item.main-menu-item.main-menu-item-1.multi-level.dropdown.drop"
                                                "-menu").click()
        self.driver.find_element(By.CLASS_NAME, "menu-item.main-menu-item.main-menu-item-1.multi-level.dropdown.drop"
                                                "-menu").click()
        time.sleep(4)
        self.asteapta.until(ec.presence_of_element_located((By.ID, "input-email")))
        self.driver.find_element(By.NAME, "email").send_keys("1")
        self.driver.find_element(By.XPATH,
                                 "/html/body/div[7]/div[2]/div/div/div/div[2]/div/form/div[2]/input").send_keys("1")
        self.asteapta.until(ec.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Autentificare")))
        self.driver.find_element(By.XPATH,
                                 "/html/body/div[7]/div[2]/div/div/div/div[2]/div/form/div[3]/div/button").click()
        self.asteapta.until(ec.presence_of_element_located((By.CLASS_NAME, "alert.alert-danger.alert-dismissible")))

        raspuns = self.driver.find_element(By.CLASS_NAME, "alert.alert-danger.alert-dismissible")
        try:
            assert rezult_expect == raspuns.text
            rasp_test = "trecut".upper()
        except AssertionError:
            rasp_test = "respins".upper()
        print(rasp_test)
        time.sleep(5)
        gen_raport(self.test_login1.__doc__, rasp_test)

    # test_case_4
    @pytest.mark.test
    def test_login2(self) -> None:
        """test_case_4"""

        rezult_expect: str = "Marius Ioan Fodor"
        self.asteapta.until(ec.element_to_be_clickable((By.CLASS_NAME, "menu-item.main-menu-item.main-menu-item-1.multi"
                                                                       "-level.dropdown.drop-menu")))
        self.driver.find_element(By.CLASS_NAME, "menu-item.main-menu-item.main-menu-item-1.multi-level.dropdown.drop"
                                                "-menu").click()
        self.driver.find_element(By.CLASS_NAME, "menu-item.main-menu-item.main-menu-item-1.multi-level.dropdown.drop"
                                                "-menu").click()
        time.sleep(4)
        self.asteapta.until(ec.presence_of_element_located((By.ID, "input-email")))
        self.driver.find_element(By.NAME, "email").send_keys(self.USER)
        self.driver.find_element(By.XPATH,
                                 "/html/body/div[7]/div[2]/div/div/div/div[2]/div/form/div[2]/input").send_keys(
            self.PASS)
        self.asteapta.until(ec.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Autentificare")))
        self.driver.find_element(By.XPATH,
                                 "/html/body/div[7]/div[2]/div/div/div/div[2]/div/form/div[3]/div/button").click()
        self.asteapta.until(ec.presence_of_element_located((By.LINK_TEXT, "Adresele mele")))
        self.asteapta.until(ec.element_to_be_clickable((By.LINK_TEXT, "Adresele mele")))
        self.driver.find_element(By.LINK_TEXT, "Adresele mele").click()

        raspunsuri: list = self.asteapta.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "text-left")))

        try:

            assert rezult_expect == raspunsuri[0].text.split("\n")[0]
            rasp_test = "trecut".upper()
        except AssertionError:
            rasp_test = "respins".upper()
        time.sleep(5)
        print(rasp_test)
        gen_raport(self.test_login2.__doc__, rasp_test)

    # test_case_5
    @pytest.mark.test
    def test_produse1(self) -> None:
        """test_case_5"""
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Produse").click()
        self.driver.find_element(By.CLASS_NAME,
                                 "menu-item.flyout-menu-item.flyout-menu-item-1.dropdown.mega-menu").click()
        self.asteapta.until(ec.presence_of_element_located((By.CLASS_NAME, "refine-name")))
        self.driver.find_element(By.CLASS_NAME, "refine-name").click()
        self.asteapta.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "product-layout  ")))
        anunturi = self.asteapta.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "name")))
        try:
            assert len(anunturi) > 0
            rezultat_final: str = "trecut".upper()
        except AssertionError:
            rezultat_final = "respins".upper()
        print(rezultat_final)
        time.sleep(5)
        gen_raport(self.test_produse1.__doc__, rezultat_final)

    # test_case_6
    @pytest.mark.test
    def test_produse2(self) -> None:
        """test_case_6"""
        latimile: list = []
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Produse").click()
        self.driver.find_element(By.CLASS_NAME,
                                 "menu-item.flyout-menu-item.flyout-menu-item-1.dropdown.mega-menu").click()
        self.asteapta.until(ec.presence_of_element_located((By.CLASS_NAME, "refine-name")))
        self.driver.find_element(By.CLASS_NAME, "refine-name").click()

        self.asteapta.until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, "#filter-65ab7c6867065-collapse-5 > div > div > label > select")))
        elemente: list = self.asteapta.until(ec.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "#filter-65ab7c6867065-collapse-5 > div > div > label > select")))
        valoare: str = ''
        for elem1 in elemente:
            valoare += elem1.text
        list_elem = valoare.split(" ")
        print(list_elem)
        my_element = WebElement(self.driver, f"{random.choice(list_elem)}")
        print(my_element.get_attribute("XPATH"))
        element_path = my_element.get_attribute("class")
        print(element_path)

        # self.driver.find_element(By.CLASS_NAME, 'module-item.module-item-f4.panel.panel-active').click()
        # self.asteapta.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "module-item.module-item-f4.panel.panel-active")))
        # self.driver.find_element(By.LINK_TEXT, f"{random.choice(latimile)}")
        time.sleep(10)

        # elem_str = elem_str.replace("\n", "")
        # elem_str = elem_str.replace("Latime", "")
        # elem_str = elem_str.format()
        # print(elem_str)
        # # anunturi: list = self.asteapta.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "name")))
        # # # for elem in anunturi:
        # # #     print(elem.text)
        # # try:
        # #     assert len(anunturi) > 0
        # #     rezultat_final: str = "trecut".upper()
        # # except AssertionError:
        # #     rezultat_final = "respins".upper()
        # # print(rezultat_final)
        # # time.sleep(5)
        # # gen_raport(self.test_produse2.__doc__, rezultat_final)
