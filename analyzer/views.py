from django.shortcuts import render, redirect
from .forms import UploadFileForm, ChoiceForm

from .analyze import parse_uploaded_file, create_graph


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

    choice_form = ChoiceForm()
    list_of_dicts = request.session.get('list_of_dicts', '')
    df = pd.DataFrame(list_of_dicts)

    if request.method == "POST":
        choice_form = ChoiceForm(request.POST)
        if choice_form.is_valid():
            choice_num = request.POST['field']
            graph_div = create_graph(df, choice_num)

            return render(request, 'analyzer/results.html', {'graph_div': graph_div,
                                                             'choice_form': choice_form})

    graph_div = create_graph(df, '1')

    return render(request, 'analyzer/results.html', {'graph_div': graph_div,
                                                     'choice_form': choice_form})


