from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def simulate_coin_tosses(n):
    """Προσομοίωση ρίψεων νομίσματος και επιστροφή της σύγκλισης της πιθανότητας"""
    outcomes = np.random.choice(["Κορώνα", "Γράμματα"], size=n)
    heads_count = np.cumsum(outcomes == "Κορώνα")
    probabilities = heads_count / np.arange(1, n+1)
    return probabilities

@app.route("/", methods=["GET", "POST"])
def index():
    probability_plot = None
    if request.method == "POST":
        try:
            n = int(request.form["num_tosses"])
            if n <= 0:
                raise ValueError("Ο αριθμός των ρίψεων πρέπει να είναι θετικός.")

            probabilities = simulate_coin_tosses(n)

            # Δημιουργία διαγράμματος
            plt.figure(figsize=(8, 5))
            plt.plot(probabilities, label="Σχετική συχνότητα Κορώνας", color="blue")
            plt.axhline(y=0.5, color="red", linestyle="--", label="Θεωρητική πιθανότητα 50%")
            plt.xlabel("Αριθμός ρίψεων")
            plt.ylabel("Πιθανότητα Κορώνας")
            plt.legend()
            plt.title("Νόμος των Μεγάλων Αριθμών - Ρίψεις νομίσματος")

            plot_path = os.path.join("static", "plot.png")
            plt.savefig(plot_path)
            plt.close()

            probability_plot = plot_path
        except ValueError:
            return render_template("index.html", error="Δώστε έναν έγκυρο αριθμό ρίψεων.")

    return render_template("index.html", probability_plot=probability_plot)

if __name__ == "__main__":
    app.run(debug=True)
