from shiny import ui

outro_ui = ui.nav(
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.h3(
                {"style": "text-align: center; font-size: 45px;"},
                ui.markdown("**Your favorite Far Side cartoon was**:")
            ),
            ui.div(
                {"style": "text-align: center;"},
                ui.output_image("fav_cartoon")
            ),
        ),
        ui.column(3)
    ),
    value="panel_outro"
)
