from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class MhrsRandevuFind:

    def __init__(self, data):
        self.data = dict(data)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")

        #chrome_options.add_argument("--headless")

        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 3)
        self.driver.get("https://mhrs.gov.tr/vatandas/#/")
        self.driver.implicitly_wait(30)
        self.eDevletLogin()
        self.mhrs()
        
    def eDevletLogin(self):
        self.driver.implicitly_wait(30)

        self.wait.until(EC.element_to_be_clickable((self.driver.find_element(By.CSS_SELECTOR, '[type="button"]'))))
        buttons = self.driver.find_elements(By.CSS_SELECTOR, '[type="button"]')
        for button in buttons:
            if "e-Devlet İle Giriş" in button.get_attribute("textContent"):
                button.click()

        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="tridField"]')))
        self.driver.find_element(By.CSS_SELECTOR, '[name="tridField"]').send_keys(self.data["IdentificationNum"])

        self.driver.find_element(By.CSS_SELECTOR, '[name="egpField"]').send_keys(self.data["Password"])

        self.driver.find_element(By.CSS_SELECTOR, '[class="submitButton"]').click()

    def mhrs(self):
        self.driver.implicitly_wait(30)

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[id="vatandasApp"]')))

        try:
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="ant-modal-confirm-btns"] [class="ant-btn"]')))
            self.driver.find_element(By.CSS_SELECTOR, '[class="ant-modal-confirm-btns"] [class="ant-btn"]').click()

        except:
            pass

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="randevu-turu-grup-article"]')))
        randevuContents = self.driver.find_elements(By.CSS_SELECTOR, '[class="randevu-turu-grup-article"]')
        for randevuContent in randevuContents:
            if "Hastane Randevusu Al" in randevuContent.get_attribute("textContent"):
                sleep(1)
                randevuContent.click()
                sleep(1)

        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="ant-btn randevu-turu-button genel-arama-button ant-btn-lg"]')))
        self.driver.find_element(By.CSS_SELECTOR, '[class="ant-btn randevu-turu-button genel-arama-button ant-btn-lg"]').click()
        sleep(1)

        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[placeholder="Randevu aradığınız hastane, klinik veya hekim bilgisini yazınız."]')))

        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),\'İl Seçiniz')]")))
        self.driver.find_element(By.XPATH, "//span[contains(text(),\'İl Seçiniz')]").click()
        _city = self.data["City"]
        self.driver.find_elements(By.XPATH,  f"//span[contains(text(),\'{_city}')]")[1].click()
        sleep(1)

        if not self.data["District"] == "FARK ETMEZ":
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),\'-FARK ETMEZ-')]")))
            self.driver.find_elements(By.XPATH, "//div[contains(text(),\'-FARK ETMEZ-')]")[0].click()
            selectDistrict = self.driver.find_elements(By.CSS_SELECTOR, '[role="option"]')
            for district in selectDistrict:
                if district.text == self.data["District"]:
                    district.click()
                    sleep(1)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),\'Klinik Seçiniz')]")))
        self.driver.find_element(By.XPATH, "//span[contains(text(),\'Klinik Seçiniz')]").click()
        _clinic = self.data["Clinic"]
        self.driver.find_element(By.XPATH,  f"//span[contains(text(),\'{_clinic}')]").click()
        sleep(1)

        if not self.data["Hospital"] == "FARK ETMEZ":
            hospitalSelectMenu = self.driver.find_elements(By.XPATH, "//span[contains(text(),\'-FARK ETMEZ-')]")[0]
            self.wait.until(EC.element_to_be_clickable(hospitalSelectMenu))
            hospitalSelectMenu.click()
            _hospital = self.data["Hospital"]
            self.driver.find_element(By.XPATH,  f"//span[contains(text(),\'{_hospital}')]").click()
            sleep(1)

        if not self.data["DateSelect"] == "FARK ETMEZ":
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="ant-calendar-picker-input ant-input"]')))
            self.driver.find_element(By.CSS_SELECTOR, '[class="ant-calendar-picker-input ant-input"]').click()
            sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, '[class="ant-calendar-input "]').send_keys(self.data["DateSelect"])

        self.driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()
        sleep(1)

        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[class="ant-page-header-heading-title"]')))

        try:
            dataMsg = self.driver.find_element(By.CSS_SELECTOR, '[class="ant-modal-confirm-content"]').text
            if "bulunamamıştır." in dataMsg:
                print("randevu yok")
        except:
            print("randevu var")

        self.driver.quit()

MhrsRandevuFind({
    "IdentificationNum":"kimlik",
    "Password":"e devlet sifre",
    "City":"İSTANBUL(AVRUPA)",
    "District":"KÜÇÜKÇEKMECE",
    "Clinic":"Aile Hekimliği",
    "Hospital":"İSTANBUL- (AVRUPA)- KÜÇÜKÇEKMECE- KANUNİ SULTAN SÜLEYMAN EĞİTİM VE ARAŞTIRMA HASTANESİ",
    "DateSelect":"19.02.2023",
    })

MhrsRandevuFind({
    "IdentificationNum":"kimlik",
    "Password":"e devlet sifre",
    "City":"İSTANBUL(AVRUPA)",
    "District":"BAĞCILAR",
    "Clinic":"Çocuk Cerrahisi",
    "Hospital":"İSTANBUL- (AVRUPA)- BAĞCILAR EĞİTİM VE ARAŞTIRMA HASTANESİ",
    "DateSelect":"19.02.2023",
    })

MhrsRandevuFind({
    "IdentificationNum":"kimlik",
    "Password":"e devlet sifre",
    "City":"BURSA",
    "District":"FARK ETMEZ",
    "Clinic":"Diş Hekimliği (Genel Diş)",
    "Hospital":"FARK ETMEZ",
    "DateSelect":"FARK ETMEZ",
    })