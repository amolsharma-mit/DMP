# Sample class with init method
class Relationship:

    # init method or constructor
    def __init__(self, subject, predicate, object):
        self.subject = subject
        self.predicate = predicate
        self.object = object


    # Sample Method
    def get(self):
        relationship = self.subject+" : "+self.predicate+" : "+self.object
        return relationship

    def __str__(self):
        relationship = self.subject + " : " + self.predicate + " : " +self.object
        return relationship