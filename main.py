import argparse, os, pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template
from dateutil.parser import parse as parse_date

TEMPLATE = '''
<!doctype html>
<html><head><meta charset="utf-8"><title>Reporte KPI</title></head>
<body>
<h1>Reporte KPI</h1>
<p>Total registros: {{n}}</p>
<p>Suma de valores: {{total}}</p>
<p>Promedio: {{avg}}</p>
<img src="series.png" width="720"/>
<img src="by_group.png" width="720"/>
</body></html>
'''

def load_df(path, date_col, value_col, group_col):
    df = pd.read_csv(path)
    df[date_col] = df[date_col].apply(lambda x: parse_date(str(x)))
    df[value_col] = pd.to_numeric(df[value_col], errors="coerce").fillna(0)
    if group_col and group_col not in df.columns:
        df[group_col] = "unknown"
    return df

def chart_series(df, date_col, value_col, out):
    s = df.sort_values(date_col).set_index(date_col)[value_col].resample("D").sum()
    plt.figure()
    s.plot()  # No styles or colors set per instruction
    plt.title("Serie temporal")
    plt.xlabel("Fecha")
    plt.ylabel(value_col)
    plt.tight_layout()
    plt.savefig(out)
    plt.close()

def chart_by_group(df, group_col, value_col, out):
    g = df.groupby(group_col)[value_col].sum().sort_values(ascending=False)
    plt.figure()
    g.plot(kind="bar")
    plt.title("Total por grupo")
    plt.xlabel(group_col)
    plt.ylabel(value_col)
    plt.tight_layout()
    plt.savefig(out)
    plt.close()

def render_report(n, total, avg, out_dir):
    html = Template(TEMPLATE).render(n=n, total=total, avg=avg)
    with open(os.path.join(out_dir, "report.html"), "w", encoding="utf-8") as f:
        f.write(html)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--date-col", required=True)
    parser.add_argument("--value-col", required=True)
    parser.add_argument("--group-col", default="channel")
    args = parser.parse_args()

    df = load_df(args.csv, args.date_col, args.value_col, args.group_col)
    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)

    chart_series(df, args.date_col, args.value_col, os.path.join(out_dir, "series.png"))
    chart_by_group(df, args.group_col, args.value_col, os.path.join(out_dir, "by_group.png"))
    render_report(len(df), df[args.value_col].sum(), round(df[args.value_col].mean(),2), out_dir)
    print("Listo. Revisa carpeta 'output'.")

if __name__ == "__main__":
    main()