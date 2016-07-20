"""Pilot experiment for the berry game."""

from wallace.experiments import Experiment
from wallace.models import Info
from wallace.networks import Empty
from sqlalchemy import Integer, Float, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import cast


class BerryPilot(Experiment):
    """Define the structure of the experiment."""

    def __init__(self, session):
        """Call the same function in the super (see experiments.py in wallace).

        A few properties are then overwritten.
        Finally, setup() is called.
        """
        super(BerryPilot, self).__init__(session)
        self.experiment_repeats = 1
        self.initial_recruitment_size = 3
        self.known_classes["Decision"] = Decision
        self.min_acceptable_performance = 1.00
        self.num_trials = 120
        self.setup()

    def recruit(self):
        """pass."""
        pass

    def create_network(self):
        """Use the Empty network."""
        return Empty()

    def attention_check(self, participant):
        """Check that the data are acceptable."""
        infos = participant.infos()

        score = (
            float(len([i for i in infos if i.right is True])) /
            (float(len(infos)))
        )

        return score >= self.min_acceptable_performance

    def bonus(self, participant):
        """The bonus to be awarded to the given participant."""
        infos = participant.infos()

        score = (
            float(len([i for i in infos if i.right])) /
            (float(len(infos)))
        )

        print "score: {}".format(score)

        return round(min(max((score - 0.5) * 2, 0), 1), 2)


class Decision(Info):
    """A decision."""

    __mapper_args__ = {"polymorphic_identity": "decision"}

    """Property 1"""

    @hybrid_property
    def dimension(self):
        """Convert property1 to dimension."""
        return self.property1

    @dimension.setter
    def dimension(self, dimension):
        """Make dimension settable."""
        self.property1 = dimension

    @dimension.expression
    def dimension(self):
        """Make dimension queryable."""
        return self.property1

    """Property 2"""

    @hybrid_property
    def trial(self):
        """Convert property2 to trial."""
        return int(self.property2)

    @trial.setter
    def trial(self, trial):
        """Make trial settable."""
        self.property2 = repr(trial)

    @trial.expression
    def trial(self):
        """Make trial queryable."""
        return cast(self.property2, Integer)

    """Property 3"""

    @hybrid_property
    def value(self):
        """Convert property3 to value."""
        return float(self.property3)

    @value.setter
    def value(self, value):
        """Make value settable."""
        self.property3 = repr(value)

    @value.expression
    def value(self):
        """Make value queryable."""
        return cast(self.property3, Float)

    """Property 4"""

    @hybrid_property
    def dimensions(self):
        """Convert property4 to dimensions."""
        return self.property4

    @dimensions.setter
    def dimensions(self, dimensions):
        """Make dimensions settable."""
        self.property4 = dimensions

    @dimensions.expression
    def dimensions(self):
        """Make dimensions queryable."""
        return self.property4

    """Property 5"""

    @hybrid_property
    def right(self):
        """Convert property5 to right."""
        return self.property5 in ["true", "True"]

    @right.setter
    def right(self, right):
        """Make right settable."""
        self.property5 = repr(right)

    @right.expression
    def right(self):
        """Make right queryable."""
        return cast(self.property5, Boolean)
