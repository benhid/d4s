from pathlib import Path

import requests
from cached_property import cached_property

from d4s.context import context


class Item:

    def __init__(self, id: str, base_url: str):
        self.id = id
        self.base_url = base_url

    @cached_property
    def public_url(self):
        """ Get public url from item in workspace.
        """
        url = f'{self.base_url}/workspace/items/{self.id}/publiclink?gcube-token={self.token}'
        x = requests.get(url)

        # for some reason, the response returns an url with surrounding quote marks
        return x.text[1:-1]

    @property
    def token(self):
        return context.token


class StoreHubClient:

    def __init__(self, base_url: str = 'https://workspace-repository.d4science.org/storagehub'):
        self.base_url = base_url

    def create_folder(self, name: str, description: str = ''):
        """ Create folder under user workspace.

        :return: Folder id.
        """
        # create folder under workspace
        url = f'{self.base_url}/workspace/items/{self.workspace}/create/FOLDER?gcube-token={self.token}'
        x = requests.post(url, data={'name': name, 'description': description})

        return x.text

    def upload_file(self, folder_id: str, file_path: str, name: str, description: str = ''):
        """ Upload file to StorageHub.

        ..note: See https://gcube.wiki.gcube-system.org/gcube/StorageHub_REST_API
        :return: File id.
        """
        if not Path(file_path).is_file():
            raise FileNotFoundError(f'File was not found at {file_path}')

        url = f'{self.base_url}/workspace/items/{folder_id}/create/FILE?gcube-token={self.token}'
        x = requests.post(url, data={'name': name, 'description': description}, files={'file': open(file_path, 'rb')})

        return Item(id=x.text, base_url=self.base_url)

    @cached_property
    def workspace(self):
        """ Get current workspace.

        :return: Workspace id.
        """
        url = f'{self.base_url}/workspace/?gcube-token={self.token}'

        x = requests.get(url)
        x = x.json()

        return x["item"]["id"]

    @property
    def token(self):
        return context.token
