import os
import shutil
from datetime import datetime, timedelta

def cleanup_archives(archive_dir: str, days: int = 90):
    """Delete archived files older than N days"""
    cutoff = datetime.now() - timedelta(days=days)
    for root, dirs, files in os.walk(archive_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if mtime < cutoff:
                    print(f"Deleting old archive: {file_path}")
                    os.remove(file_path)

if __name__ == "__main__":
    cleanup_archives("./archived_emails/")
    cleanup_archives("./archived_docs/")
