from shiny import ui
from modules.sidebar_module import sidebar_ui
from modules.main_content_module import main_content_ui

app_ui = ui.page_sidebar(
    sidebar_ui(),
    main_content_ui(),
    ui.row(ui.output_ui("map")),
    ui.include_css("www/styles.css"),
    title="Global Biodiversity Information Dashboard",
)
