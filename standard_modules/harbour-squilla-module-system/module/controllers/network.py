import re
import subprocess

from flask.ext.restful import Resource

from squilla import api




def get_interfaces():
    s = subprocess.Popen("/sbin/ip a",
                         shell=True, stdout=subprocess.PIPE)
    output = s.stdout.readlines()
    interfaces = []
    tmp_dict = {}
    for line in output:
        # interface name
        m = re.match(b"^[0-9]*: (.*):.*", line)
        if m:
            interface_name = m.groups()[0].decode("utf-8")
            # Save interface
            if "ipv4" in tmp_dict or "ipv6" in tmp_dict:
                interfaces.append(tmp_dict)
            # New interface
            tmp_dict = {"name": interface_name}
            continue
        # ipv4
        m = re.match(b"^    inet ([0-9\./]*) .*", line)
        if m:
            tmp_dict["ipv4"] = m.groups()[0].decode("utf-8")
            continue
        # ipv6
        m = re.match(b"^    inet6 ([a-fA-F0-9:/]*) .*", line)
        if m:
            tmp_dict["ipv6"] = m.groups()[0].decode("utf-8")

    # Save last interface if needed
    if "ipv4" in tmp_dict or "ipv6" in tmp_dict:
        interfaces.append(tmp_dict)

    return interfaces


class Networks(Resource):
    def get(self):
        data = [{"name": "eth0", "ip": "192.168.2.1"}]
        data = get_interfaces()
        return {'networks': data}

api.add_resource(Networks, '/system/networks')
