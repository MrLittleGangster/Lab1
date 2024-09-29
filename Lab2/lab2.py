import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import pandas as pd
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Список учебной группы")
        
        self.students = pd.DataFrame(columns=["ID", "Фамилия", "Имя", "Дата рождения"])
        self.exams = pd.DataFrame(columns=["Студент ID", "Предмет", "Дата экзамена", "Преподаватель"])

        self.create_widgets()

    def create_widgets(self):
        self.add_student_button = tk.Button(self.root, text="Добавить студента", command=self.add_student)
        self.add_student_button.pack(pady=10)

        self.show_students_button = tk.Button(self.root, text="Показать студентов", command=self.show_students)
        self.show_students_button.pack(pady=10)

        self.save_data_button = tk.Button(self.root, text="Сохранить данные", command=self.save_data)
        self.save_data_button.pack(pady=10)

        self.student_tree = ttk.Treeview(self.root, columns=("Фамилия", "Имя", "Дата рождения"), show='headings')
        self.student_tree.heading("Фамилия", text="Фамилия")
        self.student_tree.heading("Имя", text="Имя")
        self.student_tree.heading("Дата рождения", text="Дата рождения")
        self.student_tree.pack(pady=10)

    def add_student(self):
        surname = simpledialog.askstring("Фамилия", "Введите фамилию:")
        name = simpledialog.askstring("Имя", "Введите имя:")
        birth_date_str = simpledialog.askstring("Дата рождения", "Введите дату рождения (ДД-ММ-ГГГГ):")
        
        # try:
        birth_date = birth_date_str#datetime.strptime(birth_date_str, "%d-%m-%Y")
        student_id = len(self.students) + 1
        new_student = {"ID": [student_id], "Фамилия": [surname], "Имя": [name], "Дата рождения": [birth_date]}
        self.students = pd.concat([self.students,pd.DataFrame.from_dict(new_student)],ignore_index=True)

        # Добавление экзаменов
        exam_count = simpledialog.askinteger("Количество экзаменов", "Введите количество экзаменов (от 3 до 5):")
        if exam_count < 3 or exam_count > 5:
            messagebox.showerror("Ошибка", "Количество экзаменов должно быть от 3 до 5.")
            return

        for _ in range(exam_count):
            exam_subject = simpledialog.askstring("Экзамен", "Введите предмет:")
            exam_date_str = simpledialog.askstring("Экзамен", "Введите дату экзамена (ДД-ММ-ГГГГ):")
            teacher_name = simpledialog.askstring("Экзамен", "Введите ФИО преподавателя:")

            exam_data = {
                "Студент ID": [student_id],
                "Предмет": [exam_subject],
                "Дата экзамена": [exam_date_str],
                "Преподаватель": [teacher_name]
            }
            
            
            self.exams = pd.concat([self.exams,pd.DataFrame.from_dict(exam_data)], ignore_index=True)

        messagebox.showinfo("Успех", "Студент и экзамены успешно добавлены.")
        # except ValueError:
        #     messagebox.showerror("Ошибка", "Неверный формат даты.")

    def show_students(self):
        self.students = pd.read_csv("data.csv")
        self.exams = pd.read_csv("exams.csv")
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        sorted_students = self.students.sort_values(by="Дата рождения")
        
        for _, row in sorted_students.iterrows():
            exams_for_student = self.exams[self.exams["Студент ID"] == row["ID"]]
            exams_info = "\n".join(str(exams_for_student["Предмет"][0]) + " (" + str(exams_for_student["Дата экзамена"][0]) + ", " + str(exams_for_student["Преподаватель"][0]) + ")")
            self.student_tree.insert("", "end", values=(row["Фамилия"], row["Имя"], row["Дата рождения"]))
            if not exams_for_student.empty:
                messagebox.showinfo("Экзамены студента", f"Экзамены для {row['Фамилия']} {row['Имя']}:\n{exams_info}")

    def save_data(self):
        self.students.to_csv("data.csv", index=False)
        self.exams.to_csv("exams.csv", index=False)
        messagebox.showinfo("Успех", "Данные успешно сохранены в файлы data.csv и exams.csv.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

