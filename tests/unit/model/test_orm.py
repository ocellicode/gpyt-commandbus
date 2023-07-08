import datetime
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gpyt_commandbus.model.command import Command
from gpyt_commandbus.model.target import Target


class TestModels(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Target.metadata.create_all(self.engine)
        Command.metadata.create_all(self.engine)

    def tearDown(self):
        self.session.close_all()
        Target.metadata.drop_all(self.engine)
        Command.metadata.drop_all(self.engine)

    def test_create_command(self):
        command_data = {"key": "value"}
        timestamp = datetime.datetime.now()
        target = Target(url="http://example.com", name="example_target")
        command = Command(data=command_data, timestamp=timestamp, target=target)
        self.session.add(command)
        self.session.commit()
        self.assertEqual(command.data, command_data)
        self.assertEqual(command.timestamp, timestamp)
        self.assertEqual(command.target, target)

    def test_create_target(self):
        url = "http://example.com"
        name = "example_target"
        target = Target(url=url, name=name)
        self.session.add(target)
        self.session.commit()
        self.assertEqual(target.url, url)
        self.assertEqual(target.name, name)

    def test_relationship(self):
        url = "http://example.com"
        name = "example_target"
        target = Target(url=url, name=name)
        command_data = {"key": "value"}
        timestamp = datetime.datetime.now()
        command = Command(data=command_data, timestamp=timestamp)
        target.commands.append(command)
        self.session.add(target)
        self.session.commit()
        self.assertEqual(command.target, target)
        self.assertIn(command, target.commands)
