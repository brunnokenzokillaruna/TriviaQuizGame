# game_logic.py
from data_manager import load_all_questions
import random

class GameLogic:
    def __init__(self):
        self.questions = load_all_questions()
        self.selected_categories = []
        self.all_questions_pool = []
        self.current_question = None
        self.score = 0
        self.question_number = 0
        self.prize_money = [
            1000, 2000, 3000, 4000, 5000, 10000, 20000, 30000, 40000,
            50000, 100000, 200000, 300000, 400000, 500000, 1000000
        ]
        self.walk_away_money = [
            0, 1000, 2000, 3000, 4000, 5000, 10000, 20000, 30000, 40000,
            50000, 100000, 200000, 300000, 400000, 500000
        ]
        self.miss_answer_money = [
            0, 0, 0, 0, 0, 0, 10000, 10000, 10000,
            10000, 10000, 0, 100000, 100000, 100000, 100000
        ]
        self.amount_lost_wrong_answer = [
            0, 1000, 2000, 3000, 4000, 5000, 0, 10000, 20000, 30000, 40000,
            0, 100000, 200000, 300000, 400000
        ]

    def start_game(self, selected_categories):
        self.selected_categories = selected_categories
        self.score = 0
        self.question_number = 0
        self.all_questions_pool.clear()
        for category in selected_categories:
            self.all_questions_pool.extend(self.questions[category])
        random.shuffle(self.all_questions_pool)

    def load_category_questions(self):
        category = self.selected_categories[self.current_category_index]
        self.current_questions = self.questions[category]
        random.shuffle(self.current_questions)
        self.current_question_index = 0

    def next_question(self):
        if self.all_questions_pool:
            self.question_number += 1
            self.current_question = self.all_questions_pool.pop(0)
            return self.current_question
        else:
            return None

    def submit_answer(self, answer):
        if self.current_question:
            correct_answer = self.current_question["answer"]
            if answer == correct_answer:
                self.score = self.prize_money[min(self.question_number - 1, len(self.prize_money) - 1)]
                return True
            else:
                miss_value = self.calculate_miss_value()
                self.score = max(0, self.score - miss_value)
                self.end_game()
                return False
        return False

    def calculate_current_score(self):
        index = min(max(self.question_number - 1, 0), len(self.prize_money) - 1)
        return self.prize_money[index]

    def calculate_walk_away_value(self):
        return self.walk_away_money[max(self.question_number - 1, 0)]

    def calculate_miss_value(self):
        return self.miss_answer_money[max(self.question_number - 1, 0)]

    def end_game(self):
        self.question_number = 0

    def calculate_amount_lost_for_wrong_answer(self):
        index = max(0, self.question_number - 1)
        if index < len(self.amount_lost_wrong_answer):
            return self.amount_lost_wrong_answer[index]
        else:
            return 0

    def calculate_final_score(self):
        return max(0, self.score)