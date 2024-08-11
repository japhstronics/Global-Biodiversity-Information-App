import duckdb

from shiny import ui
from modules.data import import_data


def sidebar_ui():
    data = import_data()

    # Query to get unique country names
    query = "SELECT DISTINCT country FROM data"
    unique_countries = duckdb.sql(query).fetchall()
    country_choices = [row[0] for row in unique_countries]

    return ui.sidebar(
        ui.input_select(
            "country", "Select your country:", choices=sorted(country_choices)
        ),
        ui.input_radio_buttons(
            "search_criteria",
            "Search by:",
            choices=["vernacularName", "scientificName"],
        ),
        ui.input_select("species", "Select species:", choices=[]),  # Initially empty
        ui.input_action_button("submit", "Submit"),  # Submit button
    )
