
Slack Machine
=============

Simple Plugin Creation
---

[This page](https://slack-machine.readthedocs.io/en/latest/plugins/basics.html) is the best place to start for writing a plugin.

Usage
-----

1.  Create a directory for your Slack Machine bot: ``mkdir my-slack-bot && cd my-slack-bot``
2. Add (or modify) a ``local_settings.py`` file to your bot directory: ``touch local_settings.py``
3. Create a Bot User for your Slack team: https://my.slack.com/services/new/bot (take note of your API token)
4. Add the Slack API token as an environment variable `SM_SLACK_API_TOKEN` **OR** to your ``local_settings.py`` like this:

.. code-block:: python

 SLACK_API_TOKEN = 'xox-my-slack-token'

5. Start the bot with ``slack-machine``
6. \...
7. Profit!

Docker
-----

From the repo root directory

1. `# docker build -t scattorshot . `
2. `# docker run -it --name="scattorshot" -e SM_SLACK_API_TOKEN="xoxb-xxxxxxxxxxxxxxx"`

Documentation
-------------
Check the [Original Repo](https://github.com/DandyDev/slack-machine) for details repo notes.

You can find the documentation for Slack Machine here: http://slack-machine.readthedocs.io/en/latest/

Go read it to learn how to properly configure Slack Machine, write plugins, and more!