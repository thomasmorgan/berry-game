"""Experiment for the berry game."""

from wallace.experiments import Experiment
from wallace.models import Info, Node
from wallace.networks import DiscreteGenerational
from wallace.nodes import Agent, Source
from wallace.information import Gene
from sqlalchemy import Integer, Float, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import cast
import random


class BerryGame(Experiment):
    """Define the structure of the experiment."""

    def __init__(self, session):
        """Call the same function in the super (see experiments.py in wallace).

        A few properties are then overwritten.
        Finally, setup() is called.
        """
        super(BerryGame, self).__init__(session)
        self.experiment_repeats = 1
        self.known_classes["Decision"] = Decision
        self.min_acceptable_performance = 1.00
        self.num_trials = 120
        self.generation_size = 40
        self.generations = 40
        self.initial_recruitment_size = self.generation_size
        self.initial_gene_value = 0.5
        self.setup()
        self.create_sources()

    def create_sources(self):
        if not Node.query.first():
            for net in self.networks():
                source = BerrySource(network=net)
                source.create_information(
                    value=self.initial_gene_value)

    def recruit(self):
        """pass."""
        pass

    def create_network(self):
        """Use the Empty network."""
        return DiscreteGenerational(
            generations=self.generations,
            generation_size=self.generation_size,
            initial_source=True)

    def create_node(self, participant, network):
        return BerryAgent(network=network, participant=participant)
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


class BerryAgent(Agent):

    __mapper_args__ = {"polymorphic_identity": "berry_agent"}

    def _what(self):
        return Gene

    def update(self, infos):
        for i in infos:
            if isinstance(i, Gene):
                self.mutate(i)


class BerrySource(Source):

    __mapper_args__ = {"polymorphic_identity": "berry_source"}

    def _what(self):
        return Info

    def create_information(self, value):
        BerryGene(origin=self, contents=value)


class BerryGene(Gene):

    __mapper_args__ = {"polymorphic_identity": "berry_gene"}

    def _mutated_contents(self):
        return repr(max(min(float(self.contents) + random.random()*0.1 - 0.05, 1.0), 0.0))


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
