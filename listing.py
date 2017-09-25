"""
Fetch listings
"""
from time import sleep
import itertools

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from furl import furl


def load_cars(make, model, zipcode):
    """Get the page"""
    driver = webdriver.Chrome()
    driver.get('http://www.autotrader.com')
    make_element = driver.find_element_by_xpath(
        '//*[@id="makeCodeListPlaceHolder"]')
    select = Select(make_element)
    select.select_by_visible_text(make)

    model_element = driver.find_element_by_xpath(
        '//*[@id="modelCodeListPlaceHolder"]')
    select = Select(model_element)
    # Wait up to 5 seconds for models to be populated
    for _ in range(10):
        try:
            select.select_by_visible_text(model)
            break
        except NoSuchElementException:
            sleep(0.5)
    else:
        raise NoSuchElementException('Could not find model ' + model)

    zip_element = driver.find_element_by_xpath('//*[@id="zip"]')
    zip_element.clear()
    zip_element.send_keys(str(zipcode))

    driver.find_element_by_xpath('//button[.="Search"]').click()
    return driver


def get_pages(driver):
    """Set distance to any, and cars per page to 100, return URLs to fetch"""
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "searchRadius25"))
    )
    url = driver.current_url
    listing_page_furl = furl(url)
    listing_page_furl.args['searchRadius'] = '0'
    listing_page_furl.args['numRecords'] = '100'
    for i in itertools.count():
        listing_page_furl.args['firstRecord'] = str(i * 100)
        yield listing_page_furl.url


def get_cars_from_page(driver, url):
    """Get detail links from one page"""
    driver.get(url)
    results = set()
    if 'No results found.' in driver.page_source:
        return results
    links = driver.find_elements_by_css_selector('a')
    for link in links:
        target = link.get_attribute('href')
        try:
            if 'vehicledetails' in target:
                results.add(target)
        except TypeError:
            pass
    return results

def get_listings(make, model, zipcode):
    """Entry point"""
    # Make url by visiting the home page
    driver = load_cars(make, model, zipcode)
    all_car_urls = frozenset()
    for page in get_pages(driver):
        car_links = get_cars_from_page(driver, page)
        if car_links <= all_car_urls:
            break
        old_len = len(all_car_urls)
        all_car_urls = all_car_urls | car_links
        new_len = len(all_car_urls)
        print('Got', new_len - old_len, 'links.')
    driver.quit()
    return all_car_urls


if __name__ == '__main__':
    print(get_listings('Tesla', 'Model S', 78705))
