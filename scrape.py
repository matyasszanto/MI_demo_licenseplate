import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


def closead(driver):
    # with cross
    crosses = driver.find_elements('xpath', '//*[@id="dismiss-button"]/div/svg/path[1]')
    if len(crosses) > 0:
        driver.execute_script("arguments[0].click();", crosses[0])
        return

    # with "close" button
    close_buttons = driver.find_elements('xpath', '//*[@id="dismiss-button"]/div/span')
    if len(close_buttons) > 0:
        driver.execute_script("arguments[0].click();", close_buttons[0])
        return

    # with another "close" button
    close_buttons = driver.find_elements('xpath', '//*[@id="dismiss-button"]')
    if len(close_buttons) > 0:
        driver.execute_script("arguments[0].click();", close_buttons[0])
        print("close button found")
        return


def nextgallery(driver):
    nextgallery_buttons = driver.find_elements('xpath', '/html/body/div[1]/div[6]/div/div[1]/div[3]/ul/li[8]/a')
    if len(nextgallery_buttons) > 0:
        try:
            driver.execute_script("arguments[0].click();", nextgallery_buttons[0])
        except:
            time.sleep(0.5)
            closead(driver)
            nextgallery_buttons = driver.find_elements('xpath', '/html/body/div[1]/div[6]/div/div[1]/div[3]/ul/li[8]/a')
            if len(nextgallery_buttons) > 0:
                driver.execute_script("arguments[0].click();", nextgallery_buttons[0])
            else:
                closead(driver)
                nextgallery_buttons = driver.find_elements('xpath', '/html/body/div[1]/div[6]/div/div[1]/div[3]/ul/li[8]/a')
                if len(nextgallery_buttons) > 0:
                    driver.execute_script("arguments[0].click();", nextgallery_buttons[0])
    else:
        closead(driver)
        nextgallery_buttons = driver.find_elements('xpath', '/html/body/div[1]/div[6]/div/div[1]/div[3]/ul/li[8]/a')
        if len(nextgallery_buttons) > 0:
            driver.execute_script("arguments[0].click();", nextgallery_buttons[0])


if __name__ == "__main__":
    # point to firefox binary location
    binary = FirefoxBinary('/usr/bin/firefox')

    # initialize driver
    driver = webdriver.Firefox(firefox_binary=binary)  # executable_path='/usr/bin/geckodriver')

    # open webpage
    url = "https://platesmania.com/hu/gallery-6"
    driver.get(url)

    # click accept cookies
    try:
        # driver.find_element('xpath', '//*[@id="cl-consent"]/div[1]/div[1]/div[3]/a[2]').click()
        driver.find_element('xpath', '/html/body/div[3]/div[1]/div[1]/div[3]/a[2]').click()
    except:
        print("nocookies")

    data_array = []
    nojump_counter = 0
    prevgallery_num = 0

    # scroll through galleries
    for currentgallery in range(93):

        # check if there were too many nojumps
        if nojump_counter == 20:
            break

        # close ads
        closead(driver)

        # jump to next gallery
        # nextgallery(driver)
        driver.find_element('xpath', "/html/body/div[1]/div[5]/div/div[1]/div[2]/ul/li[12]/a").click()
        time.sleep(1)

        # close ads
        closead(driver)

        try:
            # check current gallery number
            currentgallery_num = driver.find_element('xpath',
                                                     "/html/body/div[1]/div[5]/div/div[1]/div[2]/ul/li[7]/a").text
            print(f"Current gallery: {int(currentgallery_num) - 1}")

            # check for nojump
            if currentgallery_num == prevgallery_num:
                nojump_counter += 1
                print(f"Nojump detected. Counter is at {nojump_counter}")
                continue
            else:
                prevgallery_num = currentgallery_num
                nojump_counter = 0

            time.sleep(0.5)

            for currentimage in range(10):

                time.sleep(0.5)

                # close ad
                closead(driver)

                # click the next thumbnail in the current gallery
                thumbnail_row = 5 + currentimage // 2
                thumbnail_col = 2 + currentimage % 2 if (
                            currentimage // 2 % 2 == 1 & currentimage % 2 == 1) else 1 + currentimage % 2
                thumbnail_xpath = '/html/body/div[1]/div[5]/div/div[1]/div[' + str(thumbnail_row) + ']/div[' + str(
                    thumbnail_col) + ']/div/div[2]/div[1]/a/img'

                next_thumbnails = driver.find_elements('xpath', thumbnail_xpath)
                if len(next_thumbnails) > 0:
                    driver.execute_script("arguments[0].click();", next_thumbnails[0])

                closead(driver)
                # get license plate data
                lic_plate_images = driver.find_elements('xpath',
                                                        '/html/body/div[1]/div[6]/div[1]/div[2]/div/div[2]/img')
                if len(lic_plate_images) > 0:
                    plate_url = lic_plate_images[0].get_attribute('src')
                else:
                    time.sleep(5)
                    lic_plate_images = driver.find_elements('xpath',
                                                            '/html/body/div[1]/div[6]/div[1]/div[2]/div/div[2]/img')
                    if len(lic_plate_images) > 0:
                        plate_url = lic_plate_images[0].get_attribute('src')

                # get vehicle data

                small_images = driver.find_elements('xpath',
                                                    '/html/body/div[1]/div[6]/div[1]/div[2]/div/div[2]/div/a/img')
                if len(small_images) > 0:
                    vehicle_data = small_images[0].get_attribute("alt")
                    url_m = small_images[0].get_attribute("src")
                    plate_number_end_index = vehicle_data.find(", ")
                    plate_number = vehicle_data[:plate_number_end_index]
                    url_o = url_m.replace("/m/", "/o/")

                    data_array.append([plate_number, vehicle_data, plate_url, url_o, url_m])

                else:
                    print("error")

                # go back to gallery
                driver.back()

            # create backup data export
            if (currentgallery + 1) % 10 == 0:
                backup_database = pd.DataFrame(data_array,
                                               columns=["Rendszam", "Adatok", "Rendszam_kep_url", "Highres_kep_url",
                                                        "Lowres_kep_url"])

                backup_csv_name = f"./rendszamok{currentgallery + 1}.csv"

                backup_database.to_csv(backup_csv_name, sep=";")

                print(f"backed up to {backup_csv_name}")

        except Exception as e:

            backup_database_error = pd.DataFrame(data_array,
                                                 columns=["Rendszam", "Adatok", "Rendszam_kep_url", "Lowres_kep_url",
                                                          "Highres_kep_url"])

            backup_csv_name = f"./rendszamok{currentgallery + 1}.csv"

            backup_database_error.to_csv(backup_csv_name, sep=";")

            print(f"There was an error! Backed up to {backup_csv_name}")
            print(f"Error: {e}")

    driver.close()

    database = pd.DataFrame(data_array,
                            columns=["Rendszam", "Adatok", "Rendszam_kep_url", "Lowres_kep_url", "Highres_kep_url"])

    database.to_csv("./rendszamok.csv", sep=";")

    print("success!")
