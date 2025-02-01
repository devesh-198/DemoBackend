from django_cron import CronJobBase, Schedule
import os
import json
from django.conf import settings
from django.db import transaction
from .models import DanceProfile

class MyCronJob(CronJobBase):
    # RUN_EVERY_MINS = 120 # every 2 hours

    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'vivproapi.dashboard.cron.MyCronJob'    # a unique code 

    def do(self):
        print("Cron is running")

        # import ipdb; ipdb.set_trace()

        json_file_path = os.path.join(settings.DATA_DIR, '', 'playlist.json')
        data = None

        try:
            # Read and parse the JSON file
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            if not data:
                # log error here
                print("!Something went wrong.")
                return

            # Now you can use the data as needed
            with transaction.atomic():
                for key in data.get('id', {}).keys():
                    DanceProfile.objects.update_or_create(
                        id=data['id'][key],
                        title=data['title'][key],
                        danceability=data['danceability'][key],
                        energy=data['energy'][key],
                        mode=data['mode'][key],
                        acousticness=data['acousticness'][key],
                        tempo=data['tempo'][key],
                        duration_ms=data['duration_ms'][key],
                        num_sections=data['num_sections'][key],
                        num_segments=data['num_segments'][key],
                    )
        except Exception as e:
            print(e)
