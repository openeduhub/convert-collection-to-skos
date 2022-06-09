from pathlib import Path

from base_logger import logger


def get_all_files():
    path = Path("data/")
    files = path.glob("graph_Taxonomie")
    return sorted(files, key=lambda x: x.stat().st_ctime)


def delete_old_files(files: list[Path]):
    files_to_delete = files[20:]
    if len(files_to_delete) < 0:
        for f in files_to_delete:
            logger.info(f"Deleting file: {f.name}")
            f.unlink()


def housekeeping():
    all_files = get_all_files()
    delete_old_files(all_files)
