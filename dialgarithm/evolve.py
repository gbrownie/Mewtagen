from .metagame import *
import numpy as np


class Evolve:
    population_size = 100
    num_generations = 100
    population = []
    fitness_dict = {}
    starting_elo = 1000
    matches = 50

    @staticmethod
    def evolve():
        print("GENERATING TEAMS!")
        Evolve.population = [Metagame.generate_team(Model.core) for _ in range(0, Evolve.population_size)]
        for generation in range(0, Evolve.num_generations):
            Evolve.next_generation()
        Evolve.final_evaluation()

    @staticmethod
    def next_generation():

        # grab |matches| sample of norms
        norm_choices = [key for key in Metagame.elo_dict]
        norms = np.random.choice(norm_choices, Evolve.matches)

        # battles all norms against team, returns elo
        def fitness(team):
            elo = Evolve.starting_elo
            for norm in norms:
                winner = Damage.battle(team, norm)
                norm_elo = Metagame.elo_dict[norm]
                team1_winner = winner == team
                elo = Elo.update_elo(elo, norm_elo, team1_winner)
            return Elo.win_prob(elo)

        Evolve.fitness_dict = {team: fitness(team) for team in Evolve.population}

        # damage - 1800, switch - 1000

        choices = [key for key in Evolve.fitness_dict]
        weights = [Evolve.fitness_dict[key] for key in Evolve.fitness_dict]
        total_weight = sum(weights)
        weights = [weight / total_weight for weight in weights]

        def get_newborn():
            parents = np.random.choice(choices, 2, p=weights)
            return Team.reproduce(parents[0], parents[1])

        elites = Evolve.get_elites()
        mutants = [get_newborn() for _ in range(0, Evolve.population_size - len(elites))]
        Evolve.population = elites + mutants

    @staticmethod
    def get_elites():
        elites = sorted(Evolve.fitness_dict, key=Evolve.fitness_dict.get, reverse=True)[:10]
        return [team.get_elite() for team in elites]

    @staticmethod
    def final_evaluation():
        # grab |matches| sample of norms
        norm_choices = [key for key in Metagame.elo_dict]
        norms = np.random.choice(norm_choices, Evolve.matches)

        # battles all norms against team, returns elo
        def fitness(team):
            for i in range(0, 50):
                elo = Evolve.starting_elo
                for norm in norms:
                    winner = Damage.battle(team, norm)
                    norm_elo = Metagame.elo_dict[norm]
                    team1_winner = winner == team
                    elo = Elo.update_elo(elo, norm_elo, team1_winner)
                return Elo.win_prob(elo)
        Evolve.fitness_dict = {team: fitness(team) for team in Evolve.population}
        elites = sorted(Evolve.fitness_dict, key=Evolve.fitness_dict.get)[:10]
        for team in elites:
            print(team, Evolve.fitness_dict[team])