from django.http import HttpResponse
from django.views import generic
from django.template import RequestContext, loader
from django.db.utils import ConnectionDoesNotExist
import string, re


from home.models import Crttype, Courts

class OutcomeView(generic.View):

    def court_info(self, outcome_data):
        court = {}
        try:
            court['type'] = Crttype.objects.using('outcomes').get(type=outcome_data[5]).name
            def get_name(court): return court.name
            courts = Courts.objects.using('outcomes').filter(number=outcome_data[11])
            if len(courts)==0:
                court_names = [outcome_data[11]]
            else:
                court_names = map(get_name,courts)
            court['name'] = court_names
        except ConnectionDoesNotExist:
            court['type'] = outcome_data[5]
            court['name'] = [outcome_data[11]]
        finally:
            return court

    def valid_outcome(self, outcome_csv):
        return re.compile('(\d+,){5}(MC|CC),(IND|SMO|SNM),(\d+,){21}\d+').match(outcome_csv)

    def get(self, request):
        outcome_csv = request.GET.get('csv','')
        if self.valid_outcome(outcome_csv):
            outcome_data = string.split(outcome_csv,',')
            context = RequestContext(request, {
                'csv': outcome_csv,
                'outcome': {
                    'court': self.court_info(outcome_data),
                    'multipers': outcome_data[0],
                    'amount1': outcome_data[1],
                    'amount2': outcome_data[2],
                    'amount3': outcome_data[3],
                    'amount4': outcome_data[4],
                    'ofgroup': outcome_data[6],
                    'force': outcome_data[7],
                    'age': outcome_data[8],
                    'month': outcome_data[9],
                    'year': outcome_data[10],
                    'sex': outcome_data[12],
                    'ethcode': outcome_data[13],
                    'classctn': outcome_data[14],
                    'plea': outcome_data[15],
                    'proc': outcome_data[16],
                    'disp1': outcome_data[17],
                    'disp2': outcome_data[18],
                    'disp3': outcome_data[19],
                    'disp4': outcome_data[20],
                    'clastype': outcome_data[21],
                    'priority': outcome_data[22],
                    'guilty': outcome_data[23],
                    'sent': outcome_data[24],
                    'result': outcome_data[25],
                    'offtyp': outcome_data[26],
                    'ofclas': outcome_data[27],
                    'notoff': outcome_data[28],
                }
            })
        else:
            context = RequestContext(request, {'csv': outcome_csv, 'outcome': None})
        template = loader.get_template('apps/outcome.html')
        return HttpResponse(template.render(context))
