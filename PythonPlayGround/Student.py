# 題目 B：學生(Student) 成績系統
# 寫一個 Student 類別，包含：
# 屬性：
# name（學生姓名）
# grades（一個 list，代表多個考試分數）
# 方法：
# add_grade(score)：把新的分數加入 grades list。
# average()：回傳平均分數。
# print_grades()：印出所有分數。
# 進階加分：
# 如果分數輸入不在 0 到 100 之間，就拒絕加入（並印錯誤訊息）。
# 新增 method highest() 跟 lowest()，分別回傳最高分和最低分。

class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, score):
        if 0 <= score <= 100:
            self.grades.append(score)
        else:
            print("Error: Score must be between 0 and 100.")

    def average(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def print_grades(self):
        print(f"Grades for {self.name}: {self.grades}")

    def highest(self):
        if not self.grades:
            return None
        return max(self.grades)

    def lowest(self):
        if not self.grades:
            return None
        return min(self.grades)