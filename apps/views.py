import string, re
from django.http import HttpResponse
from django.views import generic
from django.template import RequestContext, loader
from django.db.utils import ConnectionDoesNotExist
from home.models import Crttype, Courts, Ofgroup, Sex, Ethcode

class OutcomeView(generic.View):

    def court_info(self, outcome_data):
        court = {}
        try:
            court['type'] = Crttype.objects.using('outcomes').get(type=outcome_data[5]).name
            courts = Courts.objects.using('outcomes').filter(number=outcome_data[11])
            if len(courts)==0:
                court_names = [outcome_data[11]]
            else:
                def get_name(court): return court.name
                court_names = map(get_name,courts)
            court['name'] = court_names
        except ConnectionDoesNotExist:
            court['type'] = outcome_data[5]
            court['name'] = [outcome_data[11]]
        finally:
            return court

    def offence_info(self, outcome_data):
        offence = {}
        try:
            offence['group'] = Ofgroup.objects.using('outcomes').get(code=outcome_data[6]).description
        except ConnectionDoesNotExist:
            offence['group'] = outcome_data[6]
        finally:
            return offence

    def defendant_info(self, outcome_data):
        defendant = {'age': outcome_data[8], 'number': outcome_data[0]};
        try:
            defendant['sex'] = Sex.objects.using('outcomes').get(code=outcome_data[12]).description
            defendant['ethnicity'] = Ethcode.objects.using('outcomes').get(code=outcome_data[13]).description
        except ConnectionDoesNotExist:
            defendant['sex'] = outcome_data[12]
        finally:
            return defendant

    def valid_outcome(self, outcome_csv):
        return re.compile('(\d+,){5}(MC|CC),(IND|SMO|SNM),(\d+,){21}\d+').match(outcome_csv)

    def get(self, request):
        outcome_csv = request.GET.get('csv','')
        if self.valid_outcome(outcome_csv):
            outcome_data = string.split(outcome_csv,',')
            context = RequestContext(request, {
                'csv': outcome_csv,
                'outcome': {
                    'defendant': self.defendant_info(outcome_data),
                    'court': self.court_info(outcome_data),
                    'offence': self.offence_info(outcome_data),
                    'month': outcome_data[9],
                    'year': outcome_data[10],

                    'amount1': outcome_data[1],
                    'amount2': outcome_data[2],
                    'amount3': outcome_data[3],
                    'amount4': outcome_data[4],
                    'force': outcome_data[7],
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
