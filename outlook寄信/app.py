import os
import json
import msal
import requests


GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]
GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def get_access_token(tenant_id: str, client_id: str, client_secret: str) -> str:
    """Client Credentials flow: app-only token."""
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        authority=authority,
        client_credential=client_secret,
    )
    result = app.acquire_token_for_client(scopes=GRAPH_SCOPE)
    if "access_token" not in result:
        raise RuntimeError(
            f"Failed to get token: {result.get('error')} - {result.get('error_description')}"
        )
    return result["access_token"]


def list_inbox_messages(
    access_token: str,
    mailbox_upn: str,
    top: int = 25,
    unread_only: bool = False,
):
    """
    List messages in Inbox.
    - Select only needed fields (from, isRead, receivedDateTime, subject) like Microsoft Learn tutorial guidance. [3](https://learn.microsoft.com/en-us/graph/tutorials/python-email)
    - Order by receivedDateTime DESC.
    """
    headers = {"Authorization": f"Bearer {access_token}"}

    # Microsoft Learn tutorial示範選取欄位：from/isRead/receivedDateTime/subject，並以 receivedDateTime DESC 排序、top=25 [3](https://learn.microsoft.com/en-us/graph/tutorials/python-email)
    select_fields = "from,isRead,receivedDateTime,subject"
    order_by = "receivedDateTime DESC"

    url = f"{GRAPH_BASE}/users/{mailbox_upn}/mailFolders/inbox/messages"
    params = {
        "$select": select_fields,
        "$orderby": order_by,
        "$top": top,
    }

    if unread_only:
        params["$filter"] = "isRead eq false"

    resp = requests.get(url, headers=headers, params=params, timeout=30)
    if not resp.ok:
        # 直接把 Graph 回傳錯誤印出來，方便你定位權限/信箱/網路等問題
        try:
            raise RuntimeError(json.dumps(resp.json(), ensure_ascii=False))
        except Exception:
            raise RuntimeError(resp.text)

    data = resp.json()
    return data


def print_messages(data: dict):
    items = data.get("value", [])
    for i, msg in enumerate(items, start=1):
        from_obj = (msg.get("from") or {}).get("emailAddress") or {}
        print(f"[{i}] {msg.get('receivedDateTime')} | {'Unread' if not msg.get('isRead') else 'Read'}")
        print(f"    From: {from_obj.get('name')} <{from_obj.get('address')}>")
        print(f"    Subject: {msg.get('subject')}")
        print(f"    Id: {msg.get('id')}")
        print()


if __name__ == "__main__":
    tenant_id = os.getenv("TENANT_ID")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    mailbox_upn = os.getenv("MAILBOX_UPN")  # e.g. sean.ma@webpromaterials.com

    token = get_access_token(tenant_id, client_id, client_secret)

    inbox = list_inbox_messages(
        access_token=token,
        mailbox_upn=mailbox_upn,
        top=25,
        unread_only=False
    )

    print_messages(inbox)

    # 分頁：如果回傳含有 @odata.nextLink，代表還有下一頁
    next_link = inbox.get("@odata.nextLink")
    if next_link:
        print("More messages available via @odata.nextLink")