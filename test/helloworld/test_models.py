from helloworld.models import User, Course


def test_password_hashing():
    u = User(username='johndoe')
    u.set_password('ahoj')
    assert u.check_password('ahoj')
    assert not u.check_password('hehe')


def test_subscription(session):
    u1 = User(username='john', email='john@example.com')
    c1 = Course(title='test', description='test')
    session.add(u1)
    session.add(c1)
    session.commit()
    assert u1.courses.all() == []

    u1.subscribe(c1)

    assert u1.courses.all() == [c1]
