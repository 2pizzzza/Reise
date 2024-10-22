from sqlalchemy.orm import Session

from app.models.vote import Vote, VoteType


class VoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_vote(self, post_id: int, user_id: int) -> Vote:
        return self.db.query(Vote).filter(Vote.post_id == post_id, Vote.user_id == user_id).first()

    def create_vote(self, post_id: int, user_id: int, vote_type: VoteType) -> Vote:
        vote = Vote(post_id=post_id, user_id=user_id, vote_type=vote_type)
        self.db.add(vote)
        self.db.commit()
        self.db.refresh(vote)
        return vote

    def delete_vote(self, vote: Vote):
        self.db.delete(vote)
        self.db.commit()
