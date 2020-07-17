from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from django.views.generic import View
# Create your views here.
from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, BASE, SUBTREE, NTLM
import time
import os
import hashlib
import unittest

import anytree
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import re

class UserLdap:
    def __init__(self):
        self.host = "ldaps://172.16.8.174"
        self.port = "636"
        self.bind_dn = "test\\ldap"
        self.passwd = "12345678Aa"
        self.base_dn = 'ou=yinhe_all,dc=test,dc=local'
        # self.type = 'sAMAccountName'
        if self.port:
            self.host = self.host + ":" + self.port
        # try:
        #     # connect to server
        #     self.server = Server(self.host, use_ssl=True, get_info=ALL)
        #     self.conn = Connection(self.server, user=bind, password=passwd, auto_bind=True)
        # except Exception as e:
        #     print(e)

    #connect to server
    def connect(self):
        server = Server(self.host)
        conn = Connection(server, user=self.bind_dn, password=self.passwd, authentication=NTLM, read_only = False)
        conn.bind()
        return conn

    def get_dn(self, username):
        conn = self.connect()
        conn.search(self.base_dn, '(&(objectCategory=person)(objectCategory=user)(sAMAccountName={0}))'.format(username),
                    attributes=ALL_ATTRIBUTES)
        if (len(conn.entries) == 0):
            print("Error: User query produced no result")
            exit(1)
        else:
            user_dn = conn.response[0]['dn']
            conn.unbind()
            return user_dn


    #get all username
    def get_users(self):
        all_users = []
        conn = self.connect()
        conn.search(search_base=self.base_dn,
                    search_filter="(&(objectCategory=Person)(objectCategory=user)(sAMAccountName=*))",
                    search_scope=SUBTREE,
                    attributes = ALL_ATTRIBUTES)
        if (len(conn.entries) == 0):
            print("Error: User query produced no result")
            exit(1)
        for i in conn.entries:
            all_users.append(i.sAMAccountName.value)
        conn.unbind()
        return all_users

    #
    def user_login(self, username, password):
        all = self.get_users()
        if username not in all:
            print("user is not exit")
            exit(1)
        else:
            server_second = Server(self.host)
            conn_second = Connection(server_second, user=self.get_dn(username), password=password)
            if conn_second.bind() == True:
                conn_second.unbind()
                return True
            else:
                conn_second.unbind()
                return False


        # c.search(search_base=self.base,
        #          search_filter="(&(objectClass=*)({0}={1}))".format(ldap_type, username),
        #          search_scope=SUBTREE
        #          )
        # conn_response = conn.response[0]['dn']

    #
    def user_pwd_set(self, username, password, new_password):
        self.user_login(username, password)
        if self.user_login(username, password) == True:
            conn = self.connect()
            modify_pwd = conn.extend.microsoft.modify_password(self.get_dn(username), new_password=new_password)
            conn.unbind()
            if modify_pwd == True:
                return True
            else:
                return False




    # conn.extend.microsoft.add_members_to_groups('bind_dn',
    #                                             'cn=My Group,cn=Users,dc=example,dc=com')


    def get_user_attr(self,username,attrname):
        conn = self.connect()
        conn.search(search_base=self.base_dn,
                    search_filter="(&(objectCategory=Person)(objectCategory=user)(sAMAccountName={0}))".format(username),
                    search_scope=SUBTREE,
                    attributes=ALL_ATTRIBUTES)
        return conn.entries[0][attrname]

    def max_pwdage(self):
        conn = self.connect()
        conn.search(search_base=self.base_dn,
                    search_filter='(&(objectCategory=*))',
                    search_scope=SUBTREE,
                    attributes=ALL_ATTRIBUTES)
        max_pwdage = conn.entries[0].maxPwdAge.value
        max_pwdagesecs = round(max_pwdage.total_seconds())
        conn.unbind()
        return max_pwdagesecs

    def get_users_maxage(self):
        conn = self.connect()
        max_pwdagesecs = 0
        pwd_lastsetunix = 0
        users_pwdexpirtime = {}
        conn.search(search_base=self.base_dn,
                    search_filter="(&(objectCategory=Person)(objectCategory=user)(sAMAccountName=*))",
                    search_scope=SUBTREE,
                    attributes=ALL_ATTRIBUTES)
        for entry in conn.entries:
            pwd_lastset = entry.pwdLastSet.value
            pwd_lastsetunix = round(pwd_lastset.timestamp())
            max_pwdagesecs = self.max_pwdage()
            max_age = max_pwdagesecs + pwd_lastsetunix
            users_pwdexpirtime[entry.sAMAccountName.value] = max_age
        conn.unbind()
        return users_pwdexpirtime


    def add_user(self,
                 container,
                 chineses_name,
                 english_name,
                 telephone):
        conn = self.connect()
        conn.add(dn=f"cn={chineses_name}" + "," + container,
                 object_class='user',
                 attributes={
                     'sn': chineses_name,
                     'userPrincipalName': english_name + "@yinhe.local",
                     'sAMAccountName': english_name,
                     'displayName': chineses_name,
                     'telephoneNumber': 15675323192,
                     'pwdLastSet': 0,
                     'mail': english_name + "@yinhe.ht",
                     'accountExpires': 9223372036854775807,
                     'msNPAllowDialin': True,
                 })
        # conn.add('CN=test6,OU=IT,OU=yinhe_all,DC=test,DC=local',object_class=['user', 'posixGroup', 'top'],attributes={'sAMAccountName': "omy", "name": "张三"})
        conn.extend.microsoft.modify_password(user=f"cn={chineses_name}"+","+container, new_password="12345678Aa")
        conn.modify(f"cn={chineses_name}" + "," + container, {'userAccountControl': [('MODIFY_REPLACE', 512)]})
        conn.unbind()
        return

    def get_ou(self):
        adpath = []
        conn = self.connect()
        conn.search(self.base_dn,
                    '(objectclass=organizationalUnit)',
                    attributes=['cn'])
        if (len(conn.entries) == 0):
            print("Error: User query produced no result")
            exit(1)
        else:
            for i in range(1,len(conn.entries)):
                adpath.append(conn.response[i]['dn'])
            conn.unbind()
            return adpath

    def get_userinfo(self):
        users_info = []
        users_dec = {}
        conn = self.connect()
        conn.search(self.base_dn,
                    search_filter='(&(objectCategory=Person)(objectCategory=user)(sAMAccountName=*))',
                    attributes=['cn', 'mail', 'title', 'telephoneNumber', 'whenChanged', 'whenCreated', 'distinguishedName', 'sAMAccountName'])
        if (len(conn.entries) == 0):
            print("Error: User query produced no result")
            exit(1)
        else:
            for i in conn.entries:
                create_time = i.whenCreated.value
                change_time = i.whenChanged.value
                hir_date = round(create_time.timestamp())
                ch_time = round(change_time.timestamp())
                users_dec = {
                    "name": i.cn.value,
                    "username": i.sAMAccountName.value,
                    "title": i.title.value,
                    "mobile": i.telephoneNumber.value,
                    "email": i.mail.value,
                    "hireDate": hir_date,
                    "changed": ch_time,
                    "userdn": i.distinguishedName.value,
                }
                users_info.append(users_dec)
        conn.unbind()
        return users_info


    def get_anytree(self):
        nodes = {}
        first_node = None
        for i in self.get_ou():
            parent_node = None
            parent_node_name = ""
            ret = (r'(?<=\bOU=)\w+\b')
            ou = re.findall(ret, i)
            for index, val in enumerate(reversed(ou)):
                if index not in nodes:
                    nodes[index] = {}
                key = parent_node_name + val
                if key not in nodes[index]:

                    nodes[index][key] = Node(key, parent=parent_node, display_name=val)

                if first_node is None:
                    first_node = nodes[index][key]
                parent_node = nodes[index][key]

        for pre, fill, node in RenderTree(first_node):
            return(pre, node.name)