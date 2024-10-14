from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


    


class Browser:

  def __init__(self, driver: str, keep_open: bool, data: list) -> None:
    self.service = Service(driver)
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", keep_open)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    self.browser = webdriver.Chrome(service=self.service, options=chrome_options)
    self.data = data


  def open_page(self, url: str):
    self.browser.get(url)
  

  def scrape_all_pages(self):
    self.get_all_row_info()

    # get all the rows and each of their values
    for i in range(1, 58):
      self.go_to_next_page()
      self.get_all_row_info()


  def get_all_row_info(self):
    # waiting for the rows to load (i.e for the whole page to load) so that we can scrape
    WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.even td')))
    
    # getting each row's values
    rows = self.browser.find_elements(By.CSS_SELECTOR, 'tbody tr')

    for row in rows:
      print('\n')
      current_row_data = []
      cols = row.find_elements(By.CSS_SELECTOR, 'td')
      col_1 = cols.pop(0)

      #print each column's data
      for col in cols: 
        current_row_data.append(col.text)

      # appending all the column values and the 3 tabs' values to data
      self.data.append(current_row_data + self.get_additional_info(col_1))
    
  
  def get_additional_info(self, col):
    even_row = '.even td'

    # waiting for the rows to load (i.e for the whole page to load) so that we can scrape
    WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, even_row)))

    # getting each tab's values
    self.click_on_more_info(col)
    val1 = self.get_headquarters_info()
    val2 = self.get_sponsored_info()
    val3 = self.get_directors_info()
    self.click_on_more_info(col)

    return [val1, val2, val3]


  def click_on_more_info(self, col):
    # clicking on the "more info" button (the + sign)
    col.find_element(By.TAG_NAME, 'i').click()


  def get_headquarters_info(self):
    # getting the headquarters info
    cols_path = 'tbody .tab-pane.fade'
    cols = self.browser.find_elements(By.CSS_SELECTOR, cols_path)
    cols.pop(1)

    # returning the headquarters for this row
    return cols[0].text


  def get_sponsored_info(self):
    # getting the sponsored info
    cols_path = 'tbody .tab-pane.fade'
    card_body_path = '.card .card-body'
    
    cols = self.browser.find_elements(By.CSS_SELECTOR, cols_path)
    cols.pop(1)
    card_bodies = cols[1].find_elements(By.CSS_SELECTOR, card_body_path) 

    # returning a large string which has all the sponsored people for this row
    return ',  '.join(
      [f'{card_body.find_element(By.CSS_SELECTOR, "h5").get_attribute("textContent")} | {card_body.find_element(By.CSS_SELECTOR, "h6").get_attribute("textContent").title()}'
      for card_body in card_bodies])


  def get_directors_info(self):
    # getting the directors info
    cols_path = 'tbody .tab-pane.fade'

    cols = self.browser.find_elements(By.CSS_SELECTOR, cols_path)
    cols.pop(1)

    # returning a large string which has all the directors for this row
    return ',  '.join([
      f"{card_body.find_element(By.CSS_SELECTOR, 'h5').get_attribute('textContent')} | {card_body.find_element(By.CSS_SELECTOR, 'h6').get_attribute('textContent').title()}"
      for card_body in cols[2].find_elements(By.CSS_SELECTOR, '.card-columns .card .card-body')])


  def go_to_next_page(self):
    next_button = '#cmos_next'
    even_row = '.even td'

    # waiting for the rows to load (i.e for the whole page to load) so that we can scrape
    WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, even_row)))

    # clicking on the "next" button
    button = self.browser.find_element(By.CSS_SELECTOR, next_button)
    button.click()




















