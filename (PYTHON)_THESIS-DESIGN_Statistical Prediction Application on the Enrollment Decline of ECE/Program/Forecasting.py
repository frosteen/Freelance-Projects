import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from neuralprophet import NeuralProphet


class Forecasting:
    def __init__(self, _csv_file):
        self.df = pd.read_csv(_csv_file)
        self.df["Date"] = pd.to_datetime(self.df["Date"])

    def __create_neuralprophet_univariate(
        self, df, ds_name, y_name, freq, epochs, periods, show_plot=False
    ):
        df = df.loc[:, [ds_name, y_name]]
        df = df.rename({ds_name: "ds", y_name: "y"}, axis=1)

        m = NeuralProphet()
        m.fit(df, freq=freq, epochs=epochs)
        m_Future_df = m.make_future_dataframe(df, periods=periods)
        m_Predict = m.predict(m_Future_df)
        m_Predict["yhat1"] = m_Predict["yhat1"].apply(np.abs)

        if show_plot:
            m.plot(m_Predict)
            plt.show()

        m_Predict = m_Predict.loc[:, ["ds", "yhat1"]]
        m_Predict = m_Predict.rename({"yhat1": y_name}, axis=1)

        return m_Predict

    def forecast(self, epochs=1000, periods=10):
        # Graduates Univariate
        m_Graduates_Predict = self.__create_neuralprophet_univariate(
            self.df, "Date", "Graduates", "Y", epochs, periods
        )

        # Passers Univariate
        m_Passers_Predict = self.__create_neuralprophet_univariate(
            self.df, "Date", "Passers", "Y", epochs, periods
        )

        # Merged
        df_merged = m_Graduates_Predict.merge(m_Passers_Predict, on="ds")
        df_merged = df_merged.loc[:, ["Graduates", "Passers"]]

        # Enrollees Multivariate
        df = self.df.rename({"Date": "ds", "Enrollees": "y"}, axis=1)

        m_Enrollees = NeuralProphet()
        m_Enrollees.add_future_regressor("Graduates")
        m_Enrollees.add_future_regressor("Passers")
        m_Enrollees.fit(df, freq="Y", epochs=epochs)

        m_Enrollees_Future_df = m_Enrollees.make_future_dataframe(
            df, regressors_df=df_merged, periods=periods
        )

        df_Predict = m_Enrollees.predict(df)

        m_Enrollees_Future_df_Predict = m_Enrollees.predict(m_Enrollees_Future_df)

        return m_Enrollees, df_Predict, m_Enrollees_Future_df_Predict


if __name__ == "__main__":
    f = Forecasting("datathesis_modified.csv")

    m_Enrollees, df_Predict, m_Enrollees_Future_df_Predict = f.forecast(
        epochs=5000, periods=30
    )

    m_Enrollees.plot(pd.concat([df_Predict, m_Enrollees_Future_df_Predict]))
    m_Enrollees.plot_components(pd.concat([df_Predict, m_Enrollees_Future_df_Predict]))

    plt.show()
