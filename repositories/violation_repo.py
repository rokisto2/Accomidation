from models import Violation

class ViolationRepository:
    def __init__(self, session):
        self.session = session

    def add_violation(self, student_id, description, violation_date):
        violation = Violation(student_id=student_id, description=description, violation_date=violation_date)
        self.session.add(violation)
        self.session.commit()

    def get_all_violations(self):
        return self.session.query(Violation).all()

    def get_violation_by_id(self, violation_id):
        return self.session.query(Violation).get(violation_id)

    def update_violation(self, violation_id, **kwargs):
        violation = self.get_violation_by_id(violation_id)
        if violation:
            for key, value in kwargs.items():
                setattr(violation, key, value)
            self.session.commit()

    def delete_violation(self, violation_id):
        violation = self.get_violation_by_id(violation_id)
        if violation:
            self.session.delete(violation)
            self.session.commit()
