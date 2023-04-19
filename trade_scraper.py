import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def read_login_info():
    config = configparser.ConfigParser()
    config.read("config.ini")
    username = config.get("login", "username")
    password = config.get("login", "password")
    return username, password

def login(driver, username, password):
    # ログインページにアクセス
    driver.get("https://tb.click-sec.com/cfd/historical/historicalDataList.do")

    # ユーザー名とパスワードを入力
    driver.find_element(By.NAME, "j_username").send_keys(username)
    driver.find_element(By.NAME, "j_password").send_keys(password)

    # ログインボタンをクリック
    login_button = driver.find_element(By.XPATH, "//button[@value='Login']")
    login_button.click()

def order(driver):
    pass
    

def main():
    # ログイン情報を読み込む
    username, password = read_login_info()

    # WebDriverをセットアップ
    driver = webdriver.Edge(executable_path="path/to/msedgedriver.exe")

    try:
        # ログイン
        login(driver, username, password)

        # オーダー
        order(driver)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # WebDriverを閉じる
        driver.quit()

if __name__ == "__main__":
    main()
