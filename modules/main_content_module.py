from shiny import ui


def main_content_ui():
    return ui.layout_columns(
        ui.row(
            ui.hr(),
            ui.column(5, ui.output_ui("species_summary")),
            ui.column(5, ui.output_image("display_image")),
            ui.hr(),
        ),
    )
