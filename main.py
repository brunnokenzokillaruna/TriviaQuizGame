#main.py
import tkinter as tk
from ui_components import MainMenu, CategorySelection, QuestionDisplay
from game_logic import GameLogic

class TriviaGameApp:
    def __init__(self, root):
        self.root = root
        self.game_logic = GameLogic()
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_frame()
        MainMenu(self.root, self.start_categories_selection, self.quit_game).pack(expand=True, fill='both')

    def start_categories_selection(self):
        self.clear_frame()
        categories = list(self.game_logic.questions.keys())
        CategorySelection(self.root, categories, self.start_game).pack(expand=True, fill='both')

    def start_game(self, selected_categories):
        self.game_logic.start_game(selected_categories)
        self.display_question()

    def display_question(self):
        question_data = self.game_logic.next_question()
        if question_data:
            self.clear_frame()
            score_info = {
                'correct': self.game_logic.calculate_current_score(),
                'walk_away': self.game_logic.calculate_walk_away_value(),
                'miss': self.game_logic.calculate_miss_value(),
                'amount_lost': self.game_logic.calculate_amount_lost_for_wrong_answer()
            }
            self.current_display = QuestionDisplay(
                self.root, question_data, self.submit_answer, self.walk_away,
                self.game_logic.question_number, score_info, self.time_up
            )
            self.current_display.pack(expand=True, fill='both')
        else:
            self.show_final_score()

    def time_up(self):
        self.game_logic.end_game()
        self.show_final_score()

    def submit_answer(self, answer):
        correct = self.game_logic.submit_answer(answer)
        if correct:
            if self.game_logic.question_number > 16:
                self.show_winner()
            else:
                score_info = {
                    'correct': self.game_logic.calculate_current_score(),
                    'walk_away': self.game_logic.calculate_walk_away_value(),
                    'miss': self.game_logic.calculate_miss_value(),
                    'amount_lost': self.game_logic.calculate_amount_lost_for_wrong_answer()
                }
                self.current_display.update_prize_info(score_info)
                self.display_question()
        else:
            self.show_final_score()

    def show_winner(self):
        self.clear_frame()
        final_frame = tk.Frame(self.root, bg='black')
        final_frame.pack(expand=True, fill='both')
        tk.Label(final_frame,
                 text=f"Congratulations! You are the winner and won: R${self.game_logic.calculate_final_score()}",
                 bg='black', fg='white', font=('Helvetica', 16)).pack(expand=True)
        tk.Button(final_frame, text="Restart", command=self.show_main_menu, bg='black', fg='white',
                  font=('Helvetica', 16)).pack()

    def show_final_score(self):
        self.clear_frame()
        final_frame = tk.Frame(self.root, bg='black')
        final_frame.pack(expand=True, fill='both')
        final_score = self.game_logic.calculate_final_score()
        tk.Label(final_frame, text=f"Game Over! Your score: ${final_score}", bg='black', fg='white', font=('Helvetica', 16)).pack(expand=True)
        tk.Button(final_frame, text="Restart", command=self.show_main_menu, bg='black', fg='white', font=('Helvetica', 16)).pack()

    def walk_away(self):
        self.game_logic.end_game()
        self.show_final_score()

    def quit_game(self):
        self.root.quit()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Trivia Quiz Game")
    root.geometry("800x600")

    app = TriviaGameApp(root)
    root.mainloop()