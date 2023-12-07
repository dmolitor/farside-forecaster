import numpy as np
import os
from pathlib import Path
from shiny import App, reactive, render, ui
from shiny.types import ImgData
import shinyswatch
from ui_cartoons import Cartoons, cartoons, cartoons_ui
from ui_intro import intro_ui
from ui_outro import outro_ui

# Set absolute file paths relative to app.py
cur_dir = Path(__file__).resolve().parent

app_ui = ui.page_fluid(
    shinyswatch.theme.solar(),
    ui.br(),
    ui.panel_title(ui.markdown("**Farside Forecaster**"), "Farside Forecaster"),
    ui.hr(),
    ui.navset_hidden(
        # Intro Page
        intro_ui,
        # Cartoon Display
        cartoons_ui,
        outro_ui,
        id="hidden_tabs"
    )
)


def server(input, output, session):
    
    # Determine number of rounds to do
    @reactive.Calc
    def num_rounds():
        return input.num_rounds()
    
    # Logic for 'Next' button
    @reactive.Effect
    @reactive.event(input.next)
    def _():
        farside_sel_vals = [
            input.farside1_sel(),
            input.farside2_sel()#,
            #input.farside3_sel()
        ]
        ui.remove_ui(selector="#next_status")
        # Only proceed if one image is selected
        if sum(farside_sel_vals) != 1:
            next_status = ui.help_text(
                ui.span(
                    {"style": "color:red; text-align: center;"},
                    "Please select only one option!"
                ),
                id="next_status"
            )
            ui.insert_ui(ui=next_status, selector="#next", where="afterEnd")
        else:
            # Update counter
            cartoons.update_counter()
            print(cartoons.counter)
            # Submit form and update probs (TODO)
            key1 = cartoons.selected[0]
            key2 = cartoons.selected[1]
            if farside_sel_vals[0] is True:
                cartoons.add_win(key=key1)
                cartoons.add_loss(key=key2)
            else:
                cartoons.add_win(key=key2)
                cartoons.add_loss(key=key1)
            
            # If counter is big enough exit!!!
            if cartoons.counter >= num_rounds():
                print("passed limit")
                fav_path = cartoons.top_cartoon()
                #outro = gen_output_ui(fav_cartoon)
                # ui.insert_ui(
                #     outro,
                #     selector="#panel_cartoon",
                #     where="afterEnd"
                # )
                ui.update_navs("hidden_tabs", selected="panel_outro")
                @output
                @render.image
                def fav_cartoon():
                    img: ImgData = {"src": str(cur_dir / "img" / fav_path), "height":"500px"}
                    return img
            
            # Re-generate images
            cartoons.draw_rand()
            #print(cartoons.cartoon_betas)
            ui.update_action_button(
                id="farside1",
                label="",
                icon=ui.img(src=cartoons.selected[0], height="500px")
            )
            ui.update_action_button(
                id="farside2",
                label="",
                icon=ui.img(src=cartoons.selected[1], height="500px")
            )
            # Re-set checkboxes
            ui.update_checkbox(id="farside1_sel", label="", value=False)
            ui.update_checkbox(id="farside2_sel", label="", value=False)
    
    # Logic for 'Get Started'
    @reactive.Effect
    @reactive.event(input.get_started)
    def _():
        ui.update_navs("hidden_tabs", selected="panel_cartoon")
    
    
    # Logic for selecting cartoon checkboxes
    @reactive.Effect
    @reactive.event(input.farside1)
    def _():
        sel_value = input.farside1_sel()
        new_sel_value = not sel_value
        ui.update_checkbox(id="farside1_sel", label="", value=new_sel_value)

    @reactive.Effect
    @reactive.event(input.farside2)
    def _():
        sel_value = input.farside2_sel()
        new_sel_value = not sel_value
        ui.update_checkbox(id="farside2_sel", label="", value=new_sel_value)

    # @reactive.Effect
    # @reactive.event(input.farside3)
    # def _():
    #     sel_value = input.farside3_sel()
    #     new_sel_value = not sel_value
    #     ui.update_checkbox(id="farside3_sel", label="", value=new_sel_value)


app = App(app_ui, server, static_assets=str(cur_dir / "img"))


# if __name__ == "__main__":
#     print(Path(__file__).resolve().parent)
#     print(Path(__file__).resolve())
