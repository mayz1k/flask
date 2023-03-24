from flask import Flask, render_template
import data, random, requests


app = Flask(__name__)

@app.route("/")
def render_index():
    random_tours_id = random.sample(list(data.tours), k=3)
    random_tours = {
        num_of_tour: tour_info
        for num_of_tour, tour_info in data.tours.items()
        if num_of_tour in random_tours_id
    }

    return render_template(
        "index.html",
        title=data.title,
        description=data.description,
        all_departures=data.departures,
        all_tours=random_tours,
    )


@app.route("/data/departures/<departure>/")
def render_departures(departure):
    tours_by_departure = {
        tour_id: tour_info
        for tour_id, tour_info in data.tours.items()
        if tour_info["departure"] == departure
    }
    analytics_of_found_tours = {
        "tours_found": len(tours_by_departure),
        "prices": [v["price"] for k, v in tours_by_departure.items()],
        "nights": [v["nights"] for k, v in tours_by_departure.items()],
    }

    return render_template(
        "departure.html",
        title=data.title,
        departure=departure,
        all_tours=tours_by_departure,
        all_departures=data.departures,
        analytics=analytics_of_found_tours,
    )


@app.route("/data/tours/<int:tour_id>/")
def render_tours(tour_id):
    tour_info = data.tours.get(tour_id)

    place = tour_info["country"][1]
    return render_template(
        "tour.html",
        title=data.title,
        tour_info=tour_info,
        all_departures=data.departures,
    )


if __name__ == "__main__":
    app.run()
