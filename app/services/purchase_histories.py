"""
PurchaseHistory Service
"""
from datetime import datetime

from app.models.purchase_histories import PurchaseHistory as PurchaseHistoryModel
from app.services.service import BaseService


class PurchaseHistoryService(BaseService):
    """PurchaseHistory Service"""

    def __init__(self, db):
        """init"""
        super().__init__(db)

    def get_purchase_histories(
        self,
        skip: int = 0,
        limit: int = 100,
        from_date: datetime = None,
        to_date: datetime = None,
    ):
        """Get purchase_histories"""
        query = self.db.query(PurchaseHistoryModel)
        if from_date:
            query = query.filter(PurchaseHistoryModel.transaction_date >= from_date)
        if to_date:
            query = query.filter(PurchaseHistoryModel.transaction_date <= to_date)
        return query.offset(skip).limit(limit).all()
