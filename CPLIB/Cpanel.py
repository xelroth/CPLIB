from math import log, floor
import requests
import ftplib
import json
import base64
import os

class Cpanel:
    def __init__(self, domain, user, password, port='2083'):
        """
        Initializes the Cpanel class with domain, user credentials, and port.

        :param domain: The domain name of the cPanel account.
        :param user: The username for the cPanel account.
        :param password: The password for the cPanel account.
        :param port: The port number for the cPanel API (default is 2083).
        """
        self.user = user
        self.password = password
        self.domain = domain
        self.port = port
        self.base_url = f"https://{self.domain}:{self.port}/json-api/cpanel"

    def _connect_to_api(self, command):
        """
        Connects to the cPanel API and executes a command.

        :param command: The command to be executed on the cPanel API.
        :return: The JSON response from the API.
        """
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{self.user}:{self.password}".encode()).decode()
        }
        data = {
            'cpanel_jsonapi_version': 2,
            'cpanel_jsonapi_module': 'Cron',
            'cpanel_jsonapi_func': 'add_line',
            'command': command
        }
        response = requests.post(self.base_url, headers=headers, data=data)
        return json.loads(response.text)

    def cron_jobs(self, data):
        """
        Adds a new cron job to the cPanel account.

        :param data: A dictionary containing the cron job details, including:
                     - command: The command to run.
                     - minute: Minute when the job should run.
                     - hour: Hour when the job should run.
                     - day: Day of the month when the job should run.
                     - month: Month when the job should run.
                     - weekday: Day of the week when the job should run.
        :return: Success message or error description.
        """
        command = data["command"]
        schedule = f"{data['minute']} {data['hour']} {data['day']} {data['month']} {data['weekday']}"
        result = self._connect_to_api(schedule)
        return self._handle_response(result)

    def delete_cron(self, line):
        """
        Deletes a specified cron job from the cPanel account.

        :param line: The line number of the cron job to delete.
        :return: Success message or error description.
        """
        result = self._connect_to_api(f"remove_line&line={line}")
        return self._handle_response(result)

    def account_ftp(self, data):
        """
        Creates a new FTP account.

        :param data: A dictionary containing FTP account details, including:
                     - username: The username for the FTP account.
                     - password: The password for the FTP account.
                     - quota: The quota for the FTP account.
                     - addressdir: The home directory for the FTP account.
        :return: Success message or error description.
        """
        command = f"addftp&user={data['username']}&pass={data['password']}&quota={data['quota']}&homedir={data['addressdir']}"
        result = self._connect_to_api(command)
        return self._handle_response(result)

    def del_account_ftp(self, username):
        """
        Deletes a specified FTP account.

        :param username: The username of the FTP account to delete.
        :return: Success message or error description.
        """
        result = self._connect_to_api(f"delftp&user={username}")
        return self._handle_response(result)

    def create_database(self, name):
        """
        Creates a new database in the cPanel account.

        :param name: The name of the database to create.
        :return: Success message or error description.
        """
        dbname = f"{self.user}__{name}"
        result = self._connect_to_api(f"createdb&db={dbname}")
        return self._handle_response(result)

    def delete_database(self, name):
        """
        Deletes a specified database from the cPanel account.

        :param name: The name of the database to delete.
        :return: Success message or error description.
        """
        dbname = f"{self.user}__{name}"
        result = self._connect_to_api(f"deletedb&db={dbname}")
        return self._handle_response(result)

    def _handle_response(self, result):
        """
        Handles the response from the cPanel API.

        :param result: The JSON response from the API.
        :return: Success message or error description.
        """
        if result["cpanelresult"]["preevent"]["result"] == 1:
            return "Success"
        return f"Error: {result['cpanelresult']['error']}"


