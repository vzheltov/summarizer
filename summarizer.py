import pandas as pd
from pandas.api.types import is_bool_dtype, is_datetime64_any_dtype, is_numeric_dtype


class Summarizer:
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("ошибка, нужен DataFrame")
        self.df = df

    def analyze(self):
        rows = []
        for col in self.df.columns:
            series = self.df[col]
            row = {
                "type": str(series.dtype),
                "count": int(series.size),
                "missing_pct": round(float(series.isna().mean()) * 100, 2),
                "distinct": int(series.nunique(dropna=True)),
            }

            s = series.dropna()

            mode_val = None
            m = s.mode()
            if len(m) > 0:
                mode_val = m.iloc[0]

            if is_bool_dtype(series):
                row["kind"] = "boolean"
                if len(s) > 0:
                    true_count = 0
                    false_count = 0
                    for v in s:
                        if v == True:
                            true_count += 1
                        else:
                            false_count += 1
                    row["mode"] = mode_val
                    row["true_pct"] = round(true_count / len(s) * 100, 2)
                    row["false_pct"] = round(false_count / len(s) * 100, 2)

            elif is_datetime64_any_dtype(series):
                row["kind"] = "datetime"
                if len(s) > 0:
                    row["min"] = s.min()
                    row["max"] = s.max()
                    row["mode"] = mode_val

            elif is_numeric_dtype(series):
                row["kind"] = "numeric"
                if len(s) > 0:
                    mean = float(s.mean())
                    if len(s) > 1:
                        std = float(s.std(ddof=1))
                        var = float(s.var(ddof=1))
                    else:
                        std = 0.0
                        var = 0.0
                    q1 = float(s.quantile(0.25))
                    q3 = float(s.quantile(0.75))
                    if mean != 0:
                        cv = std / mean
                    else:
                        cv = float("nan")

                    zero_count = 0
                    for v in series:
                        if v == 0:
                            zero_count += 1

                    row["min"] = float(s.min())
                    row["max"] = float(s.max())
                    row["mean"] = mean
                    row["median"] = float(s.median())
                    row["mode"] = mode_val
                    row["zero_pct"] = round(zero_count / len(series) * 100, 2)
                    row["variance"] = var
                    row["std"] = std
                    row["iqr"] = q3 - q1
                    row["cv"] = cv

            else:
                row["kind"] = "categorical"
                if len(s) > 0:
                    vc = s.value_counts()
                    row["mode"] = vc.index[0]
                    row["top_freq_pct"] = round(float(vc.iloc[0]) / len(s) * 100, 2)

            rows.append(row)

        result = pd.DataFrame(rows, index=list(self.df.columns))
        result.index.name = "column"
        return result

    def report(self, output_type="markdown", filename=None):
        summary = self.analyze()
        fmt = output_type.lower()

        if fmt == "markdown" or fmt == "md":
            text = summary.to_markdown()
            if filename is None:
                return text
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            return None

        elif fmt == "html":
            text = summary.to_html()
            if filename is None:
                return text
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            return None

        elif fmt == "xlsx":
            if not filename:
                raise ValueError("для xlsx нужен filename")
            summary.to_excel(filename)
            return None

        else:
            raise ValueError("неизвестный формат: " + str(output_type))
