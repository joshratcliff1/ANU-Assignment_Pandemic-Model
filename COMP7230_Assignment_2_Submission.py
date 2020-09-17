"""
COMP7230 - 2020 Assignment 2 code skeleton.

Student ID: u7199704

This assignment assesses some of the topics we have covered more recently
in the course. There is a reduced emphasis on actual coding and a greater emphasis on understanding, using and
modifying existing code in order to solve a particular problem.

You are given a (more-or-less) working piece of software, that simulates a pandemic outbreak in Australia. The
pandemic could be anything from the current COVID-19 outbreak to a zombie apocalypse. A similar approach could be used to
model memes spreading out across the internet, news spreading over Twitter or animals spreading in a new habitat.

This software is much more complex than what you are expected to be able to create on your own.
However it is a good example of the type of thing you might be able to find on the Internet and use
to solve a problem. As such, your tasks are to refactor and modify the software, to improve the documentation and
add logging functionality. Finally, you are asked to use the software to answer two questions about where to target a
response to the pandemic.

The assignment will be marked out of 40 and is worth 40% of your final grade for COMP7230.

For a full specification of your tasks for this assignment please see the Assignment Specification file on Wattle.

The assignment is structured as follows:

    Part 1 consists of Questions 1 and 2 and requires you to refactor part of the City class, add in
    logging functionality and improve the documentation and code quality of the City class.
    It is worth twenty (20) marks.

    Part 2 consists of Questions 3 and it asks you to extend the functionality of the
    TreatmentCentre class by completing the move method.
    It is worth four (6) marks.

    Part 3 consists of Questions 4 and 5 and asks you to use (and modify) the software
    in order to answer some questions. It is worth a total of ten (10) marks.
    Please be aware that these are a challenging questions and make sure you have
    solved parts 1 and 2 before spending too much time here.

Part 1 contains six (6) marks which are allocated to improving the code quality in the City class (included in the 20).
There will also be four (4) additional marks allocated to code quality for your answers to Parts 2 and 3,
which includes such aspects as:

    Appropriate commenting
    Variable naming
    Efficiency of computation
    Code structure and organisation

In addition to this file COMP7230_Assignment_2_Submission.py, we have also provided
some unit tests in COMP7230_Assignment_2_Submission_Tests.py which
will help you to test your work. Please note that these tests are there to assist you,
but passing the tests is NOT a guarantee that your solution is correct.

The assignment must be entirely your own work. Copying other students or sharing
solutions is a breach of the ANU Academic Honesty Policy and will be dealt with
accordingly. We reserve the right to ask any student to explain their code, and further
action may be taken if they are unable to do so.

The Assignment is due at 11:59pm, Sunday 6 September 2020.

Submission will be done through the link in Wattle . To submit your assignment, please upload your modified version
of COMP7230_Assignment_2_Submission.py (this file) ONLY. No work you undertake in other files will be marked.

Please don't forget to include your UID at the top of the file.

Once marks are released, you will have two weeks in which to question your mark.
After this period has elapsed, your mark will be considered final and no further
changes will be made.

If you ask for a re-mark, your assignment will be re-marked entirely, and your mark
may go UP or DOWN as a result.

The city data was obtained by merging information from: http://www.tageo.com/index-e-as-cities-AU.htm
with data from https://en.wikipedia.org/wiki/List_of_cities_in_Australia_by_population
and individual Wikipedia pages for the cities.
The map was obtained from: https://www.google.com.au/maps
"""

import matplotlib.pyplot as plt
import imageio as im
import matplotlib.animation as animation
import sys
import datetime
import os
from matplotlib import gridspec

########################################################################################################################
#                               Simulation settings
########################################################################################################################
"""
    There are six different simulations that are 'built in' to the assignment (you can create others if you wish).
    They essentially change the parameters and initial setup (such as where the outbreak starts).
    You can change the simulation being run by changing the SIMULATION_NUMBER constant.
    0: the default - this is the default simulation settings, and also the settings used for the unit-testing.
    1 - 3: Other simulations you can explore, or use to check your answers to Parts 1 and 2
    4: is the simulation you should use to answer question 4
    5: is the simulation you should use to answer question 5
    Once you choose the simulation number, all the other parameters will be set accordingly.
"""
########################################################################################################################
#                           Change this to run a different simulation
SIMULATION_NUMBER = 0  # An integer from 0 to 5 corresponding to the particular simulation we are running
########################################################################################################################

'''
As my final soltion for Q4 involved running many instances of the simulation,
I chose to not write a log file during the Q4 simulation.
'''
if SIMULATION_NUMBER == 4:
    pass
else:
    # Create a logging directory if there isn't one there already.
    if not os.path.exists(os.path.join(os.getcwd(), "logs")):
        os.mkdir(os.path.join(os.getcwd(),  "logs"))

    ####################################################################################################################
    #                           Write to this log file for Question 2
    LOG_FILE = open(os.path.join(os.getcwd(), "logs", "COMP7230_Assignment_2_Log_{}.txt".format(
        str(datetime.datetime.now()).replace(":", "_"))), mode="w")

    ''' The below log file write was created as a header row for the log file. '''
    LOG_FILE.write("Turn| Alive |infected|  Dead |Survivors| Cured |Vaccines|        City        |Event\n")
    ####################################################################################################################


#  Map coordinates
MAP_LEFT = 112.2
MAP_RIGHT = 154.3
MAP_TOP = -10.3
MAP_BOTTOM = -40.2

# These parameters will be set by choosing the simulation number. They are all constant for a particular simulation.
STOPPING_CONDITIONS = 0     # An integer 0 - run to completion,
                            # otherwise an integer > 0 to describe the number of turns.
TREATMENT_MOVEMENT = False  # A boolean: False means the treatment centres are stationary, True means they move.
TREATMENT_LIMIT = 0         # The maximum number of infected a treatment unit can deal with.
MORTALITY_RATE = 1.0        # The proportion of infected people who die (float between 0 and 1.0).
INFECTION_RATE = 4.0        # The spreading factor. The number of new cases per infected per step (float >= 0).
MOVEMENT_PROPORTION = 0.1   # The proportion of infected who move cities each step (float between 0 and 1).
AVERAGE_DURATION = 4.0      # The average number of turns to recover or die, (float > 0).


