from django.db import models


class BookStatus(models.TextChoices):
    AVAILABLE = 'available', '📗 Доступна'
    BORROWED = 'borrowed', '📘 Выдана'
    RESERVED = 'reserved', '📙 Зарезервирована'
    MAINTENANCE = 'maintenance', '🛠️ На обслуживании'
    LOST = 'lost', '❌ Утеряна'
    WRITTEN_OFF = 'written_off', '📝 Списана'

    # @classmethod
    # def get_available_statuses(cls):
    #     """Статусы, когда книга доступна для выдачи"""
    #     return [cls.AVAILABLE, cls.RESERVED]
    #
    # @classmethod
    # def get_unavailable_statuses(cls):
    #     """Статусы, когда книга недоступна"""
    #     return [cls.BORROWED, cls.MAINTENANCE, cls.LOST, cls.WRITTEN_OFF]
