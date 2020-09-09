import json
from API import Sender


def makeIssue(data):
    payload = json.dumps({
        "fields": {
            "issuetype": {
                "name": "DS: Internal"
            },
            "project": {
                "key": "DS"
            },
            "summary": "This is a test " + "User " + str(data.getBadgeID()) + " returned",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": "The user " + str(data.getBadgeID()) + str(data.getName()),
                                "type": "text"
                            }
                        ]
                    }
                ]
            },
            "assignee": {
                "accountId": str((Sender.get("https://vivint.atlassian.net/rest/api/3/myself")).json()["accountId"])
            }
        }

    })

    return payload