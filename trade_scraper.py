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
    driver.get("https://kabu.click-sec.com/cfd/trade.do")

    # ユーザー名とパスワードを入力
    driver.find_element(By.NAME, "j_username").send_keys(username)
    driver.find_element(By.NAME, "j_password").send_keys(password)

    # ログインボタンをクリック
    login_button = driver.find_element(By.XPATH, "//button[@value='Login']")
    login_button.click()

    # CFDのページを表示
    link_element = driver.find_element(By.CLASS_NAME, "js-cfd")
    link_element.click()

def some_condition():
    # ここに条件判定のコードを書く
    # 条件が満たされた場合はTrueを返し、それ以外の場合はFalseを返す
    return True

def order(driver, side):

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
    
    # if some_condition():
    #     sell_button.click()
    # else:
    #     buy_button.click()

    # speed_order_element = driver.find_element(By.ID, "id_plaHref")
    # driver.execute_script("arguments[0].click();", speed_order_element)

    # iframe要素を取得する
    iframe = driver.find_element(By.ID, "iframe_trade")

    # iframe内の要素にアクセスするために、iframeを切り替える
    driver.switch_to.frame(iframe)
    
    # スピード注文タブに切り替える
    speed_order_element = driver.find_element(By.ID, "react-tabs-14")
    speed_order_element.click()

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

        # オーダー
        order(driver, pred)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # WebDriverを閉じる
        driver.quit()

if __name__ == "__main__":
    main()
