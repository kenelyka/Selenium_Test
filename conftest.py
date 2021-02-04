import pytest
from selenium import webdriver


@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
    driver.maximize_window()
    driver.get("https://www.bitdefender.com/")
    request.cls.driver = driver
    yield
    driver.quit()
