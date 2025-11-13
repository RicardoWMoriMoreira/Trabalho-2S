import unittest
import threading
import time
import sys
import os
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from app import app, service, loan_controller
import models.livro as livro_module


def limpar_cache_webdriver():
    cache_path = Path.home() / '.wdm'
    if cache_path.exists():
        try:
            print(f"Limpando cache do webdriver-manager em: {cache_path}")
            shutil.rmtree(cache_path)
            print("✅ Cache limpo com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao limpar cache: {e}")
            return False
    else:
        print("Cache não encontrado.")
        return False


class TestSeleniumPipeline(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        livro_module._livros.clear()
        service.usuarios.clear()
        service.matriculas.clear()
        service.emails.clear()
        loan_controller._loans.clear()
        loan_controller._next_id = 1
        
        def run_server():
            app.run(port=5000, use_reloader=False, debug=False)
        
        threading.Thread(target=run_server, daemon=True).start()
        time.sleep(2)
        
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--start-maximized')
        
        try:
            driver_path = ChromeDriverManager().install()
            
            if os.name == 'nt':
                driver_dir = Path(driver_path).parent
                if not driver_path.endswith('.exe'):
                    exe_files = list(driver_dir.glob('chromedriver*.exe'))
                    if exe_files:
                        driver_path = str(exe_files[0])
                    else:
                        parent_dir = driver_dir.parent
                        exe_files = list(parent_dir.glob('**/chromedriver*.exe'))
                        if exe_files:
                            driver_path = str(exe_files[0])
            
            if not os.path.exists(driver_path) or not driver_path.endswith('.exe'):
                raise FileNotFoundError(f"ChromeDriver executável não encontrado")
            
            cls.driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
        except Exception as e:
            print(f"Erro ao inicializar ChromeDriver: {e}")
            print("Tentando usar ChromeDriver do PATH...")
            try:
                cls.driver = webdriver.Chrome(options=chrome_options)
            except Exception as e2:
                print(f"Erro ao usar ChromeDriver do PATH: {e2}")
                print("\n" + "="*60)
                print("SOLUÇÕES:")
                print("1. Certifique-se de que o Google Chrome está instalado")
                print("2. Execute: pip install --upgrade webdriver-manager")
                print("3. Limpe o cache: python test_selenium.py --clear")
                if os.name == 'nt':
                    print("4. Ou manualmente: rmdir /s /q %USERPROFILE%\\.wdm")
                print("="*60)
                raise Exception(f"Não foi possível inicializar ChromeDriver: {e}")
        
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.driver.get('http://localhost:5000')
        time.sleep(1)
    
    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()
    
    def setUp(self):
        livro_module._livros.clear()
        service.usuarios.clear()
        service.matriculas.clear()
        service.emails.clear()
        loan_controller._loans.clear()
        loan_controller._next_id = 1
        self.driver.refresh()
        time.sleep(1)
    
    def test_pipeline_completa(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Usuários')]"))).click()
        time.sleep(0.5)
        
        self.driver.find_element(By.ID, "nome").send_keys("João Silva")
        self.driver.find_element(By.ID, "matricula").send_keys("ALU12345")
        Select(self.driver.find_element(By.ID, "tipo")).select_by_value("ALUNO")
        self.driver.find_element(By.ID, "email").send_keys("joao@email.com")
        self.driver.find_element(By.CSS_SELECTOR, "#formCadastro button[type='submit']").click()
        
        time.sleep(2)
        self.driver.refresh()
        time.sleep(1)
        
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Usuários')]"))).click()
        time.sleep(0.5)
        
        tabela = self.wait.until(EC.presence_of_element_located((By.ID, "tabelaUsuarios")))
        self.assertIn("João Silva", tabela.text)
        
        usuario_id = self.driver.find_element(By.XPATH, "//table[@id='tabelaUsuarios']//tbody//tr[1]//td[1]").text.replace("#", "").strip()
        
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Livros')]"))).click()
        time.sleep(0.5)
        
        self.driver.find_element(By.ID, "livro_id").send_keys("1")
        self.driver.find_element(By.ID, "livro_titulo").send_keys("Dom Casmurro")
        self.driver.find_element(By.ID, "livro_autor").send_keys("Machado de Assis")
        self.driver.find_element(By.ID, "livro_estoque").send_keys("3")
        self.driver.find_element(By.CSS_SELECTOR, "#formLivro button[type='submit']").click()
        time.sleep(1)
        
        tabela_livros = self.wait.until(EC.presence_of_element_located((By.ID, "tabelaLivros")))
        self.assertIn("Dom Casmurro", tabela_livros.text)
        
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Empréstimos')]"))).click()
        time.sleep(0.5)
        
        self.driver.find_element(By.ID, "loan_user_id").send_keys(usuario_id)
        self.driver.find_element(By.ID, "loan_book_id").send_keys("1")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Emprestar')]").click()
        time.sleep(1)
        
        tabela_loans = self.wait.until(EC.presence_of_element_located((By.ID, "tabelaLoans")))
        self.assertIn(usuario_id, tabela_loans.text)
        
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Relatórios')]"))).click()
        time.sleep(0.5)
        
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Livros Mais Emprestados')]"))).click()
        time.sleep(1)
        
        relatorios = self.wait.until(EC.presence_of_element_located((By.ID, "relatorios-container")))
        self.assertIn("Dom Casmurro", relatorios.text)
        
        print("\n✅ Pipeline completa executada com sucesso!")


def main():
    if '--clear' in sys.argv or '-c' in sys.argv:
        print("=" * 60)
        print("Limpeza de Cache do WebDriver Manager")
        print("=" * 60)
        print()
        limpar_cache_webdriver()
        print()
    
    print("=" * 60)
    print("Executando Testes Selenium - Pipeline Completa")
    print("=" * 60)
    print()
    
    unittest.main(verbosity=2, argv=sys.argv[:1])


if __name__ == '__main__':
    main()
