from slackclient import SlackClient
import yaml
import datetime
import os


class SlackEarningsService:
    def __init__(self, slack_conf):
        self.conf = self.read_config(slack_conf)
        self.host, self.port = self.check_env()
        self.slack_client = SlackClient(self.conf.get('token'))
        self.slack_channel = self.conf.get('channel')
        self.jpeg = "https://image.shutterstock.com/mosaic_250/0/0/{}.jpg"
        self.link = "https://www.shutterstock.com/image/{}"
        self.message = "Date: {} {}\nID: {}"

    def check_env(self):
        host = self.conf.get('host')
        hostprod = self.conf.get('hostprod')
        port = self.conf.get('port')

        prod = os.getenv("PROD")
        if prod == "1":
            return hostprod, port
        return host, port

    def push_message(self, message):
        self.slack_client.api_call(
            "chat.postMessage",
            channel=self.slack_channel,
            text=message)

    def push(self, location, idi, description):
        jpeg = self.jpeg.format(idi)
        link = self.link.format(idi)
        curr_date = (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')

        link_id = "<{}|{}>".format(link, idi)
        message = self.message.format(curr_date, location, link_id)
        attachments = [
            {
                "title": description,
                "image_url": jpeg
            }]
        try:
            self.slack_client.api_call(
                "chat.postMessage",
                channel=self.slack_channel,
                text=message,
                attachments=attachments)
        except Exception as err:
            return err

    @staticmethod
    def read_config(conf_path):
        with open(conf_path, 'r') as file:
            return yaml.load(file)

    def push_test(self, location, idi, description):
        jpeg = self.jpeg.format(idi)
        link = self.link.format(idi)
        curr_date = (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')

        link_id = "<{}|{}>".format(link, idi)

        message = self.message.format(curr_date, location, link_id)

        attachments = [
            {
                "title": description,
                "image_url": jpeg
            }]
        print(self.slack_channel, message, attachments)
