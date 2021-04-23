class missingvaluereg():

    def __init__(self,missing_columns,data):
        self.missing_columns=missing_columns
        self.data=data

    @staticmethod
    def random_imputation(data, features):
        import numpy as np
        number_missing = data[features].isnull().sum()
        observed_values = data.loc[data[features].notnull(), features]
        data.loc[data[features].isnull(), features + '_imp'] = np.random.choice(observed_values, number_missing, replace = True)
        return data

    def random_imp(self):
        for feature in self.missing_columns:
            self.data[feature + '_imp'] = self.data[feature]
            self.data = self.random_imputation(self.data, feature)
        return self.data
    def regressionpart(self):
        import pandas as pd
        self.random_imp()

        deter_data = pd.DataFrame(columns = ["Det" + name for name in self.missing_columns])
        for feature in self.missing_columns:

            deter_data["Det" + feature] = self.data[feature + "_imp"]
            parameters = list(set(self.data.columns) - set(self.missing_columns) - {feature + '_imp'})

            #Create a Linear Regression model to estimate the missing data
            from sklearn import linear_model
            model = linear_model.LinearRegression()
            model.fit(X = self.data[parameters], y = self.data[feature + '_imp'])

            #observe that I preserve the index of the missing data from the original dataframe
            deter_data.loc[self.data[feature].isnull(), "Det" + feature] = model.predict(self.data[parameters])[self.data[feature].isnull()]
        return pd.concat([self.data,deter_data],axis=1)
        #return deter_data
    def iterativemethod(self):
        import numpy as np
        from sklearn.experimental import enable_iterative_imputer
        from sklearn.impute import IterativeImputer
        imp_mean = IterativeImputer(random_state=0)
        for featurem in self.missing_columns:
            param= list(set(self.data.columns) - set(featurem))
            imp_mean.fit(np.array(self.data[param]).reshape(-1,1))
            self.data[featurem]=imp_mean.transform(np.array(self.data[featurem]).reshape(-1,1))
        return self.data