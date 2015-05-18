import http.client, urllib.parse
import json
import time,webbrowser
'''
'''
class Dept:
    def __init__(self,name,parent=None,members=None,subs=None):
        self.name    = name
        self.parent  = parent
        self.subs    = subs
        self.members = members
    '''
    Return json of the department
    '''
    def Serialize(self):
        data = {}
        data[self.name] = {}
        data[self.name]['成员'] = []
        data[self.name]['分部门'] = {}
        if self.subs:
            for m in self.subs:
                data[self.name]['分部门'][self.subs[m].name] = self.subs[m].Serialize()
        if self.members:
            data[self.name]['成员'] = [{u:{"邮箱":self.members[u]['Alias']}} for u in self.members]
        return data

'''
'''
class QmailUser:
    def __init__(self,email,auth_key):
        self.email    = email
        self.auth_key = auth_key

'''
'''
class Qmail:
    '''
    constructor
    '''
    def __init__(self,admin,secret,verbose=False):
        self.secret     = secret
        self.verbose    = verbose
        self.host       = 'exmail.qq.com'
        self.api_host   = 'openapi.exmail.qq.com'
        self.port       = 12211
        self.token_url  = '/cgi-bin/token'
        self.auth_url   = '/openapi/mail/authkey'
        self.listen_url = '/openapi/listen'
        self.usr_url    = '/openapi/user/get'
        self.new_url    = '/openapi/mail/newcount'
        self.party_url  = '/openapi/party/list'
        self.puser_url  = '/openapi/partyuser/list'
        self.client_id  = admin

        self.headers   = {'Content-type': 'application/json'}
        self.version   = '0'
        self.token_type   = None
        self.expires_in   = None
        self.access_token = None

        self.auth_key     = None
        self.users        = {}
        self.depts        = {}
        self.__initToken()
        self.header       = {'Content-type': 'application/json','Authorization':self.token_type+' '+self.access_token}
        self.api_conn     = http.client.HTTPConnection(self.api_host,self.port)
        self.VPrint('constructor::init api connection...')
    '''
    destructor
    '''
    def __del__(self):
        self.VPrint('destructor::close api connection...')
        self.api_conn.close()
    def VPrint(self,data):
        if self.verbose:
            print(data)
    '''
    request api host,get data from server
    '''
    def __reqServerApi(self,url,param):
        params  = urllib.parse.urlencode(param)
        self.api_conn.request('POST',url, params, self.header)
        resp    = self.api_conn.getresponse()
        if resp.status != 200:
            self.VPrint ("[FAIL] with:%d-%s\n" %(resp.status,resp.reason))
            return None
        try:
            data = json.loads(resp.read().decode())
        except:
            self.VPrint('[FAIL] with loading data to be json.')
            return None
        return data
        
    '''
    Get the access token,private
    '''
    def __initToken(self):
        params = urllib.parse.urlencode({'grant_type': 'client_credentials',
                                         'client_id': self.client_id,
                                         'client_secret': self.secret})
        conn = http.client.HTTPSConnection(self.host)
        conn.request('POST',self.token_url, params, self.headers)
        resp = conn.getresponse()
        if resp.status != 200:
            self.VPrint ("[FAIL] with:%d-%s\n" %(resp.status,resp.reason))
            return False
        try:
            data = json.loads(resp.read().decode())
        except:
            self.VPrint('[FAIL] with loading data to be json.')
            return False
        self.VPrint(data)
        self.token_type   = data['token_type']
        self.expires_in   = data['expires_in']
        self.access_token = data['access_token']
        conn.close()
        return True
    '''
    Get authkey for an user
    '''
    def initAuthKey(self,email):
        param   = {'alias': email}
        data    = self.__reqServerApi(self.auth_url,param)
        if data:
        	usr = QmailUser(email,data['auth_key'])
        	self.users[email] = usr
        	return True
        return False

    '''
    Get department information for the company
    '''
    def initDepts(self,pt,path=''):
        depts = self.getParty(path)
        if depts['Count']:
            for dept in depts['List']:
                pt[dept['Value']] = {}
                newpath = (path == '') and dept['Value'] or path+'/'+dept['Value']
                self.VPrint(newpath)
                d = Dept(dept['Value'],
                    None,
                    self.getPartyUsers(newpath),
                    self.initDepts(pt[dept['Value']],newpath))
                pt[dept['Value']] = d
            return pt
    '''
    get one-click login url for an user
    '''
    def getFastLane(self,email):
        return 'https://exmail.qq.com/cgi-bin/login?fun=bizopenssologin&method=bizauth&agent='+self.client_id+'&user='\
        +email+'&ticket='+self.users[email].auth_key

    '''
    not implemented:listen to mail server 
    '''
    def listenMailServer(self):
        params  = {'ver':self.version,'access_token':self.access_token}
        while True:
        	data = self.__reqServerApi(self.listen_url,params)
        	if not data:
        		return False
        	if 'Ver' in data:
        		params = urllib.parse.urlencode({'ver':data['Ver'],'access_token':self.access_token})
        	time.sleep(20)
        return True

    '''
    get detailed information for a specific user
    '''
    def getUserDetail(self,email):
        params  = {'alias':email}
        data    = self.__reqServerApi(self.usr_url,params)
        if data:
        	self.VPrint(data)
        return data
    '''
    get unread count for an user specified by the email
    '''
    def getUnreadCount(self,email):
        params  = {'alias':email}
        data    = self.__reqServerApi(self.new_url,params)
        if data:
        	self.VPrint(data)
        return data

    '''
    get party information,specify by partypath
    '''
    def getParty(self,partypath=''):
        params  = {'partypath':partypath}
        data    = self.__reqServerApi(self.party_url,params)
        if data:
        	self.VPrint(data)
        return data
    '''
    get all user(s) that belong to a party 
    '''
    def getPartyUsers(self,partypath=''):
        params  = {'partypath':partypath}
        data    = self.__reqServerApi(self.puser_url,params)
        if data:
        	self.VPrint(data)
        dt = {}
        for email in data['List']:
            x = self.getUserDetail(email['Value'])
            dt[x['Name']] = x
        return dt
        
if __name__ == '__main__':
    m   = Qmail('<usr>','<key>')
    del m
    