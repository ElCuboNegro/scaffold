"""Example Celery task."""

import time

from app.core.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3)
def example_task(self, message: str) -> dict[str, str]:
    """
    Example Celery task that processes a message.

    Args:
        message: The message to process

    Returns:
        Dictionary with processing result
    """
    try:
        # Simulate some work
        time.sleep(2)

        # Process the message
        result = f"Processed: {message}"

        return {
            "status": "success",
            "result": result,
            "message": message,
        }
    except Exception as exc:
        # Retry on failure with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@celery_app.task
def send_email_task(recipient: str, subject: str, body: str) -> dict[str, str]:
    """
    Example email sending task.

    Args:
        recipient: Email recipient
        subject: Email subject
        body: Email body

    Returns:
        Dictionary with send status
    """
    # TODO: Implement actual email sending logic
    # For now, just simulate the task
    time.sleep(1)

    return {
        "status": "sent",
        "recipient": recipient,
        "subject": subject,
    }
