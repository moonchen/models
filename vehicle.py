"""
Fetch a vehicle's details
"""
import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger(__name__)

def load_page(url):
    """Get the page"""
    #driver = webdriver.Chrome()
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    driver.get(url)
    return driver


def get_comments(driver):
    """Returns the text from comments"""
    comments_text = ''
    try:
        comments = driver.find_element_by_class_name('see-more')
        comments_text = comments.text
        see_more = comments.find_element_by_css_selector('div.text-link')
        see_more.click()
        comments_text = comments.text
    except NoSuchElementException:
        print('Failed to find comments')
        driver.save_screenshot('error.png')
    return comments_text


def list_items_under(parent):
    """Returns all text items under the parent element"""
    features = set()
    list_items = parent.find_elements_by_css_selector('li')
    for feature_element in list_items:
        features.add(feature_element.text)
    return features

def get_features(driver):
    """Returns a list of features from the page"""
    # First try to pop up the "all features" dialog
    span_links = driver.find_elements_by_css_selector('span.text-link')
    for span_link in span_links:
        if 'View all features' in span_link.text:
            features_link = span_link
            logger.debug('Opening features dialog')
            features_link.click()

    try:
        dialog = driver.find_element_by_class_name('modal-dialog')
        logger.debug('Getting features from dialog')
        return list_items_under(dialog)
    except NoSuchElementException:
        # Try to get the partial list on the main page
        logger.debug('Falling back to partial features list')
        list_elements = driver.find_elements_by_css_selector('ul')
        for list_element in list_elements:
            if list_element.get_attribute('data-qaid') == 'lst-options':
                logger.debug('Found features on main page')
                return list_items_under(list_element)
    return set()


def get_vehicle_details(url):
    """Entry point"""
    logger.info('Loading page')
    driver = load_page(url)
    logger.info('Getting comments')
    comments = get_comments(driver)
    logger.info('Getting features')
    features = get_features(driver)
    driver.quit()
    return {'comments': comments, 'features': features}


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG)
    TEST_URL = "https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=465666240&zip=78705&referrer=%2Fcars-for-sale%2Fsearchresults.xhtml%3Fzip%3D78705%26startYear%3D1981%26numRecords%3D100%26sortBy%3DdistanceASC%26incremental%3Dall%26firstRecord%3D400%26endYear%3D2018%26modelCodeList%3DTESMODS%26makeCodeList%3DTESLA%26searchRadius%3D0&startYear=1981&numRecords=100&firstRecord=400&endYear=2018&modelCodeList=TESMODS&makeCodeList=TESLA&searchRadius=0&makeCode1=TESLA&modelCode1=TESMODS,/cars-for-sale/vehicledetails.xhtml?listingId=465666240&zip=78705&referrer=%2Fcars-for-sale%2Fsearchresults.xhtml%3Fzip%3D78705%26startYear%3D1981%26numRecords%3D100%26sortBy%3DdistanceASC%26incremental%3Dall%26firstRecord%3D400%26endYear%3D2018%26modelCodeList%3DTESMODS%26makeCodeList%3DTESLA%26searchRadius%3D0&startYear=1981&numRecords=100&firstRecord=400&endYear=2018&modelCodeList=TESMODS&makeCodeList=TESLA&searchRadius=0&makeCode1=TESLA&modelCode1=TESMODS"
    print(get_vehicle_details(TEST_URL))
