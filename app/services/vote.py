from sqlalchemy.orm import Session

from app.models.vote import VoteType
from app.repositories.post import PostRepository
from app.repositories.vote import VoteRepository


class VoteService:
    def __init__(self, db: Session):
        self.vote_repository = VoteRepository(db)
        self.post_repository = PostRepository(db)

    def upvote(self, post_id: int, user_id: int):
        existing_vote = self.vote_repository.get_user_vote(post_id, user_id)
        if existing_vote:
            if existing_vote.vote_type == VoteType.LIKE:
                self.vote_repository.delete_vote(existing_vote)
                return -1
            else:
                existing_vote.vote_type = VoteType.LIKE
                self.db.commit()
                return 2
        else:
            self.vote_repository.create_vote(post_id, user_id, VoteType.LIKE)
            return 1

    def downvote(self, post_id: int, user_id: int):
        existing_vote = self.vote_repository.get_user_vote(post_id, user_id)
        if existing_vote:
            if existing_vote.vote_type == VoteType.DISLIKE:
                self.vote_repository.delete_vote(existing_vote)
                return 1
            else:
                existing_vote.vote_type = VoteType.DISLIKE
                self.db.commit()
                return -2
        else:
            self.vote_repository.create_vote(post_id, user_id, VoteType.DISLIKE)
            return -1
