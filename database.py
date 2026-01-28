import json
import os
from datetime import datetime
from config import DATA_FILE


class Database:
    def __init__(self):
        self.data_file = DATA_FILE
        self.data = self.load_data()

    def load_data(self): # загрузка данных
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_data(self): #сохранение
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_item(self, name, item_type): #добавление в таблицу
        item = {
            'id': len(self.data) + 1,
            'name': name,
            'type': item_type,
            'date': datetime.now().strftime('%Y-%m-%d')
        }

        self.data.append(item)
        self.save_data()
        return item

    def get_all_items(self): #весь список
        return self.data

    def delete_item(self, item_id): #функ удаления по id
        for i, item in enumerate(self.data):
            if item['id'] == item_id:
                del self.data[i]
                self.save_data()
                return True
        return False

    def get_last_items(self, count=10): #последние 10 добавленных
        return self.data[-count:] if len(self.data) > count else self.data