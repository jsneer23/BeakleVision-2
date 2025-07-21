from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.api.deps import get_current_active_superuser
from app.models.app import Message
from app.utils import generate_test_email, send_email

router = APIRouter(prefix="/utils", tags=["utils"])


# @router.get("search_index/",
#             status_code=200)
# def search_index() -> SearchIndex:
#     """
#     Get the search index.
#     """
#     return SearchIndex()


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")


@router.get("/health-check/")
async def health_check() -> bool:
    return True
