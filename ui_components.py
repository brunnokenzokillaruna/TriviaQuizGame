#ui_components.py
import tkinter as tk

class MainMenu(tk.Frame):
    def __init__(self, parent, start_callback, quit_callback):
        super().__init__(parent, bg='black')
        self.pack(expand=True, fill='both')
        title = tk.Label(self, text="Trivia Game", fg="white", bg="black", font=('Helvetica', 24))
        title.pack(pady=(20, 10))
        start_button = tk.Button(self, text="Start", command=start_callback, fg='white', bg='black', font=('Helvetica', 16))
        start_button.pack(pady=10)
        quit_button = tk.Button(self, text="Quit", command=quit_callback, fg='white', bg='black', font=('Helvetica', 16))
        quit_button.pack(pady=10)

class CategorySelection(tk.Frame):
    def __init__(self, parent, categories, start_game_callback):
        super().__init__(parent, bg='black')
        self.pack(expand=True, fill='both')
        self.vars = []
        for category in categories:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=category, variable=var, selectcolor='black', fg='white', bg='black', activebackground='black', activeforeground='white', font=('Helvetica', 14))
            chk.pack(anchor='w', padx=20, pady=5)
            self.vars.append((var, category))
        start_game_button = tk.Button(self, text="Start Game", command=lambda: start_game_callback([category for var, category in self.vars if var.get()]), fg='white', bg='black', font=('Helvetica', 16))
        start_game_button.pack(pady=20)

class QuestionDisplay(tk.Frame):
    def __init__(self, parent, question_data, submit_callback, walk_away_callback, current_question_number, score_info, time_up_callback):
        super().__init__(parent, bg='black')
        self.pack(expand=True, fill='both')
        self.question_data = question_data
        self.submit_callback = submit_callback
        self.walk_away_callback = walk_away_callback
        self.time_up_callback = time_up_callback
        self.selected_answer = tk.StringVar(value="")

        self.selected_answer = tk.StringVar(value="none")

        question_number_label = tk.Label(self, text=f"Question {current_question_number}", fg='white', bg='black', font=('Helvetica', 18))
        question_number_label.pack(pady=(10, 0))
        question_label = tk.Label(self, text=question_data["question"], fg='white', bg='black', font=('Helvetica', 18))
        question_label.pack(pady=(0, 10))

        for option in question_data["options"]:
            option_button = tk.Radiobutton(self, text=option, variable=self.selected_answer, value=option, fg='white', bg='black', selectcolor='black', activebackground='black', activeforeground='white', font=('Helvetica', 14))
            option_button.pack(anchor='w', padx=20, pady=2)

        submit_button = tk.Button(self, text="Submit", command=lambda: submit_callback(self.selected_answer.get()), fg='white', bg='black', font=('Helvetica', 16))
        submit_button.pack(side=tk.LEFT, padx=20, pady=20)
        walk_away_button = tk.Button(self, text="Walk Away", command=walk_away_callback, fg='white', bg='black', font=('Helvetica', 16))
        walk_away_button.pack(side=tk.RIGHT, padx=20, pady=20)

        self.update_prize_info(score_info)

        self.timer_label = tk.Label(self, fg='green', bg='black', font=('Helvetica', 20))
        self.timer_label.pack(pady=5)
        self.countdown(60)

    def update_prize_info(self, score_info):
        self.correct_answer_label = tk.Label(self, text=f"Correct Answer Value: ${score_info['correct']}", fg='white', bg='black', font=('Helvetica', 14))
        self.correct_answer_label.pack(pady=5, padx=10)
        self.walk_away_label = tk.Label(self, text=f"Walk Away Value: ${score_info['walk_away']}", fg='white', bg='black', font=('Helvetica', 14))
        self.walk_away_label.pack(pady=5, padx=10)
        self.miss_answer_label = tk.Label(self, text=f"Miss Answer Value: ${score_info['miss']}", fg='white', bg='black', font=('Helvetica', 14))
        self.miss_answer_label.pack(pady=5, padx=10)
        self.amount_lost_label = tk.Label(self, text=f"Amount Lost for Wrong Answer: ${score_info['amount_lost']}", fg='white', bg='black', font=('Helvetica', 14))
        self.amount_lost_label.pack(pady=5, padx=10)

    def countdown(self, count):
        self.timer_label.config(text=str(count), fg='green' if count > 30 else 'yellow' if count > 15 else 'red')
        if count > 0:
            self.after(1000, lambda: self.countdown(count - 1))
        else:
            self.time_up_callback()