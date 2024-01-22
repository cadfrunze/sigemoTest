from selenium import webdriver, common
from raport import gen_raport
import time
import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import random
from tkinter import messagebox


class Testing:
    TARGET: str = os.getenv("target")
    USER: str = os.getenv("user_sigemo")
    PASS: str = os.getenv("pass_sigemo")

    # settings
    ch_options = webdriver.ChromeOptions()
    ch_options.add_experimental_option("detach", True)
    driver: webdriver = webdriver.Chrome(options=ch_options)

    driver.maximize_window()
    asteapta: WebDriverWait = WebDriverWait(driver, 10)

    # setup driver inainte de exec. fiecarui test_case
    def setup_method(self) -> None:
        # inainte de exec. fiecarei test_case, tzuca-l tata!
        self.driver.get(self.TARGET)
        try:
            self.asteapta.until(ec.element_to_be_clickable((By.CLASS_NAME, "cc-btn.cc-dismiss")))
        except common.exceptions.TimeoutException:
            pass
        else:
            self.driver.find_element(By.CLASS_NAME, "cc-btn.cc-dismiss").click()

    def teardown_class(self) -> None:
        time.sleep(3)
        self.driver.quit()

    # search1
    @pytest.mark.test
    def test_case1(self) -> None:
        """test_case_1"""
        expected_rez: str = "Niciun produs nu îndeplineşte criteriile de căutare."
        self.driver.find_element(By.NAME, "search").clear()
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
        gen_raport(self.test_case1.__doc__, rezultat_final)
        messagebox.showinfo(title=f"{self.test_case1.__doc__}",
                            message=f"Am incheiat {self.test_case1.__doc__}\nApasa \"OK\" pt. a continua")

    # search2
    @pytest.mark.test
    def test_case2(self) -> None:
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
        gen_raport(self.test_case2.__doc__, rezultat_final)
        messagebox.showinfo(title=f"{self.test_case2.__doc__}",
                            message=f"Am incheiat {self.test_case2.__doc__}\nApasa \"OK\" pt. a continua")

    # login1
    @pytest.mark.test
    def test_case3(self) -> None:
        """test_case_3"""

        rezult_expect: str = "Eroare: Datele de autentificare sunt greşite!"
        self.asteapta.until(ec.element_to_be_clickable((By.CLASS_NAME, "menu-item.main-menu-item.main-menu-item-1.multi"
                                                                       "-level.dropdown.drop-menu")))
        self.driver.find_element(By.CLASS_NAME, "menu-item.main-menu-item.main-menu-item-1.multi-level.dropdown.drop"
                                                "-menu").click()
        self.driver.find_element(By.CLASS_NAME, "menu-item.main-menu-item.main-menu-item-1.multi-level.dropdown.drop"
                                                "-menu").click()
        time.sleep(2)
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
        gen_raport(self.test_case3.__doc__, rasp_test)
        messagebox.showinfo(title=f"{self.test_case3.__doc__}",
                            message=f"Am incheiat {self.test_case3.__doc__}\nApasa \"OK\" pt. a continua")

    # login2
    @pytest.mark.test
    def test_case4(self) -> None:
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
        print(rasp_test)
        gen_raport(self.test_case4.__doc__, rasp_test)
        messagebox.showinfo(title=f"{self.test_case4.__doc__}",
                            message=f"Am incheiat {self.test_case4.__doc__}\nApasa \"OK\" pt. a continua")

    # produse1
    @pytest.mark.test
    def test_case5(self) -> None:
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
        gen_raport(self.test_case5.__doc__, rezultat_final)
        messagebox.showinfo(title=f"{self.test_case5.__doc__}",
                            message=f"Am incheiat {self.test_case5.__doc__}\nApasa \"OK\" pt. a continua")

    # produse2
    @pytest.mark.test
    def test_case6(self) -> None:
        """test_case_6"""
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Produse").click()
        self.driver.find_element(By.CLASS_NAME,
                                 "menu-item.flyout-menu-item.flyout-menu-item-1.dropdown.mega-menu").click()
        self.asteapta.until(ec.presence_of_element_located((By.CLASS_NAME, "refine-name")))
        self.driver.find_element(By.CLASS_NAME, "refine-name").click()
        while True:
            try:
                self.driver.find_element(By.XPATH,
                                         "/html/body/div[7]/div[2]/div/div/div/div/div/div[1]/div/div/div/div[5]/div")
                break
            except:
                self.driver.refresh()
                continue
        # De aici incepe GREUL
        html_content = self.driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        option_elements = soup.find_all('option')
        elemente: list = [x.get("value") for x in option_elements if x.get("value").isnumeric()]
        incercari: list = []
        while not (len(incercari) == len(elemente)):
            zarul = random.choice(elemente)
            while zarul in incercari:
                if len(incercari) == (len(elemente) - 1):
                    for elem1 in elemente:
                        if elem1 not in incercari:
                            zarul = elem1
                            break
                else:
                    zarul = random.choice(elemente)
            incercari.append(zarul)
            self.driver.get(f'https://www.sigemo.ro/anvelope-turisme?ff4={zarul}')
            try:
                lista_produse: list = self.asteapta.until(ec.presence_of_all_elements_located((By.XPATH,
                                                                                               "/html/body/div[7]/div[3]/div/div/div/div[2]/div[1]/div/div[2]/div[1]/div[1]")))
                for elem in lista_produse:
                    print(elem.text)
                try:
                    assert len(lista_produse) > 0
                    rezultat_final = "trecut".upper()
                except AssertionError:
                    rezultat_final = "respins".upper()
                    break
                break
            except:
                continue
        else:
            rezultat_final = "respins".upper()
        gen_raport(self.test_case6.__doc__, rezultat_final)
        messagebox.showinfo(title=f"{self.test_case6.__doc__}",
                            message=f"Am incheiat {self.test_case6.__doc__}\nApasa \"OK\" pt. a continua")

    # locatii
    @pytest.mark.test
    def test_case7(self) -> None:
        """test_case_7"""
        self.asteapta.until(ec.element_to_be_clickable((By.LINK_TEXT, "Locatii")))
        self.driver.find_element(By.LINK_TEXT, "Locatii").click()
        self.driver.find_element(By.LINK_TEXT, "Locatii").click()
        self.asteapta.until(ec.element_to_be_clickable((By.CLASS_NAME, "tab-6")))
        self.driver.find_element(By.CLASS_NAME, "tab-6").click()
        try:
            assert self.asteapta.until(ec.presence_of_element_located((By.CLASS_NAME, "block-image")))
            rezultat_final: str = "trecut".upper()
        except AssertionError:
            rezultat_final = "respins".upper()
        print(rezultat_final)
        gen_raport(self.test_case7.__doc__, rezultat_final)
        messagebox.showinfo(title=f"{self.test_case7.__doc__}",
                            message=f"Am incheiat {self.test_case7.__doc__}\nApasa \"OK\" pt. a continua")

    # servicii
    @pytest.mark.test
    def test_case8(self) -> None:
        """test_case_8"""
        WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable((By.LINK_TEXT, "Servicii")))
        self.driver.find_element(By.LINK_TEXT, "Servicii").click()
        self.driver.find_element(By.LINK_TEXT, "Servicii").click()
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME,
                                                                             "module-item.module-item-1.info-blocks.info-blocks-icon")))
        self.driver.find_element(By.CLASS_NAME, "module-item.module-item-1.info-blocks.info-blocks-icon").click()
        WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.CLASS_NAME, "lazyload.lazyloaded")))
        try:
            assert self.driver.find_element(By.CLASS_NAME, "lazyload.lazyloaded").is_displayed()
            rezultat_final: str = "trecut".upper()
        except AssertionError:
            rezultat_final = "respins".upper()
        print(rezultat_final)
        gen_raport(self.test_case8.__doc__, rezultat_final)
        messagebox.showinfo(title=f"{self.test_case8.__doc__}",
                            message=f"Am incheiat {self.test_case8.__doc__}\nApasa \"OK\" pt. a continua")

    # informatii clienti
    @pytest.mark.test
    def test_case9(self) -> None:
        """test_case_9"""
        self.driver.find_element(By.CLASS_NAME, "menu-item.top-menu-item.top-menu-item-1").click()
        try:
            assert (self.driver.find_element(By.LINK_TEXT, "0364 880 820") and
                    (self.driver.find_element(By.LINK_TEXT, "0736 404 151")))
            rezultat_final: str = "trecut".upper()
        except AssertionError:
            rezultat_final = "respins".upper()
        print(rezultat_final)
        time.sleep(2)
        gen_raport(self.test_case9.__doc__, rezultat_final)
        messagebox.showinfo(title=f"{self.test_case9.__doc__}",
                            message=f"Am incheiat {self.test_case9.__doc__}\nApasa \"OK\" pt. a continua")

    # linkul
    @pytest.mark.test
    def test_case10(self) -> None:
        """test_case_10"""
        WebDriverWait(self.driver, 40).until(ec.element_to_be_clickable(
            (By.CLASS_NAME, "module-item.module-item-11.ms-slide.ms-slide-auto-height")))

        if self.driver.find_element(By.CLASS_NAME,
                                 "module-item.module-item-11.ms-slide.ms-slide-auto-height"):
            self.driver.find_element(By.CLASS_NAME,
                                     "module-item.module-item-11.ms-slide.ms-slide-auto-height").click()
            rezultat_final: str = "trecut".upper()
        else:
            rezultat_final = "respins".upper()
        print(rezultat_final)
        gen_raport(self.test_case10.__doc__, rezultat_final)
        messagebox.showinfo(title=f"{self.test_case10.__doc__}",
                            message=f"Am incheiat ultimul {self.test_case10.__doc__}\nApasa \"OK\" pt. a inchide driverul")
