from django.shortcuts import render, redirect
from .forms import UploadFileForm, ChoiceForm

from .analyze import parse_uploaded_file


def index(request):
    return render(request, 'analyzer/index.html')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            record_dict = parse_uploaded_file(request.FILES['file'])
            request.session['list_of_dicts'] = record_dict
            return redirect('show_results')
    else:
        form = UploadFileForm()
    return render(request, 'analyzer/upload.html', {'form': form})


def show_results(request):
    import pandas as pd
    from plotly import offline
    import plotly.graph_objs as go

    choice_form = ChoiceForm()
    list_of_dicts = request.session.get('list_of_dicts', '')
    df = pd.DataFrame(list_of_dicts)

    if request.method == "POST":
        choice_form = ChoiceForm(request.POST)
        if choice_form.is_valid():
            if request.POST['field'] == '2':
                df2 = df[['time', 'clientID']].groupby(['time']).count().sort_index()
                time_ax = list(df2.index)
                process_count = list(df2['clientID'])
                fig = go.Figure(layout={'title': 'Number of processes vs Time'})
                bar = go.Bar(x=time_ax, y=process_count,
                             name='Number of processes vs Time')
                fig.add_trace(bar)
                graph_div = offline.plot(fig, auto_open=False, output_type='div')

                return render(request, 'analyzer/results.html', {'graph_div': graph_div,
                                                                 'choice_form': choice_form})

            else:
                df1 = df[['Usr', 'clientID']].groupby(['Usr']).count().sort_values(by=['clientID'])
                users = list(df1.index)
                process_count = list(df1['clientID'])

                fig = go.Figure(layout={'title': 'Number of processes vs User'})
                bar = go.Bar(x=users, y=process_count,
                             name='Number of processes vs User')
                fig.add_trace(bar)
                graph_div = offline.plot(fig, auto_open=False, output_type="div")

                return render(request, 'analyzer/results.html', {'graph_div': graph_div,
                                                                 'choice_form': choice_form})


    df1 = df[['Usr', 'clientID']].groupby(['Usr']).count().sort_values(by=['clientID'])
    users = list(df1.index)
    process_count = list(df1['clientID'])
    fig = go.Figure(layout={'title': 'Number of processes vs User'})
    bar = go.Bar(x=users, y=process_count,
                 name='Number of processes vs User')
    fig.add_trace(bar)
    graph_div = offline.plot(fig, auto_open=False, output_type="div")

    return render(request, 'analyzer/results.html', {'graph_div': graph_div,
                                                     'choice_form': choice_form})
