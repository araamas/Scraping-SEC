from openpyxl import Workbook
from get_info import Browser

CHROMEDRIVER_PATH = "C:\\Users\\Puja\\Python\\chromedriver"

# Create a new workbook and select the active sheet
workbook = Workbook()
sheet = workbook.active
sheet.title = 'Info'

# Define data to be written in the Excel file
data = [
    ['Operator Name', 'Function 1', 'Function 2', 'Function 3', 'Function 4', 'Fidelity Bond Expiry Date', 'Headquarters', 'Sponsored Individuals', 'Director(s)/Partner(s)']
]

def run():

    # get data from the website
    global data
    browser = Browser(driver=CHROMEDRIVER_PATH, keep_open=False, data=data)
    browser.open_page("https://sec.gov.ng/cmos/")
    browser.scrape_all_pages()
    data = browser.data

    # Write data to the sheet
    for row in data:
        sheet.append(row)

    # Save the workbook
    workbook.save('SEC Data.xlsx')


if __name__ == '__main__':
    run()

