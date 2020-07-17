from ldap_users import UserLdap
from apps.accounts.models import User, Deployment
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, MODIFY_REPLACE
import re
test=UserLdap()
# print(test.get_userinfo())
# for i in test.get_userinfo():
#     print(i)


class SynAdmon:
    def __init__(self):
        self.host = "ldaps://172.16.8.174"
        self.port = "636"
        self.bind_dn = "test\\ldap"
        self.passwd = "12345678Aa"
        self.base_dn = 'ou=yinhe_all,dc=test,dc=local'
        # self.type = 'sAMAccountName'
        if self.port:
            self.host = self.host + ":" + self.port


    #connect to server
    def connect(self):
        server = Server(self.host)
        conn = Connection(server, user=self.bind_dn, password=self.passwd, authentication=NTLM, read_only = False)
        conn.bind()
        return conn

    def deployment(self):
        conn = self.connect()
        conn.search(self.base_dn,
                    search_filter='(&(objectCategory=organizationalUnit))',
                    attributes=['ou', 'distinguishedName', 'whenChanged'])
        for i in range(0,(len(conn.entries))):
            Deployment.objects.create(name = conn.entries[i].ou.value,
                                      path = conn.entries[i].distinguishedName.value,
                                      present = 0,
                                      utime = conn.entries[i].whenChanged.value)
        conn.unbind()
        return

    def user(self):
        test = UserLdap()
        users = test.get_userinfo()
        for i in users:
            rec = re.compile(r'(?<=\bOU=)\w+\b')
            ret = re.findall(rec, i.distinguishedName.value)
            d_name = ret[0]
            User.objects.create(userid= i["username"],
                 name = i["name"],
                 position = i["title"],
                 mobile = i["mobile"],
                 email = i["email"],
                 isLeader = False,
                 isActive = 0,
                 utime = i["hireDate"],
                 deployment_id = User.objects.filter(name=d_name).uid)

        test.connect().unbind()