from pyramid.view import view_config, view_defaults
from pyramid.renderers import render_to_response

from server.SentimentAnalysis import SentimentAnalysis

text = ""


@view_defaults(renderer='templates/index.html')
class SiteViews:
    def __init__(self, request):
        self.request = request
        self.data = {
                'Text': '',
                'Sentiment': '',
                'Model': ''
            }

    @view_config(route_name='form', renderer='templates/index.html')
    def form(self):
        global text
        result = ""
        self.json()
        if self.data['Sentiment'] == 'Positive':
            color = "color:green;"
        else:
            color = "color:red;"
        if text != "":
            result = self.data['Sentiment']

        return {'color': color, 'PredictionValue': result}

    @view_config(route_name='json', renderer='json')
    def json(self):
        global text
        if self.request.POST:
            text = self.request.POST['text']
        obj = SentimentAnalysis(text)
        obj.clean_text()
        obj.bag_of_words()
        self.data = obj.predict()
        return self.data