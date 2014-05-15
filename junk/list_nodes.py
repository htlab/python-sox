#!/usr/bin/python
# -*- coding: utf-8 -*-
import sleekxmpp
import pprint
import logging
from bs4 import BeautifulSoup


class PubsubClient(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        super(PubsubClient, self).__init__(jid, password)
        self.__my_own_jid = jid
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0059')
        self.register_plugin('xep_0060')

        self.add_event_handler('session_start', self.start, threaded=True)

    def start(self, event):
        print 'start'
        # self.get_roster()
        print 'got roster'
        # self.send_presence()
        print 'sent presence'

        def cb(*args, **kwargs):
            result = args[0]
            xml_str = '%s' % result

            soup = BeautifulSoup(xml_str)
            items = soup.find_all('item')
            nodes = []

            for item in items:
                nodes.append(item.attrs['node'])

            nodes.sort()
            for item in nodes:
                print item


            self.disconnect()
        print 'defined callback'

        self['xep_0060'].get_nodes('pubsub.sox.ht.sfc.keio.ac.jp', callback=cb)
        print 'requested'


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    jid = 'guest@sox.ht.sfc.keio.ac.jp'
    pw = 'miroguest'

    xmpp = PubsubClient(jid, pw)
    if xmpp.connect():
        print 'connected'
        xmpp.process(block=True)
    else:
        print 'could NOT connect'
