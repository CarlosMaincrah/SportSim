## FRIO MX
By Carlos Rodríguez (Pisich)

A sports betting simulator that depends on teams stats to emulate scores.

## Project description
It has a fully functional betting system, where the user has to create an account and deposit some money to start betting. The user selects the matches they want to bet in and when the matches end the final score and the result of their bets will be shown to the user. If they won their bet, depends on how high the reputation of the team was the user will get their initial bet multiplied by. The higher the reputation of the team, the less the user will profit from that bet and the lower the reputation of the team, the more the user will profit. (Higher risk = Higher reward)

At first, this was a school project, but then I decided to continue developing it because I liked where this idea was going. I have tweaked every single aspect of the application so it mimics real matches where the team that has better statistics has a bigger chance of winning but, that will not always end up happening.

</br>Best of luck betting in FRIO MX!

## Technical specifications
This program was fully developed with Python, team stats are updated daily in a separate database based on past days results. If the user can't connect for nay reason to the database, the program will use the data retrieved from last connection to ensure functionality.

## Installation

```bash
# Clone the repo
$ git clone https://github.com/pisich/FRIO-MX

# Change the working directory to FRIO-MX
$ cd FRIO-MX

# Install python3 and python3-pip if they are not installed

# Install the requirements
$ python3 -m pip install -r requirements.txt
```

## Contributions
If you would like to see a feature added, feel free to submit an issue or a pull request.
