from math import sqrt, pi
import pandas as pd

from ldadata import data

from bokeh.models import ColumnDataSource, LinearAxis, CategoricalAxis, Plot, DataRange1d, FactorRange, GlyphRenderer, TapTool
from bokeh.models.glyphs import Circle, Text, Rect
from bokeh.models.widgets import TextInput, Button, Slider, HBox, VBox

from bokeh.browserlib import view
from bokeh.document import Document
from bokeh.session import Session
from bokeh.browserlib import view

document = Document()
session = Session()
session.use_doc('ldavis_server')
session.load_document(document)

print("MDSPLOT")

R = data["R"]

mds = pd.DataFrame.from_dict(data["mdsDat"])
lam = pd.DataFrame.from_dict(data["tinfo"])

barDefault2 = lam[lam.Category=="Default"]

mdswidth = 530
mdsheight = 530

circle_prop = 0.25

base_color = "#1f77b4"
high_color = "#d62728"

current_topic = None

mdssource = ColumnDataSource(dict(
    x = mds.x,
    y = mds.y,
    text = mds.topics,
    r = [ sqrt((Freq/100)*mdswidth*mdsheight*circle_prop/pi) for Freq in mds.Freq ],
))

topicsource = ColumnDataSource(dict(
    x = list(barDefault2.Total/2),
    y = list(barDefault2.Term),
    width = list(barDefault2.Total),
))

def mdsplot():
    xdr = DataRange1d(sources=[mdssource.columns("x")])
    ydr = DataRange1d(sources=[mdssource.columns("y")])

    title = "Intertopic Distance Map (via multidimensional scaling)"
    plot = Plot(title=title, title_text_font_size="16px", x_range=xdr, y_range=ydr, plot_width=mdswidth, plot_height=mdsheight)

    circle1 = Circle(x="x", y="y", radius=dict(field="r", units="screen"), fill_color=base_color, fill_alpha=0.2)
    circle2 = Circle(x="x", y="y", radius=dict(field="r", units="screen"), fill_color=high_color, fill_alpha=0.6)

    circles = GlyphRenderer(data_source=mdssource, glyph=circle1, selection_glyph=circle2, nonselection_glyph=circle1)
    plot.renderers.append(circles)

    plot.add_glyph(mdssource, Text(x="x", y="y", text="text", text_font_style="bold", text_align="center", text_baseline="middle", text_font_size="11px"))

    plot.tools.append(TapTool(plot=plot, renderers=[circles]))

    #plot.add_layout(LinearAxis(axis_label="PC1"), "below")
    #plot.add_layout(LinearAxis(axis_label="PC2"), "left")

    return plot

def topicplot():
    xdr = DataRange1d(sources=[topicsource.columns("width")])
    ydr = FactorRange(factors=list(reversed(list(barDefault2.Term))))

    #"Top-{R} Most Relevant Terms for Topic {topic} ({count}% of tokens)".format(R=R, ...)
    title = "Top-{R} Most Salient Terms".format(R=R)
    plot = Plot(title=title, title_text_font_size="16px", x_range=xdr, y_range=ydr, plot_width=mdswidth, plot_height=mdsheight)

    plot.add_glyph(topicsource, Rect(x="x", y="y", width="width", height=1, fill_color=base_color, fill_alpha=0.2, line_color=base_color))

    plot.add_layout(LinearAxis(), "above")
    plot.add_layout(CategoricalAxis(), "left")

    return plot

def on_mdssel(obj, attr, _, indices):
    global current_topic

    if len(indices) >= 1:
        current_topic = indices[0] + 1
        selected = lam[lam.Category == "Topic%d" % current_topic][:R]
    else:
        current_topic = None
        selected = barDefault2

    top_R_terms.y_range.factors = list(reversed(list(selected.Term)))
    topicsource.data = dict(
        x = list(selected.Total/2),
        y = list(selected.Term),
        width = list(selected.Total),
    )

    session.store_objects(topicsource, top_R_terms)

mdssource.on_change('selected', on_mdssel)

intertopic_distance_map = mdsplot()
top_R_terms = topicplot()

#selected_topic = TextInput(title="Selected topic", value="")

btn_prev = Button(label="Previous Topic")
btn_next = Button(label="Next Topic")
btn_clear = Button(label="Clear Topic")

min_topic = mds.topics.min()
max_topic = mds.topics.max()

def on_btn_prev():
    global current_topic
    if current_topic is None:
        current_topic = min_topic
    elif current_topic == min_topic:
        current_topic = max_topic
    else:
        current_topic -= 1
    mdssource.selected = [current_topic-1]
    session.store_objects(mdssource)

def on_btn_next():
    global current_topic
    if current_topic is None:
        current_topic = min_topic
    elif current_topic == max_topic:
        current_topic = min_topic
    else:
        current_topic += 1
    mdssource.selected = [current_topic-1]
    session.store_objects(mdssource)

def on_btn_clear():
    current_topic = None
    mdssource.selected = []
    session.store_objects(mdssource)

btn_prev.on_click(on_btn_prev)
btn_next.on_click(on_btn_next)
btn_clear.on_click(on_btn_clear)

slider = Slider(title="Slide to adjust relevance metric", value=0.25, start=0.0, end=1.0, step=0.01)

topics = HBox(height=50, children=[btn_prev, btn_next, btn_clear])
metric = HBox(height=50, children=[slider])

left_panel = VBox(children=[topics, intertopic_distance_map])
right_panel = VBox(children=[metric, top_R_terms])

layout = HBox(children=[left_panel, right_panel])

document.add(layout)
session.store_document(document)

if __name__ == "__main__":
    link = session.object_link(document.context)
    print("Please visit %s to see the plots" % link)
    view(link)
    print("\npress ctrl-C to exit")
    session.poll_document(document)