from django.db.models import Q
from django.db.utils import ConnectionDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from django.utils import timezone
from django.views import generic
from home.models import Outcomes, Crttype, Courts, Ofgroup, Sex, Ethcode, PoliceForces, Pleas, Proceedings, Offences, Disposals
from feedback.models import Feedback
import string, re

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
            offences = Offences.objects.using('outcomes').filter(lookup=outcome_data[14])
            if len(offences) > 1:
                offence['description'] = 'n/a'
                offence['act'] = 'n/a'
            else:
                offence['description'] = offences[0].description
                offence['act'] = offences[0].act
        except Exception as e:
            print e
            offence['group'] = outcome_data[6]
            offence['description'] = outcome_data[14]
        finally:
            return offence

    def defendant_info(self, outcome_data):
        defendant = {'age': outcome_data[8], 'number': outcome_data[0]}
        try:
            defendant['sex'] = Sex.objects.using('outcomes').get(code=outcome_data[12]).description
            defendant['ethnicity'] = Ethcode.objects.using('outcomes').get(code=outcome_data[13]).description
        except Exception as e:
            print e
            defendant['sex'] = outcome_data[12]
        finally:
            return defendant

    def db_retrieve(self, object_type, query, default=None):
        try:
            result = object_type.objects.using('outcomes').filter(query)[0]
        except Exception as e:
            print "going to default"
            print e
            result = default
        finally:
            return result

    def outcome_info(self, outcome_data):
        proceeding_code = int(outcome_data[16])
        outcome = {'proceeding':{}, 'disposals':[], 'amounts':[]}
        try:
            if outcome_data[5] == 'MC':
                query = Q(code=proceeding_code) & (Q(court='M') | Q(court='M & C'))
                outcome['proceeding']['description'] = Proceedings.objects.using('outcomes').get(query).description
            elif outcome_data[5] == 'CC':
                query = Q(code=proceeding_code) & (Q(court='C') | Q(court='M & C'))
                outcome['proceeding']['description'] = Proceedings.objects.using('outcomes').get(query).description
            else:
                outcome['proceeding']['description'] = proceeding_code
            outcome['disposals'].append({'disp':self.db_retrieve(Disposals,Q(code=int(outcome_data[17]))),'amount':outcome_data[1]})
            outcome['disposals'].append({'disp':self.db_retrieve(Disposals,Q(code=int(outcome_data[18]))),'amount':outcome_data[2]})
            outcome['disposals'].append({'disp':self.db_retrieve(Disposals,Q(code=int(outcome_data[19]))),'amount':outcome_data[3]})
            outcome['disposals'].append({'disp':self.db_retrieve(Disposals,Q(code=int(outcome_data[20]))),'amount':outcome_data[4]})
        except Exception as e:
            print e
            outcome['proceeding']['description'] = proceeding_code
            outcome['disposals']=[]
            outcome['disposals'].append({'disp':self.db_retrieve(Disposals,Q(code=int(outcome_data[17]))),'amount':outcome_data[1]})
            outcome['disposals'].append({'disp':self.db_retrieve(Disposals,Q(code=int(outcome_data[18]))),'amount':outcome_data[2]})
            outcome['disposals'].append({'disp':self.db_retrieve(Disposals,Q(code=int(outcome_data[19]))),'amount':outcome_data[3]})
            outcome['disposals'].append({'disp':self.db_retrieve(Disposals,Q(code=int(outcome_data[20]))),'amount':outcome_data[4]})
        finally:
            return outcome


    def valid_outcome(self, outcome_csv):
        return re.compile('(\d+,){5}(MC|CC),(IND|SMO|SNM),(\d+,){21}\d+').match(outcome_csv)

    def police_info(self, outcome_data):
      police = {}
      try:
          police['force'] = PoliceForces.objects.using('outcomes').get(code=outcome_data[7]).name
          police['region'] = PoliceForces.objects.using('outcomes').get(code=outcome_data[7]).region
      except ConnectionDoesNotExist:
          police['force'] = outcome_data[7]
      finally:
          return police

    def plea_info(self, outcome_data):
        try:
            plea = Pleas.objects.using('outcomes').get(code=outcome_data[15]).description
        except ConnectionDoesNotExist:
            plea = outcome_data[15]
        finally:
            return plea

    def get(self, request, outcome_id):
        if outcome_id:
            try:
                outcome = Outcomes.objects.using('outcomes').get(id=outcome_id)
            except:
                raise Http404
            outcome_data = [outcome.multipers,outcome.amount1,outcome.amount2,outcome.amount3,outcome.amount4,outcome.crttype,outcome.ofgroup,outcome.force,outcome.age,outcome.month,outcome.year,outcome.court,outcome.sex,outcome.ethcode,outcome.classctn,outcome.plea,outcome.proc,outcome.disp1,outcome.disp2,outcome.disp3,outcome.disp4,outcome.clastype,outcome.priority,outcome.guilty,outcome.sent,outcome.result,outcome.offtyp,outcome.ofclas,outcome.notoff,outcome.id]
            outcome_csv = ''
        else:
            outcome_csv = request.GET.get('csv','')
            if not self.valid_outcome(outcome_csv):
                context = RequestContext(request, {'csv': outcome_csv, 'outcome': None})
                template = loader.get_template('apps/outcome.html')
                return HttpResponse(template.render(context))
            else:
                outcome_data = string.split(outcome_csv,',')

        context = RequestContext(request, {
            'csv': outcome_csv,
            'outcome': {
                'defendant': self.defendant_info(outcome_data),
                'court': self.court_info(outcome_data),
                'offence': self.offence_info(outcome_data),
                'month': outcome_data[9],
                'year': outcome_data[10],
                'police' : self.police_info(outcome_data),
                'plea': self.plea_info(outcome_data),
                'outcome': self.outcome_info(outcome_data),

                'amount1': outcome_data[1],
                'amount2': outcome_data[2],
                'amount3': outcome_data[3],
                'amount4': outcome_data[4],
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
        template = loader.get_template('home/outcome.html')
        return HttpResponse(template.render(context))


class ThanksView(generic.View):
    def post(self, request):
        Feedback.objects.create(email=request.POST['email'],
                                name=request.POST['name'],
                                comment=request.POST['comment'],
                                date=timezone.now())
        return render(request, 'home/thanks.html')

    def get(self, request):
        return redirect('home:index')
