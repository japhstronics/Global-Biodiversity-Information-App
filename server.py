import tempfile
from shiny import reactive, render, ui
import duckdb
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import folium
from modules.data import import_data


def server(input, output, session):
    # Initialize a flag to control image rendering
    submit_flag = reactive.Value(False)

    @reactive.Calc
    def filtered_data():
        selected_country = input.country()
        search_criteria = input.search_criteria()
        data = import_data()

        if selected_country and search_criteria:
            data_country = duckdb.sql(
                f"""
            SELECT * 
            FROM data 
            WHERE LOWER(country) = '{selected_country.lower()}'
            """
            )

            if search_criteria == "vernacularName":
                search_str = "vernacularName"
                species_names = duckdb.sql(
                    f""" SELECT DISTINCT {search_str} FROM data_country
                    """
                ).fetchall()

            elif search_criteria == "scientificName":
                search_str = "scientificName"
                species_names = duckdb.sql(
                    f""" SELECT DISTINCT {search_str} FROM data_country 
                    """
                ).fetchall()

        return data_country, species_names

    @reactive.Effect
    def update_species_options():
        species = filtered_data()[1]
        if species:
            # Filter out None values
            species_options = [row[0] for row in species if row[0] is not None]
            ui.update_selectize("species", choices=sorted(species_options))

    # Update the flag when the submit button is clicked
    @reactive.Effect
    def on_submit():
        if input.submit() > 0:
            submit_flag.set(True)

    @output
    @render.image
    def display_image():
        if submit_flag():  # Check if the submit flag is set
            selected_species = input.species()
            search_criteria = input.search_criteria()
            data = filtered_data()[0]

            if selected_species:
                try:
                    # Filter the data based on the selected species
                    selected_data = duckdb.sql(
                        f""" SELECT occurrenceID FROM data
                        WHERE {search_criteria} = '{selected_species}'
                        """
                    ).to_df()

                    if selected_data.empty:
                        raise IndexError("No data found for the selected species")

                    observation_id = (
                        selected_data["occurrenceID"].iloc[0].split("/")[-1]
                    )
                    imageUrl = (
                        f"https://observation.org/media/photo/{observation_id}.jpg"
                    )

                    # Send a GET request to fetch the image
                    response = requests.get(imageUrl)
                    response.raise_for_status()  # Raise an error for bad status codes

                    img = Image.open(BytesIO(response.content))

                    # Resize the image to a smaller size
                    max_size = (400, 400)  # Maximum size for width and height
                    img.thumbnail(max_size, Image.LANCZOS)

                    # Save the image to a temporary file
                    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                    img.save(tmp_file.name)

                    # Return the path to the image
                    return {"src": tmp_file.name}

                except (
                    IndexError,
                    requests.exceptions.RequestException,
                    Image.UnidentifiedImageError,
                ) as e:
                    # If any error occurs, log the error and return the default image path
                    print(f"Error loading image: {e}")
                    return {"src": "www/noImage.jpg"}

        return None  # Do not render until submit is clicked

    @output
    @render.text
    def species_summary():
        if submit_flag():
            selected_species = input.species()
            search_criteria = input.search_criteria()
            data = filtered_data()[0]

            if selected_species:
                # Filter the data based on the selected species
                selected_data = duckdb.sql(
                    f""" SELECT continent, country, stateProvince, locality, 
                    latitudeDecimal, longitudeDecimal , eventDate, eventTime,
                    individualCount
                    FROM data
                    WHERE {search_criteria} = '{selected_species}'
                    LIMIT 1
                    """
                ).to_df()

                if not selected_data.empty:
                    continent = selected_data["continent"].iloc[0]
                    country = selected_data["country"].iloc[0]
                    state_province = selected_data["stateProvince"].iloc[0]
                    locality = selected_data["locality"].iloc[0]
                    eventDate = selected_data["eventDate"].iloc[0].date()
                    eventTime = selected_data["eventTime"].iloc[0]
                    individualCount = selected_data["individualCount"].iloc[0]

                    if search_criteria == "vernacularName":
                        search_str = "Vernacular Name"
                    elif search_criteria == "scientificName":
                        search_str = "Scientific Name"

                    # Generate HTML content for the card
                    summary_html = f"""
                    <div class="card">
                        <div class="card-header"><strong>{search_str}:</strong> {selected_species}</div>
                        <div class="card-body">
                            <p class="card-text"><strong>Continent:</strong> {continent}</p>
                            <p class="card-text"><strong>Country:</strong> {country}</p>
                            <p class="card-text"><strong>State/Province:</strong> {state_province}</p>
                            <p class="card-text"><strong>Locality:</strong> {locality}</p>
                            <p class="card-text"><strong>Total individual count:</strong> {individualCount}</p>
                            <p class="card-text"><strong>Date observed:</strong> {eventDate}</p>
                            <p class="card-text"><strong>Time observed:</strong> {eventTime}</p>
                        </div>
                    </div>
                    """
                    return summary_html
        return "<p>No species selected</p>"

    @output
    @render.ui
    def map():
        if submit_flag():
            selected_species = input.species()
            search_criteria = input.search_criteria()
            data = filtered_data()[0]

            if selected_species:
                selected_data = duckdb.sql(
                    f""" SELECT latitudeDecimal, longitudeDecimal, locality FROM data
                    WHERE {search_criteria} = '{selected_species}'
                    LIMIT 1
                    """
                ).to_df()

                if not selected_data.empty:
                    latitude = selected_data["latitudeDecimal"].iloc[0]
                    longitude = selected_data["longitudeDecimal"].iloc[0]
                    locality = selected_data["locality"].iloc[0]

                    # Create a Folium map centered at the species' location
                    folium_map = folium.Map(
                        location=[latitude, longitude], zoom_start=12
                    )

                    # Create a Bootstrap-styled card for the popup
                    popup_content = f"""
                    <div class="card" style="width: 30rem;">
                        <div class="card-body">
                        <h3><strong>{selected_species}</strong></h3>
                            <p class="card-text"><strong>Last known Location: </strong>{locality}</p>
                            <p class="card-text"><strong>Latidude: </strong>{latitude}</p>
                            <p class="card-text"><strong>Longitude: </strong>{longitude}</p>
                        </div>
                    </div>
                    """

                    # Add a marker for the species' location with the card popup
                    folium.Marker(
                        location=[latitude, longitude],
                        popup=folium.Popup(popup_content, max_width=300),
                        tooltip=locality,
                    ).add_to(folium_map)

                    return folium_map
        return ui.HTML("<p>No map available</p>")
