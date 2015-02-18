import pandas as pd
import numpy as np

import blaze as bz
from into import into

from bokeh.plotting import *
from bokeh.models import HoverTool
from collections import OrderedDict

output_file("salary.html")

TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset,hover,previewsave"



db = bz.Data('sqlite:///../lahman2013.sqlite')


expr = bz.by(db.Salaries.teamID,
               avg=db.Salaries.salary.mean(),
               max=db.Salaries.salary.max(),
               ratio=db.Salaries.salary.max() / db.Salaries.salary.min())
expr = expr.sort('ratio', ascending=False)

df_salary_gb = into(pd.DataFrame, expr)

source_salary_gb = ColumnDataSource(df_salary_gb)

p_salary = figure(x_range=list(df_salary_gb["teamID"]), title="Salary ratio by team", tools=TOOLS)
p_salary.scatter(x="teamID", y="ratio", source=source_salary_gb, size=10)
p_salary.xaxis.major_label_orientation = np.pi/3

hover = p_salary.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
    ("index", "$index"),
    ("fill color", "$color[hex, swatch]:fill_color"),
    ])

show(p_salary)
