import numpy as np
import os
from pathlib import Path
import random
from shiny import ui

# Simple class to handle updated probabilities and random cartoon assignment
class Cartoons:
    def __init__(self, img_dir):
        cartoon_categories = ["alien", "cow", "hunting", "neanderthal", "science"]
        cartoon_fps = [
            os.path.join(k, file) for k 
            in cartoon_categories for file
            in os.listdir(str(img_dir / k))
            if file != ".DS_Store"
        ]
        self.cartoon_betas = {k: [0, 0, 0.5, 0.5] for k in cartoon_fps}
        self.cartoon_fps = cartoon_fps
        self.counter = 0
        self.selected = None
        self.used_combinations = list()
    
    def add_loss(self, key):
        val = self.cartoon_betas[key]
        w = val[0]
        l = val[1] + 1
        theta_hat = val[2]
        ev = (w + 1)/(w + l + 2)
        self.cartoon_betas[key] = [w, l, theta_hat, ev]
        return self
    
    def add_win(self, key):
        val = self.cartoon_betas[key]
        w = val[0] + 1
        l = val[1]
        theta_hat = val[2]
        ev = (w + 1)/(w + l + 2)
        self.cartoon_betas[key] = [w, l, theta_hat, ev]
        return self
    
    def draw_rand(self):
        beta = np.random.Generator(np.random.PCG64())
        thetas = dict()
        # Random draws from each cartoons current Beta prior
        for key in self.cartoon_betas.keys():
            val = self.cartoon_betas[key]
            w = val[0]
            l = val[1]
            ev = val[3]
            theta_hat = beta.beta(1 + w, 1 + l)
            self.cartoon_betas[key] = [w, l, theta_hat, ev]
            thetas[key] = theta_hat
        # Find top two and pit them against each other
        top_cartoons = list()
        while len(top_cartoons) < 2:
            max_theta = np.max(list(thetas.values()))
            [max_theta_cartoon] = [k for k, v in thetas.items() if v == max_theta]
            top_cartoons.append(max_theta_cartoon)
            del thetas[max_theta_cartoon]
        if sorted(top_cartoons) in self.used_combinations:
            self.draw_rand()
        elif top_cartoons[0] == top_cartoons[1]:
            raise Exception("Algorithm should never select duplicate cartoons")
        else:
            self.selected = top_cartoons
            self.used_combinations.append(sorted(top_cartoons))
        return self
    
    def top_cartoon(self):
        evs = dict()
        for key in self.cartoon_betas.keys():
            val = self.cartoon_betas[key]
            ev = val[3]
            evs[key] = ev
        # Find cartoon with max expected value
        max_ev = np.max(list(evs.values()))
        max_ev_cartoon = [k for k, v in evs.items() if v == max_ev][0]
        return max_ev_cartoon
    
    def update_counter(self):
        self.counter += 1

# Create cartoons class
cur_dir = Path(__file__).resolve().parent
cartoons = Cartoons(cur_dir / "img").draw_rand()

# Cartoons Shiny App UI
cartoons_ui = ui.nav(
    None,
    # Cartoons (as clickable buttons)
    ui.row(
        ui.column(2),
        ui.column(4,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button(
                    "farside1", "",
                    icon=ui.img(src=cartoons.selected[0], height="500px")
                )
            )
        ),
        ui.column(4,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button(
                    "farside2", "",
                    icon=ui.img(src=cartoons.selected[1], height="500px")
                )
            )
        ),
        ui.column(2)
    ),
    # Select boxes below cartoons
    ui.row(
        ui.column(3),
        ui.column(2,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_checkbox("farside1_sel", "")
            )
        ),
        ui.column(2),
        ui.column(2,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_checkbox("farside2_sel", "")
            )
        ),
        ui.column(3)
    ),
    # 'Next' button for navigating through the survey
    ui.row(
        ui.column(5),
        ui.column(2,
            ui.div(
                {"style": "text-align: center;"},
                ui.input_action_button("next", "Next", width="100%")
            )
        ),
        ui.column(5)
    ),
    value="panel_cartoon"
)
