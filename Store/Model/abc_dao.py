from abc import ABC, abstractmethod

class AbcDao(ABC):

    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def get_byid(self):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass
