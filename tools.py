from pydantic import BaseModel, Field


class ToCRMAgent(BaseModel):
    """
    Escalate to this agent to inquire about customer data
    """

    hubspot_id: str = Field(
        ..., description="hubspot id of the customer to fetch CRM Data"
    )


class ToCSMAgent(BaseModel):
    zendesk_id: str = Field(
        ..., description="zendesk id of the customer to fetch CSM Data"
    )


class ToHelpDeskAgent(BaseModel):
    pass


class ToChatDataAgent(BaseModel):
    user_id: str = Field(..., description="user id of the customer to fetch Chat Data")
