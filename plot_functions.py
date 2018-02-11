from polls import *

def plot_constructor(data, polls=polls, categories=None, to_plot=None):

    import numpy as np
    import pandas as pd

    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import pandas as pd

    if categories == None:
        categories = input("Name of the column variable to sort by: ")
    else:
        categories = categories

    if to_plot == None:
        to_plot = input("Variable to plot: ")
    else:
        to_plot = to_plot

    polls = polls

    num_cats = len(polls[to_plot][2])

    def sort_respondents(data, categories, to_plot):
        num_cats = len(polls[categories][2])
        num_plts = len(polls[to_plot][2])
        answers = np.zeros((num_cats, num_plts))
        ans_count = np.zeros((num_cats, num_plts))
        totals = np.zeros(num_plts)
        tots_count = np.zeros(num_plts)
        for i in range(8000):
            for k in range(num_plts):
                for j in range(num_cats):
                    if data[categories][i] in polls[categories][2][j]:
                        if data[to_plot][i] in polls[to_plot][2][k]:
                            answers[j, k] += data['weight'][i]
                            ans_count[j, k] += 1
                if data[to_plot][i] in polls[to_plot][2][k]:
                    totals[k] += data['weight'][i]
                    tots_count[k] += 1

        cats_nulls = data[categories].isnull().sum()
        to_plt_nulls = data[to_plot].isnull().sum()

        return answers, ans_count, totals, tots_count, cats_nulls, to_plt_nulls

    answers, count, totals, tots_count, cats_nulls, to_plt_nulls = sort_respondents(data, categories, to_plot)

    def convert_to_perc(answers_vec):
        new_answers = np.zeros(answers.shape)
        for i in range(answers_vec.shape[0]):
            row_tot = np.sum(answers_vec, axis=1)[i]
            for j in range(answers_vec.shape[1]):
                new_answers[i, j] = answers[i, j]/row_tot

        return new_answers

    answers_perc = convert_to_perc(answers)
    print(answers_perc)
    new_ans = np.zeros(answers_perc.size + 2)
    new_ans[1:-1] = answers_perc.reshape(1,answers_perc.size)

    #Give every 3 bars in the graph an inch
    fig_width = len(new_ans)/3
    fig_height = fig_width/2 + 1

    f,ax = plt.subplots(figsize=(fig_width, fig_height))
    index = np.arange(len(new_ans))
    bar_width = 1

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            if height != float(0):
                if height > 3.5:
                    ax.text(rect.get_x() + rect.get_width()/2., height-0.02,
                            '{:.1%}'.format(height), ha='center', va='bottom',
                            fontsize=8, fontweight='bold')
                else:
                    ax.text(rect.get_x() + rect.get_width()/2., height+0.02,
                            '{:.1%}'.format(height), ha='center', va='bottom',
                            fontsize=8, fontweight='bold')

    plt.suptitle(polls[to_plot][0], fontsize=16, fontweight='bold', family='serif', ha='center', y=0.95)
    plt.title(polls[to_plot][1], fontsize=14, family='serif')
    ##IF I NEED TO WRAP THE TITLE -- title("\n".join(wrap("Some really really long long long title I really really need - and just can't - just can't - make it any - simply any - shorter - at all.", 60)))
    ax.grid(True, which='both', linestyle=':')
    ax.set_axisbelow(True)
    rects = ax.bar(index, new_ans, bar_width)
    color_opts = ['#80aaff', '#aaff80', '#ffb366', '#d98cd9', '#ff80aa', '#994d00', '0.3', '0.5', '0.7']
    for k in [i for i in range(1,(len(index)-num_cats),num_cats)]:
        for m in range(num_cats):
            rects[k+m].set_color(color_opts[m])
    rects_labels = []
    for n in range(num_cats):
        rects_labels.append(rects[n+1:(len(rects)-(num_cats - n)+1):num_cats])
    ax.legend((rects_labels), polls[to_plot][3])
    autolabel(rects)
    ax.set_yticks((0.2, 0.4, 0.6, 0.8, 1.0))
    ax.set_yticklabels(('20%', '40%', '60%', '80%', '100%'))
    ax.set_xticks(np.arange((num_cats/2 + bar_width/2),(index[-1] - num_cats/2),num_cats))
    ax.set_xticklabels(polls[categories][3], rotation=15, fontsize=10, ha='right')
    ax.set_xlabel(polls[categories][0], fontsize=14, fontweight='bold', family='serif')

    f.show()

