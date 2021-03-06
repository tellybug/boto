# Copyright (c) 2014 Tellybug, Matt Millar
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

from tests.integration.route53 import Route53TestCase

from boto.route53.healthcheck import HealthCheck
from boto.route53.record import ResourceRecordSets

class TestRoute53HealthCheck(Route53TestCase):
    def test_create_health_check(self):
        hc = HealthCheck(ip_addr="54.217.7.118", port=80, hc_type="HTTP", resource_path="/testing")
        result = self.conn.create_health_check(hc)
        self.assertEquals(result[u'CreateHealthCheckResponse'][u'HealthCheck'][u'HealthCheckConfig'][u'Type'], 'HTTP')
        self.assertEquals(result[u'CreateHealthCheckResponse'][
                          u'HealthCheck'][u'HealthCheckConfig'][u'IPAddress'], '54.217.7.118')
        self.assertEquals(result[u'CreateHealthCheckResponse'][u'HealthCheck'][u'HealthCheckConfig'][u'Port'], '80')
        self.assertEquals(result[u'CreateHealthCheckResponse'][
                          u'HealthCheck'][u'HealthCheckConfig'][u'ResourcePath'], '/testing')
        self.conn.delete_health_check(result['CreateHealthCheckResponse']['HealthCheck']['Id'])

    def test_create_https_health_check(self):
        hc = HealthCheck(ip_addr="54.217.7.118", port=80, hc_type="HTTPS", resource_path="/testing")
        result = self.conn.create_health_check(hc)
        self.assertEquals(result[u'CreateHealthCheckResponse'][u'HealthCheck'][u'HealthCheckConfig'][u'Type'], 'HTTPS')
        self.assertEquals(result[u'CreateHealthCheckResponse'][
                          u'HealthCheck'][u'HealthCheckConfig'][u'IPAddress'], '54.217.7.118')
        self.assertEquals(result[u'CreateHealthCheckResponse'][u'HealthCheck'][u'HealthCheckConfig'][u'Port'], '80')
        self.assertEquals(result[u'CreateHealthCheckResponse'][
                          u'HealthCheck'][u'HealthCheckConfig'][u'ResourcePath'], '/testing')
        self.conn.delete_health_check(result['CreateHealthCheckResponse']['HealthCheck']['Id'])


    def test_create_and_list_health_check(self):
        hc = HealthCheck(ip_addr="54.217.7.118", port=80, hc_type="HTTP", resource_path="/testing")
        result1 = self.conn.create_health_check(hc)
        hc = HealthCheck(ip_addr="54.217.7.119", port=80, hc_type="HTTP", resource_path="/testing")
        result2 = self.conn.create_health_check(hc)
        result = self.conn.get_list_health_checks()
        self.assertTrue(len(result['ListHealthChecksResponse']['HealthChecks']) > 1)
        self.conn.delete_health_check(result1['CreateHealthCheckResponse']['HealthCheck']['Id'])
        self.conn.delete_health_check(result2['CreateHealthCheckResponse']['HealthCheck']['Id'])

    def test_delete_health_check(self):
        hc = HealthCheck(ip_addr="54.217.7.118", port=80, hc_type="HTTP", resource_path="/testing")
        result = self.conn.create_health_check(hc)
        hc_id = result['CreateHealthCheckResponse']['HealthCheck']['Id']
        result = self.conn.get_list_health_checks()
        found = False
        for hc in result['ListHealthChecksResponse']['HealthChecks']:
            if hc['Id'] == hc_id:
                found = True
                break
        self.assertTrue(found)
        result = self.conn.delete_health_check(hc_id)
        result = self.conn.get_list_health_checks()
        for hc in result['ListHealthChecksResponse']['HealthChecks']:
            self.assertFalse(hc['Id'] == hc_id)

    def test_create_health_check_string_match(self):
        hc = HealthCheck(ip_addr="54.217.7.118", port=80, hc_type="HTTP_STR_MATCH", resource_path="/testing", string_match="test")
        result = self.conn.create_health_check(hc)
        self.assertEquals(result[u'CreateHealthCheckResponse'][u'HealthCheck'][u'HealthCheckConfig'][u'Type'], 'HTTP_STR_MATCH')
        self.assertEquals(result[u'CreateHealthCheckResponse'][
                          u'HealthCheck'][u'HealthCheckConfig'][u'IPAddress'], '54.217.7.118')
        self.assertEquals(result[u'CreateHealthCheckResponse'][u'HealthCheck'][u'HealthCheckConfig'][u'Port'], '80')
        self.assertEquals(result[u'CreateHealthCheckResponse'][
                          u'HealthCheck'][u'HealthCheckConfig'][u'ResourcePath'], '/testing')
        self.assertEquals(result[u'CreateHealthCheckResponse'][u'HealthCheck'][u'HealthCheckConfig'][u'SearchString'], 'test')
        self.conn.delete_health_check(result['CreateHealthCheckResponse']['HealthCheck']['Id'])

    def test_create_health_check_https_string_match(self):
        hc = HealthCheck(ip_addr="54.217.7.118", port=80, hc_type="HTTPS_STR_MATCH", resource_path="/testing", string_match="test")
        result = self.conn.create_health_check(hc)
        self.assertEquals(result[u'CreateHealthCheckResponse'][u'HealthCheck'][u'HealthCheckConfig'][u'Type'], 'HTTPS_STR_MATCH')
        self.assertEquals(result[u'CreateHealthCheckResponse'][
                          u'HealthCheck'][u'HealthCheckConfig'][u'IPAddress'], '54.217.7.118')
        self.assertEquals(result[u'CreateHealthCheckResponse'][u'HealthCheck'][u'HealthCheckConfig'][u'Port'], '80')
        self.assertEquals(result[u'CreateHealthCheckResponse'][
                          u'HealthCheck'][u'HealthCheckConfig'][u'ResourcePath'], '/testing')
        self.assertEquals(result[u'CreateHealthCheckResponse'][u'HealthCheck'][u'HealthCheckConfig'][u'SearchString'], 'test')
        self.conn.delete_health_check(result['CreateHealthCheckResponse']['HealthCheck']['Id'])


    def test_create_resource_record_set(self):
        hc = HealthCheck(ip_addr="54.217.7.118", port=80, hc_type="HTTP", resource_path="/testing")
        result = self.conn.create_health_check(hc)
        records = ResourceRecordSets(
            connection=self.conn, hosted_zone_id=self.zone.id, comment='Create DNS entry for test')
        change = records.add_change('CREATE', 'unittest.bototest.com.', 'A', ttl=30, identifier='test',
                                    weight=1, health_check=result['CreateHealthCheckResponse']['HealthCheck']['Id'])
        change.add_value("54.217.7.118")
        records.commit()

        records = ResourceRecordSets(self.conn, self.zone.id)
        deleted = records.add_change('DELETE', "unittest.bototest.com.", "A", ttl=30, identifier='test',
                                    weight=1, health_check=result['CreateHealthCheckResponse']['HealthCheck']['Id'])
        deleted.add_value('54.217.7.118')
        records.commit()
