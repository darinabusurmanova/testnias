import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE_NAME = "movies.json"

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")

        self.movies = []

        # ---------- Поля ввода ----------
        tk.Label(root, text="Название").grid(row=0, column=0)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(root, text="Жанр").grid(row=1, column=0)
        self.genre_entry = tk.Entry(root)
        self.genre_entry.grid(row=1, column=1)

        tk.Label(root, text="Год выпуска").grid(row=2, column=0)
        self.year_entry = tk.Entry(root)
        self.year_entry.grid(row=2, column=1)

        tk.Label(root, text="Рейтинг").grid(row=3, column=0)
        self.rating_entry = tk.Entry(root)
        self.rating_entry.grid(row=3, column=1)

        # ---------- Кнопки ----------
        add_button = tk.Button(root, text="Добавить фильм", command=self.add_movie)
        add_button.grid(row=4, column=0, columnspan=2, pady=5)

        save_button = tk.Button(root, text="Сохранить JSON", command=self.save_movies)
        save_button.grid(row=5, column=0)

        load_button = tk.Button(root, text="Загрузить JSON", command=self.load_movies)
        load_button.grid(row=5, column=1)

        # ---------- Фильтры ----------
        tk.Label(root, text="Фильтр по жанру").grid(row=0, column=3)
        self.genre_filter = tk.Entry(root)
        self.genre_filter.grid(row=0, column=4)

        tk.Label(root, text="Фильтр по году").grid(row=1, column=3)
        self.year_filter = tk.Entry(root)
        self.year_filter.grid(row=1, column=4)

        filter_button = tk.Button(root, text="Применить фильтр", command=self.filter_movies)
        filter_button.grid(row=2, column=3, columnspan=2)

        show_all_button = tk.Button(root, text="Показать все", command=self.update_table)
        show_all_button.grid(row=3, column=3, columnspan=2)

        # ---------- Таблица ----------
        self.tree = ttk.Treeview(root, columns=("Title", "Genre", "Year", "Rating"), show="headings")

        self.tree.heading("Title", text="Название")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Year", text="Год")
        self.tree.heading("Rating", text="Рейтинг")

        self.tree.grid(row=6, column=0, columnspan=5, pady=10)

        self.load_movies()

    def add_movie(self):
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()
        rating = self.rating_entry.get()

        # Проверка года
        if not year.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return

        # Проверка рейтинга
        try:
            rating = float(rating)
            if rating < 0 or rating > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": int(year),
            "rating": rating
        }

        self.movies.append(movie)
        self.update_table()

        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def update_table(self, movies_list=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        if movies_list is None:
            movies_list = self.movies

        for movie in movies_list:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    movie["title"],
                    movie["genre"],
                    movie["year"],
                    movie["rating"]
                )
            )

    def filter_movies(self):
        genre = self.genre_filter.get().lower()
        year = self.year_filter.get()

        filtered = self.movies

        if genre
