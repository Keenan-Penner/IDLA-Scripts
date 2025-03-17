"""
Python file for simulating EDEN (?) process.
"""
# imports
import copy 
import os
import random

from typing import List
from math import *
import matplotlib.pyplot as plt
import numpy

from tqdm import tqdm


class Eden:
    """
    Class defining the EDEN process
    """
    def __init__(
        self,
        birth_scale: float = 10,
        time_scale: float = 0.1,
        final_size: int = 100,
        do_plot: bool = False,
        save_path: str = "C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\data\\eden",
        debug: bool = False,
        sim_number: int = 0
    ):
        """
        Args:
            birth_scale (float): exponential scale for birth. Default is 10.
            time_scale (float): exponential scale for movement. Default is 0.1.
            final_size (int): Final size of the aggregate. Default is 100.
            do_plot (bool): whether to plot the aggregate at each step. Default is False.
            grid_size (int): size of the grid (used for plotting). Default is 100.
            save_path (str): path to save the plots. Default is "C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\data\\eden".
        might be good to put here some explanation of the attributes of the class
        """
        self.birth_scale = birth_scale
        self.time_scale = time_scale
        self.final_size = final_size
        self.do_plot = do_plot
        self.grid_size = floor(sqrt(final_size/2)+1)
        self.save_path = save_path
        self.debug = debug 
        self.sim_number = sim_number
        self.save_path = os.path.join(self.save_path, f"sim{self.sim_number}")
        # check if save_path exists
        if not os.path.exists(self.save_path):
            # create the directory
            print(f"Creating directory {self.save_path}")
            os.makedirs(self.save_path)

        # initialize the aggregate
        self.aggregate = [[0, 0]]
        self.times = [numpy.random.exponential(self.birth_scale)]
        self.sites = [[0, 0]]
        self.births = [True] # says whether or not the site is free

    def single_step(self):
        """
        Simulate a single step of the EDEN process.
        """
        # here we assume that self.times, self.sites, self.births
        # are sorted by increasing time
        new_site_in_agg = False
        while not new_site_in_agg:
            time = self.times[0]
            birth = self.births[0]
            site = self.sites[0]
            if birth:
                if site not in self.aggregate:
                    # cannot spawn a particle on a site that isn't in aggregate
                    pass
                else:
                    # generate time of particle move
                    if self.debug:
                        print("Particle born")
                    new_time = time + numpy.random.exponential(self.time_scale)
                    self.times[0] = new_time
                    self.births[0] = False
            else:
                # do a random move
                site2visit = self.move(copy.deepcopy(site))
                if site2visit in self.sites:
                    # site may be occupied by a particle or free (birth programmed)
                    index = self.sites.index(site2visit)
                    if self.births[index]:
                        if self.debug:
                            print("Particle moved to site in aggregate")
                        # the site we want to move to is free
                        new_time = time + numpy.random.exponential(self.time_scale)
                        self.times[0] = new_time
                        self.births[0] = False # site is now occupied
                        self.sites[0] = site2visit
                        # remove the particle that was supposed to be born on site2visit
                        # since there is a particle moving there before birth
                        # possible since exponential is memoryless
                        self.times.pop(index)
                        self.sites.pop(index) 
                        self.births.pop(index)
                        new_time = time + numpy.random.exponential(self.birth_scale)
                        self.times.append(new_time)
                        self.births.append(True)
                        self.sites.append(site)
                    else:
                        # the site we want to move to is occupied
                        # we stay on the same site
                        new_time = time + numpy.random.exponential(self.time_scale)
                        self.times[0] = new_time
                else:
                    if self.debug:
                        print("Particle is added to aggregate")
                    # the site has not been visited yet
                    self.aggregate.append(site2visit)
                    # the current particle is killed
                    # and we program a birth on site2visit and on site
                    new_time = time + numpy.random.exponential(self.birth_scale)
                    self.times[0] = new_time
                    self.births[0] = True
                    new_time = time + numpy.random.exponential(self.birth_scale)
                    self.times.append(new_time)
                    self.births.append(True)
                    self.sites.append(site2visit)
                    new_site_in_agg = True
            # sort the lists by increasing time
            assert len(self.aggregate) == len(self.sites)
            times, sites, births = zip(*sorted(zip(self.times, self.sites, self.births)))
            self.times = list(times)
            self.sites = list(sites)
            self.births = list(births)
        if self.do_plot:
            self.plot()

    def simulate(self):
        """
        Simulate the EDEN process.
        """
        for _ in tqdm(range(self.final_size)):
            self.single_step()
        self.plot() # plots the aggregate at the final step 
        txt_file_path = os.path.join(self.save_path, 'parameters.txt')
        with open(txt_file_path, 'w') as file:
            file.write(f"Birth scale: lambda = {1/self.birth_scale}\n")
            file.write(f"Time scale: mu = {1/self.time_scale}\n")
            file.write(f"Final size: {self.final_size}\n")

    def plot(self):
        """
        Plot the aggregate.
        """
        xline = [self.aggregate[i][0] for i in range(len(self.aggregate))]
        yline = [self.aggregate[i][1] for i in range(len(self.aggregate))]
        plt.clf()
        plt.scatter(xline, yline, s = 2, color = 'C0')
        plt.axis('square')
        plt.xlim([-self.grid_size, self.grid_size])
        plt.ylim([-self.grid_size, self.grid_size])
        plt.savefig(os.path.join(self.save_path, f"{len(self.aggregate)}.png"), dpi=500)

    @staticmethod
    def move(site: List[int]):
        """
        Do a random walk move from site.

        Args:
            site (List[int]): site to move from

        Returns:
            site (List[int]): updated site
        """
        prob = random.random()
        if prob < 0.25:
            # move right
            site[0] += 1
        elif prob < 0.5:
            # move left
            site[0] -= 1
        elif prob < 0.75:
            # move up
            site[1] += 1
        else:
            # move down
            site[1] -= 1
        return site

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--birth_scale", type=float, default=10)
    parser.add_argument("--time_scale", type=float, default=0.1)
    parser.add_argument("--final_size", type=int, default=100)
    parser.add_argument("--do_plot", action="store_true")
    parser.add_argument("--save_path", type=str, default="C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\Scripts IDLA\\data\\eden")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--sim_number", type=int, default=0)
    args = parser.parse_args()

    process = Eden(
        birth_scale=args.birth_scale,
        time_scale=args.time_scale,
        final_size=args.final_size,
        do_plot=args.do_plot,
        save_path=args.save_path,
        debug=args.debug,
        sim_number=args.sim_number
    )
    process.simulate()
