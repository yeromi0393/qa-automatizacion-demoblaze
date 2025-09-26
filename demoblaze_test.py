from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

URL = "https://www.demoblaze.com"
USERNAME = "iydtester"
PASSWORD = "IYD05"
PRODUCT_NAME = "Samsung galaxy s6"

def main():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # opcional, modo sin ventana
    driver = webdriver.Chrome(options=options)   # Selenium Manager gestiona el driver
    wait = WebDriverWait(driver, 15)

    try:
        # 1) Abrir sitio
        driver.get(URL)

        # 2) Abrir modal de login
        wait.until(EC.element_to_be_clickable((By.ID, "login2"))).click()

        # 3) Completar credenciales y enviar
        wait.until(EC.visibility_of_element_located((By.ID, "loginusername"))).send_keys(USERNAME)
        driver.find_element(By.ID, "loginpassword").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[text()='Log in']").click()

        # 4) Validar login
        user_welcome = wait.until(EC.visibility_of_element_located((By.ID, "nameofuser")))
        assert USERNAME in user_welcome.text, "No apareció 'Welcome <user>' tras login."

        # 5) Abrir producto
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, PRODUCT_NAME))).click()

        # 6) Agregar al carrito
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Add to cart']"))).click()

        # 7) Aceptar alerta
        wait.until(EC.alert_is_present())
        driver.switch_to.alert.accept()

        # 8) Ir al carrito
        wait.until(EC.element_to_be_clickable((By.ID, "cartur"))).click()

        # 9) Validar producto en el carrito
        wait.until(EC.visibility_of_element_located((By.XPATH, f"//td[text()='{PRODUCT_NAME}']")))
        print("[OK] Producto agregado correctamente al carrito.")

        # 10) Logout
        wait.until(EC.element_to_be_clickable((By.ID, "logout2"))).click()
        wait.until(EC.element_to_be_clickable((By.ID, "login2")))
        try:
            wait.until(EC.invisibility_of_element_located((By.ID, "nameofuser")))
        except TimeoutException:
            print("[WARN] 'nameofuser' tardó en ocultarse tras logout.")
        print("[OK] Logout realizado correctamente.")

    finally:
        time.sleep(1)
        driver.quit()

if __name__ == "__main__":
    main()
