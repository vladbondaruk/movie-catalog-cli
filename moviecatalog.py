import json
import os

DATA_FILE = "movies.json"

def load_movies():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, PermissionError):
        print("\n[Помилка] Не вдалося зчитувати файл даних. Створено новий список.")
        return []

def save_movies(movies):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(movies, file, ensure_ascii=False, indent=4)
    except IOError:
        print("\n[Помилка] Не вдалося зберегти дані у файл!")

def get_input_string(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("[Помилка] Поле не може бути порожнім. Спробуйте ще раз.")

def get_input_int(prompt, min_val, max_val):
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"[Помилка] Число має бути в діапазоні від {min_val} до {max_val}.")
        except ValueError:
            print("[Помилка] Будь ласка, введіть коректне ціле число.")

def add_movie(movies):
    print("\n--- ДОДАВАННЯ НОВОГО ФІЛЬМУ ---")
    title = get_input_string("Введіть назву фільму: ")
    genre = get_input_string("Введіть жанр фільму: ")
    year = get_input_int("Введіть рік випуску (1895-2026): ", 1895, 2026)
    
    print("Оберіть статус перегляду:")
    print("1. Планую переглянути")
    print("2. Переглянуто")
    status_choice = get_input_int("Ваш вибір (1-2): ", 1, 2)
    status = "Переглянуто" if status_choice == 2 else "Планую переглянути"
    
    rating = None
    if status == "Переглянуто":
        print("Бажаєте залишити оцінку зараз?")
        print("1. Так\n2. Ні")
        rate_now = get_input_int("Ваш вибір (1-2): ", 1, 2)
        if rate_now == 1:
            rating = get_input_int("Введіть оцінку (1-10): ", 1, 10)

    movie = {
        "title": title,
        "genre": genre,
        "year": year,
        "status": status,
        "rating": rating
    }
    movies.append(movie)
    save_movies(movies)
    print(f"\n[Успіх] Фільм '{title}' успішно додано до каталогу!")

def view_movies(movies, filtered_list=None):
    list_to_show = filtered_list if filtered_list is not None else movies
    if not list_to_show:
        print("\nКаталог порожній або фільмів за такими критеріями не знайдено.")
        return False

    print("\n" + "="*85)
    print(f"{'№':<4} | {'Назва фільму':<25} | {'Жанр':<15} | {'Рік':<6} | {'Статус':<18} | {'Оцінка':<6}")
    print("="*85)
    for idx, movie in enumerate(list_to_show, start=1):
        rating_str = str(movie['rating']) if movie['rating'] is not None else "-"
        print(f"{idx:<4} | {movie['title']:<25} | {movie['genre']:<15} | {movie['year']:<6} | {movie['status']:<18} | {rating_str:<6}")
    print("="*85)
    return True

def filter_movies(movies):
    if not movies:
        print("\nКаталог порожній. Немає чого фільтрувати.")
        return
    print("\n--- ФІЛЬТРАЦІЯ ФІЛЬМІВ ---")
    print("1. Фільтрувати за жанром")
    print("2. Фільтрувати за статусом перегляду")
    choice = get_input_int("Оберіть варіант (1-2): ", 1, 2)

    if choice == 1:
        search_genre = get_input_string("Введіть жанр для пошуку: ").lower()
        filtered = [m for m in movies if search_genre in m['genre'].lower()]
        print(f"\nРезультати фільтрації за жанром '{search_genre}':")
        view_movies(movies, filtered)
    elif choice == 2:
        print("Оберіть статус:")
        print("1. Планую переглянути")
        print("2. Переглянуто")
        status_choice = get_input_int("Ваш вибір (1-2): ", 1, 2)
        search_status = "Переглянуто" if status_choice == 2 else "Планую переглянути"
        filtered = [m for m in movies if m['status'] == search_status]
        print(f"\nРезультати фільтрації за статусом '{search_status}':")
        view_movies(movies, filtered)

def rate_movie(movies):
    print("\n--- ОЦІНЮВАННЯ ФІЛЬМУ ---")
    if not view_movies(movies):
        return
    movie_idx = get_input_int("Введіть номер фільму, який хочете оцінити: ", 1, len(movies)) - 1
    selected_movie = movies[movie_idx]
    new_rating = get_input_int(f"Введіть оцінку для фільму '{selected_movie['title']}' (1-10): ", 1, 10)
    selected_movie['rating'] = new_rating
    if selected_movie['status'] == "Планую переглянути":
        selected_movie['status'] = "Переглянуто"
    save_movies(movies)
    print(f"\n[Успіх] Фільму '{selected_movie['title']}' виставлено оцінку {new_rating}!")

def delete_movie(movies):
    print("\n--- ВИДАЛЕННЯ ФІЛЬМУ ---")
    if not view_movies(movies):
        return
    movie_idx = get_input_int("Введіть номер фільму, який хочете видалити: ", 1, len(movies)) - 1
    removed_movie = movies.pop(movie_idx)
    save_movies(movies)
    print(f"\n[Успіх] Фільм '{removed_movie['title']}' видалено з каталогу.")

def main():
    movies = load_movies()
    while True:
        print("\n=== ГОЛОВНЕ МЕНЮ КАТАЛОГУ ФІЛЬМІВ ===")
        print("1. Переглянути весь каталог")
        print("2. Додати новий фільм")
        print("3. Фільтрувати фільми за критерієм")
        print("4. Виставити/змінити оцінку фільму")
        print("5. Видалити фільм із каталогу")
        print("6. Вихід")
        choice = get_input_int("Оберіть дію (1-6): ", 1, 6)
        if choice == 1:
            print("\n--- ВЕСЬ КАТАЛОГ ФІЛЬМІВ ---")
            view_movies(movies)
        elif choice == 2:
            add_movie(movies)
        elif choice == 3:
            filter_movies(movies)
        elif choice == 4:
            rate_movie(movies)
        elif choice == 5:
            delete_movie(movies)
        elif choice == 6:
            print("\nДані збережено. До побачення!")
            break

if __name__ == "__main__":
    main()