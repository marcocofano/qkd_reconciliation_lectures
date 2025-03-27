import numpy as np
from error_correction.binary_entropy import (
    crossprob_from_params,
    efficiency_from_params,
)
import os 
import re
from error_correction.outputs import StatusDecodingPerformance
from functools import partial

# tot, fec, fer, bec, ber
import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, data_dirs):
        self.data_dirs = data_dirs

    # --- Helper Functions for Efficiency Mappings ---
    # def _efficiency_from_p(self, p, cr):
    #     """Forward mapping: compute efficiency f from channel parameter p."""
    #     return efficiency_from_params( cr=cr
    #
    # def _p_from_efficiency(self, f, cr):
    #     """Inverse mapping: compute channel parameter p from efficiency f."""
    #     # If f is below the valid minimum (f < 1-cr), return the only valid value.
    #     return partial(crossprob_from_params, cr=cr)

    def _setup_plot(self, title, xlabel, ylabel, cr):
        """
        Create and configure a matplotlib figure and axes.

        This method also adds a secondary x-axis (for efficiency) using lambda functions
        that capture the fixed code rate (cr).
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        # Setup secondary axis with the forward and inverse functions
        secax = ax.secondary_xaxis(
            "top",
            functions=(
                lambda p: efficiency_from_params(p, cr),
                lambda f: crossprob_from_params(f, cr),
            ),
        )
        secax.set_xlabel("Efficiency f = (1-cr)/h(p)")
        return fig, ax

    # --- Plotting a Single Performance Curve ---
    def _plot_performance(self, ax, performance, cr):
        """
        Plot the FER curve of a single StatusDecodingPerformance instance on the given axes.

        Args:
            ax: matplotlib Axes to plot on.
            performance: an instance of StatusDecodingPerformance.
            cr: Code rate used for efficiency calculation.
        """
        # Convert the keys to floats.
        x_values = np.array([float(key) for key in performance.fer.keys()])
        y_values = list(performance.fer.values())
        label = f"{performance.channel}_{performance.decoder}_{performance.max_iter}_{performance.code}"
        ax.plot(x_values, y_values, marker="o", linestyle="-", label=label)

    # --- Public Methods ---
    def plot(self, performance, cr=0.5):
        """
        Plot a single StatusDecodingPerformance instance.

        Args:
            performance: an instance of StatusDecodingPerformance.
            cr: Code rate used in the efficiency calculation.
        """
        title = "Status Decoding Performance"
        xlabel = "Channel Parameter (p)"
        ylabel = "FER"
        fig, ax = self._setup_plot(title, xlabel, ylabel, cr)
        self._plot_performance(ax, performance, cr)
        ax.legend()
        plt.show()

    def plot_from_dir(self, regex_pattern, cr=0.5):
        """
        Search the output directory for JSON files matching regex_pattern,
        load them into StatusDecodingPerformance objects, and plot their FER curves on one plot.

        Args:
            regex_pattern: A regex pattern to filter file names.
            cr: Code rate used in the efficiency calculation.
        """
        out_dir = self.data_dirs.outputs
        print(out_dir)
        all_files = os.listdir(out_dir)
        matching_files = [f for f in all_files if re.match(regex_pattern, f)]
        if not matching_files:
            print("No files matching the pattern were found.")
            return

        performances = []
        for filename in matching_files:
            # Assume StatusDecodingPerformance.read_from_json returns an instance.
            performance = StatusDecodingPerformance.read_from_json(
                filename, self.data_dirs
            )
            if performance is not None:
                performances.append(performance)

        if not performances:
            print("No valid performance data found.")
            return

        title = "Status Decoding Performance (Multiple Files)"
        xlabel = "Channel Parameter (p)"
        ylabel = "FER"
        fig, ax = self._setup_plot(title, xlabel, ylabel, cr)

        for performance in performances:
            self._plot_performance(ax, performance, cr)
        ax.legend()
        plt.show()

    def _plot_old(self, data: StatusDecodingPerformance, cr: float, save: bool = False):
        """
        Plot the FER vs. channel parameter, with a secondary x-axis showing efficiency.

        Efficiency is defined as: f = (1-CR) / h(p)
        where h(p) = -p*log2(p) - (1-p)*log2(1-p) is the binary entropy.

        Args:
            data: An object that has an attribute `fer`, a dictionary where keys are channel parameters (p)
                  and values are FER values.
            cr: Code rate (CR) used in the efficiency calculation (default is 0.5).
        """

        efficiency_from_p = lambda p: efficiency_from_params(p, cr)
        p_from_efficiency = lambda f: crossprob_from_params(f, cr)

        # Prepare the primary data (channel parameter and FER)
        x_values = np.array(list(data.fer.keys())).astype(np.float64)
        y_values = list(data.fer.values())
        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(
            x_values,
            y_values,
            marker="o",
            linestyle="-",
            label="FER vs Channel Parameter",
        )
        plt.xlabel("Channel Parameter (p)")
        plt.ylabel("FER")
        plt.title("Status Decoding Performance")
        plt.grid(True)
        plt.legend()

        # Get the current axis and add a secondary x-axis
        ax = plt.gca()
        secax = ax.secondary_xaxis(
            "top", functions=(efficiency_from_p, p_from_efficiency)
        )
        secax.set_xlabel("Efficiency f = (1-CR)/h(p)")

        if save:
            plt.save(self.data_dirs.plot_path("test"))
        plt.show()
