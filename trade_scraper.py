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
    # access target url
    driver.get("https://kabu.click-sec.com/cfd/trade.do")

    # input user-name and password
    driver.find_element(By.NAME, "j_username").send_keys(username)
    driver.find_element(By.NAME, "j_password").send_keys(password)

    login_button = driver.find_element(By.XPATH, "//button[@value='Login']")
    login_button.click()

    # CFDのページを表示
    link_element = driver.find_element(By.CLASS_NAME, "js-cfd")
    link_element.click()

# 売りと買いのどちらも0なら建て玉なし
def exists_open_interest(driver):

    # ローカルストレージの値を設定
    local_storage_data = {
        'cfd.228435341.introduction-modal-flag': 'false',
        'cfd.228435341.order-tab-select': '2',
        'cfd.228435341.cfd-product-code': '00003060000', # '00004060000',
        # 'cfd.228435341.scroll-kbn': '{"speed":"","trade":"1"}',
        # 'cfd.228435341.chart-tab-select': '1',
        # 'cfd.228435341.position-tab-select': '0',
        # 'cfd.228435341.cfd-product-code-speed': '00001060000',
        # 'cfd.228435341.order-product-code': '00004060000',
    }

    for key, value in local_storage_data.items():
        driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")

    # ページをリロードして、新しいローカルストレージの値でアクセス
    driver.refresh()

    # iframe要素を取得する
    iframe = driver.find_element(By.ID, "iframe_trade")

    # iframe内の要素にアクセスするために、iframeを切り替える
    driver.switch_to.frame(iframe)
    
    # スピード注文タブに切り替える
    speed_order_element = driver.find_element(By.ID, "react-tabs-14")
    speed_order_element.click()

    # 建て玉を確認 => 損益(pips)の値を確認
    sell_oi = driver.find_element(By.XPATH, '//*[@id="react-tabs-15"]/div/div[3]/div[3]/div/div[5]/div/div[1]/label')
    buy_oi = driver.find_element(By.XPATH, '//*[@id="react-tabs-15"]/div/div[3]/div[3]/div/div[5]/div/div[3]/label')

    return {"sell": sell_oi.text, "buy": buy_oi.text} 

def order(driver, pred):

    # lot
    lot_button = driver.find_element(By.XPATH, '//*[@id="react-tabs-15"]/div/div[3]/div[4]/div[2]/div/div[2]/button[1]')
    lot_button.click()

    sell_button = driver.find_element(By.XPATH, '//*[@id="react-tabs-15"]/div/div[3]/div[2]/div[1]/div[1]/div/label')
    buy_button = driver.find_element(By.XPATH, '//*[@id="react-tabs-15"]/div/div[3]/div[2]/div[1]/div[2]/div/label')

    if pred == 1:
        buy_button.click()
    else:
        sell_button.click()


def main():
    # ログイン情報を読み込む
    username, password = read_login_info()

    # WebDriverをセットアップ
    driver = webdriver.Edge(executable_path="path/to/msedgedriver.exe")

    try:
        # ログイン
        login(driver, username, password)

        # モデルによる予測
        pred = ""

        # 建て玉の損益を確認
        oi = exists_open_interest(driver)

        # プラスかマイナスなら利確・損切りの判断


        # 建て玉がある場合、決済するかを判断


        # 建て玉がない場合、予測方向にポジションを持つ
        order(driver, pred)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # WebDriverを閉じる
        driver.quit()

if __name__ == "__main__":
    main()
