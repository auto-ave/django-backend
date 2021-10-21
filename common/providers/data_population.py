
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
from common.colors import *
import sys

class DataPopulationProvider:
    def __init__(self, model, data, serializer):
        self.model = model
        self.data = data
        self.serializer = serializer

    def populate(self):
        total_items = len(self.data)
        populated_now = 0
        already_populated = 0
        invalid_data = 0
        
        for item in self.data:
            if self.serializer:
                serializer_instance = self.serializer(data=item)
                if serializer_instance.is_valid():
                    serializer_instance.save()
                    populated_now = populated_now + 1
                else:
                    if serializer_instance.errors.get('model') and serializer_instance.errors.get('model')[0].code == 'unique':
                        already_populated = already_populated + 1
                    else:
                        print(serializer_instance.errors)
                        invalid_data = invalid_data + 1
                    continue
            else:
                try:
                    self.model.objects.create(**item)
                    populated_now = populated_now + 1
                except IntegrityError as e:
                    already_populated = already_populated + 1
            
        
        sys.stdout.write(REVERSE + CYAN)
        print('Stats for {}:'.format(self.model._meta.model_name))

        sys.stdout.write(RESET)
        print('Total items in data: \033[92m{}'.format(total_items))
        sys.stdout.write(RESET)
        print('Already populated: \033[92m{}'.format(already_populated))
        sys.stdout.write(RESET)
        print('Populated now: \033[92m{}'.format(populated_now))
        sys.stdout.write(RESET)
        print('Rejected by Serializer(if any): \033[92m{}'.format(invalid_data))
        sys.stdout.write(RESET)
        
        print('\n\n')
        