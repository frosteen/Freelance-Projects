import numpy as np

from CustomLib.ECG_Delineate_Plot import ecg_delineate_plot
from CustomLib.ECG_Preprocess import ecg_process


class ECG:
    def __init__(self, ecg_raw, sampling_rate=1000):
        self.sampling_rate = sampling_rate
        self.ecg_filtered = ecg_raw
        self.signals, self.info = ecg_process(
            self.ecg_filtered,
            sampling_rate=self.sampling_rate,
            clean_method="neurokit",
            peaks_method="neurokit",
            delineate_method="dwt",
        )
        self.ecg_clean = self.signals["ECG_Clean"]
        self.Heart_Rate = self.signals["ECG_Rate"].mean()
        self.ECG = {
            "Peaks": {},
            "Onsets": {},
            "Offsets": {},
            "Peaks_Ave": {},
            "Onsets_Ave": {},
            "Offsets_Ave": {},
        }

        # PEAKS
        self.ECG["Legends"] = ["P", "Q", "R", "S", "T"]
        self.ECG["Legends_With_Offsets_Onsets"] = ["P", "R", "T"]
        for legend in self.ECG["Legends"]:
            self.ECG["Peaks"][legend] = self.signals[
                self.signals[f"ECG_{legend}_Peaks"] == 1
            ]["ECG_Clean"]
            self.ECG["Peaks_Ave"][legend] = self.ECG["Peaks"][legend].mean()
        for legend in self.ECG["Legends_With_Offsets_Onsets"]:
            self.ECG["Onsets"][legend] = self.signals[
                self.signals[f"ECG_{legend}_Onsets"] == 1
            ]["ECG_Clean"]
            self.ECG["Onsets_Ave"][legend] = self.ECG["Onsets"][legend].mean()
        for legend in self.ECG["Legends_With_Offsets_Onsets"]:
            self.ECG["Offsets"][legend] = self.signals[
                self.signals[f"ECG_{legend}_Offsets"] == 1
            ]["ECG_Clean"]
            self.ECG["Offsets_Ave"][legend] = self.ECG["Offsets"][legend].mean()

        # INTERVALS & AVERAGE
        self.ECG["PWave_Interval"], self.ECG["PWave"] = self.get_interval(
            self.ECG["Onsets"]["P"], self.ECG["Offsets"]["P"]
        )
        self.ECG["PWave_Interval_Ave"] = self.ECG["PWave_Interval"].mean()
        self.ECG["TWave_Interval"], self.ECG["TWave"] = self.get_interval(
            self.ECG["Onsets"]["T"], self.ECG["Offsets"]["T"]
        )
        self.ECG["TWave_Interval_Ave"] = self.ECG["TWave_Interval"].mean()
        self.ECG["PR_Interval"], self.ECG["PR"] = self.get_interval(
            self.ECG["Onsets"]["P"], self.ECG["Onsets"]["R"]
        )
        self.ECG["PR_Interval_Ave"] = self.ECG["PR_Interval"].mean()
        self.ECG["QT_Interval"], self.ECG["QT"] = self.get_interval(
            self.ECG["Onsets"]["R"], self.ECG["Offsets"]["T"]
        )
        self.ECG["QT_Interval_Ave"] = self.ECG["QT_Interval"].mean()
        self.ECG["ST_Interval"], self.ECG["ST"] = self.get_interval(
            self.ECG["Offsets"]["R"], self.ECG["Offsets"]["T"]
        )
        self.ECG["ST_Interval_Ave"] = self.ECG["ST_Interval"].mean()
        self.ECG["QS_Interval"], self.ECG["QS"] = self.get_interval(
            self.ECG["Peaks"]["Q"], self.ECG["Peaks"]["S"]
        )
        self.ECG["QS_Interval_Ave"] = self.ECG["QS_Interval"].mean()

        # FOR RR INTERVAL & AVERAGE
        self.ECG["RR_Interval"] = (
            np.diff(self.signals.index[self.signals[f"ECG_R_Peaks"] == 1])
            / self.sampling_rate
        )
        self.ECG["RR_Interval_Ave"] = self.ECG["RR_Interval"].mean()

        # FOR QRS INTERVAL & AVERAGE
        self.ECG["QRS_Interval"], self.ECG["QRS"] = self.get_interval(
            self.ECG["Onsets"]["R"], self.ECG["Offsets"]["R"]
        )
        self.ECG["QRS_Interval_Ave"] = self.ECG["QRS_Interval"].mean()

    def get_interval(self, points_A, points_B):
        min_len = min([len(points_A), len(points_B)])
        result = np.abs(
            points_A[:min_len,].index.values - points_B[:min_len,].index.values
        )
        points = list(
            zip(points_A[:min_len,].index.values, points_B[:min_len,].index.values)
        )
        return (result / self.sampling_rate), points

    def ecg_raw_plot(self, ecg_raw, ax):
        ax.plot(ecg_raw, label="ECG_Raw")

    def ecg_filtered_plot(self, ax):
        ax.plot(self.ecg_filtered, label="ECG_Filtered")

    def ecg_cleaned_plot(self, ax, is_show_legends=False):
        ax.plot(self.ecg_clean, label="ECG_Clean")
        if is_show_legends:
            for legend in self.ECG["Legends"]:
                ax.plot(self.ECG["Peaks"][legend], "o", label=f"ECG_{legend}_Peaks")
            for legend in self.ECG["Legends_With_Offsets_Onsets"]:
                ax.plot(self.ECG["Onsets"][legend], "o", label=f"ECG_{legend}_Onsets")
                ax.plot(self.ECG["Offsets"][legend], "o", label=f"ECG_{legend}_Offsets")

            intervals = [self.ECG["ST"], self.ECG["QRS"]]
            colors = ["g", "y"]
            for interval, color in zip(intervals, colors):
                for A, B in interval:
                    ax.fill_between(
                        self.ecg_clean.index,
                        self.ecg_clean.min(),
                        self.ecg_clean.max(),
                        where=(self.ecg_clean.index >= A) & (self.ecg_clean.index <= B),
                        alpha=0.25,
                        color=color,
                    )

            # Shrink current axis by 20%
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

            # Put a legend to the right of the current axis
            ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), ncol=2)

    def ecg_delineate_plot(self, ax):
        ecg_delineate_plot(
            ax,
            self.ecg_clean,
            rpeaks=self.info["ECG_R_Peaks"],
            signals=self.signals,
            signal_features_type="peaks",
            sampling_rate=self.sampling_rate,
        )
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
        ax.legend(loc="upper right", bbox_to_anchor=(1.10, 1.10))


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import neurokit2 as nk

    # FOR TESTING
    sampling_rate = 1000
    ecg_raw = nk.ecg_simulate(duration=60, sampling_rate=sampling_rate, heart_rate=60)
    ecg_raw = nk.signal_distort(
        ecg_raw,
        sampling_rate=sampling_rate,
        noise_amplitude=0.1,
        noise_frequency=[25, 50],
        artifacts_amplitude=0.05,
        artifacts_frequency=60,
    )

    ECG_SIGNAL = ECG(ecg_raw, sampling_rate=sampling_rate)

    # PLOTTING
    fig, ax = plt.subplots(2, 1)
    fig.set_figwidth(20)
    fig.tight_layout()
    ECG_SIGNAL.ecg_raw_plot(ecg_raw, ax[0])
    ECG_SIGNAL.ecg_cleaned_plot(ax[1])
    plt.show()
    ECG_SIGNAL.ecg_delineate_plot(plt)
    plt.show()
