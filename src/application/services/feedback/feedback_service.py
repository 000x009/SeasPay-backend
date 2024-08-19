from src.infrastructure.dal import FeedbackDAL


class FeedbackService:
    def __init__(self, feedback_dal: FeedbackDAL):
        self._feedback_dal = feedback_dal

    # async def feedback_list(self, ):