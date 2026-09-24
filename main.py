import time
from playwright.sync_api import sync_playwright

# Variables
login_page = 'https://www.mercadocuentas.com/app/index.php'
stock_update_page = 'https://www.mercadocuentas.com/app/edicion_tnube.php'
playwright = sync_playwright().start()
browser = playwright.firefox.launch(headless=False)
page = browser.new_page(
        java_script_enabled=True,
        viewport={'width': 1920, 'height': 1080}
    )

# Functions

def url_check(expected_url: str, actual_url: str):
    if expected_url not in actual_url:
        print("The browser is not in the correct URL.")
        print("Want to try again?")
        choice = input()
        if choice != 'Y' or 'y':
            print("Exiting now")
            time.sleep(1)
            page.close()
            browser.close()
            playwright.stop()
        else:
            print("Retrying")
            page.goto(expected_url, wait_until='load')
    else:
        print("URL strings are a match. All fine and dandy!")

def stop_playwright():
    page.close()
    browser.close()
    playwright.stop()

### Main function (entry point)

def main():

    page.goto(login_page, wait_until='load')

    # Check if the correct page was loaded
    actual_page = str(page)
    url_check(login_page, actual_page)

    inputUser = input()
    inputPasswd = input()

    '''
    We can also hard-code it
    inputUser = "user goes here"
    inputPasswd = "passwd goes here"
    and comment the input() lines...
    '''

    page.get_by_role("textbox", name="USUARIO").fill(inputUser)
    page.get_by_role("textbox", name="Contraseña").fill(inputPasswd)
    page.get_by_role("button").click()

    time.sleep(2)

    page.goto(stock_update_page, wait_until='load')

    # Check if the correct page was loaded (again)
    actual_page = str(page)
    url_check(stock_update_page, actual_page)

    # Update stock
    page.get_by_role("link", name="TODAS").click()
    page.get_by_role("link", name="Diferentes a ML").click()

    # Add logic to stop program if no updates are needed
    # ///
    page.get_by_role("link", name="ACTUALIZAR TODOS LOS STOCK EN TIENDA NUBE").click()
    page.get_by_role("link", name="ACTUALIZAR STOCK EN TIENDA NUBE").click()

    time.sleep(10)

    # Close everything
    stop_playwright()


## Main function guard

if __name__=="__main__":
    main()


# TODO
'''
    Implementar mejores practicar para "error and exception handling"
'''
