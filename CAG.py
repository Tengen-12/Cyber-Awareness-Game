import time
import random
import sys
import os
import tkinter as tk
from tkinter import ttk  # Use ttk for better styling
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk  # Add PIL for image support

class CyberSecurityGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cyber Security Awareness Training")
        self.root.geometry("800x600")  # Set a fixed window size
        self.root.configure(bg="black")  # Set background color
        self.score = 0
        self.player_name = ""
        self.current_level = 1
        self.max_level = 5
        self.used_scenarios = []
        self.current_question_index = 0
        self.questions = []
        self.main_frame = tk.Frame(self.root, bg="black")
        self.main_frame.pack(padx=100, pady=80)

        # Add level selection dropdown
        self.level_var = tk.StringVar(value="Select Level")
        level_dropdown = ttk.Combobox(
            self.root,
            textvariable=self.level_var,
            values=[f"Level {i}" for i in range(1, self.max_level + 1)],
            state="readonly",
            width=15
        )
        level_dropdown.place(x=10, y=10)
        level_dropdown.bind("<<ComboboxSelected>>", self.select_level)

        self.display_header()

    def display_header(self):
        header = tk.Label(self.main_frame, text="Cyber Security Awareness Training", font=("Arial", 24, "bold"), bg="black", fg="white")
        header.pack(pady=50)

        # Simulate fade-in by delaying the appearance of the start button
        start_button = tk.Button(self.main_frame, text="Start Game", command=self.start_game, font=("Arial", 14), bg="#4CAF50", fg="white")
        self.root.after(500, lambda: start_button.pack(pady=80))  # Delay the appearance by 500ms

    def start_game(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.player_name = tk.simpledialog.askstring("Player Name", "Enter your name:")
        if not self.player_name:
            self.player_name = "Player"
        self.show_level()

    def select_level(self, event):
        selected_level = self.level_var.get()
        if (selected_level.startswith("Level")):
            self.current_level = int(selected_level.split()[1])
            self.show_level()

    def show_level(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Display the level name and completed levels
        level_label = tk.Label(
            self.main_frame,
            text=f"Level {self.current_level} of {self.max_level}",
            font=("Arial", 20, "bold"),
            bg="black",
            fg="white"
        )
        level_label.pack(pady=20)

        completed_label = tk.Label(
            self.main_frame,
            text=f"Completed Levels: {self.current_level - 1}",
            font=("Arial", 14),
            bg="black",
            fg="white"
        )
        completed_label.pack(pady=10)

        # Add a delay before loading questions
        self.root.after(2000, self.load_questions)

    def load_questions(self):
        if self.current_level == 1:
            self.questions = self.get_phishing_questions()
        elif self.current_level == 2:
            self.questions = self.get_password_questions()
        elif self.current_level == 3:
            self.questions = self.get_wifi_questions()
        elif self.current_level == 4:
            self.questions = self.get_ransomware_questions()
        elif self.current_level == 5:
            self.questions = self.get_social_engineering_questions()
        else:
            self.show_score()
            return

        self.current_question_index = 0
        self.show_question()

    def show_question(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if self.current_question_index >= len(self.questions):
            self.current_level += 1
            if self.current_level > self.max_level:
                self.show_score()
            else:
                self.show_level()
            return

        # Map levels to their categories
        level_categories = {
            1: "Phishing",
            2: "Password Security",
            3: "WiFi Security",
            4: "Ransomware",
            5: "Social Engineering"
        }
        category = level_categories.get(self.current_level, "Unknown")

        # Display level and category
        tk.Label(
            self.main_frame,
            text=f"LEVEL{self.current_level}: {category}",
            font=("Arial", 18, "bold"),
            bg="black",
            fg="white"
        ).pack(pady=10)

        # Display question number
        tk.Label(
            self.main_frame,
            text=f"Question {self.current_question_index + 1}",
            font=("Arial", 16),
            bg="black",
            fg="white"
        ).pack(pady=5)

        # Display the question and choices
        question, choices, correct_choice = self.questions[self.current_question_index]
        tk.Label(
            self.main_frame,
            text=question,
            justify="left",
            wraplength=400,
            bg="black",
            fg="white"
        ).pack(pady=10)

        for i, choice in enumerate(choices):
            button = tk.Button(
                self.main_frame,
                text=choice,
                command=lambda v=i: self.handle_answer(v, correct_choice),
                font=("Arial", 12),
                bg="#2196F3",
                fg="white"
            )
            button.pack(pady=5)

    def handle_answer(self, choice, correct_choice):
        if choice == correct_choice:
            messagebox.showinfo("Result", "✅ Correct!")
            self.score += 10
        else:
            messagebox.showwarning("Result", "❌ Incorrect!")
            self.score -= 5

        self.current_question_index += 1
        self.show_question()

    def get_phishing_questions(self):
        return [
            ("You receive an email asking for your password. What do you do?", ["Ignore it", "Reply with password", "Report to IT"], 2),
            ("An email claims you won a prize. What should you do?", ["Click the link", "Verify the sender", "Ignore it"], 1),
            ("What is a sign of a phishing email?", ["Grammatical errors", "Professional tone", "No links"], 0),
            ("You receive an email from an unknown sender. What do you do?", ["Open it", "Delete it", "Reply"], 1),
            ("A link in an email looks suspicious. What should you do?", ["Hover over it", "Click it", "Ignore it"], 0),
            ("What should you avoid in emails?", ["Sharing personal info", "Using polite language", "Replying quickly"], 0),
            ("You receive an email with an attachment. What do you do?", ["Open it", "Scan it", "Ignore it"], 1),
            ("How can you verify an email's authenticity?", ["Check the sender's address", "Reply to the email", "Ignore it"], 0),
            ("You get a text asking to renew your password via a link. What do you do?", ["Reply to confirm", "Call the vendor using a known number", "Click the link"], 1),
            ("An email says your account is locked and asks for your credentials. What do you do?", ["Provide credentials", "Ignore the email", "Verify with the official website"], 2),
            ("A pop-up claims your computer is infected and asks for payment. What do you do?", ["Pay immediately", "Close the pop-up", "Run antivirus software"], 2),
            ("You receive a message from your bank asking for your PIN. What do you do?", ["Provide the PIN", "Ignore the message", "Contact the bank directly"], 2),
            ("An email attachment claims to be an invoice but looks suspicious. What do you do?", ["Open it", "Delete it", "Scan it with antivirus"], 2),
            ("A website asks for your personal details to claim a prize. What do you do?", ["Provide details", "Ignore the website", "Verify the website's authenticity"], 2),
        ]

    def get_password_questions(self):
        return [
            ("Which password is most secure?", ["123456", "P@ssw0rd!", "qwerty"], 1),
            ("How often should you change your password?", ["Every month", "Every year", "Never"], 0),
            ("What should you avoid in passwords?", ["Personal info", "Special characters", "Numbers"], 0),
            ("What is a password manager?", ["A tool to store passwords", "A hacker tool", "A password generator"], 0),
            ("What is two-factor authentication?", ["A second password", "A security measure", "A backup password"], 1),
            ("What is a strong password length?", ["4 characters", "8 characters", "12+ characters"], 2),
            ("What should you do if your password is compromised?", ["Change it", "Ignore it", "Use it anyway"], 0),
            ("What is the best way to store passwords?", ["Write them down", "Use a password manager", "Memorize all"], 1),
            ("What is a sign of a weak password?", ["Contains special characters", "Is short and simple", "Is unique"], 1),
            ("Why is it important to use different passwords for different accounts?", ["To confuse hackers", "To prevent a single breach from affecting all accounts", "To make it easier to remember"], 1),
        ]

    def get_wifi_questions(self):
        return [
            ("Which network is safest to use?", ["Open WiFi", "WPA2-secured WiFi", "Personal hotspot"], 2),
            ("What is a VPN?", ["A secure network", "A public network", "A WiFi booster"], 0),
            ("How can you secure your home WiFi?", ["Use WPA2", "Use open WiFi", "Disable encryption"], 0),
            ("What is a WiFi password?", ["A security key", "A network name", "A router setting"], 0),
            ("What should you do if WiFi is slow?", ["Check for intruders", "Ignore it", "Restart the router"], 0),
            ("What is MAC address filtering?", ["A security feature", "A WiFi booster", "A network name"], 0),
            ("What is SSID?", ["WiFi name", "WiFi password", "WiFi speed"], 0),
            ("Why avoid public WiFi for sensitive tasks?", ["Lack of encryption", "Slow speed", "High cost"], 0),
            ("You connect to a public WiFi. What should you avoid?", ["Streaming videos", "Accessing sensitive accounts", "Browsing news"], 1),
            ("What is the safest way to use public WiFi?", ["Use a VPN", "Disable encryption", "Share the network"], 0),
            ("What should you do if you suspect someone is using your home WiFi?", ["Ignore it", "Change the password", "Turn off the router"], 1),
            ("What is the purpose of a WiFi encryption protocol?", ["To secure data", "To boost speed", "To reduce interference"], 0),
            ("How can you identify a secure WiFi network?", ["It requires a password", "It has a strong signal", "It is free"], 0),
            ("Why is it important to disable SSID broadcasting?", ["To hide your network from attackers", "To increase speed", "To reduce interference"], 0),
        ]

    def get_ransomware_questions(self):
        return [
            ("How can you prevent ransomware?", ["Backup data", "Install antivirus", "Both"], 2),
            ("What is ransomware?", ["A virus", "A scam", "Malware demanding payment"], 2),
            ("What should you do if infected by ransomware?", ["Disconnect from the network", "Pay the ransom", "Ignore it"], 0),
            ("What is a ransomware attack vector?", ["Phishing emails", "Strong passwords", "Encrypted files"], 0),
            ("What is a ransomware demand?", ["Payment for data", "A security update", "A password reset"], 0),
            ("What is a ransomware encryption key?", ["A decryption tool", "A virus", "A password"], 0),
            ("How can you detect ransomware?", ["Unusual file behavior", "Fast internet", "No symptoms"], 0),
            ("You receive a ransomware demand. What should you do?", ["Pay the ransom", "Report to authorities", "Ignore it"], 1),
            ("What is the first step to take after a ransomware attack?", ["Disconnect from the internet", "Pay the ransom", "Restart the computer"], 0),
            ("How can you reduce the risk of ransomware?", ["Avoid opening suspicious emails", "Disable antivirus", "Ignore updates"], 0),
            ("What is a ransomware decryption key?", ["A tool to unlock files", "A password", "A virus"], 0),
            ("What should you do if your backups are also encrypted by ransomware?", ["Contact a cybersecurity expert", "Pay the ransom", "Delete the backups"], 0),
            ("What is the purpose of ransomware?", ["To steal data", "To demand payment for encrypted files", "To slow down computers"], 1),
            ("How can you identify a ransomware infection?", ["Files are inaccessible", "Computer runs faster", "No symptoms"], 0),
            ("What is the best way to recover from a ransomware attack?", ["Restore from backups", "Pay the ransom", "Reinstall the OS"], 0),
        ]

    def get_social_engineering_questions(self):
        return [
            ("A caller asks for your password. What do you do?", ["Give it", "Verify identity", "Ignore"], 1),
            ("What is a common social engineering tactic?", ["Phishing", "Brute force", "Malware"], 0),
            ("What is social engineering?", ["Manipulation to gain info", "A hacking tool", "A security measure"], 0),
            ("How can you prevent social engineering?", ["Verify requests", "Ignore all calls", "Share info"], 0),
            ("What is pretexting?", ["Creating a fake scenario", "A hacking tool", "A password reset"], 0),
            ("What is baiting?", ["Offering something to gain info", "A phishing email", "A secure method"], 0),
            ("What is tailgating?", ["Following someone into a secure area", "A phishing tactic", "A password reset"], 0),
            ("What is a social engineering red flag?", ["Urgency", "Politeness", "Professionalism"], 0),
            ("What is a vishing attack?", ["Voice phishing", "Email phishing", "Malware"], 0),
            ("How can you identify social engineering?", ["Unusual requests", "Professional tone", "No urgency"], 0),
            ("A stranger asks for your login credentials. What do you do?", ["Provide them", "Ignore the request", "Verify their identity"], 2),
            ("What is a common sign of a social engineering attack?", ["Urgency", "Politeness", "Professionalism"], 0),
            ("What should you do if someone asks for sensitive information over the phone?", ["Provide it", "Verify their identity", "Ignore the call"], 1),
            ("What is the goal of social engineering?", ["To gain unauthorized access", "To improve security", "To test systems"], 0),
            ("How can you protect yourself from social engineering?", ["Be cautious with requests", "Share information freely", "Ignore all emails"], 0),
            ("What is a common tactic used in social engineering?", ["Creating a sense of urgency", "Offering rewards", "Both"], 2),
            ("What should you do if you suspect a social engineering attack?", ["Report it", "Ignore it", "Engage with the attacker"], 0),
            ("Why is it important to verify requests for sensitive information?", ["To prevent unauthorized access", "To save time", "To avoid confusion"], 0),
        ]

    def show_score(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Add a score animation
        score_label = tk.Label(self.main_frame, text=f"Your Score: {self.score}/610", font=("Arial", 16, "bold"), bg="black", fg="white")
        score_label.pack(pady=10)
        self.animate_score(score_label)

        if self.score >= 450:
            result = "🌟 Cyber Security Champion!"
            self.celebrate_animation()  # Trigger celebration anFimation
        elif self.score >= 300:
            result = "👍 Good Awareness!"
        elif self.score >= 150:
            result = "👏 Keep Learning!"
        else:
            result = "⚠️ Get Better!"
        tk.Label(self.main_frame, text=result, font=("Arial", 14), bg="black", fg="white").pack(pady=10)

        # Display the player's name with the score
        tk.Label(
            self.main_frame,
            text=f"Well done, {self.player_name}!",
            font=("Arial", 14, "bold"),
            bg="black",
            fg="white"
        ).pack(pady=10)

        # Add "Return to Home" button
        tk.Button(
            self.main_frame,
            text="Return to Home",
            command=self.return_to_home,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=20)

        tk.Button(self.main_frame, text="Exit", command=self.root.quit, font=("Arial", 12), bg="#f44336", fg="white").pack(pady=10)

    def return_to_home(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.display_header()

    def celebrate_animation(self):
        # Create a canvas for the animation
        canvas = tk.Canvas(self.main_frame, width=800, height=400, bg="black", highlightthickness=0)
        canvas.pack()

        # Generate bouncing stars
        stars = []
        for _ in range(10):
            x, y = random.randint(50, 750), random.randint(50, 350)
            size = random.randint(20, 40)
            color = random.choice(["gold", "yellow", "white"])
            star = canvas.create_text(x, y, text="★", font=("Arial", size), fill=color)
            stars.append({"id": star, "dx": random.choice([-5, 5]), "dy": random.choice([-5, 5])})

        def animate_stars():
            for star in stars:
                canvas.move(star["id"], star["dx"], star["dy"])
                x, y = canvas.coords(star["id"])
                if x <= 0 or x >= 800:  # Bounce horizontally
                    star["dx"] = -star["dx"]
                if y <= 0 or y >= 400:  # Bounce vertically
                    star["dy"] = -star["dy"]
            self.root.after(50, animate_stars)

        animate_stars()

    def animate_score(self, label, current=0):
        if current <= self.score:
            label.config(text=f"Your Score: {current}/610")
            self.root.after(50, self.animate_score, label, current + 5)

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberSecurityGameApp(root)
    root.mainloop()