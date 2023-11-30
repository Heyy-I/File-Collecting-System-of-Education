import os

from apscheduler.executors.pool import ThreadPoolExecutor

from configs import COLLECTIONS_FOLDER_URL
from apscheduler.schedulers.background import BackgroundScheduler

# 1.定义执行器
exeutors = {
    "default":ThreadPoolExecutor(max_workers=10)
}

scheduler = BackgroundScheduler(exeutors=exeutors)

def collection_packages_clear():
    for dir_path, dir_names, file_names in os.walk(COLLECTIONS_FOLDER_URL + 'packages/'):
        for file_name in file_names:
            os.remove(dir_path + file_name)

def one_day_forward(datetime):
    return datetime.fromtimestamp(datetime.timestamp() - 24 * 60 * 60)