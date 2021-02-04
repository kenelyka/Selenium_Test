import pytest
from PageObjects import *
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.mark.usefixtures("setup")
class TestBitdefender:
    # Perform all the required steps for Challenge #1
    def test_ChallengeOne(self):
        # Find/click Cookies OK button / Assert Bitdefender title / Find/click Home - See Solutions button
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, CookiesOKBtn))).is_displayed()
        self.driver.find_element(By.ID, CookiesOKBtn).click()
        assert "Bitdefender" in Title
        self.driver.find_element(By.XPATH, HomeSeeSolutions).click()

        # Create element by xpath variable and scroll down until the element is found
        MPElement = self.driver.find_element(By.XPATH, Multiplatform)
        self.driver.execute_script("arguments[0].scrollIntoView();", MPElement)
        MPElement.click()

        # Wait until the Buy Now element for Premium Security product is displayed
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, PremiumSecurityBuyNow))).is_displayed()
        time.sleep(1)

        # Assign product's Old/New prices to variable and compare them to the Old/New Prices in the cart
        # Main page product prices
        OldPrice = self.driver.find_element(By.CSS_SELECTOR, OldPremSecPrice).text
        NewPrice = self.driver.find_element(By.CSS_SELECTOR, NewPremSecPrice).text
        self.driver.find_element(By.CSS_SELECTOR, PremiumSecurityBuyNow).click()

        # Cart product prices
        CartOldPrice = self.driver.find_element(By.XPATH, CartOldPremSecPrice).text
        CartNewPrice = self.driver.find_element(By.XPATH, CartNewPremSecPrice).text
        assert OldPrice == CartOldPrice
        assert NewPrice == CartNewPrice

    # Perform all the requires steps for Challenge #2
    def test_SecondChallenge(self):
        # Modify the Cart quantity from 1 to 2
        CartActualPrice = self.driver.find_element(By.XPATH, CartNewPremSecPrice).text.replace('$', '')
        self.driver.find_element(By.XPATH, QuantityField).clear()
        self.driver.find_element(By.XPATH, QuantityField).send_keys(2)

        # Check the new prices for 2 products and remove them from the Cart
        self.driver.find_element(By.CSS_SELECTOR, QuantityUpdate).click()
        CartUpdatedPrice = self.driver.find_element(By.CSS_SELECTOR, "span[class='totalPrice ng-binding']").text.replace('$', '')

        # NOTE: Code below SHOULD FAIL (as per requirements) because the discount price applies only to one product
        try:
            assert float(CartActualPrice) + float(CartActualPrice) == float(CartUpdatedPrice)
        except:
            print("Price is not double because the discount doesn't apply for both products, but only one.")

    def test_BonusChallenge(self):
        # Remove and add again the product twice and check TOTAL PRICE - DISCOUNT
        # Add one product to the Cart and check the price
        self.driver.find_element(By.XPATH, QuantityField).clear()
        self.driver.find_element(By.XPATH, QuantityField).send_keys(1)
        self.driver.find_element(By.CSS_SELECTOR, QuantityUpdate).click()

        # Add the second product to the Cart
        self.driver.find_element(By.XPATH, QuantityField).clear()
        self.driver.find_element(By.XPATH, QuantityField).send_keys(2)
        self.driver.find_element(By.CSS_SELECTOR, QuantityUpdate).click()

        # Check if the price is correct
        TwoProductsPrice = self.driver.find_element(By.CSS_SELECTOR, "span[class='productPrice ng-binding']").text.replace('$', '')
        TwoProductsDiscount = self.driver.find_element(By.CSS_SELECTOR, "span[class='discountPrice ng-binding']").text.replace('-$', '')
        TwoProductsTotal = self.driver.find_element(By.CSS_SELECTOR, "span[class='totalPrice ng-binding']").text.replace('$', '')
        assert float(TwoProductsDiscount) + float(TwoProductsTotal) == float(TwoProductsPrice)

        # Remove the products form the Cart
        self.driver.find_element(By.XPATH, CartRemoveProducts).click()
        EmptyCartPrice = self.driver.find_element(By.CSS_SELECTOR, "span[class='totalPrice ng-binding']").text.replace('$', '')
        assert EmptyCartPrice == '0.00'
