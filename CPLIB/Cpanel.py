try:
    import requests
    import ftplib
    import json
    import base64
    import urllib
    import os
    from math import *
except ImportError:
    print("Please Install Librarys Using The Command pip install -r requiremnts.txt")

class Cpanel:
    def __init__(self, domain, user, password, port='2083'):
        self.user = user
        self.password = password
        self.domain = domain
        self.port = port

    def connect_to_api(self, command):
        urlcp = f"https://{self.domain}:{self.port}/json-api/cpanel"
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{self.user}:{self.password}".encode()).decode()
        }
        data = {
            'cpanel_jsonapi_version': 2,
            'cpanel_jsonapi_module': 'Cron',
            'cpanel_jsonapi_func': 'add_line',
            'command': command
        }
        response = requests.post(urlcp, headers=headers, data=data)
        result = json.loads(response.text)
        if result["cpanelresult"]["preevent"]["result"] == 1:
            return "true"
        else:
            error = result["cpanelresult"]["error"]
            return f"Error: {error}"

    def cron_jobs(self, data={}):
        command = data["command"]
        minute = data["minute"]
        day = data["day"]
        hour = data["hour"]
        month = data["month"]
        weekday = data["weekday"]
        return self.connect_to_api(f"cpanel_jsonapi_version=2&cpanel_jsonapi_module=Cron&cpanel_jsonapi_func=add_line&command={command}&day={day}&hour={hour}&minute={minute}&month={month}&weekday={weekday}")

    def delete_cron(self, data={}):
        line = data["line"]
        return self.connect_to_api(f"cpanel_jsonapi_version=2&cpanel_jsonapi_module=Cron&cpanel_jsonapi_func=remove_line&line={line}")

    def account_ftp(self, data={}):
        username = data["username"]
        password = data["password"]
        quota = data["quota"]
        homedir = data["addressdir"]
        return self.connect_to_api(f"cpanel_jsonapi_version=2&cpanel_jsonapi_module=Ftp&cpanel_jsonapi_func=addftp&user={username}&pass={password}&quota={quota}&homedir={homedir}")

    def del_account_ftp(self, data={}):
        username = data["username"]
        return self.connect_to_api(f"cpanel_jsonapi_version=2&cpanel_jsonapi_module=Ftp&cpanel_jsonapi_func=delftp&user={username}")

    def create_database(self, name):
        dbname = f"{self.user}__{name}"
        return self.connect_to_api(f"cpanel_jsonapi_version=2&cpanel_jsonapi_module=MysqlFE&cpanel_jsonapi_func=createdb&db={dbname}")

    def delete_database(self, name):
        dbname = f"{self.user}__{name}"
        return self.connect_to_api(f"cpanel_jsonapi_version=2&cpanel_jsonapi_module=MysqlFE&cpanel_jsonapi_func=deletedb&db={dbname}")


class FileManager:
    def __init__(self, domain, user, password):
        self.user = user
        self.password = password
        self.domain = domain

    def connect_to_server(self):
        connection = ftplib.FTP(self.domain)
        connection.login(self.user, self.password)
        if connection.getwelcome():
            return "true"
        else:
            return "false"

    def create_folder(self, data={}):
        name = data["address"]
        connection = ftplib.FTP(self.domain)
        connection.login(self.user, self.password)
        if connection.mkd(name):
            return "Created"
        else:
            return "Error"

    def delete_folder(self, data={}):
        name = data["address"]
        connection = ftplib.FTP(self.domain)
        connection.login(self.user, self.password)
        if connection.rmd(name):
            return "Deleted"
        else:
            return "Error"

    def create_file(self, data={}):
        name = data["address"]
        g = name.replace("/", "\n")
        j = g.split("\n")
        f = len(j) - 1
        open(j[f], 'w').close()
        connection = ftplib.FTP(self.domain)
        connection.login(self.user, self.password)
        with open(j[f], 'rb') as file:
            if connection.storbinary(f"STOR {name}", file):
                return "Created"
            else:
                return "Error"
        os.remove(j[f])

    def delete_file(self, data={}):
        name = data["address"]
        connection = ftplib.FTP(self.domain)
        connection.login(self.user, self.password)
        if connection.delete(name):
            return "Deleted"
        else:
            return "Error"

    def rename(self, data={}):
        name = data["address"]
        new_name = data["Newaddress"]
        connection = ftplib.FTP(self.domain)
        connection.login(self.user, self.password)
        if connection.rename(name, new_name):
            return "true"
        else:
            return "Error"

    def upload(self, data={}):
        url = data["url"]
        name = data["address"]
        namefile = data["namefile"]
        urllib.request.urlretrieve(url, namefile)
        connection = ftplib.FTP(self.domain)
        connection.login(self.user, self.password)
        with open(namefile, 'rb') as file:
            if connection.storbinary(f"STOR {name}/{namefile}", file):
                return "Uploaded"
            else:
                return "Error"
        os.remove(namefile)

    def info_file(self, data={}):
        name = data["address"]
        connection = ftplib.FTP(self.domain)
        connection.login(self.user, self.password)
        size = connection.size(name)
        units = ['bit', 'kb', 'mb', 'gb', 'tb']
        base = log(size, 1024)
        resu = round(pow(1024, base - floor(base)), 2) + ' ' + units[base]
        g = name.replace("/", "\n")
        j = g.split("\n")
        f = len(j) - 1
        if size is not None:
            return {
                'status': True,
                'size': resu,
                'namefile': j[f]
            }
        else:
            return "Error"

    def list_content(self, data={}):
        name = data["address"]
        connection = ftplib.FTP(self.domain)
        connection.login(self.user, self.password)
        array = connection.nlst(name)
        content = ""
        for item in array:
            content += f"{item}\n"
        return content

    def copy_file(self, data={}):
        name1 = data["localaddress"]
        name2 = data["Newaddress"]
        connection = ftplib.FTP(self.domain)
        connection.login(self.user, self.password)
        with open(name1, 'rb') as file:
            if connection.storbinary(f"STOR {name2}", file):
                return "true"
            else:
                return "Error"

    def file_put(self, data={}):
        name = data["address"]
        datas = data["data"]
        connection = ftplib.FTP(self.domain)
        connection.login(self.user, self.password)
        g = name.replace("/", "\n")
        j = g.split("\n")
        f = len(j) - 1
        with open(j[f], 'w') as file:
            file.write(datas)
        with open(j[f], 'rb') as file:
            if connection.storbinary(f"STOR {name}", file):
                return "true"
            else:
                return "Error"
        os.remove(j[f])
