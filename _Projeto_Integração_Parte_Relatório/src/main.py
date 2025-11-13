import sys
from pathlib import Path

# Adiciona o diretório pai ao path para importar do main.py da raiz
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import main

if __name__ == "__main__":
    main.main()
