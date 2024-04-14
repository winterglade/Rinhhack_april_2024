import re
import email
import os

eml_folder_path = "C:/Users/User/Desktop/hacaton/small"  # путь к папке с файлами EML.

# фильтры:
filters = {
    'Паспорта': [
        r'\b\d{4}\s\d{6}\b', 
        r"\b\d{4} № \d{6}\b", 
        r"\b\d{4}-\d{6}\b", 
        r"\b\d{4}№\d{6}\b", 
        r"\b\d{4}№\d{6}\b", 
        r"\b\d{4} N\d{6}\b", 
        r"\b\d{4} №\d{6}\b", 
        r"\b\d{4}\s\d{6}\b", 
        r"\b\d{4} N\d{6}\b", 
        r"\b\d{4}№\d{6}\b", 
        r"\b\d{4}N\d{6}\b", 
        r"\b\d{4} N \d{6}\b", 
        r"\b\d{2}\s\d{2} N \d{6}\b", 
        r"\b\d{2}\s\d{2} № \d{6}\b", 
        r"\b\d{4} N \d{6}\b", 
        r"\b\d{4} N \d{6}\b", 
        r"\b\d{4}\s\d{6}\b", 
        r"\b\d{4}\s\d{6}\b", 
        r"\b\d{4} N \d{6}\b"
    ],
    'Данные аккаунта': [
        r'[0-9]{13,16}'   
    ],
    'СНИЛС': [
        r'^\d{3}-\d{3}-\d{3} \d{2}$', r'\b\d{3}-\d{3}-\d{3}\s\d{2}\b'   
    ],
    'Номер телефона': [
        r'\d{10}'
    ]
}

def search_leaks(eml_file_path, filters):
    leaks = {}
    with open(eml_file_path, 'r', encoding='utf-8') as eml_file:
        eml_message = email.message_from_file(eml_file)
        
        for category, category_filters in filters.items():
            category_leaks = []
            for part in eml_message.walk():
                if part.get_content_type() == 'text/plain':
                    text = part.get_payload(decode=True).decode('utf-8')
                    for filter_pattern in category_filters:
                        if re.findall(filter_pattern, text):
                            category_leaks.append(category)
                            break  # Останавливаемся при первом совпадении
                    if category_leaks:
                        break  # Останавливаемся при первом совпадении
            
            for part in eml_message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                filename = part.get_filename()
                if filename:
                    for filter_pattern in category_filters:
                        if re.search(filter_pattern, filename):
                            category_leaks.append(category)
                            break  # Останавливаемся при первом совпадении
                    if category_leaks:
                        break  # Останавливаемся при первом совпадении
            
            if category_leaks:
                leaks[category] = category_leaks
    
    return leaks

def save_leaks_to_file(leaks, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        for category, category_leaks in leaks.items():
            f.write(f"Утечки в категории '{category}':\n")
            for leak in category_leaks:
                f.write(f"- {leak}\n")
            f.write('\n')

def main(eml_folder_path, filters):
    total_leaks_count = {category: 0 for category in filters.keys()}  # Инициализация счетчиков утечек для каждой категории
    total_leaks = 0  # Инициализация общего счетчика утечек
    emails_with_leaks = 0  # Инициализация счетчика писем с утечками данных

    for filename in os.listdir(eml_folder_path):
        if filename.endswith('.eml'):
            eml_file_path = os.path.join(eml_folder_path, filename)
            leaks = search_leaks(eml_file_path, filters)
            if leaks:
                emails_with_leaks += 1
                save_leaks_to_file(leaks, "leaks.txt")
            for category, category_leaks in leaks.items():
                if category_leaks:
                    print(f"Утечки в файле {filename}, категория {', '.join(category_leaks)}")
                    total_leaks_count[category] += len(category_leaks)  # Увеличиваем счетчик утечек для данной категории
                    total_leaks += len(category_leaks)  # Увеличиваем общий счетчик утечек

    print("\nОбщее количество утечек для каждой категории:")
    for category, count in total_leaks_count.items():
        print(f"{category}: {count}")

    print(f"\nОбщее количество утечек: {total_leaks}")
    print(f"Количество писем с утечками данных: {emails_with_leaks}")

if __name__ == "__main__":
    main(eml_folder_path, filters)