def bokeh_constructor(data, polls=polls):

    import numpy as np
    import pandas as pd

    from bokeh.io import show, output_notebook, output_file, save
    from bokeh.models import ColumnDataSource, FactorRange, HoverTool, NumeralTickFormatter, Select
    from bokeh.plotting import figure, curdoc
    from bokeh.transform import factor_cmap, dodge
    from bokeh.core.properties import value
    from bokeh.palettes import Set3
    from bokeh.embed import components, autoload_static
    from bokeh.resources import CDN
    from bokeh.layouts import row, widgetbox

    data = data

    def update(attr, old, new):
        layout.children[1] = create_figure()

    def create_figure(data, polls, categories='birthyr_baseline', to_plot='fav_trump_2016'):

        def sort_respondents(data, categories, to_plot):
            num_cats = len(polls[categories][2])
            num_plts = len(polls[to_plot][2])
            answers = np.zeros((num_cats, num_plts))
            ans_count = np.zeros((num_cats, num_plts))
            totals = np.zeros(num_plts)
            tots_count = np.zeros(num_plts)
            for i in range(8000):
                for k in range(num_plts):
                    for j in range(num_cats):
                        if data[categories][i] in polls[categories][2][j]:
                            if data[to_plot][i] in polls[to_plot][2][k]:
                                answers[j, k] += data['weight'][i]
                                ans_count[j, k] += 1
                    if data[to_plot][i] in polls[to_plot][2][k]:
                        totals[k] += data['weight'][i]
                        tots_count[k] += 1

            cats_nulls = data[categories].isnull().sum()
            to_plt_nulls = data[to_plot].isnull().sum()

            return answers, ans_count, totals, tots_count, cats_nulls, to_plt_nulls

        def convert_to_perc(answers_vec):
            new_answers = np.zeros(answers.shape)
            for i in range(answers_vec.shape[0]):
                row_tot = np.sum(answers_vec, axis=1)[i]
                for j in range(answers_vec.shape[1]):
                    new_answers[i, j] = answers[i, j]/row_tot

            return new_answers

        def get_offsets(plot_subcategories, num_subcats, spacing):
            if num_subcats % 2 == 0:
                offsets = [(spacing*i)+(0.5*spacing) for i in range(-int(num_subcats/2), int(num_subcats/2)+1)]
            else:
                offsets = [spacing*i for i in range(-int(num_subcats/2), int(num_subcats/2)+1)]

            return offsets

        categories = categories
        to_plot = to_plot

        plot_categories = polls[categories][3]
        plot_subcategories = polls[to_plot][3]

        num_cats = len(polls[to_plot][2])

        answers, count, totals, tots_count, cats_nulls, to_plt_nulls = sort_respondents(data, categories, to_plot)
        answers_perc = convert_to_perc(answers)

        data_dict = dict()
        data_dict['categories'] = plot_categories
        for j in range(len(plot_subcategories)):
            data_dict[plot_subcategories[j]] = list(np.dstack(answers_perc)[0][j])
            data_dict[plot_subcategories[j]+' Count'] = list(np.dstack(count)[0][j])

        num_subcats = len(plot_subcategories)
        spacing = 1 / (num_subcats+1)

        offsets = get_offsets(plot_subcategories, num_subcats, spacing)

        source = ColumnDataSource(data=data_dict)

        color_opts = Set3[num_cats]

        fig_width = int(40*answers_perc.size)
        fig_height = int((4/5)*fig_width)

        hover_lbl_vec = []
        for j in range(len(plot_subcategories)):
            lbl_str1 = "@{%s}{.3f}" % plot_subcategories[j]
            lbl_str2 = "@{%s Count}" % plot_subcategories[j]
            hover_lbl_vec.append(("{} (%, unweighted N)".format(plot_subcategories[j]), "{} {}".format(lbl_str1, lbl_str2)))

        hover = HoverTool(tooltips=hover_lbl_vec)

        p = figure(x_range=plot_categories, y_range=(0,1), plot_height=fig_height, plot_width=fig_width,
                   title=polls[to_plot][0], toolbar_location=None, tools=[hover])

        for n in range(len(plot_subcategories)):
            lbl = polls[to_plot][3][n]
            p.vbar(x=dodge('categories', offsets[n], range=p.x_range), top=polls[to_plot][3][n], width=0.8*spacing,
                  source=source, color=color_opts[n], legend=value(lbl))

        p.x_range.range_padding = 0.1
        p.xaxis.major_label_orientation = 1
        p.xgrid.grid_line_color = None
        p.xaxis.axis_label=polls[categories][1]
        p.yaxis[0].formatter = NumeralTickFormatter(format="0.%")
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"

        output_file("YouGov_Data_Plot.html")

        show(p)

        #return p

    polls = polls
    #menu_options = sorted([key[0] for key in polls.keys()])

    categories = input("Categorize by: ")
    to_plot = input("Plot:")

    create_figure(data, polls, categories, to_plot)

    #update()

    #categories = Select(title="Categorize by:", value='birthyr_baseline', options=menu_options)
    #categories.on_change('value', update)
    #to_plot = Select(title="Plot:", value='fav_trump_2016', options=menu_options)
    #to_plot.on_change('value', update)

    #controls = widgetbox([categories, to_plot], width=200)
    #layout = row(controls, create_figure(categories, to_plot))

    #curdoc().add_root(layout)
    #curdoc().title = "Democracy Fund Data"

    #output_file("YouGov_Data_Plot.html")

    #show(p)
