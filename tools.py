import os
import base64
import requests
from pydantic import BaseModel, Field
from langchain_core.tools import tool


# HubSpot API
hubspot_api = "https://api.hubapi.com/crm/v3/objects"
hubspot_headers = {
    "Authorization": f'Bearer {os.environ["HUBSPOT_BEARER_TOKEN"]}',
    "Content-Type": "application/json",
}

# Zendesk API
zendesk_api = "https://instwisehelp.zendesk.com/api/v2"
encoded_credentials = base64.b64encode(
    (f'{os.getenv("ZENDESK_EMAIL")}/token:{os.getenv("ZENDESK_TOKEN")}').encode("utf-8")
).decode("utf-8")
zendesk_headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/json",
}


class ToCRMAgent(BaseModel):
    """
    Escalate to this agent to inquire about customer data
    """

    hubspot_id: str = Field(
        ..., description="hubspot id of the customer to fetch CRM Data"
    )


class ToCSMAgent(BaseModel):
    """
    Escalate to this agent to inquire about customer data
    """

    zendesk_id: str = Field(
        ..., description="zendesk id of the customer to fetch CSM Data"
    )


class ToHelpDeskAgent(BaseModel):
    """
    Escalate to this agent to inquire about helpdesk assistance
    """

    pass


class ToChatDataAgent(BaseModel):
    """
    Escalate to this agent to inquire about customer support chat history
    """

    user_id: str = Field(..., description="user id of the customer to fetch Chat Data")


# CRM Agent Tools
@tool()
def fetch_hubspot_contacts():
    """
    Fetch HubSpot contacts for the given HubSpot ID.

    Returns:
        str: The response message.
    """
    # Fetch HubSpot contacts
    try:
        response = requests.get(
            f"{hubspot_api}/contacts",
            headers=hubspot_headers,
        )
        print(response.json())
        return response.json()
    except Exception as e:
        return f"Error fetching HubSpot contacts: {e}"


# print(fetch_hubspot_contacts())


@tool()
def fetch_hubspot_deals(hubspot_id: str):
    """
    Fetch HubSpot deals for the given HubSpot ID.

    Args:
        hubspot_id (str): The HubSpot ID of the customer.

    Returns:
        str: The response message.
    """
    try:
        # Fetch HubSpot deals
        response = requests.get(
            f"{hubspot_api}/deals",
            headers=hubspot_headers,
        )
        return response.json()
    except Exception as e:
        return f"Error fetching HubSpot deals: {e}"


@tool("zendesk tickets")
def fetch_zendesk_tickets(zendesk_id: str):
    """
    Fetch Zendesk tickets for the given Zendesk ID.

    Args:
        zendesk_id (str): The Zendesk ID of the customer.

    Returns:
        str: The response message.
    """
    try:
        response = requests.get(zendesk_api, headers=zendesk_headers)
        return response.json()
    except Exception as e:
        return f"Error fetching Zendesk tickets: {e}"
