# Python Data Applications using Blaze and Bokeh

## Requirements

- Install [Anaconda](http://continuum.io/downloads)
- Download [Baseball Statistics SQLite database](https://github.com/jknecht/baseball-archive-sqlite/raw/master/lahman2013.sqlite)

Update `blaze` and `into`

    conda install --yes blaze
    conda install --yes into
    conda install --yes bokeh


## Outline

1. Introduction (5 min)
2. Intro to Blaze (30 min)
3. Blaze in Hadoop Ecosystem (15 min)
4. Intro to Bokeh (15 min)
5. Blaze-Bokeh Applications (20 min)
6. Conclusions (5 min)


Blaze Notebooks
---------------

1.  [Introduction](01-introduction.ipynb)
    ([nbviewer](http://nbviewer.ipython.org/github/ContinuumIO/pydata-strata-2014-sj/blob/master/01-introduction.ipynb))
    ([solution](http://nbviewer.ipython.org/github/ContinuumIO/pydata-strata-2014-sj/blob/slides/01-introduction.ipynb))
2.  [`into`](02-into.ipynb)
    ([nbviewer](http://nbviewer.ipython.org/github/ContinuumIO/pydata-strata-2014-sj/blob/master/02-into.ipynb))
    ([solution](http://nbviewer.ipython.org/github/ContinuumIO/pydata-strata-2014-sj/blob/slides/02-into.ipynb))
3.  [Blaze](03-blaze.ipynb)
    ([nbviewer](http://nbviewer.ipython.org/github/ContinuumIO/pydata-strata-2014-sj/blob/master/03-blaze.ipynb))
    ([solution](http://nbviewer.ipython.org/github/ContinuumIO/pydata-strata-2014-sj/blob/slides/03-blaze.ipynb))
4.  [Remote Data](04-remote.ipynb)
    ([nbviewer](http://nbviewer.ipython.org/github/ContinuumIO/pydata-strata-2014-sj/blob/master/04-remote.ipynb))
    ([solution](http://nbviewer.ipython.org/github/ContinuumIO/pydata-strata-2014-sj/blob/slides/04-remote.ipynb))

Bokeh
-----
1.  [Introduction](05-bokeh-intro.ipynb) - ([nbviewer](http://nbviewer.ipython.org/github/ContinuumIO/pydata-strata-2014-sj/blob/master/05-bokeh-intro.ipynb))
2.  Simple apps
  - static html pages,
  - embedded in flask,
  - interactivity via bokeh-server
3. Final app
  - [explore](07-final-app/Explore.ipynb) - ([nbviewer](http://nbviewer.ipython.org/github/ContinuumIO/pydata-strata-2014-sj/blob/master/07-final-app/Explore.ipynb))
  - linking plots all together
