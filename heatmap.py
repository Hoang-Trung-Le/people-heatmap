import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Sbopen, Pitch

# Initialize the StatsBomb data loader
parser = Sbopen()


# List all competitions
competitions = parser.competition()

print(
    competitions[["competition_id", "competition_name", "country_name", "season_name"]]
)

competitions = parser.competition()
# parser.match(competition_id=9, season_id=281)
df, df_related, df_freeze, df_tactics = parser.event(3895052)
# print(df.team_name.unique())


def generatePlayerHeatmapGrid(team_name):
    # filtering to passes by team_name players
    team_passes = (
        (df.type_name == "Pass")
        & (df.team_name == team_name)
        & (df.sub_type_name != "Throw-in")
    )
    # selecting only relevant columsn for the pass map
    team_passes = df.loc[
        team_passes, ["x", "y", "end_x", "end_y", "player_name", "outcome_name"]
    ]
    # get the list of all players who made a pass
    names = team_passes["player_name"].unique()
    # draw 4x4 pitches
    pitch = Pitch(line_color="white", pitch_color="#02540b")
    fig, axs = pitch.grid(
        ncols=4,
        nrows=4,
        grid_height=0.85,
        title_height=0.06,
        axis=False,
        endnote_height=0.04,
        title_space=0.04,
        endnote_space=0.01,
    )
    plt.figure(figsize=(14, 10))
    # for each player
    for name, ax in zip(names, axs["pitch"].flat[: len(names)]):
        # take only passes by this player
        player_df = team_passes.loc[team_passes["player_name"] == name]
        # put player name over the plot
        ax.text(60, -10, name.split()[-1], ha="center", va="center", fontsize=14)
        # Create the heatmap
        pitch.kdeplot(
            x=player_df["x"],
            y=player_df["y"],
            # shade=True,
            fill=True,
            shade_lowest=False,
            alpha=0.5,
            n_levels=10,
            cmap="plasma",
            ax=ax,
        )
    # We have more than enough pitches - remove them
    for ax in axs["pitch"][-1, 25 - len(names) :]:
        ax.remove(ax)

    # Another way to set title using mplsoccer
    axs["title"].text(
        0.5, 0.5, team_name + " Heatmaps", ha="center", va="center", fontsize=20
    )


generatePlayerHeatmapGrid("Bayer Leverkusen")
plt.show()
generatePlayerHeatmapGrid("RB Leipzig")
plt.show()
