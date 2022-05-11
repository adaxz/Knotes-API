import subprocess
import os
from dotenv import load_dotenv
from typing import List

import requests
import json

import config


class NotionApiActions:
    def __init__(self, database_id: str) -> None:
        load_dotenv()
        self.auth = os.getenv('AUTH')
        self.database_id = database_id
        self.database_query_url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
        self.block_query_url = f"https://api.notion.com/v1/blocks/"
        self.version = '2022-02-22'

        self.request_header = {
            "Authorization": f"Bearer {self.auth}",
            "Notion-Version": self.version
        }

        self.pages = self.get_all_pages_from_database()

    def get_all_pages_from_database(self) -> dict:
        req = requests.post(self.database_query_url,
                            headers=self.request_header)

        if req.status_code == 200:
            all_pages = req.json()['results']
            return all_pages
        else:
            raise Exception(
                f"Request for querying all pages failed with status code: {req.status_code}")

    def get_pages_by_name(self, name: str) -> List[dict]:
        result_pages = [page for page in self.pages if page['properties']['Name']
                        ['title'][0]['text']['content'] == name]
        return result_pages

    def get_page_content(self, page_id: str):
        url = self.block_query_url + f'{page_id}/children'
        req = requests.get(url, headers=self.request_header)
        if req.status_code == 200:
            return req.json()
        else:
            raise Exception(
                f"Request for page content of page {page_id} failed with status code: {req.status_code}")

    def append_content(self, page_id: str, notion_notes: List[dict]):
        url = self.block_query_url + f'{page_id}/children'
        data = {
            "children": notion_notes
        }

        json_data = json.dumps(data)
        bash_command = ['sh', config.BASH_DIR, page_id, json_data]
        subprocess.call(bash_command)


if __name__ == "__main__":
    api_actions = NotionApiActions()
    page = api_actions.get_pages_by_name('老舍散文')[0]
    page_id = page['id']
    api_actions.get_page_content(page_id)
