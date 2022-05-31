import pandas as pd
import xgboost as xgb


class MultiClassificator:
    # MODEL_FILENAME = "./test/task_2_model.json"
    MODEL_FILENAME = "task_2/test/task_2_model.json"
    FEATURES = ['is_usb', 'is_washingmachine', 'is_lenses', 'is_bicycle']

    @staticmethod
    def preprocess(df: pd.DataFrame) -> pd.DataFrame:
        df["is_usb"] = (
                df["text"].str.contains("usb")
                | df["text"].str.contains("memory")
                | df["text"].str.contains("datentraeger")
                | df["text"].str.contains("speicher")
                | df["text"].str.contains("storage")
        ).astype("int")

        df["is_washingmachine"] = (
                df["text"].str.contains("wasch")
                | df["text"].str.contains("wash")
        ).astype("int")

        df["is_lenses"] = (
                df["text"].str.contains("linse")
                | df["text"].str.contains("lenses")
                | df["text"].str.contains("acuvue")
                | df["text"].str.contains("acumed")
                | df["text"].str.contains("contact")
                | df["text"].str.contains("dailies")
                | df["text"].str.contains("optix")
                | df["text"].str.contains("medic")
                | df["text"].str.contains("myday")
                | df["text"].str.contains("vision")
        ).astype("int")

        df["is_bicycle"] = (
                df["text"].str.contains("bike")
                | df["text"].str.contains("bicycle")
                | df["text"].str.contains("fahrraeder")
                | df["text"].str.contains("fahrrad")
                | df["text"].str.contains("freizeit")
                | df["text"].str.contains("sport")
                | df["text"].str.contains("berg")
                | df["text"].str.contains("city")
                | df["text"].str.contains("cross")
        ).astype("int")

        return df

    def fit(self):
        df = pd.read_csv("../testset_C.csv", sep=";")
        df["main_text"] = df["main_text"].str.lower()
        df["add_text"] = df["add_text"].str.lower()
        df["manufacturer"] = df["manufacturer"].str.lower()
        df["manufacturer"] = df["manufacturer"].fillna("unknown")
        df["text"] = df["main_text"] + " " + df["add_text"] + " " + df["manufacturer"]
        df["text"] = df["text"].fillna("missed")
        df = self.preprocess(df)

        mapping_values = {
            "WASHINGMACHINES": 0,
            "USB MEMORY": 1,
            "BICYCLES": 2,
            "CONTACT LENSES": 3,
        }

        df["productgroup"] = df["productgroup"].replace(mapping_values)
        target = "productgroup"
        X = df[MultiClassificator.FEATURES]
        y = df[target]
        params = {
            'objective': 'multi:softmax',  # error evaluation for multiclass training
            'num_class': 4,
        }
        model = xgb.XGBClassifier(**params)
        model.fit(X, y)
        model.save_model(MultiClassificator.MODEL_FILENAME)

    def eval_model(self, df):
        model = xgb.XGBClassifier()
        model.load_model(MultiClassificator.MODEL_FILENAME)
        pred = model.predict(df[MultiClassificator.FEATURES])
        return pred

    def predict(self, text: str) -> str:
        mapping_values = {
            0: "WASHINGMACHINES",
            1: "USB MEMORY",
            2: "BICYCLES",
            3: "CONTACT LENSES",
        }
        input = pd.DataFrame([text], columns=["text"])
        input["text"] = input["text"].str.lower()
        model = xgb.XGBClassifier()
        model.load_model(MultiClassificator.MODEL_FILENAME)
        pred = model.predict(self.preprocess(input)[MultiClassificator.FEATURES])
        pred_value = pred[0]
        return mapping_values[pred_value]


