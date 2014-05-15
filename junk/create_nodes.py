#!/usr/bin/python
# -*- coding: utf-8 -*-
import sleekxmpp
import pprint
import logging
import sys



class PubsubClient(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, nodes):
        super(PubsubClient, self).__init__(jid, password)
        self.__my_own_jid = jid
        # self.node_to_create = node_to_create
        self.nodes = nodes
        self.register_plugin('xep_0030')
        self.register_plugin('xep_0059')
        self.register_plugin('xep_0060')

        self.add_event_handler('session_start', self.start, threaded=True)

        # self.add_event_handler('pubsub_publish', self._publish)

    def start(self, event):
        print 'start'
        self.get_roster()
        self.send_presence()
        # self._start_receiving()

        self.count = 0

        def _create_callback(*args, **kwargs):
            # print '_create_callback: args=%s, kwargs=%s' % (pprint.pformat(args), pprint.pformat(kwargs))
            self.count += 1

            # self.disconnect()
            if self.count == len(self.nodes):
                self.disconnect()

        for node in self.nodes:
            for suffix in ('_meta', '_data'):
                real_node = node + suffix
                self['xep_0060'].create_node('pubsub.sox.ht.sfc.keio.ac.jp', real_node, callback=_create_callback)
                print 'create %s' % real_node

        # self['xep_0060'].create_node('pubsub.ps.ht.sfc.keio.ac.jp', self.node_to_create, callback=_create_callback)
        # print 'created'


    # def _start_receiving(self):
    #     print 'start receiving!'
    #     self._subscribe('pubsub.ps.ht.sfc.keio.ac.jp', 'sample_data')

    # def _subscribe(self, server, node):
    #     try:
    #         ifrom = self.__my_own_jid
    #         result = self['xep_0060'].subscribe(server, node, ifrom=ifrom, callback=self._subscribe_callback)
    #         print 'subscribe ok result=%s' % pprint.pformat(result)
    #     except:
    #         print 'subscribe ERROR'

    # def _subscribe_callback(self, *args, **kwargs):
    #     print 'got something'
    #     print 'args=%s, kwargs=%s' % (pprint.pformat(args), pprint.pformat(kwargs))

    # def _publish(self, msg):
    #     print 'got! %s' % msg


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print 'USAGE: python ./create_node.py NODE_NAME'
    #     sys.exit(0)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # node_name = sys.argv[1]
    # print 'node name to create: %s' % node_name

    nodes = ['sb-data1', 'sb-image1', 'sb-graph1', 'sb-tagcloud1']

    n = 5
    while n <= 32:
        nodes.append('genova%d' % n)
        n += 1

    print '---nodes:'
    for node in nodes:
        print node

    # sys.exit(0)

    # jid = 'guest@ps.ht.sfc.keio.ac.jp'
    jid = 'guest@sox.ht.sfc.keio.ac.jp'
    pw = 'miroguest'

    xmpp = PubsubClient(jid, pw, nodes)
    if xmpp.connect():
        print 'connected'
        xmpp.process(block=True)
    else:
        print 'could NOT connect'




