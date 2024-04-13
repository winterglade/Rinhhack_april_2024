import re       # модуль re, который предназначен исключительно для работы с регулярными выражениями. 
import email    # предназначен для работы с 
import os       # предназначен для работы с файлами системы.


eml_folder_path = "C:/Users/User/Desktop/hacaton/small" # путь к папке с файлами EML.
filters = [r'\d{10}', r'\d{16}', r'^\d{3}-\d{3}-\d{3} \d{2}$', r'[0-9]{13,16}', r'\b\d{3}-\d{3}-\d{3}\s\d{2}\b', r'\b\d{4}\s\d{6}\b', r"\b\d{4} № \d{6}\b", r"\b\d{4}-\d{6}\b", r"\b\d{4}№\d{6}\b", r"\b\d{4}№\d{6}\b", r"\b\d{4} N\d{6}\b", r"\b\d{4} №\d{6}\b", r"\b\d{4}\s\d{6}\b", r"\b\d{4} N\d{6}\b", r"\b\d{4}№\d{6}\b", r"\b\d{4}N\d{6}\b", r"\b\d{4} N \d{6}\b", r"\b\d{2}\s\d{2} N \d{6}\b", r"\b\d{2}\s\d{2} № \d{6}\b", r"\b\d{4} N \d{6}\b", r"\b\d{4} N \d{6}\b", r"\b\d{4}\s\d{6}\b", r"\b\d{4}\s\d{6}\b", r"\b\d{4} N \d{6}\b"]  # регулярные выражения для поиска номеров паспортов и банковских карт

def search_leaks(eml_file_path, filters):     
    leaks = []  # список, который будет хранить утечки.
    with open(eml_file_path, 'r', encoding='utf-8') as eml_file:    # открытие файла.
        eml_message = email.message_from_file(eml_file)     # анализирует текстовое содержимое файла и создает объект сообщения на его основе.
        
        # проверяем текст письма на соответствие фильтрам:
        for part in eml_message.walk():
            if part.get_content_type() == 'text/plain':     # проверка типа сообщения.
                # позволяет получить текст сообщения из его тела, который можно дальше анализировать или обрабатывать.
                text = part.get_payload(decode=True).decode(part.get_content_charset())     # декодирует содержимое части сообщения в текстовую строку, используя соответствующую кодировку. 
                for filter_pattern in filters:
                    if re.findall(filter_pattern, text):
                        leaks.append(filter_pattern)
        
        # Проверяем вложения на соответствие фильтрам
        for part in eml_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            if filename:
                for filter_pattern in filters:
                    if re.search(filter_pattern, filename):
                        leaks.append(filter_pattern)
    return leaks

def main(eml_folder_path, filters):
    for filename in os.listdir(eml_folder_path):
        if filename.endswith('.eml'):
            eml_file_path = os.path.join(eml_folder_path, filename)
            leaks = search_leaks(eml_file_path, filters)
            if leaks:
                print(f"Утечки в файле {filename}: {', '.join(leaks)}")

def main(eml_folder_path, filters):     # считает количество утечек.
    leaked_files_count = 0  # счетчик утечек файлов.
    
    for filename in os.listdir(eml_folder_path):
        if filename.endswith('.eml'):
            eml_file_path = os.path.join(eml_folder_path, filename)
            leaks = search_leaks(eml_file_path, filters)
            if leaks:
                print(f"Утечки в файле {filename}: {', '.join(leaks)}")
                leaked_files_count += 1
    
    print(f"Всего утечек в {leaked_files_count} файл(ах).")

if __name__ == "__main__":
    main(eml_folder_path, filters)