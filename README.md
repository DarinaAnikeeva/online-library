# Парсер книг с сайта tululu.org

Проект позволяет скачивать обложки и текст книг с сайта http://tululu.org. Число книг задаёт пользователь, об этом позже

## Как установить
- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Запустите файл `main.py` с указанием с какого номера по какой вывести информацию о книгах в консоль: `python main.py 5 20`. Если книги с указанным номером нет в библиотеке ее не выведет в консоль.

`Python` уже должен быть установлен на устройство

Пример выполнение программы:

```
5 Название: Бал хищников. Автор: Брук Конни.
['Биографии и мемуары', 'О бизнесе популярно']
Комментарии:
Книга просто супер, прочитав ее я много чего узнала о бизнесе!
МНЕ КНИГА ОЧЕНЬ ПОМОГЛА.
Super kniga.
```

Далее необходимо выбрать понравившуюся книгу для скачивания
```
Введите номера через запятую: 5, 6
```

#Цели проекта
Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте Devman.