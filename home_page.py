import time
from PIL import Image, ImageDraw

class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.qr_button_class = "btn-l-gary"
        self.qr_button_xpath = "//button[contains(@class, 'btn-rds')]"

        self.qr_id = "qrImageBl"

        self.lang_select_class = "lang-select"

        self.english_item_xpath = "//a[@href='/en/']"

        self.russion_your_email_title_xpath = "//h2[text()='Ваш временный Email адрес']"
        self.english_your_email_title_xpath = "//h2[text()='Your Temporary Email Address']"
        self.images_class = "lazy"

    def open_qr(self):
        assert not self.driver.find_element_by_id(self.qr_id).is_displayed()
        self.driver.find_element_by_xpath(self.qr_button_xpath).click()
        assert self.driver.find_element_by_id(self.qr_id).is_displayed()
        self.driver.find_element_by_xpath(self.qr_button_xpath).click()
        assert not self.driver.find_element_by_id(self.qr_id).is_displayed()

    def language_change(self):
        assert len(self.driver.find_elements_by_xpath(self.russion_your_email_title_xpath)) >= 1
        assert not len(self.driver.find_elements_by_xpath(self.english_your_email_title_xpath)) >= 1

        self.driver.find_element_by_class_name(self.lang_select_class).click()
        self.driver.find_element_by_xpath(self.english_item_xpath).click()


        assert not len(self.driver.find_elements_by_xpath(self.russion_your_email_title_xpath)) >= 1
        self.driver.implicitly_wait(5)
        assert len(self.driver.find_elements_by_xpath(self.english_your_email_title_xpath)) >= 1

    def test_fullpage_screenshot(self):
        print("SCREEEEENSHOT")
        self.driver.save_screenshot("test_screenshots/1.png")
        self.analyze()

    def analyze(self):
        screenshot_staging = Image.open("base_screenshots/1.png")
        screenshot_production = Image.open("test_screenshots/1.png")
        columns = 60
        rows = 80
        screen_width, screen_height = screenshot_staging.size

        block_width = ((screen_width - 1) // columns) + 1  # this is just a division ceiling
        block_height = ((screen_height - 1) // rows) + 1

        for y in range(0, screen_height, block_height + 1):
            for x in range(0, screen_width, block_width + 1):
                region_staging = self.process_region(screenshot_staging, x, y, block_width, block_height)
                region_production = self.process_region(screenshot_production, x, y, block_width, block_height)

                # IF DIFFERENCE IS DETECTED
                if region_staging is not None and region_production is not None and region_production != region_staging:
                    draw = ImageDraw.Draw(screenshot_staging)
                    draw.rectangle((x, y, x + block_width, y + block_height), outline="red")

        screenshot_staging.save("report_screenshots/1.png")

    def process_region(self, image, x, y, width, height):
        region_total = 0

        # This can be used as the sensitivity factor, the larger it is the less sensitive the comparison
        factor = 100

        for coordinateY in range(y, y + height):
            for coordinateX in range(x, x + width):
                try:
                    pixel = image.getpixel((coordinateX, coordinateY))
                    region_total += sum(pixel) / 4
                except:
                    return

        return region_total / factor


