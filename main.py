import pandas as pd
from sklearn.datasets import load_iris
from summarizer import Summarizer

iris = load_iris(as_frame=True)
df = iris.frame.drop(columns="target")
df["species"] = pd.Categorical.from_codes(iris.target, iris.target_names)

summarizer = Summarizer(df)
print(summarizer.report("markdown"))
summarizer.report("html", "iris_report.html")
summarizer.report("xlsx", "iris_report.xlsx")
print("Сохранено: iris_report.html, iris_report.xlsx")