class FileManager:
    def __init__(self, domain, user, password):
        self.user = user
        self.password = password
        self.domain = domain
        self.connection = self._connect_to_server()

    def _connect_to_server(self):
        """Establishes an FTP connection to the server."""
        connection = ftplib.FTP(self.domain)
        connection.login(self.user, self.password)
        return connection

    def create_folder(self, name):
        """
        Creates a new folder on the FTP server.

        Parameters:
        name (str): The name of the folder to create.

        Returns:
        str: Success message or error description.
        """
        return self._execute_ftp_command('mkd', name)

    def delete_folder(self, name):
        """
        Deletes a folder from the FTP server.

        Parameters:
        name (str): The name of the folder to delete.

        Returns:
        str: Success message or error description.
        """
        return self._execute_ftp_command('rmd', name)

    def create_file(self, name):
        """
        Creates a new file on the local system and uploads it to the FTP server.

        Parameters:
        name (str): The name of the file to create.

        Returns:
        str: Success message or error description.
        """
        with open(name, 'w') as file:
            file.write("")
        return self._upload_file(name)

    def delete_file(self, name):
        """
        Deletes a file from the FTP server.

        Parameters:
        name (str): The name of the file to delete.

        Returns:
        str: Success message or error description.
        """
        return self._execute_ftp_command('delete', name)

    def rename(self, old_name, new_name):
        """
        Renames a file or folder on the FTP server.

        Parameters:
        old_name (str): The current name of the file or folder.
        new_name (str): The new name for the file or folder.

        Returns:
        str: Success message or error description.
        """
        try:
            self.connection.rename(old_name, new_name)
            return "Success"
        except Exception as e:
            return f"Error: {str(e)}"

    def upload(self, local_path, remote_path):
        """
        Uploads a local file to the FTP server.

        Parameters:
        local_path (str): The path of the local file to upload.
        remote_path (str): The destination path on the FTP server.

        Returns:
        str: Success message or error description.
        """
        return self._upload_file(local_path, remote_path)

    def _upload_file(self, local_path, remote_path=None):
        """
        Uploads a file to the FTP server.

        Parameters:
        local_path (str): The path of the local file to upload.
        remote_path (str, optional): The destination path on the FTP server. Defaults to the basename of local_path.

        Returns:
        str: Success message or error description.
        """
        remote_path = remote_path or os.path.basename(local_path)
        with open(local_path, 'rb') as file:
            try:
                self.connection.storbinary(f"STOR {remote_path}", file)
                return "Uploaded"
            except Exception as e:
                return f"Error: {str(e)}"

    def _execute_ftp_command(self, command, name):
        """
        Executes a specified FTP command.

        Parameters:
        command (str): The FTP command to execute (e.g., 'mkd', 'rmd').
        name (str): The name of the file or folder to act upon.

        Returns:
        str: Success message or error description.
        """
        try:
            getattr(self.connection, command)(name)
            return "Success"
        except Exception as e:
            return f"Error: {str(e)}"

    def info_file(self, name):
        """
        Retrieves information about a file on the FTP server.

        Parameters:
        name (str): The name of the file to retrieve information for.

        Returns:
        dict: A dictionary containing the file size and name, or an error message.
        """
        size = self.connection.size(name)
        if size is not None:
            units = ['bit', 'kb', 'mb', 'gb', 'tb']
            base = log(size, 1024)
            resu = round(pow(1024, base - floor(base)), 2) + ' ' + units[int(base)]
            return {'status': True, 'size': resu, 'namefile': os.path.basename(name)}
        return "Error"

    def list_content(self, name):
        """
        Lists the contents of a specified directory on the FTP server.

        Parameters:
        name (str): The name of the directory to list.

        Returns:
        str: A newline-separated string of the directory contents.
        """
        return "\n".join(self.connection.nlst(name))

    def copy_file(self, local_path, remote_path):
        """
        Copies a local file to the FTP server.

        Parameters:
        local_path (str): The path of the local file to copy.
        remote_path (str): The destination path on the FTP server.

        Returns:
        str: Success message or error description.
        """
        return self.upload(local_path, remote_path)

    def file_put(self, name, data):
        """
        Creates a file with specified data and uploads it to the FTP server.

        Parameters:
        name (str): The name of the file to create.
        data (str): The content to write to the file.

        Returns:
        str: Success message or error description.
        """
        with open(name, 'w') as file:
            file.write(data)
        return self._upload_file(name)

