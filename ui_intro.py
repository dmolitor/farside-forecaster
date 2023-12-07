from shiny import ui

intro_ui = ui.nav(
    None,
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.h1(
                {"style": "text-align: center; font-size: 45px;"},
                ui.markdown("**Welcome to the Farside Forecaster**")
            ),
            ui.div(
                {"style": "text-align: center;"},
                ui.img(src="fs_intro.avif", height="400px")
            ),
            ui.br(),
            ui.div(
                {"style": "text-align: justify; font-size: 20px;"},
                ui.markdown(
                    "The Farside has a wealth of categories; from"
                    + " Neanderthals to archeological endeavors to "
                    + "cows, it's got a little something for"
                    + " everyone. So take this quiz and see which Far"
                    + " Side cartoons are your cup of tea!\n\n"
                    + "You'll be shown pairs of cartoons. For each pair,"
                    + " select whichever one is your favorite and move on"
                    + " to the next pair. You can choose how many rounds to do!"
                )
            )
        ),
        ui.column(3)
    ),
    ui.row(ui.column(3), ui.column(6, ui.hr()), ui.column(3)),
    ui.row(
        ui.column(3),
        ui.column(6,
            ui.div(
                {"style": "text-align: center; font-size: 20px;"},
                ui.input_numeric(
                    "num_rounds",
                    ui.markdown("**How many rounds should we do?**"),
                    value=20,
                    min=1,
                    max=45,
                    step=1,
                    width="100%"
                )
            )
        ),
        ui.column(3)
    ),
    ui.row(
        ui.column(5),
        ui.column(2,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button("get_started", "Get Started")
            )
        ),
        ui.column(5)
    ),
    ui.br()
)
