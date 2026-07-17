"""
Lance tous les tests des patterns algorithmiques.
Usage : py -3 algorithms/run_all.py
"""

from pathlib import Path
import importlib.util
import sys


def run_module(path: Path) -> None:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    module.run_tests()


def main() -> None:
    folder = Path(__file__).parent / "lessons"
    files = sorted(folder.glob("**/*.py"))
    files = [f for f in files if f.name not in ("run_all.py", "__init__.py")]

    print("=" * 60)
    print("EXECUTION DE TOUS LES TESTS ALGORITHMES")
    print("=" * 60)

    for file in files:
        print(f"\n>>> {file.name}")
        run_module(file)

    print("\n" + "=" * 60)
    print(f"SUCCES : {len(files)} fichiers OK")
    print("=" * 60)


if __name__ == "__main__":
    main()
