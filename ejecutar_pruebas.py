"""Ejecuta todas las pruebas del proyecto.

Uso: python ejecutar_pruebas.py
"""

import sys
import unittest
from pathlib import Path

if __name__ == "__main__":
    raiz = Path(__file__).resolve().parent
    sys.path.insert(0, str(raiz))
    suite = unittest.defaultTestLoader.discover(str(raiz / "pruebas"), top_level_dir=str(raiz))
    resultado = unittest.TextTestRunner(verbosity=1).run(suite)
    sys.exit(0 if resultado.wasSuccessful() else 1)
