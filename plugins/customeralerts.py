from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to
import re

class OverageAlerts(MachineBasePlugin):
    # Bot will @listen_to the channel for the regex expression to be matched.
    @listen_to(regex=r'^overagesalert ')
    def question(self, message):
        # message contains multiple lines from Sumologic. Messages that are too-long from Sumo are split (nicely)
        text = message.text
        # The messages is parsed using regex into its specific fields.
        # This is the parse expression
        pattern = re.compile('^overagesalert (?P<deployment>[^\t]+)\t(?P<org_id>[^\t]+)\t(?P<org_name>[^\t]+)\t(?P<arr>[^\t]+)\t(?P<account_exec_manager>[^\t]+)\t(?P<account_exec_manager_email>[^\t]+)\t(?P<account_exec>[^\t]+)\t(?P<account_exec_email>[^\t]+)\t(?P<cam_owner>[^\t]+)\t(?P<cam_owner_email>[^\t]+)\t(?P<cs_owner>[^\t]+)\t(?P<cs_owner_email>[^\t]+)\t(?P<se_owner>[^\t]+)\t(?P<se_owner_email>[^\t]+)\t(?P<plan_type>[^\t]+)\t(?P<zuora_link>[^\t]+)\t(?P<sfdc_link>[^\t]+)\t(?P<closed_cross_sell>[^\t]+)\t(?P<closed_upgrade>[^\t]+)\t(?P<closed_overage>[^\t]+)\t(?P<daily_gb_limit>[^\t]+)\t(?P<logs>[^\t]+)\t(?P<metrics>[^\t]+)\t(?P<other>[^\t]+)\t(?P<storage>[^\t]+)$')
        # Because multiple lines may be output by Sumo Logic, this  loop iterates over the message payload,
        # splitting it into individual lines.
        for line in text.split('\n'):
            # Parse the individual line
            result = pattern.search(line)
            # If it properly parses,
            if result:
                # Create a payload
                payload = ""
                customerUsageURL = "https://service.us2.sumologic.com/ui/dashboard.html?k=KoE040tWj1DFZQV7MCrViRfWC0i29F5zdXMEPG8b9NtLzOzErbnHmXXQutuz&f=&t=r&filters=org_id*eq*{}**deployment*eq*null**callermodule*eq*service**user*eq*null".format(result.group('org_id'))
                # Create an Attachment
                attachment = [{
                    'pretext': 'New overages from *'+result.group('org_name')+"*",
                    'title': 'Overage: Yesterday',
                    'title_link': customerUsageURL,
                    'text': 'Take action to resolve.',
                    'color': 'warning',
                    "fields": [
                        {
                            "title": "Logs",
                            "value": result.group('logs'),
                            "short": True
                        },{
                            "title": "Metrics",
                            "value": result.group('metrics'),
                            "short": True
                        },{
                            "title": "Other",
                            "value": result.group('other'),
                            "short": True
                        },{
                            "title": "Storage",
                            "value": result.group('storage'),
                            "short": True
                        }
                    ],
                    'actions': [{
                        'text': 'SalesForce',
                        'type': 'button',
                        'url': 'https://www.salesforce.com/'
                    },{
                        'text': 'Customer Usage',
                        'type': 'button',
                        'url': customerUsageURL
                    },{
                        'text': 'Email',
                        'type': 'button',
                        'url': 'mailto:someone@yoursite.com?subject=Mail%20from%20Our%20Site&body=This%20is%20the%20body'
                    }]
                }]
                # Identify AE
                ae_email = extractemail(result.group('account_exec_email'))
                # get ae ID
                ae_id = lookup_by_email(message,ae_email)
                # Send Message
                if ae_id:
                    # Send DM
                    self.send_dm_webapi(ae_id,payload,attachment)
                else:
                    # If you can't find AE, send an error message.
                    message.say("Cannot find slack account for " + ae_email)
                    message.say_webapi(payload,attachment)

def lookup_by_email(message,lookup_email):
    for user in message._client.users:
        user_email = message._client.users[user].email
        if user_email == lookup_email:
            return user
    return None


def extractemail(emailField):
    pattern = re.compile('^<(?P<mailto>[^|]+)\|(?P<email>[^|]+)>$')
    result = pattern.search(emailField)
    email = result.group('email')
    return email