########################################################################################################################
#                               City Class - Parts 1 and 2 of the Assignment
########################################################################################################################

# Note that for Question 2 - you should write to the file opened as LOG_FILE above

class City(object):
    """ A class used to represent a city within the pandemic simulation

    Note: cities include other forms of population centres (eg. towns, dual-cities, etc.)
    """

    def __init__(self, lat, long, name, population):
        """ Initialises the City class.

        Parameters
        -----------
        lat: float
            The latitude of the city
        long: float
            The longitude of the city
        name: string
            The name of the city
        population: int
            The population of the city

        Attributes
        ----------
        name: str
            The name of the city
        lat: float
            The latitude of the city
        long: float
            The longitude of the city
        infected: int
            The number of infected people in the city.
        incoming_infected: int
            The number of infected people arriving from a neighbouring city
        survivors: int
            The number of surviving people in the city
        cured: int
            The number of cured people in the city
        dead: int
            The number of people who have died in the city
        initial_population: int
            The population of the city prior to the disease
        healthy_population: int
            The current healthy population of the city
        neighbours : set
            A set of other city class instances that neighbour the city.
        alive: int
            The alive population of the city (including infected, healthy, cured and survivors)
        treatment_remaining: int
            The number of vaccines that are remaining in the city
        total_infections: int
            The total number of people ever infected in the city
        first_infection_flag: bool
            Indicates if the city has been infected
        all_infected_flag: bool
            Indicates if every person in the city is infected
        all_dead_flag: bool
            Indicates if everyone in the city is dead
        first_infection_log_flag: bool
            Indicates if the first infection log has already been run
        infection_free_log_flag: bool
            Indicates if the infection free log has already been run
        all_infected_log_flag: bool
            Indicates if the all infected log has already been run
        all_dead_log_flag: bool
            Indicates if the all dead log has already been run
        """

        self.name = name
        self.lat = lat
        self.long = long
        self.infected = 0
        self.incoming_infected = 0
        self.survivors = 0
        self.cured = 0
        self.dead = 0
        self.initial_population = population
        self.healthy_population = population
        self.neighbours = set()
        self.alive = population                         # added alive attribute for logging
        self.treatment_remaining = 0                    # added treatment_remaining attribute for logging in City class
        self.total_infections = 0                       # added total_infections attribute for Q5 logging

        ''' The below attributes are all used to assist with logging activities.'''
        self.first_infection_flag = False
        self.all_infected_flag = False
        self.all_dead_flag = False

        self.first_infection_log_flag = False
        self.infection_free_log_flag = True
        self.all_infected_log_flag = False
        self.all_dead_log_flag = False

    def __hash__(self):
        return hash(self.name)

    def __ne__(self, other):
        return self.name != other.name

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __str__(self):
        """ This dunder method allows the city name to be utilized when printing to console. """
        return "{}".format(self.name)

    def add_neighbour(self, neighbour):
        """ Adds a neighbouring city to the current city.

        Parameter
        ---------
        neighbour: City
            A neighbouring city to the current city to be added as a neighbour.
        """
        self.neighbours.add(neighbour)

    def remove_neighbour(self, neighbour):
        """ Removes a neighbour from the current city.

        Parameter
        ---------
        neighbour: City
            A neighbouring city to the current city to be removed as a neighbour.
        """
        self.neighbours.remove(neighbour)

    def start_of_turn(self):
        """ Converts the incoming_infected into infected people in the city.

        The infected_flag is triggered here when a city has its first infection.
        """

        if self.incoming_infected > 0:
            self.first_infection_flag = True
            self.infection_free_log_flag = False    # Allows for the infection free log to be run again.
            self.all_dead_log_flag = False          # Allows for the all dead log to be run again.

        self.infected += self.incoming_infected
        self.alive += self.incoming_infected
        self.incoming_infected = 0

    def run_turn(self, turn_number):
        """ The turn for each city is run by completing the stages of the turn in order.

        The methods associated with the three stages of the turn are:
        move_infected, change_in_infected_numbers and spread_infection.

        Each turn:
        A proportion of infected cases move to a neighbouring city (leaving the current city).
        A proportion of the infected cases in the city either die or become survivors.
        The infected people spread the disease to more people in the city.

        At the conclusion of the turn, logging is performed by the logging_process method.

        Parameter
        ----------
        turn_number: int
             The current number of turns (ie. number of rounds of infections).
        """

        self.move_infected()
        self.change_in_infected_numbers()
        self.spread_infection()

        ''' Logging is not completed for Q4, so the logging process is removed.'''
        if SIMULATION_NUMBER == 4:
            pass
        else:
            self.logging_process(turn_number)

    def move_infected(self):
        """ A proportion of the infected population travel to a neighbouring city.

        The number of infected that will depart the city is determined by the global variable MOVEMENT_PROPORTION.
        The travelling people will be split evenly between the neighbouring cities.

        The current city has the number of infected people reduced.
        Each neighbouring city will have its incoming_infected parameter increased.
        Note that incoming_infected is converted to infected within the start_of_turn method of each neighbouring city.
        """

        total_infected_people_travelling = int(self.infected * MOVEMENT_PROPORTION)

        ''' Added this conditional statement as some cities may not have neighbours if all of their
        connections are removed. '''
        if SIMULATION_NUMBER == 4:
            if len(self.neighbours) > 0:
                infected_people_travelling_per_city = total_infected_people_travelling // len(self.neighbours)
            else:
                infected_people_travelling_per_city = 0
        else:
            infected_people_travelling_per_city = total_infected_people_travelling // len(self.neighbours)

        for city in self.neighbours:
            city.incoming_infected += infected_people_travelling_per_city
            self.infected -= infected_people_travelling_per_city
            self.alive -= infected_people_travelling_per_city

    def change_in_infected_numbers(self):
        """ The values of infected, survivors and dead for the city are adjusted.

        If there are still infected people remaining in the city, they will spread the infection during the
        spread_infection method.
        """

        ''' To reduce the runtime of the simulation, the minimum number of infected cases that either die or
        recover is 5 (or all cases if less than 5 people are infected). '''
        if self.infected > 5:
            num_resolved = int(max(self.infected // AVERAGE_DURATION, 5))
        else:
            num_resolved = self.infected

        num_deaths = int(num_resolved * MORTALITY_RATE)

        self.infected -= num_resolved
        self.survivors += (num_resolved - num_deaths)
        self.dead += num_deaths
        self.alive -= num_deaths

        if self.healthy_population == 0 and self.infected == 0:
            self.all_dead_flag = True

    def spread_infection(self):
        """ The infected population spreads the disease to a proportion of the healthy population.

        Note that people who have survived or have been cured can not be infected again.
        Therefore their numbers within the city reduce the infection_ratio and therefore the
        number of new infections.
        """

        uninfected_population = self.healthy_population + self.survivors + self.cured

        if uninfected_population > 0:

            infection_ratio = self.healthy_population / uninfected_population
            new_infections = int(infection_ratio * self.infected * INFECTION_RATE)

            if self.healthy_population < new_infections:
                self.infected += self.healthy_population
                self.healthy_population = 0
                self.all_infected_flag = True

                ''' Adjustment to total_infections for Q5. '''
                if SIMULATION_NUMBER == 5:
                    self.total_infections += self.healthy_population

            elif self.infected > 0:
                self.healthy_population -= new_infections
                self.infected += new_infections

                ''' Adjustment to total_infections for Q5. '''
                if SIMULATION_NUMBER == 5:
                    self.total_infections += new_infections


        ''' To reduce the runtime of the simulation, if there are no more healthy people in the city and the number of
        infected people is less than 10, then the infected people are resolved to either be dead or a survivor.'''
        if self.infected < 10 and self.healthy_population == 0:
            final_deaths = int(self.infected * MORTALITY_RATE)
            self.dead += final_deaths
            self.alive -= final_deaths
            self.survivors += (self.infected - final_deaths)
            self.infected = 0
            self.all_dead_flag = True

    def logging_process(self, turn_number):
        """ Provides a new line to the log file when one of the conditions are met.

        All logs will show the turn number, number of people alive, number of people infected, number of people dead,
        number of survivors, number of people cured, number of vaccines remaining in the city, the city name and the
        event that has occured.

        Events that will trigger a log are:
         - First case of infection in a city
         - City becoming infection free
         - Everyone in the the city being infected
         - Everyone in the city dying
         - A city has vaccines remaining

        Parameters
        -----------
        turn_number:
            The current number of turns (ie. number of rounds of infections).
        """

        ''' First case of infection in a city. '''
        if self.first_infection_flag == True and self.first_infection_log_flag == False:
            self.first_infection_log_flag = True           # This flag prevents this log from running every turn.
            LOG_FILE.write(
                "{0: >4}|{1: >7}|{2: >8}|{3: >7}|{4: >9}|{5: >7}|{6: >8}|{7: ^20}|"
                "The city has its first infected case\n".format(turn_number, self.alive, self.infected, self.dead,
                    self.survivors, self.cured, self.treatment_remaining, self.name))

        ''' City becoming infection free. Note that the below log can occur multiple times for each city. '''
        if self.first_infection_flag == True and self.infected == 0 and self.healthy_population > 0 \
                and self.infection_free_log_flag == False:
            self.infection_free_log_flag = True             # This flag prevents this log from running every turn.
            LOG_FILE.write(
                "{0: >4}|{1: >7}|{2: >8}|{3: >7}|{4: >9}|{5: >7}|{6: >8}|{7: ^20}|"
                "The city has become infection free\n".format(turn_number, self.alive, self.infected, self.dead,
                    self.survivors, self.cured, self.treatment_remaining, self.name))

        ''' Everyone in the the city being infected. Note that the below log can occur multiple times for each city. '''
        if self.all_infected_flag == True and self.all_infected_log_flag == False:
            self.all_infected_log_flag = True   # This flag prevents this log from running every turn.
            LOG_FILE.write(
                "{0: >4}|{1: >7}|{2: >8}|{3: >7}|{4: >9}|{5: >7}|{6: >8}|{7: ^20}|"
                "Everyone in the city is infected\n".format(turn_number, self.alive, self.infected, self.dead,
                    self.survivors, self.cured, self.treatment_remaining, self.name))

        ''' Everyone in the city dying. Note that the below log can occur multiple times for each city '''
        if self.all_dead_flag == True and self.all_dead_log_flag == False:
            self.all_dead_log_flag = True       # This flag prevents this log from running every turn.
            LOG_FILE.write(
                "{0: >4}|{1: >7}|{2: >8}|{3: >7}|{4: >9}|{5: >7}|{6: >8}|{7: ^20}|"
                "Everyone in the city is dead\n".format(turn_number, self.alive, self.infected, self.dead,
                    self.survivors, self.cured, self.treatment_remaining, self.name))

        ''' A city has vaccines remaining. '''
        if self.treatment_remaining > 0:
            LOG_FILE.write(
                "{0: >4}|{1: >7}|{2: >8}|{3: >7}|{4: >9}|{5: >7}|{6: >8}|{7: ^20}|"
                "This city still has vaccines remaining\n".format(turn_number, self.alive, self.infected, self.dead,
                    self.survivors, self.cured, self.treatment_remaining, self.name))

########################################################################################################################
#                               Treatment Centre Class - Part 2
########################################################################################################################
class TreatmentCentre(object):
    """
    Class for a treatment for the pandemic (Could be a cure for a virus, soldiers for a zombie apocalypse, etc.

    """

    def __init__(self, treatment_id, city):
        """
        :param treatment_id: The id of the TreatmentCentre
        :param city: The city where it is located (instance of the City class).
        """

        self.treatment = treatment_id
        self.treatment_remaining = TREATMENT_LIMIT
        self.city = city

    def move(self):
        """ Moves the treatment centre if a neighbouring city has more infected people than the current city.

        Looks at neighbouring cities of the current city to find the one with the largest number of infected people.
        The TreatmentCentre city is set as the city with the maximum.

        Note: The city will remain the same if the current city has an equal number of infected people as the
        highest neighbour.
        """

        max_infected = self.city.infected
        max_city = self.city

        for neighbour in self.city.neighbours:
            if neighbour.infected > max_infected:
                max_infected = neighbour.infected
                max_city = neighbour

        self.city = max_city

    def run_turn(self, turn_number):
        """ Runs the turn for the treatment unit.
        If movement is on, tries to move.
        Then treats any infected people in the city.
        """

        if TREATMENT_MOVEMENT:
            self.move()

        if self.city.infected <= self.treatment_remaining:
            self.treatment_remaining -= self.city.infected
            self.city.cured += self.city.infected
            self.city.infected = 0
        else:
            self.city.cured += self.treatment_remaining
            self.city.infected -= self.treatment_remaining
            self.treatment_remaining = 0

        # added the below line to feed the treatment_remaining into the City Class
        self.city.treatment_remaining = self.treatment_remaining

########################################################################################################################
#                               Engine Class
########################################################################################################################
class Engine(object):
    """ Class to actually run the simulation. """

    def __init__(self, cities, treatments):

        self.turn_number = 0
        self.cities = cities
        self.treatments = treatments

        # Attributes for collecting simulation statistics.
        self.healthy_population = []
        self.infected = []
        self.survivors = []
        self.deaths = []
        self.cured = []

        if SIMULATION_NUMBER == 5:
            self.total_infections = []

    def run_turn(self):
        """ Advances the simulation by a single turn."""

        self.turn_number += 1

        # Run the start of turn in each city.
        for city in self.cities.values():
            city.start_of_turn()

        # Run the actual turn in each city.
        for city in self.cities.values():
            city.run_turn(self.turn_number)

        ''' The below information was added for Q5. New treatment centres from the medicine distribution are added at
        this point. The distribution option can be chosen by changing the integer in the distribute method. '''
        if SIMULATION_NUMBER == 5:
            TheDistribution.distribute_4(self.turn_number)

        # Run the turn for each treatment centre
        for treatment in self.treatments.values():
            treatment.run_turn(self.turn_number)

        # Gather the statistics
        self.infected.append(sum([city.infected for city in self.cities.values()]))
        self.healthy_population.append(sum([city.healthy_population for city in self.cities.values()]))
        self.survivors.append(sum([city.survivors for city in self.cities.values()]))
        self.deaths.append(sum([city.dead for city in self.cities.values()]))
        self.cured.append(sum([city.cured for city in self.cities.values()]))

        ''' The below extra statistics were added for Q5 to count the total infections.'''
        if SIMULATION_NUMBER == 5:
            self.total_infections.append(sum([city.total_infections for city in self.cities.values()]))

########################################################################################################################
#                               Other functions
########################################################################################################################
def convert_lat_long(lat, long):
    """ Converts a latitude and longitude pair into an x, y pair of map-coordinates.
    :param lat: the latitude value.
    :param long: the longitude value.
    :return an (x, y) tuple of coordinates, where x and y are floats between 0.0 and 1.0.
    """

    x_diff = MAP_RIGHT - MAP_LEFT
    y_diff = MAP_TOP - MAP_BOTTOM

    return (long - MAP_LEFT) / x_diff, (lat - MAP_BOTTOM) / y_diff


def get_city_data(file_name):
    """ Reads in city and connection data from the specified file.
    Format of the file is:
    lat,long,name,population
    ### - break point between the two sections.
    city_1,city_2
    """

    input_file = open(file_name, mode="r")

    # Get the cities first
    cities = dict()
    for line in input_file:
        # Check for the end of the city information
        if line[0:3] == "###":
            break
        line = line.strip().split(",")

        lat = float(line[0])
        long = float(line[1])
        name = line[2]
        population = int(line[3])
        cities[name] = City(lat, long, name, population)

    # Now read in the connections
    for line in input_file:
        city_1, city_2 = line.strip().split(",")
        cities[city_1].add_neighbour(cities[city_2])
        cities[city_2].add_neighbour(cities[city_1])

    return cities


def get_initial_parameters(scenario_number):
    """
    Gets the initial parameters and treatment options for the given scenario.
    :param scenario_number: The scenario being run.
    :return: a tuple of (stopping, treatment move, treat lim, mortality, infection rt, movement prop, average dur).
    """

    #       Stop    TrtMo   TRtL    MoR     InR     MoP     AvgDur
    scenario_dict = {
        0: (0,      False,  0,      1.0,    4.0,    0.1,    4.0),
        1: (150,    False,  0,      0.1,    0.4,    0.25,   3.0),
        2: (150,    True,   150000, 0.1,    0.4,    0.25,   3.0),
        3: (0,      True,   150000, 0.25,   1.5,    0.1,    4.0),
        4: (20,     False,  0,      0.3,    1.0,    0.05,   4.0),
        5: (0,      False,  1000,   0.05,   0.7,    0.1,    3.0)

    }

    if scenario_number not in scenario_dict:
        scenario_number = 0

    return scenario_dict[scenario_number]


def set_initial_state(scenario_number, engine):
    """
    Sets the initial infection cases and treatment centres.
    The initial infection cases are added using the 'incoming_infected' attribute.
    Modifies the state of cities and treatment centres in the engine directly.
    :param scenario_number: The scenario being run.
    :param engine: the engine running the simulation.
    :return: None
    """

    state_dict = {
        0: (tuple(), (("Alice Springs", 1000),)),
        1: (tuple(), (("Rockhampton", 1000), ("Brisbane", 10000), ("Gold Coast", 1000))),
        2: (("Sydney", "Melbourne", "Adelaide"), (("Rockhampton", 1000), ("Brisbane", 10000), ("Gold Coast", 1000))),
        3: (("Sydney", "Perth", "Melbourne"), (("Canberra", 5000), ("Cairns", 5000))),
        4: (tuple(), (("Rockhampton", 1000), ("Brisbane", 10000), ("Gold Coast", 1000))),
        5: (("Sydney", "Perth", "Melbourne"), (("Canberra", 5000), ("Cairns", 5000)))
    }
    if scenario_number not in state_dict:
        scenario_number = 0

    for index, city in enumerate(state_dict[scenario_number][0]):
        engine.treatments[index] = TreatmentCentre(index, engine.cities[city])

    for city, cases in state_dict[scenario_number][1]:
        engine.cities[city].incoming_infected = cases

        ''' The below code adds the starting infections to the total_infections count for Q5. '''
        if SIMULATION_NUMBER == 5:
            engine.cities[city].total_infections = cases

def animate_map(data, engine, map_image, sp1, sp2, sp3, sp4):

    if not engine:
        return

    # Check for termination conditions here.
    if (engine.infected and engine.infected[-1] == 0) or (STOPPING_CONDITIONS and
                                                          engine.turn_number >= STOPPING_CONDITIONS):
        get_input = input("The simulation has ended; press 'Enter' to finish.")
        LOG_FILE.close()                        #close log file prior to exit

        if SIMULATION_NUMBER == 5:                                    # The below code will finalize the logfile for Q5
            LOG_FILE_Q5.write("Option 4: Max healthy population over 1000\n\tTotal infection count (each turn) = {}\n"
                              "Total infected at end of turn 20 = {}\n\n".format(
                engine.total_infections,engine.total_infections[-1]))
            LOG_FILE_Q5.close()                 #close log file prior to exit for Q5

        sys.exit()

    # Advance the simulation by 1 turn
    engine.run_turn()

    # Display the map and statistics
    height, width = len(map_image), len(map_image[0])

    sp1.clear()
    sp1.set_axis_off()
    sp1.imshow(map_image)
    sp1.set_title("Pandemic Simulation - {} turns".format(engine.turn_number))

    # Plot the cities
    for city in engine.cities.values():
        x, y = convert_lat_long(city.lat, city.long)
        if city.infected > 0.1 * city.initial_population:
            color = "red"
        elif city.infected > 0.01 * city.initial_population:
            color = "orange"
        elif city.infected > 0:
            color = "yellow"
        elif city.healthy_population == 0 and city.survivors == 0 and city.cured == 0:
            color = "black"
        else:
            color = "blue"

        sp1.plot(x * width, (1 - y) * height, "o", markersize=10.0, color=color)
        if city.initial_population > 150000:
            sp1.text(x * width + 12, (1 - y) * height + 12, s=city.name)

        # Uncomment the following four lines if you wish to see the connections on the map during simulation.
        for neighbour in city.neighbours:
            if neighbour < city:
                nx, ny = convert_lat_long(neighbour.lat, neighbour.long)
                sp1.plot((x * width, nx * width), ((1 - y) * height, (1 - ny) * height), color="black")

    # Plot the line graphs
    sp2.clear()
    sp2.plot(range(1, engine.turn_number + 1), engine.healthy_population, color="blue", label="Healthy")
    sp2.plot(range(1, engine.turn_number + 1), engine.infected, color="red", label="Infected")
    sp2.set_xlim([1, engine.turn_number + 15])
    sp2.legend(loc="right")
    sp2.set_xlabel("Turns")
    sp2.set_ylabel("People")
    sp2.set_title("Simulation Statistics")
    if (max(engine.healthy_population) > 10 * max(engine.infected) or
            max(engine.healthy_population) * 10 < max(engine.infected)):
        sp2.set_yscale("log")

    sp3.clear()
    sp3.plot(range(1, engine.turn_number + 1), engine.survivors, color="green", label="Survivors")
    sp3.plot(range(1, engine.turn_number + 1), engine.deaths, color="black", label="Deaths")
    sp3.set_xlim([1, engine.turn_number + 15])
    sp3.legend(loc="right")
    sp3.set_xlabel("Turns")
    sp3.set_ylabel("People")
    if (max(engine.survivors) > 10 * max(engine.deaths) or
            max(engine.survivors) * 10 < max(engine.deaths)):
        sp3.set_yscale("log")

    sp4.clear()
    sp4.plot(range(1, engine.turn_number + 1), engine.cured, color="purple", label="Cured")
    sp4.set_xlim([1, engine.turn_number + 15])
    sp4.legend(loc="right")
    sp4.set_xlabel("Turns")
    sp4.set_ylabel("People")

########################################################################################################################
#                               Main Function - Part 4
########################################################################################################################
if __name__ == "__main__":

    # Set the scenario parameters
    STOPPING_CONDITIONS, TREATMENT_MOVEMENT, TREATMENT_LIMIT, MORTALITY_RATE, \
        INFECTION_RATE, MOVEMENT_PROPORTION, AVERAGE_DURATION = get_initial_parameters(SIMULATION_NUMBER)

    # Get the city data and population
    cities = get_city_data("final_city_data.csv")
    treatments = dict()

    # Create the engine that will run the simulation
    engine = Engine(cities, treatments)

    # Setup initial infected cases and treatment centres
    set_initial_state(SIMULATION_NUMBER, engine)

    ####################################################################################################################
    #                               Answer to Q4 goes here
    ####################################################################################################################
    if SIMULATION_NUMBER == 4:

        '''
        This section details the process of adding additional road block functionality to the simulation.
        
        I have assumed that if a road block occurs, the number of travelling people from the city are distributed
        evenly to the other available connections.
        
        I first started by creating a new log file for this question as my original logfile wasn't immediately useful
        and I didn't want to update it as it was working well for the earlier questions. This log file will
        append the results of each successive trial.
        '''

        if not os.path.exists(os.path.join(os.getcwd(), "logsQ4")):
            os.mkdir(os.path.join(os.getcwd(), "logsQ4"))

        LOG_FILE_Q4 = open(os.path.join(os.getcwd(), "logsQ4", "COMP7230_Assignment_2_LogQ4.txt"), mode="a")

        '''
        I decided to create a new class for the road blocks. This could very easily be completed as a series of
        functions. However, I wanted to keep the functionality grouped together, so a new class seemed acceptable.
        
        The class is very simple. It takes in two cities and then has the create_block method which implements
        the remove_neighbour method already present in the City class.
        
        Note that there is a string dunder method to assist with the logging.
        
        Also note that the create_block method has been written in a way that allows for the same road to be
        blocked twice (the second block will have no effect).
        '''

        class RoadBlock(object):
            """ Removes a connection between two cities.

            Closing the connection between two cities prevents any infected people from travelling between
            the two cities.
            """

            def __init__(self,city_1,city_2):
                """ Initializes the RoadBlock object.

                Parameters
                ----------
                city_1: City
                    City at one end of the blocked connection
                city_2: City
                    City at other end of the blocked connection
                """
                self.city_1 = city_1
                self.city_2 = city_2

            def __str__(self):
                """ This allows the road connections to be printed in the preferred format."""
                return "('{}','{}')".format(self.city_1,self.city_2)

            def create_block(self):
                """ This creates a block between cities

                The if statements allow the method to run, even if the neighbour has already been removed.
                """

                if self.city_1 in self.city_2.neighbours:
                    self.city_2.remove_neighbour(self.city_1)
                if self.city_2 in self.city_1.neighbours:
                    self.city_1.remove_neighbour(self.city_2)

        '''
        I innitialy started to answer this question by taking some educated guesses.
        
        Below were the four roadblock options that I considered. Each option is a list of three tuples.
        Note that these are not used in my solution, but left in as a reference.
        
        I knew the starting conditions for Option 4 (Rockhampton (1000), Brisbane(10,000), Gold Coast (1000)
        and used this information to have some educated guesses at the best road block locations.
        
        I thought that with Option 4 I was very close to the final solution.
        '''
        # Q4_Option_1 = [('Gold Coast','Coffs Harbour'),('Gold Coast','Tamworth'),('Mackay','Rockhampton')]
        # Q4_Option_2 = [('Broome','Darwin'),('Kalgoorlie Boulder','Port Augusta'),('Kalgoorlie Boulder','Alice Springs')]
        # Q4_Option_3 = [('Sydney','Newcastle'),('Sydney','Wollongong'),('Sydney','Canberra')]
        # Q4_Option_4 = [('Brisbane','Sunshine Coast'),('Brisbane','Toowoomba'),('Brisbane','Gold Coast')]

        '''
        The below code allowed me to select my preferred road block options and execute the road blocks.
        Note that these are not used in my solution, but left in as a reference.
        '''
        #roadblocks =  Q4_Option_4

        #RoadBlock1 = RoadBlock(cities[roadblocks[0][0]], cities[roadblocks[0][1]])
        #RoadBlock2 = RoadBlock(cities[roadblocks[1][0]], cities[roadblocks[1][1]])
        #RoadBlock3 = RoadBlock(cities[roadblocks[2][0]], cities[roadblocks[2][1]])

        #RoadBlock1.create_block()
        #RoadBlock2.create_block()
        #RoadBlock3.create_block()

        '''
        I then decided to attempt to brute force a solution. This would take a much more involved effort.
        
        I first created the function create_road_tuples to extract the road connections
        as a list of tuple pairs for each road connection.
        '''
        def create_road_tuples(file_name):
            """ Creates a list of tuples of all of the road connections from the input file.

            Parameter
            ---------
            file_name: str
                The file that is to be accessed by the function
            Return
            --------
            road_tuples: list
                A list of tuples in the form ('city_1'),('city_2')
            """

            road_list = []
            road_tuples = []

            with open(file_name, 'r') as input_file:

                for line in input_file:
                    ''' Check for the end of the city information '''
                    if line[0:3] == "###":
                        break
                    else:
                        pass

                ''' Extract city1 and city2'''
                for line in input_file:
                    new_line = line.strip()
                    comma = new_line.find(',')

                    city1 = new_line[0:comma]
                    city2 = new_line[comma + 1:]

                    road_list.append(city1)
                    road_list.append(city2)

            ''' Create a tuple for each city pair. '''
            for i in range(len(road_list)):
                if i % 2 == 0:
                    road_tuples.append((road_list[i], road_list[i + 1]))

            return road_tuples

        '''The below variable all_roads contains all the road connection tuples'''
        all_roads = create_road_tuples("final_city_data.csv")

        '''
        The below function simulation_sans_animation runs the program without running the animation.
        
        It will terminate with the same termination conditions as the animation.
        
        Note that I have wrapped the animation function at the bottom of this Python file in an if statement
        for SIMULATION_NUMBER == 4 to avoid running it.
        '''

        def simulation_sans_animation(engine,min_deaths):
            """ Run the simulation model without showing the animation.

            For Q4, we are only interested in the total number of deaths.
            This value is returned from this function.

            Paramters
            ----------
            engine: Engine

            min_deaths: int
                The current minimum number of deaths from running multiple simulations
            Return
            --------
            engine.deaths[-1]: int
                The total deaths of the simulation
            """

            for _ in range(STOPPING_CONDITIONS):
                if not engine:
                    return

                engine.run_turn()

                ''' Check for termination conditions here. '''
                if (engine.infected and engine.infected[-1] == 0) or (
                        STOPPING_CONDITIONS and engine.turn_number >= STOPPING_CONDITIONS) or (
                        engine.deaths[-1] > min_deaths):
                    return engine.deaths[-1]

        '''
        The below function runs multiple versions of the simulation.
        The initial parameters, cities, treatments and engine are reset during every simulation. This was done
        because attempting to set a default city and engine and then copying it lead to aliasing errors. I also
        attempted to use copy.deepcopy(), but this didn't seem to work either.
        
        So I settled for a semi-brute force option. 
        
        My run_multiple_simulations function isn't a complete brute force O(n^3), it instead has two loops O(n^2).

        The variable default_block has three road connections. One of these default option is selected for RoadBlock3.
        The function then finds the optimal solution assuming the one fixed road block.
        
        I ran this simulation multiple times, cycling through different options.
        
        With the current default_block of ('Brisbane', 'Sunshine Coast'), ('Brisbane', 'Toowoomba')
        and ('Mackay', 'Rockhampton'), by locking any one of the three, it will still yield the same answer.
        
        I can not be confident that this is the complete optimum solution, but I am fairly confident it is
        the optimum solution.
        '''

        def run_multiple_simulations():
            ''' Runs multiple iterations of the pandemic simulation

            An option must be selected from the default_block variable for RoadBlock3.
            RoadBlock1 and Roadblock2 will be iterated through until the optimum combination is found.
            '''
            default_block = [('Brisbane', 'Sunshine Coast'), ('Brisbane', 'Toowoomba'), ('Mackay', 'Rockhampton')]
            min_deaths = 1000000
            blocks = ()

            '''loop through the first and second road blocks'''
            for i in range(len(all_roads)-1):
                for j in range(len(all_roads) - 1):

                    ''' Reset the City and Engine objects for each new simulation run. '''
                    new_cities = get_city_data("final_city_data.csv")
                    new_engine = Engine(new_cities, treatments)
                    set_initial_state(SIMULATION_NUMBER, new_engine)

                    ''' Each of the three RoadBlocks are initialised. '''
                    RoadBlock1 = RoadBlock(new_cities[all_roads[i][0]], new_cities[all_roads[i][1]])
                    RoadBlock2 = RoadBlock(new_cities[all_roads[j][0]], new_cities[all_roads[j][1]])
                    RoadBlock3 = RoadBlock(new_cities[default_block[2][0]], new_cities[default_block[2][1]])

                    ''' The create_block method is implemented for each of the three road blocks. '''
                    RoadBlock1.create_block()
                    RoadBlock2.create_block()
                    RoadBlock3.create_block()

                    ''' Calculate the deaths for the simulation and compare to the current minimum. '''
                    deaths_at_turn_20 = simulation_sans_animation(new_engine,min_deaths)

                    if deaths_at_turn_20 < min_deaths:
                        min_deaths = deaths_at_turn_20
                        blocks = "{},{} and {}".format(RoadBlock1,RoadBlock2,RoadBlock3)

            LOG_FILE_Q4.write("Min deaths = {}\t\tRoad blocks at: {}\n".format(min_deaths,blocks))
            LOG_FILE_Q4.close()  # close log file prior to exit for Q4


        ''' Start the function to run the multiple simulations. '''
        run_multiple_simulations()

        '''
        This provides the final solution of the road blocks placed at:
        ('Brisbane', 'Sunshine Coast'), ('Brisbane', 'Toowoomba'), ('Mackay', 'Rockhampton')
        This solution ends with 841,411 total deaths.
        '''

    ####################################################################################################################
    #                               Answer to Q5 goes here
    ####################################################################################################################
    if SIMULATION_NUMBER == 5:

        '''
        This section details the process of adding additional medicine distribution functionality to the simulation.
        
        Firstly, a few notes on how I interpreted this question. "minimise the total number of people who get infected 
        prior to the end of turn 20". Although there is statistics within the engine for the number of infected, I don't
        believe this is a count of the total number of people who get infected. I will only be counting new infections
        during the spread_infection method within the Cities object (Line 393 and Line 401). This is because an infected
        person who arrives from another city will already have been counted in the original city.
        
        I have added an additional parameter to the city class, total_infections, and this increases in value each 
        turn during the spread_infections method. Note that total_infections includes the original 5000 each in
        Canberra and Cairns. These values are added on line 691.
        
        I have also added a new line item in the engine class, under statistics, for total infections (line 587).
        
        
        This problem can not be brute forced as there are 39^20 different options.
        
        Note that in my final solution, there are only 7 cities that receive medical centres.
        A brute force, even when only considering these cities would still require 7^20 simulations.
        '''
        
        '''
        I first started by creating a new log file for this question. This log file is similar to the one used for Q4.
        '''

        if not os.path.exists(os.path.join(os.getcwd(), "logsQ5")):
            os.mkdir(os.path.join(os.getcwd(), "logsQ5"))

        LOG_FILE_Q5 = open(os.path.join(os.getcwd(), "logsQ5", "COMP7230_Assignment_2_LogQ5.txt"), mode="a")

        '''
        The question also requires the number of infections to be minimised by the end of Turn 20.
        So the below statement overrides the original parameters and sets the stopping conditions to 20. 
        '''
        STOPPING_CONDITIONS = 20

        '''
        To answer this question I have created a new class called MedicalDistribution.
        The medical distribution class is initialized with an initial index of the treatment locations and also
        a set of cities where there are currently treatment locations.
        Note that I created the functionality of this cities set, however I didn't end up using it (except for
        Option 2).
        
        Within the MedicalDistribution object, there are numbered distribute methods. Each one shows, in order,
        the options that I tried to attempt to optimize the medical distribution.
        
        The distribute method is called on Line 572 of the engine function.
        Note that distribute_4 is currently selected.
        
        Note that for each of the options, The 20 distribution locations will be printed to the console.
        '''

        class MedicalDistribution(object):
            """ Determines the location of new medical centres.

            Different distribute options are available for use within the class.
            Each option will select a city for a new medical centre to be placed.
            """

            def __init__(self):
                """ Initialises the MedicalDistribution class.

                Attributes
                ----------
                initial_index: int
                    Calculates the most recently used treatment index. New treatment centres will continue with the
                    existing numbering system.
                distribution_set: set
                    A set of cities with treatment centres.
                """
                self.initial_index = max([index for index in engine.treatments.keys()])
                self.distribution_set = set([treatment.city for treatment in engine.treatments.values()])

            def distribute_1(self,turn_number):
                """ Distribute to largest number of infections.

                Distribution option 1 sends the new medicine distribution to the city with the highest
                current infected population.

                Parameters
                ----------
                turn_number: int
                    The current number of turns (ie. number of rounds of infections).
                """
                index = self.initial_index + turn_number
                max_infected = 0
                distribution_location = City

                for city in cities.values():
                    if city.infected > max_infected:
                        max_infected = city.infected
                        distribution_location = city

                treatments[index] = TreatmentCentre(index,distribution_location)

                print("{}".format(distribution_location))

            def distribute_2(self, turn_number):
                """ Distribute to new cities where possible.

                Distribution Option 2 will only create a treatment centre if a treatment centre doesn't already
                exist in the city.If there are no cities left that have infections and do not have a treatment centre,
                then the medical distribution defaults to the city with the largest infected population.

                Parameters
                ----------
                turn_number: int
                    The current number of turns (ie. number of rounds of infections).
                """
                index = self.initial_index + turn_number
                max_infected = 0
                new_location_flag = False
                distribution_location = City
                distribution_location_max = City

                for city in cities.values():
                    if city.infected > max_infected:
                        max_infected = city.infected
                        distribution_location_max = city

                max_infected = 0

                for city in cities.values():
                    if city.infected > max_infected and city not in self.distribution_set:
                        max_infected = city.infected
                        distribution_location = city
                        new_location_flag = True

                self.distribution_set.add(distribution_location)

                if not new_location_flag:
                    distribution_location = distribution_location_max

                treatments[index] = TreatmentCentre(index,distribution_location)

                print("{}".format(distribution_location))

            def distribute_3(self, turn_number):
                """ Distribute based on manual selection.

                Distribution Option 3 places a medical centre at manually chosen locations.

                Once the manually chosen cities have been distributed, the distribution defaults to the city with
                the largest infected population.

                Parameters
                ----------
                turn_number: int
                    The current number of turns (ie. number of rounds of infections).
                """

                index = self.initial_index + turn_number
                max_infected = 0
                distribution_location = City

                for city in cities.values():
                    if city.infected > max_infected:
                        max_infected = city.infected
                        distribution_location = city

                manual_cities_strings = ['Darwin', 'Alice Springs', 'Port Augusta', 'Adelaide']
                manual_cities = [cities[x] for x in manual_cities_strings]

                if turn_number < 5:
                    distribution_location = manual_cities[turn_number-1]
                    treatments[index] = TreatmentCentre(index, distribution_location)
                else:
                    treatments[index] = TreatmentCentre(index, distribution_location)

                print("{}".format(distribution_location))

            def distribute_4(self, turn_number):
                """ Distribute to minimum of 1000 people. Based on healthy population.

                Distribution Option 4 will only send vaccines to cities with 1000 or more infected people,
                but will select the city with the highest number of healthy people.

                Parameters
                ----------
                turn_number: int
                    The current number of turns (ie. number of rounds of infections).
                """
                index = self.initial_index + turn_number
                max_healthy_pop = 0
                distribution_location = City

                for city in cities.values():
                    if city.infected > 1000 and city.healthy_population > max_healthy_pop:
                        max_healthy_pop = city.healthy_population
                        distribution_location = city

                treatments[index] = TreatmentCentre(index,distribution_location)

                print("{}".format(distribution_location))

            def distribute_5(self, turn_number):
                """ Distribute based on new infections

                Distribution Option 5 will only send vaccines to cities with 1000 or more infected people,
                but it will select the city that will prevent the most new infections occurring on that turn.

                Parameters
                ----------
                turn_number: int
                    The current number of turns (ie. number of rounds of infections).
                """
                index = self.initial_index + turn_number
                max_new_infections = 0
                distribution_location = City

                for city in cities.values():

                    city_uninfected_population = city.healthy_population + city.survivors + city.cured

                    if city_uninfected_population > 0:  # This will prevent division by zero
                        city_new_infections = city.infected * city.healthy_population / city_uninfected_population
                    else:
                        break

                    if city_new_infections > max_new_infections:
                        max_new_infections = city_new_infections
                        distribution_location = city

                treatments[index] = TreatmentCentre(index,distribution_location)

                print("{}".format(distribution_location))

            def distribute_6(self, turn_number):
                """ Distribute based on new infections. Forced starting locations.

                Distribution Option 6 will only send vaccines to cities with 1000 or more infected people,
                but it will select the city that will prevent the most new infections occurring on that turn.

                There is the option to input manual cities that will override the above condition.

                Parameters
                ----------
                turn_number: int
                    The current number of turns (ie. number of rounds of infections).
                """
                index = self.initial_index + turn_number
                max_new_infections = 0
                distribution_location = City

                manual_cities = ['Cairns', 'Cairns', 'Cairns', 'Cairns']
                man_dist = [cities[x] for x in manual_cities]

                if turn_number < 5:
                    distribution_location = man_dist[turn_number - 1]
                    treatments[index] = TreatmentCentre(index, distribution_location)
                else:
                    for city in cities.values():

                        city_uninfected_population = city.healthy_population + city.survivors + city.cured

                        if city_uninfected_population > 0:          # This will prevent division by zero
                            city_new_infections = city.infected * city.healthy_population / city_uninfected_population
                        else:
                            break

                        if city_new_infections > max_new_infections:
                            max_new_infections = city_new_infections
                            distribution_location = city

                treatments[index] = TreatmentCentre(index,distribution_location)

                print("{}".format(distribution_location))

        '''Initialize the Medical Distribution Class for use within the engine.'''
        TheDistribution = MedicalDistribution()

        '''
        After looking at all 6 of my options, Number 4 results in the lowest total infections. It's definitely possible 
        that this number could be refined, however I believe that this is a very decent solution.
        
        The order of distributions was:
        Canberra
        Canberra
        Canberra
        Canberra
        Canberra
        Townsville
        Darwin
        Cairns
        Townsville
        Darwin
        Cairns
        Darwin
        Townsville
        Cairns
        Cairns
        Cairns
        Canberra
        Albury Wodonga
        Alice Springs
        Wagga Wagga
        This resulted in a total of 88,482 infections at the end of turn 20.
        '''
    ####################################################################################################################


    if SIMULATION_NUMBER == 4:
        pass
    else:
        # Get the map and fade it for better viewing.
        aus_map = im.imread("Aus_Map.PNG")
        aus_map[:,:,3] = (aus_map[:,:,3] * 0.6)

        # Setup the plot layout
        fig = plt.figure(figsize=[10, 13])
        sps1, sps2, sps3, sps4 = gridspec.GridSpec(4, 1, height_ratios=(10, 1, 1, 1))

        sp1 = plt.subplot(sps1)
        sp2 = plt.subplot(sps2)
        sp3 = plt.subplot(sps3)
        sp4 = plt.subplot(sps4)

        # Produce the animation and run the simulation.
        display = animation.FuncAnimation(fig, animate_map, interval=100, repeat=False,
                                          fargs=(engine, aus_map, sp1, sp2, sp3, sp4),
                                          frames=None)
        plt.show()
