# Import Tkinter, sandbox, and reportlab
import tkinter as tk
from tkinter import ttk, messagebox
from sandbox import simulate_brute_force
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import time

# Function to check password and start simulation
def check_password():
    password = entry.get()
    if not password:
        sandbox_label.config(text="Please enter a password!", fg="red")
        return
    score = 0
    feedback = []

    # Check length
    length = len(password)
    if length < 8:
        feedback.append(f"Length: {length} chars - Too short!")
    elif length < 12:
        feedback.append(f"Length: {length} chars - Decent.")
        score += 30
    else:
        feedback.append(f"Length: {length} chars - Excellent!")
        score += 50

    # Check uppercase
    has_upper = any(c.isupper() for c in password)
    if has_upper:
        feedback.append("Uppercase: Yes - Good!")
        score += 20
    else:
        feedback.append("Uppercase: No - Add some (e.g., A, B).")

    # Check numbers
    has_number = any(c.isdigit() for c in password)
    if has_number:
        feedback.append("Numbers: Yes - Nice!")
        score += 20
    else:
        feedback.append("Numbers: No - Add some (e.g., 1, 2).")

    # Check symbols
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    has_symbol = any(c in symbols for c in password)
    if has_symbol:
        feedback.append("Symbols: Yes - Awesome!")
        score += 30
    else:
        feedback.append("Symbols: No - Add some (e.g., !, @).")

    # Determine status
    if score <= 50:
        status = "Weak - Improve it!"
        color = "red"
    elif score <= 80:
        status = "Moderate - Almost there!"
        color = "orange"
    else:
        status = "Strong - Great job!"
        color = "green"

    # Run sandbox simulation
    crack_time = simulate_brute_force(password)
    sandbox_result = f"Password cracked in {crack_time} seconds!"

    # Update GUI
    result_label.config(text=f"Score: {score} / 100\nStatus: {status}", fg=color)
    feedback_text.delete(1.0, tk.END)
    feedback_text.insert(tk.END, "\n".join(feedback))
    progress_bar["value"] = 0
    simulate_attack(crack_time)

    # Store results for report
    window.current_results = {
        "score": score,
        "status": status,
        "feedback": feedback,
        "sandbox": sandbox_result
    }

# Function to animate the progress bar
def simulate_attack(crack_time):
    total_steps = 100
    step_time = crack_time * 1000 / total_steps
    
    def update_progress(step=0):
        if step <= total_steps:
            progress_bar["value"] = step
            window.after(int(step_time), update_progress, step + 1)
        else:
            sandbox_label.config(text=window.current_results["sandbox"], fg="yellow")
    
    update_progress()

# Function to generate PDF report with tips
def generate_report():
    if not hasattr(window, "current_results"):
        sandbox_label.config(text="Check a password first!", fg="red")
        return

    if not os.path.exists("reports"):
        os.makedirs("reports")

    results = window.current_results
    filename = f"reports/CipherShield_Report_{int(time.time())}.pdf"
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        # Set title
        c.setFillColorRGB(0, 0.5, 1)  # Cyan
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "CipherShield Sentinel Report")
        
        # Reset color and font for body
        c.setFillColorRGB(0, 0, 0)  # Black
        c.setFont("Helvetica", 12)
        
        # Add content with better spacing
        y = 720  # Start below title
        c.drawString(50, y, f"Score: {results['score']} / 100")
        y -= 30
        c.drawString(50, y, f"Status: {results['status']}")
        y -= 30
        
        c.drawString(50, y, "Feedback:")
        y -= 20
        for line in results['feedback']:
            c.drawString(70, y, f"- {line}")
            y -= 20
        
        y -= 20
        c.drawString(50, y, f"Sandbox: {results['sandbox']}")
        y -= 40
        
        c.drawString(50, y, "Tips to Improve:")
        y -= 20
        tips = [
            "Use at least 12 characters.",
            "Mix uppercase, lowercase, numbers, and symbols.",
            "Avoid common words or patterns (e.g., 'password123')."
        ]
        for tip in tips:
            c.drawString(70, y, f"- {tip}")
            y -= 20
        
        c.save()
        sandbox_label.config(text=f"Report saved as {filename}", fg="green")
    except Exception as e:
        sandbox_label.config(text=f"Error: {str(e)}", fg="red")

# Function to show about info
def show_about():
    messagebox.showinfo("About", "CipherShield Sentinel v1.0\nCreated by Nirpesh\nA cybersecurity tool for password strength and malware simulation.")

# Splash screen
splash = tk.Tk()
splash.overrideredirect(True)  # No window borders
splash.geometry("300x200+500+300")  # Centered-ish
splash.configure(bg="#1a1a1a")
splash_label = tk.Label(splash, text="CipherShield Sentinel\nv1.0", font=("Arial", 20, "bold"), fg="cyan", bg="#1a1a1a")
splash_label.pack(expand=True)
splash.after(2000, splash.destroy)  # Close after 2 seconds
splash.mainloop()

# Create the main window
window = tk.Tk()
window.title("CipherShield Sentinel v1.0")
window.geometry("400x450")
window.configure(bg="#1a1a1a")
try:
    window.iconphoto(True, tk.PhotoImage(file="shield.png"))
except:
    pass

# Welcome label
welcome_label = tk.Label(window, text="CipherShield Sentinel", font=("Arial", 16, "bold"), fg="cyan", bg="#1a1a1a", relief="raised", bd=2)
welcome_label.pack(pady=10)

# Password input frame
input_frame = tk.Frame(window, bg="#1a1a1a")
input_frame.pack(pady=5)
entry_label = tk.Label(input_frame, text="Enter Password:", font=("Arial", 10), fg="white", bg="#1a1a1a")
entry_label.pack(side="left")
entry = tk.Entry(input_frame, width=25, show="*", font=("Arial", 12), bg="#333333", fg="white", insertbackground="white")
entry.pack(side="left", padx=5)

# Buttons frame
button_frame = tk.Frame(window, bg="#1a1a1a")
button_frame.pack(pady=5)
check_button = tk.Button(button_frame, text="Check Strength", command=check_password, bg="cyan", fg="black", font=("Arial", 10, "bold"), relief="groove")
check_button.pack(side="left", padx=5)
report_button = tk.Button(button_frame, text="Generate Report", command=generate_report, bg="lime", fg="black", font=("Arial", 10, "bold"), relief="groove")
report_button.pack(side="left", padx=5)
about_button = tk.Button(button_frame, text="About", command=show_about, bg="grey", fg="white", font=("Arial", 10, "bold"), relief="groove")
about_button.pack(side="left", padx=5)

# Result label
result_label = tk.Label(window, text="", font=("Arial", 12, "bold"), bg="#1a1a1a", fg="white")
result_label.pack(pady=5)

# Feedback text box
feedback_text = tk.Text(window, height=6, width=40, font=("Arial", 10), bg="#333333", fg="white", wrap="word", relief="sunken", bd=2)
feedback_text.pack(pady=5)

# Sandbox simulation area
sandbox_label = tk.Label(window, text="", font=("Arial", 10, "italic"), bg="#1a1a1a", fg="yellow")
sandbox_label.pack(pady=5)

# Progress bar
progress_bar = ttk.Progressbar(window, length=300, maximum=100, mode="determinate", style="TProgressbar")
progress_bar.pack(pady=5)

# Style the progress bar
style = ttk.Style()
style.configure("TProgressbar", troughcolor="#1a1a1a", background="cyan")

# Start the window
window.mainloop()
