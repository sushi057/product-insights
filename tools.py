from pydantic import BaseModel, Field


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
