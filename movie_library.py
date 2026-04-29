import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class MovieLibrary:
    """Главный класс приложения для управления личной кинотекой"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # АВТОР: ДАНИИЛ ИЛЬИН
        self.author = "Даниил Ильин"
        
        # Файл для хранения данных
        self.data_file = "movies.json"
        
        # Загружаем данные
        self.movies = self.load_movies()
        
        # Создаем интерфейс
        self.create_widgets()
        
        # Обновляем таблицу
        self.refresh_table()
        
        # Настройка обработки закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка веса колонок
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Заголовок с именем автора
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="🎬 Movie Library", font=('Arial', 18, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # ОТОБРАЖЕНИЕ ИМЕНИ АВТОРА
        author_label = ttk.Label(title_frame, text=f"Разработчик: {self.author}", font=('Arial', 10))
        author_label.pack(side=tk.RIGHT)
        
        # ===== Панель ввода данных =====
        input_frame = ttk.LabelFrame(main_frame, text="➕ Добавление фильма", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        
        # Поле: Название
        ttk.Label(input_frame, text="Название фильма:*").grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(input_frame, textvariable=self.title_var, width=30)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 20))
        
        # Поле: Жанр
        ttk.Label(input_frame, text="Жанр:*").grid(row=0, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        self.genre_var = tk.StringVar()
        self.genre_combo = ttk.Combobox(input_frame, textvariable=self.genre_var, width=28)
        self.genre_combo['values'] = ('Драма', 'Комедия', 'Боевик', 'Триллер', 'Ужасы', 
                                       'Фантастика', 'Фэнтези', 'Мелодрама', 'Детектив', 
                                       'Приключения', 'Анимация', 'Документальный')
        self.genre_combo.grid(row=0, column=3, sticky=(tk.W, tk.E), pady=5)
        
        # Поле: Год выпуска
        ttk.Label(input_frame, text="Год выпуска:*").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.year_var = tk.StringVar()
        self.year_entry = ttk.Entry(input_frame, textvariable=self.year_var, width=30)
        self.year_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 20))
        
        # Поле: Рейтинг
        ttk.Label(input_frame, text="Рейтинг (0-10):*").grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        self.rating_var = tk.StringVar()
        self.rating_entry = ttk.Entry(input_frame, textvariable=self.rating_var, width=30)
        self.rating_entry.grid(row=1, column=3, sticky=(tk.W, tk.E), pady=5)
        
        # Кнопка добавления
        self.add_btn = ttk.Button(input_frame, text="🎬 Добавить фильм", command=self.add_movie)
        self.add_btn.grid(row=2, column=0, columnspan=4, pady=10)
        
        # ===== Панель фильтрации =====
        filter_frame = ttk.LabelFrame(main_frame, text="🔍 Фильтрация фильмов", padding="10")
        filter_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        filter_frame.columnconfigure(1, weight=1)
        filter_frame.columnconfigure(3, weight=1)
        
        # Фильтр по жанру
        ttk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, padx=(0, 10), pady=5)
        self.filter_genre_var = tk.StringVar(value="Все жанры")
        self.filter_genre_combo = ttk.Combobox(filter_frame, textvariable=self.filter_genre_var, width=25)
        self.filter_genre_combo['values'] = ['Все жанры'] + list(self.genre_combo['values'])
        self.filter_genre_combo.grid(row=0, column=1, padx=(0, 20), pady=5)
        self.filter_genre_combo.bind('<<ComboboxSelected>>', self.apply_filters)
        
        # Фильтр по году выпуска (диапазон)
        ttk.Label(filter_frame, text="Год выпуска от:").grid(row=0, column=2, padx=(0, 10), pady=5)
        self.year_from_var = tk.StringVar()
        self.year_from_entry = ttk.Entry(filter_frame, textvariable=self.year_from_var, width=10)
        self.year_from_entry.grid(row=0, column=3, padx=(0, 10), pady=5)
        
        ttk.Label(filter_frame, text="до:").grid(row=0, column=4, padx=(0, 10), pady=5)
        self.year_to_var = tk.StringVar()
        self.year_to_entry = ttk.Entry(filter_frame, textvariable=self.year_to_var, width=10)
        self.year_to_entry.grid(row=0, column=5, padx=(0, 10), pady=5)
        
        # Кнопки фильтрации
        self.apply_btn = ttk.Button(filter_frame, text="🔍 Применить фильтр", command=self.apply_filters)
        self.apply_btn.grid(row=0, column=6, padx=(10, 0), pady=5)
        
        self.reset_btn = ttk.Button(filter_frame, text="🗑️ Сбросить фильтр", command=self.reset_filters)
        self.reset_btn.grid(row=0, column=7, padx=(10, 0), pady=5)
        
        # ===== Таблица с фильмами =====
        table_frame = ttk.LabelFrame(main_frame, text="📽️ Список фильмов", padding="10")
        table_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Создание таблицы
        columns = ('ID', 'Название', 'Жанр', 'Год', 'Рейтинг', 'Дата добавления')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Настройка колонок
        self.tree.heading('ID', text='ID')
        self.tree.heading('Название', text='Название фильма')
        self.tree.heading('Жанр', text='Жанр')
        self.tree.heading('Год', text='Год выпуска')
        self.tree.heading('Рейтинг', text='Рейтинг')
        self.tree.heading('Дата добавления', text='Дата добавления')
        
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Название', width=280)
        self.tree.column('Жанр', width=130)
        self.tree.column('Год', width=100, anchor='center')
        self.tree.column('Рейтинг', width=80, anchor='center')
        self.tree.column('Дата добавления', width=150, anchor='center')
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Кнопки управления
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        self.delete_btn = ttk.Button(btn_frame, text="❌ Удалить выбранный фильм", command=self.delete_movie)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        self.edit_btn = ttk.Button(btn_frame, text="✏️ Редактировать фильм", command=self.edit_movie)
        self.edit_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(btn_frame, text="🗑️ Очистить всю коллекцию", command=self.clear_all_movies)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.stats_btn = ttk.Button(btn_frame, text="📊 Статистика", command=self.show_stats)
        self.stats_btn.pack(side=tk.LEFT, padx=5)
        
        # Статусная строка
        self.status_var = tk.StringVar(value="✅ Готово. Все изменения автоматически сохраняются.")
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
    
    def validate_movie(self, title, genre, year, rating):
        """Валидация введенных данных"""
        
        if not title or not title.strip():
            return False, "❌ Ошибка: Название фильма не может быть пустым!"
        
        if len(title.strip()) > 200:
            return False, "❌ Ошибка: Название не может превышать 200 символов!"
        
        if not genre:
            return False, "❌ Ошибка: Выберите жанр фильма!"
        
        if not year:
            return False, "❌ Ошибка: Введите год выпуска!"
        
        try:
            year_int = int(year)
            current_year = datetime.now().year
            if year_int < 1888:
                return False, f"❌ Ошибка: Год должен быть не меньше 1888! (вы ввели {year_int})"
            if year_int > current_year:
                return False, f"❌ Ошибка: Год не может быть больше текущего ({current_year})! (вы ввели {year_int})"
        except ValueError:
            return False, "❌ Ошибка: Год должен быть целым числом! (например: 1994)"
        
        if not rating:
            return False, "❌ Ошибка: Введите рейтинг!"
        
        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 10:
                return False, f"❌ Ошибка: Рейтинг должен быть в диапазоне от 0 до 10! (вы ввели {rating_float})"
        except ValueError:
            return False, "❌ Ошибка: Рейтинг должен быть числом! (например: 8.5)"
        
        return True, ""
    
    def add_movie(self):
        """Добавление нового фильма"""
        title = self.title_var.get().strip()
        genre = self.genre_var.get()
        year = self.year_var.get().strip()
        rating = self.rating_var.get().strip()
        
        is_valid, error_msg = self.validate_movie(title, genre, year, rating)
        
        if not is_valid:
            messagebox.showerror("Ошибка ввода", error_msg)
            return
        
        movie_id = max([m['id'] for m in self.movies], default=0) + 1
        
        movie = {
            'id': movie_id,
            'title': title,
            'genre': genre,
            'year': int(year),
            'rating': float(rating),
            'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.movies.append(movie)
        self.save_movies()
        self.refresh_table()
        
        self.title_var.set("")
        self.genre_var.set("")
        self.year_var.set("")
        self.rating_var.set("")
        
        self.status_var.set(f"✅ Фильм '{title}' успешно добавлен! Всего фильмов: {len(self.movies)}")
        self.title_entry.focus()
    
    def delete_movie(self):
        """Удаление выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите фильм для удаления!")
            return
        
        item = self.tree.item(selected[0])
        movie_id = item['values'][0]
        movie_title = item['values'][1]
        
        if messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить фильм:\n'{movie_title}'?"):
            self.movies = [m for m in self.movies if m['id'] != movie_id]
            self.save_movies()
            self.refresh_table()
            self.status_var.set(f"🗑️ Фильм '{movie_title}' успешно удален! Осталось фильмов: {len(self.movies)}")
    
    def edit_movie(self):
        """Редактирование выбранного фильма"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите фильм для редактирования!")
            return
        
        item = self.tree.item(selected[0])
        movie_id = item['values'][0]
        movie_to_edit = next((m for m in self.movies if m['id'] == movie_id), None)
        
        if movie_to_edit:
            self.title_var.set(movie_to_edit['title'])
            self.genre_var.set(movie_to_edit['genre'])
            self.year_var.set(str(movie_to_edit['year']))
            self.rating_var.set(str(movie_to_edit['rating']))
            self.movies = [m for m in self.movies if m['id'] != movie_id]
            self.status_var.set(f"✏️ Редактирование фильма '{movie_to_edit['title']}'")
    
    def clear_all_movies(self):
        """Очистка всех фильмов"""
        if not self.movies:
            messagebox.showinfo("Информация", "Кинотека уже пуста!")
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить ВСЕ фильмы?\nЭто действие нельзя отменить!"):
            self.movies = []
            self.save_movies()
            self.refresh_table()
            self.reset_filters()
            self.status_var.set("🗑️ Все фильмы удалены. Кинотека пуста.")
    
    def load_movies(self):
        """Загрузка фильмов из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    return []
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_movies(self):
        """Сохранение фильмов в JSON файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные: {e}")
            return False
    
    def validate_year_filter(self, year_str, field_name):
        """Валидация значений фильтра по году"""
        if not year_str:
            return True, None, ""
        
        try:
            year_int = int(year_str)
            current_year = datetime.now().year
            if year_int < 1888:
                return False, None, f"{field_name}: год не может быть меньше 1888!"
            if year_int > current_year:
                return False, None, f"{field_name}: год не может быть больше {current_year}!"
            return True, year_int, ""
        except ValueError:
            return False, None, f"{field_name}: введите целое число (например: 2000)"
    
    def apply_filters(self, event=None):
        """Применение фильтров к таблице"""
        year_from_str = self.year_from_var.get().strip()
        year_to_str = self.year_to_var.get().strip()
        
        errors = []
        
        is_valid_from, year_from, error_from = self.validate_year_filter(year_from_str, "Год (от)")
        if not is_valid_from:
            errors.append(error_from)
        
        is_valid_to, year_to, error_to = self.validate_year_filter(year_to_str, "Год (до)")
        if not is_valid_to:
            errors.append(error_to)
        
        if is_valid_from and is_valid_to and year_from is not None and year_to is not None:
            if year_from > year_to:
                errors.append("Ошибка: Год «от» не может быть больше года «до»!")
        
        if errors:
            messagebox.showerror("Ошибка в фильтре", "\n".join(errors))
            return
        
        self.refresh_table(filtered=True)
    
    def reset_filters(self):
        """Сброс всех фильтров"""
        self.filter_genre_var.set("Все жанры")
        self.year_from_var.set("")
        self.year_to_var.set("")
        self.refresh_table()
        self.status_var.set("🔄 Фильтры сброшены. Показаны все фильмы.")
    
    def refresh_table(self, filtered=False):
        """Обновление таблицы с учетом фильтров"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        movies_to_show = self.movies.copy()
        
        if filtered:
            selected_genre = self.filter_genre_var.get()
            if selected_genre != "Все жанры":
                movies_to_show = [m for m in movies_to_show if m['genre'] == selected_genre]
            
            year_from_str = self.year_from_var.get().strip()
            year_to_str = self.year_to_var.get().strip()
            
            if year_from_str:
                try:
                    year_from_int = int(year_from_str)
                    movies_to_show = [m for m in movies_to_show if m['year'] >= year_from_int]
                except ValueError:
                    pass
            
            if year_to_str:
                try:
                    year_to_int = int(year_to_str)
                    movies_to_show = [m for m in movies_to_show if m['year'] <= year_to_int]
                except ValueError:
                    pass
        
        movies_to_show.sort(key=lambda x: x['id'])
        
        for movie in movies_to_show:
            rating_display = f"{movie['rating']:.1f}"
            self.tree.insert('', tk.END, values=(
                movie['id'],
                movie['title'],
                movie['genre'],
                movie['year'],
                rating_display,
                movie.get('date_added', '')
            ))
        
        filter_status = " (с фильтрацией)" if filtered else ""
        self.status_var.set(f"📊 Показано фильмов: {len(movies_to_show)} из {len(self.movies)}{filter_status}")
    
    def show_stats(self):
        """Показ статистики по фильмам"""
        if not self.movies:
            messagebox.showinfo("Статистика", "В вашей кинотеке пока нет фильмов.\nДобавьте первый фильм!")
            return
        
        total_movies = len(self.movies)
        total_rating = sum(m['rating'] for m in self.movies)
        avg_rating = total_rating / total_movies if total_movies > 0 else 0
        
        genres_count = {}
        for movie in self.movies:
            genre = movie['genre']
            genres_count[genre] = genres_count.get(genre, 0) + 1
        
        most_common_genre = max(genres_count, key=genres_count.get) if genres_count else "Нет"
        
        highest_rated = max(self.movies, key=lambda x: x['rating']) if self.movies else None
        oldest_movie = min(self.movies, key=lambda x: x['year']) if self.movies else None
        newest_movie = max(self.movies, key=lambda x: x['year']) if self.movies else None
        
        stats_text = f"""
📊 СТАТИСТИКА ВАШЕЙ КИНОТЕКИ

🎬 Всего фильмов: {total_movies}
⭐ Средний рейтинг: {avg_rating:.1f}/10

🏆 Самый популярный жанр: {most_common_genre} ({genres_count.get(most_common_genre, 0)} фильмов)

🌟 Самый высокий рейтинг: {highest_rated['title'] if highest_rated else 'Нет'} ({highest_rated['rating'] if highest_rated else 0}/10)

📅 Самый старый фильм: {oldest_movie['title'] if oldest_movie else 'Нет'} ({oldest_movie['year'] if oldest_movie else 0} год)
📅 Самый новый фильм: {newest_movie['title'] if newest_movie else 'Нет'} ({newest_movie['year'] if newest_movie else 0} год)

📊 Распределение по жанрам:
"""
        for genre, count in sorted(genres_count.items(), key=lambda x: x[1], reverse=True):
            stats_text += f"   • {genre}: {count} фильмов\n"
        
        messagebox.showinfo("Статистика кинотеки", stats_text)
    
    def on_closing(self):
        """Обработка закрытия окна"""
        self.save_movies()
        self.root.destroy()


def main():
    """Точка входа в приложение"""
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()


if __name__ == "__main__":
    main()