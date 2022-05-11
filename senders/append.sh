#!/bin/sh

# NOTION_API_KEY = 'secret_EZdk2H2rVcRiTC2Ko5oUCLvwvtYmWFSAMnWjBRbHWwV'
# echo ${NOTION_API_KEY}


curl -X PATCH 'https://api.notion.com/v1/blocks/'$1'/children' \
  -H 'Authorization: Bearer '"secret_EZdk2H2rVcRiTC2Ko5oUCLvwvtYmWFSAMnWjBRbHWwV"'' \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-02-22" \
  --data "$2"