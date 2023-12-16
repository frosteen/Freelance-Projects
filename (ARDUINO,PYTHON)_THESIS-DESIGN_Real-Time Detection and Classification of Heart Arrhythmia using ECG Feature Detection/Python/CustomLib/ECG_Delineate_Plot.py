# -*- coding: utf-8 -*-
import pandas as pd
from neurokit2 import epochs_create, epochs_to_df


def ecg_delineate_plot(
    ax,
    ecg_signal,
    rpeaks=None,
    signals=None,
    signal_features_type="all",
    sampling_rate=1000,
    window_start=-0.35,
    window_end=0.55,
):
    """
    import neurokit2 as nk
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    ecg_signal = nk.data("ecg_100hz")

    # Extract R-peaks locations
     _, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=1000)

    # Delineate the ECG signal with ecg_delineate()
    signals, waves = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=1000)

    # Plot the ECG signal with markings on ECG peaks
    _ecg_delineate_plot(ecg_signal, rpeaks=rpeaks, signals=signals,
                        signal_features_type='peaks', sampling_rate=1000)

    # Plot the ECG signal with markings on boundaries of R peaks
    _ecg_delineate_plot(ecg_signal, rpeaks=rpeaks, signals=signals,
                        signal_features_type='bound_R', sampling_rate=1000)

    # Plot the ECG signal with markings on boundaries of P peaks
    _ecg_delineate_plot(ecg_signal, rpeaks=rpeaks, signals=signals,
                        signal_features_type='bound_P', sampling_rate=1000)

    # Plot the ECG signal with markings on boundaries of T peaks
    _ecg_delineate_plot(ecg_signal, rpeaks=rpeaks, signals=signals,
                        signal_features_type='bound_T', sampling_rate=1000)

    # Plot the ECG signal with markings on all peaks and boundaries
    _ecg_delineate_plot(ecg_signal, rpeaks=rpeaks, signals=signals,
                        signal_features_type='all', sampling_rate=1000)

    """

    data = pd.DataFrame({"Signal": list(ecg_signal)})
    data = pd.concat([data, signals], axis=1)
    # print(signals)

    # Try retrieving right column
    if isinstance(rpeaks, dict):
        rpeaks = rpeaks["ECG_R_Peaks"]
    # Segment the signal around the R-peaks
    epochs = epochs_create(
        data,
        events=rpeaks,
        sampling_rate=sampling_rate,
        epochs_start=window_start,
        epochs_end=window_end,
    )
    data = epochs_to_df(epochs)
    data_cols = data.columns.values

    dfs = []
    for feature in data_cols:
        if signal_features_type == "peaks":
            if any(x in str(feature) for x in ["Peak"]):
                df = data[feature]
                dfs.append(df)
        elif signal_features_type == "bounds_R":
            if any(x in str(feature) for x in ["ECG_R_Onsets", "ECG_R_Offsets"]):
                df = data[feature]
                dfs.append(df)
        elif signal_features_type == "bounds_T":
            if any(x in str(feature) for x in ["ECG_T_Onsets", "ECG_T_Offsets"]):
                df = data[feature]
                dfs.append(df)
        elif signal_features_type == "bounds_P":
            if any(x in str(feature) for x in ["ECG_P_Onsets", "ECG_P_Offsets"]):
                df = data[feature]
                dfs.append(df)
        elif signal_features_type == "all":
            if any(x in str(feature) for x in ["Peak", "Onset", "Offset"]):
                df = data[feature]
                dfs.append(df)
    features = pd.concat(dfs, axis=1)

    data.Label = data.Label.astype(int)
    ax.axhline(y=0, color="red", linestyle="-", label="Baseline")
    for label in data.Label.unique():
        epoch_data = data[data.Label == label]
        ax.plot(epoch_data.Time, epoch_data.Signal, color="grey", alpha=0.2)
    for i, feature_type in enumerate(features.columns.values):  # pylint: disable=W0612
        event_data = data[data[feature_type] == 1.0]
        ax.scatter(
            event_data.Time, event_data.Signal, label=feature_type, alpha=0.5, s=200
        )
        ax.legend()
