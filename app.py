from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def simulate_coin_tosses(n):
    """Προσομοίωση ρίψεων νομίσματος και επιστροφή δεδομένων"""
    outcomes = np.random.choice(["Κορώνα", "Γράμματα"], size=n)
    heads_count = np.sum(outcomes == "Κορώνα")
    tails_count = n - heads_count

    heads_percentage = (heads_count / n) * 100
    tails_percentage = (tails_count / n) * 100

    heads_probabilities = np.cumsum(outcomes == "Κορώνα") / np.arange(1, n+1)
    tails_probabilities = np.cumsum(outcomes == "Γράμματα") / np.arange(1, n+1)

    return heads_count, tails_count, heads_percentage, tails_percentage, heads_probabilities, tails_probabilities

@app.route("/", methods=["GET", "POST"])
def index():
    probability_plot = None
    heads_count = tails_count = heads_percentage = tails_percentage = None

    if request.method == "POST":
        try:
            n = int(request.form["num_tosses"])
            if n <= 0:
                raise ValueError("Ο αριθμός των ρίψεων πρέπει να είναι θετικός.")

            heads_count, tails_count, heads_percentage, tails_percentage, heads_probabilities, tails_probabilities = simulate_coin_tosses(n)

            # Δημιουργία διαγράμματος
            plt.figure(figsize=(8, 5))
            plt.plot(heads_probabilities, label="Σχετική συχνότητα Κορώνας", color="blue")
            plt.plot(tails_probabilities, label="Σχετική συχνότητα Γραμμάτων", color="orange")
            plt.axhline(y=0.5, color="red", linestyle="--", label="Θεωρητική πιθανότητα 50%")
            plt.xlabel("Αριθμός ρίψεων")
            plt.ylabel("Σχετική συχνότητα")
            plt.legend()
            plt.title("Νόμος των Μεγάλων Αριθμών - Ρίψεις νομίσματος")

            plot_path = os.path.join("static", "plot.png")
            plt.savefig(plot_path)
            plt.close()

            probability_plot = plot_path
        except ValueError:
            return render_template("index.html", error="Δώστε έναν έγκυρο αριθμό ρίψεων.")

    return render_template("index.html", 
                           probability_plot=probability_plot,
                           heads_count=heads_count, 
                           tails_count=tails_count,
                           heads_percentage=heads_percentage, 
                           tails_percentage=tails_percentage)

if __name__ == "__main__":
    app.run(debug=True)
